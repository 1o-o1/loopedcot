"""Generate each prompt at each requested token budget and write resumable forced-readout and protocol-v2 cell rows."""
import gc, json, os, sys, time, traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import targets as G


def parse_budgets(s):
    """Return a list of token caps from a comma-separated string; the empty value and none/null mean no limit."""
    out = []
    for p in s.split(","):
        p = p.strip()
        out.append(None if p in ("none", "null", "") else int(p))
    return out


def main(argv):
    """Generate once per budget, score every cap of that generation, and append one resumable cell row per (question, budget, cap); returns a process exit code."""
    ARM_NAME, TASK = argv[0], argv[1]
    cfg_path, root, arm = G.DEFAULT_CONFIG, None, None
    K, NP, SUFFIX, ADAPTER, WAIT, GRID_OVR = 4, None, "", None, True, None
    for a in argv[2:]:
        k, _, v = a.lstrip("-").partition("=")
        if k == "config":
            cfg_path = v
        elif k == "root":
            root = v
        elif k == "arm":
            arm = v
        elif k == "k":
            K = int(v)
        elif k == "n":
            NP = int(v)
        elif k == "suffix":
            SUFFIX = v
        elif k == "adapter":
            ADAPTER = v
        elif k == "budgets":
            GRID_OVR = parse_budgets(v)
        elif k == "no-wait":
            WAIT = False
    G.require_root(root, "run_grid.py")
    cfg = G.load_config(cfg_path)
    arm = arm or cfg["default_arm"]
    WITH_LINE = bool(cfg.arm(arm)["budget_line"])
    P = G.paths(root)
    G.ensure_dirs(P)
    if ADAPTER is None and ARM_NAME != "A0":
        ADAPTER = os.path.join(P["adapters"], ARM_NAME)
    TAG = "%s_%s_k%d%s" % (TASK, ARM_NAME, K, SUFFIX)
    GRID = GRID_OVR if GRID_OVR is not None else cfg["eval_budgets"]
    CAPS = [int(c) for c in cfg["eval_standard_caps"]]
    HORIZON = int(cfg["eval_horizon"])     # the no-limit pass runs to here, not to the harness default
    TAIL = int(cfg["chain_tail_chars"])
    PROTOCOL = str(cfg["protocol"])

    def caps_for(T):
        """Return the token caps scored from one generation: the standard caps for the no-limit pass, otherwise the budget itself."""
        return CAPS if T is None else [int(T)]
    T0 = time.time()

    from s32_common import (MAXB, MEM_FRACTION, BATCH_CAP, set_steps, static_cache_factory,
                            batch_for, split_rows, make_find_cut, decode, strip_tail,
                            token_pieces, parse_forced, parse_own, ans_eq, score_v2, nvsmi,
                            gpu_procs, load_ckpt, Appender, load_base)
    from s3_patch import patch_universal_cache
    import torch
    print("[s36 run %s arm=%s frac=%.2f line=%s] %s | %s"
          % (TAG, arm, MEM_FRACTION, WITH_LINE, nvsmi(), gpu_procs()), flush=True)

    ev, cal = split_rows(TASK)
    rows = ev + cal
    split = ["eval"] * len(ev) + ["cal"] * len(cal)
    if NP:
        rows, split = rows[:NP], split[:NP]
    N = len(rows)
    NANS_T = int(cfg["n_answer_tokens"][TASK])
    NL = int(cfg["n_layers"])
    qp, ap_, suffix_text, stops, marker, kind = G.task_bits(TASK)

    if ARM_NAME == "A0":
        tok, model = load_base()
        minfo = {"arm": "A0", "merged": False, "adapter": None}
    else:
        from peft import PeftModel
        tok, _m = load_base()
        _pm = PeftModel.from_pretrained(_m, ADAPTER, is_trainable=False)
        model = _pm.merge_and_unload().to(G.DEV).eval()
        minfo = {"arm": ARM_NAME, "merged": True, "adapter": ADAPTER}
    if WAIT:
        G.wait_for_gpu(os.path.join(P["logs"], "gpu_wait.log"))
    patched, already = patch_universal_cache(model)
    set_steps(model, K)
    CF = static_cache_factory(model, K)
    PAD = tok.pad_token_id
    pieces = token_pieces(tok, model.config.vocab_size)
    find_cut = make_find_cut(tok, "base", stops, [tok.eos_token_id])
    SUF = tok(suffix_text, add_special_tokens=False)["input_ids"]

    # the exemplar block must be the one the targets were built against, byte for byte
    man = G.jload(os.path.join(P["artifacts"], "target_manifest_%s.json" % arm), {}) or {}
    G.check_exemplars(tok, cfg, man.get("exemplar_sha256"), tasks=[TASK])
    if TASK in ("math", "math500"):
        G.check_exemplar_source(G.math_shot_source())

    META = os.path.join(P["artifacts"], "meta_%s.json" % TAG)
    meta = G.jload(META, {}) or {}
    meta.update({"name": ARM_NAME, "arm": arm, "task": TASK, "k": K, "n_problems": N,
                 "n_eval": min(len(ev), N), "n_cal": max(0, N - len(ev)),
                 "grid_budgets": [str(t) for t in GRID], "standard_caps": CAPS,
                 "horizon": HORIZON, "harness_default_horizon": MAXB,
                 "budget_line": WITH_LINE,
                 "exemplar_sha256": G.exemplar_fingerprints(tok, cfg, tasks=[TASK]),
                 "protocol": PROTOCOL,
                 "stopping": "natural stop or hard stop at T, then a forced read-out",
                 "n_answer_tokens": NANS_T,
                 "mem_fraction": MEM_FRACTION, "batch_cap": BATCH_CAP, "model_info": minfo,
                 "suffix_text": suffix_text, "cache_patched_now": patched,
                 "nvidia_smi_at_start": nvsmi()})
    meta.setdefault("oom_events", [])
    meta.setdefault("errors", {})
    meta.setdefault("passes", {})

    def save_meta():
        """Write the run's metadata file, so an interrupted run still reports what it did."""
        G.jdump(meta, META)

    # The no-limit pass is the grid the base checkpoints ran: one row per (question, cap), the same
    # fields, the same file-name shape, so alloc loads it beside them (work/production/alloc/cells.py
    # cell_paths matches cells_<task>_<checkpoint>_k*.jsonl). The budgeted passes are a DIFFERENT
    # protocol -- one generation per stated budget -- and would collide with it on (k, cap, row), so
    # they go in their own file, which no alloc pattern matches.
    CP = os.path.join(P["artifacts"], "cells_%s.jsonl" % TAG)
    CPB = os.path.join(P["artifacts"], "cells_budget_%s.jsonl" % TAG)

    def ckpt_key(r):
        """Return the resume key of one written cell row: dataset row, budget, token cap."""
        return (int(r["row_idx"] if "row_idx" in r else r["idx"]), G.budget_key(r["budget"]),
                r["B"])

    done = load_ckpt(CP, ckpt_key)
    done.update(load_ckpt(CPB, ckpt_key))
    apc, apb = Appender(CP), Appender(CPB)

    def prompts_for(T):
        """Return one prompt per question at token cap T, built by the same function training uses."""
        return [G.eval_prompt(cfg, tok, TASK, r["input"], T, WITH_LINE) for r in rows]

    def generate(enc, plen, limit, key):
        """Generate each question's chain up to limit tokens; returns the token ids per question and (natural stop position, stop marker) per question."""
        cur = {i: {"ids": [], "done": False} for i in range(N)}
        if limit <= 0:
            return cur, {i: (0, None) for i in range(N)}
        waves = G.generation_waves(limit)
        for T_next in waves:
            stuck = 0
            while True:
                todo = [i for i in range(N) if not cur[i]["done"] and len(cur[i]["ids"]) < T_next]
                if not todo or stuck > 2:
                    break
                Tn = min(len(cur[i]["ids"]) for i in todo)
                at_T = sorted([i for i in todo if len(cur[i]["ids"]) == Tn], key=lambda i: plen[i])
                before = sum(len(cur[i]["ids"]) for i in range(N))
                b, gi = BATCH_CAP, 0
                while gi < len(at_T):
                    grp = at_T[gi:gi + b]
                    nb, _ = batch_for(K, max(plen[i] for i in grp) + T_next + len(SUF) + NANS_T)
                    if nb < len(grp):
                        b = min(b, nb)
                        grp = at_T[gi:gi + b]
                    try:
                        g, _dt = decode(model, tok, [enc[i] + cur[i]["ids"] for i in grp],
                                        T_next - Tn, PAD, CF, K, [tok.eos_token_id], pieces,
                                        stops)
                    except torch.OutOfMemoryError as e:
                        line = "OOM gen %s b=%d T=%d->%d: %s" % (key, len(grp), Tn, T_next,
                                                                 str(e).split("\n")[0])
                        meta["oom_events"].append(line)
                        print("[OOM] " + line, flush=True)
                        traceback.clear_frames(e.__traceback__)
                        e.__traceback__ = None
                        gc.collect(); torch.cuda.empty_cache(); gc.collect()
                        if b == 1:
                            meta["errors"]["gen_%s" % key] = line
                            save_meta()
                            break
                        b = max(1, b // 2)
                        continue
                    g = strip_tail(g, [tok.eos_token_id])
                    for j, i in enumerate(grp):
                        cur[i]["ids"] = cur[i]["ids"] + g[j]
                        c, mk = find_cut(cur[i]["ids"])
                        cur[i]["done"] = bool((mk is not None) or len(cur[i]["ids"]) >= limit)
                    gi += len(grp)
                    gc.collect(); torch.cuda.empty_cache()
                stuck = stuck + 1 if sum(len(cur[i]["ids"]) for i in range(N)) == before else 0
            if all(cur[i]["done"] for i in cur):
                break
        if any(not cur[i]["done"] for i in range(N)):
            raise RuntimeError("generation did not reach a natural stop or its token cap")
        st = {}
        for i in range(N):
            c, mk = find_cut(cur[i]["ids"])
            st[i] = (min(c, limit), mk)
        return cur, st

    def stop_reason(T, marker):
        """Return why one generation ended: its own stop marker, the stated budget, or the horizon."""
        if marker is not None:
            return "natural"
        return "horizon" if T is None else "budget"

    def read_out(enc, cur, st_cur, plen, jobs, T, bl, bl_text, key, limit):
        """Write missing cell rows for (prompt,cut length,caps) jobs; token costs include prompt, cut, suffix, and realised read-out."""
        jobs = [(i, c, bs) for (i, c, bs) in jobs
                if any((int(rows[i]["idx"]), G.budget_key(T), B) not in done for B in bs)]
        jobs.sort(key=lambda t: plen[t[0]] + t[1])
        b, gi, nrows = BATCH_CAP, 0, 0
        while gi < len(jobs):
            grp = jobs[gi:gi + b]
            nb, _ = batch_for(K, max(plen[i] + c for (i, c, _) in grp) + len(SUF) + NANS_T)
            if nb < len(grp):
                b = min(b, nb)
                grp = jobs[gi:gi + b]
            try:
                o, _dt = decode(model, tok,
                                [enc[i] + cur[i]["ids"][:c] + SUF for (i, c, _) in grp],
                                NANS_T, PAD, CF, K, [tok.eos_token_id], pieces, None)
            except torch.OutOfMemoryError as e:
                line = "OOM read %s b=%d: %s" % (key, len(grp), str(e).split("\n")[0])
                meta["oom_events"].append(line)
                print("[OOM] " + line, flush=True)
                traceback.clear_frames(e.__traceback__)
                e.__traceback__ = None
                gc.collect(); torch.cuda.empty_cache(); gc.collect()
                if b == 1:
                    meta["errors"]["read_%s" % key] = line
                    save_meta()
                    raise RuntimeError(line)
                b = max(1, b // 2)
                continue
            o = strip_tail(o, [tok.eos_token_id])
            for j, (i, c, bs) in enumerate(grp):
                atxt = tok.decode(o[j], clean_up_tokenization_spaces=False)
                ctxt = tok.decode(cur[i]["ids"][:c], clean_up_tokenization_spaces=False)
                opts = rows[i].get("options") or None
                gold = rows[i]["target"]
                pred_raw, own_raw = parse_forced(atxt, TASK, opts), parse_own(ctxt, TASK, opts)
                pred = G.parse_forced_fixed(atxt, TASK, opts)
                own = G.parse_own_fixed(ctxt, TASK, opts)
                ngen = c + len(o[j])
                for B in bs:
                    if (int(rows[i]["idx"]), G.budget_key(T), B) in done:
                        continue
                    row = {"idx": i, "row_idx": rows[i]["idx"], "split": split[i],
                           "arm": ARM_NAME, "target_arm": arm, "task": TASK, "k": K,
                           "budget": ("none" if T is None else int(T)),
                           "budget_line": bl_text, "no_budget_line": (not WITH_LINE), "B": B,
                           "correct": bool(G.ans_eq_fixed(pred, gold, TASK)), "pred": pred,
                           "gold": gold, "trace_answer": own,
                           "trace_correct": bool(G.ans_eq_fixed(own, gold, TASK)),
                           "pred_raw": pred_raw, "correct_raw": bool(ans_eq(pred_raw, gold, TASK)),
                           "trace_answer_raw": own_raw,
                           "trace_correct_raw": bool(ans_eq(own_raw, gold, TASK)),
                           "n_cut": c, "natural_stop": st_cur[i][0], "stop_marker": st_cur[i][1],
                           "stop_reason": stop_reason(T, st_cur[i][1]),
                           "chain_tail": ctxt[-TAIL:], "horizon": limit,
                           "n_trace": len(cur[i]["ids"]), "n_generated": ngen,
                           "n_prompt_tokens": plen[i], "n_budget_line_tokens": bl,
                           "n_answer_tokens": len(o[j]), "n_suffix_tokens": len(SUF),
                           "realised_tokens": ngen + len(SUF),
                           "cap_cost_tokens": B + len(SUF) + NANS_T,
                           "layer_passes": K * NL * (plen[i] + ngen + len(SUF)),
                           "layer_passes_promptfree": K * NL * (ngen + len(SUF)),
                           "layer_passes_cap": K * NL * (plen[i] + B + len(SUF) + NANS_T),
                           "layer_passes_cap_promptfree": K * NL * (B + len(SUF) + NANS_T),
                           "answer_text": atxt, "protocol": PROTOCOL,
                           "parser": "fixed_eos_strip"}
                    row["correct_v2"] = score_v2(row)
                    (apc if T is None else apb).write(row)
                    done[(int(rows[i]["idx"]), G.budget_key(T), B)] = row
                    nrows += 1
            gi += len(grp)
            gc.collect(); torch.cuda.empty_cache()
            if gi % (16 * max(1, b)) == 0 or gi >= len(jobs):
                print("    read %s %d/%d rows %d %.0fs peak %.2f GB"
                      % (key, gi, len(jobs), nrows, time.time() - T0,
                         torch.cuda.max_memory_allocated() / 1024 ** 3), flush=True)
                save_meta()
        return nrows

    for T in dict.fromkeys(GRID):
        caps = caps_for(T)
        if all((int(rows[i]["idx"]), G.budget_key(T), B) in done for i in range(N) for B in caps):
            continue
        key = "none" if T is None else G.budget_key(T)
        bl_text = G.budget_line(cfg, T, WITH_LINE)
        prompts = prompts_for(T)
        enc = [tok(p, add_special_tokens=False)["input_ids"] for p in prompts]
        plen = [len(e) for e in enc]
        bl = len(tok(bl_text, add_special_tokens=False)["input_ids"]) if bl_text else 0
        limit = HORIZON if T is None else int(T)
        cur, st_cur = generate(enc, plen, limit, key)
        nat = [st_cur[i][0] for i in range(N)]
        meta["passes"][key] = {"budget_line": bl_text, "budget_line_tokens": bl,
                               "prompt_tokens_mean": sum(plen) / max(1, len(plen)),
                               "generation_limit": limit, "caps_scored": list(caps),
                               "natural_stop_mean": sum(nat) / max(1, len(nat)),
                               "natural_stop_median": sorted(nat)[len(nat) // 2],
                               "natural_stop_max": max(nat) if nat else 0,
                               "hit_limit_share": sum(1 for i in st_cur if st_cur[i][1] is None)
                                                  / max(1, N)}
        save_meta()
        jobs = []
        for i in range(N):
            m = {}
            for B in caps:
                m.setdefault(min(st_cur[i][0], B), []).append(B)
            for c, bs in m.items():
                jobs.append((i, c, bs))
        read_out(enc, cur, st_cur, plen, jobs, T, bl, bl_text, key, limit)
        print("  budget %s done: natural stop mean %.1f, %.0fs"
              % (key, meta["passes"][key]["natural_stop_mean"], time.time() - T0), flush=True)
        del cur, enc
        gc.collect(); torch.cuda.empty_cache()

    apc.close()
    apb.close()
    meta["cells_written"] = len(done)
    meta["cells_file_no_limit"] = CP
    meta["cells_file_budgeted"] = CPB
    acc = {}
    for (i, tkey, B), r in done.items():
        if r["split"] != "eval":
            continue
        acc.setdefault(tkey, {}).setdefault(str(B), []).append(r)
    meta["acc_by_budget"] = {t: {b: {"n": len(v),
                                     "acc": sum(x["correct"] for x in v) / len(v),
                                     "acc_own": sum(x["trace_correct"] for x in v) / len(v),
                                     "acc_v2": sum(x["correct_v2"] for x in v) / len(v)}
                                 for b, v in d.items()} for t, d in acc.items()}
    meta["seconds"] = round(time.time() - T0, 1)
    meta["peak_gb"] = round(torch.cuda.max_memory_allocated() / 1024 ** 3, 3)
    save_meta()
    print("DONE %s %d cells %.0fs peak %.2f GB"
          % (TAG, len(done), meta["seconds"], meta["peak_gb"]), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
