"""Generate standard-exemplar and short-exemplar chains and write one correctness-labelled candidate row per pool question."""
import gc, json, os, sys, time, traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import targets as G


def main(argv):
    """Generate one chain per pool question under the standard or short exemplar block and append a correctness-labelled row per question; returns a process exit code."""
    TASK = argv[0]
    cfg_path, root, prompt_kind = G.DEFAULT_CONFIG, None, "standard"
    NP, BATCH, WAIT = None, None, True
    for a in argv[1:]:
        k, _, v = a.lstrip("-").partition("=")
        if k == "config":
            cfg_path = v
        elif k == "root":
            root = v
        elif k == "prompt":
            prompt_kind = v
        elif k == "n":
            NP = int(v)
        elif k == "batch":
            BATCH = int(v)
        elif k == "no-wait":
            WAIT = False
    G.require_root(root, "harvest.py")
    cfg = G.load_config(cfg_path)
    assert TASK in cfg["harvest"], "%s is not a harvest source (%s)" % (TASK, cfg.sources)
    assert prompt_kind in ("standard", "short"), prompt_kind
    TAGC = "A" if prompt_kind == "standard" else "B"
    K = int(cfg["k_harvest"])
    HORIZON = cfg.horizon(TASK)      # per source: the base model's chains are not one length
    NP = NP if NP is not None else int(cfg["harvest"][TASK]["n"])
    BATCH = BATCH if BATCH is not None else int(cfg["harvest_batch"])
    EVAL_TASK = cfg.eval_task(TASK)
    P = G.paths(root)
    G.ensure_dirs(P)
    TAG = "%s_%s_k%d" % (TASK, TAGC, K)
    T0 = time.time()

    from s32_common import (MEM_FRACTION, set_steps, static_cache_factory, batch_for,
                            make_find_cut, decode, strip_tail, token_pieces, nvsmi, gpu_procs,
                            load_ckpt, Appender, load_base)
    from s3_patch import patch_universal_cache
    import torch
    print("[harvest %s prompt=%s frac=%.2f] %s | %s"
          % (TAG, prompt_kind, MEM_FRACTION, nvsmi(), gpu_procs()), flush=True)

    rows = []
    with open(os.path.expanduser(cfg["pool_jsonl"]), encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if r.get("src") == TASK:
                rows.append(r)
                if len(rows) >= NP:
                    break
    N = len(rows)
    print("[%s] %d questions from the pool (asked for %d)" % (TAG, N, NP), flush=True)

    qp, ap_, suffix_text, stops, marker, kind = G.task_bits(EVAL_TASK)
    tok, model = load_base()
    if WAIT:
        G.wait_for_gpu(os.path.join(P["logs"], "gpu_wait.log"))
    patch_universal_cache(model)
    set_steps(model, K)
    CF = static_cache_factory(model, K)
    PAD = tok.pad_token_id
    pieces = token_pieces(tok, model.config.vocab_size)
    find_cut = make_find_cut(tok, "base", stops, [tok.eos_token_id])

    if prompt_kind == "standard":
        prefix, prefix_src = G.few_shot_prefix(tok, EVAL_TASK), "evaluation harness"
    else:
        prefix_src = G.short_prompt_path(P, cfg, TASK)
        with open(prefix_src, encoding="utf-8") as f:
            prefix = f.read()
    prompts = [prefix + qp + r["question"] + ap_ for r in rows]
    enc = [tok(p, add_special_tokens=False)["input_ids"] for p in prompts]
    plen = [len(e) for e in enc]

    OUT = os.path.join(P["artifacts"], "harvest_%s.jsonl" % TAG)
    done = load_ckpt(OUT, lambda r: int(r["pool_i"]))
    todo0 = [i for i in range(N) if int(rows[i]["pool_i"]) not in done]
    print("[%s] resume: %d done, %d to do; prefix %d tokens, prompt mean %.0f"
          % (TAG, len(done), len(todo0),
             len(tok(prefix, add_special_tokens=False)["input_ids"]),
             sum(plen) / max(1, len(plen))), flush=True)
    ap = Appender(OUT)
    cur = {i: {"ids": [], "done": False} for i in todo0}
    written = set()

    def emit(i):
        """Write a completed pool question once, including chain text, token length, parsed answer, and correctness; resume keys use pool IDs."""
        if i in written or int(rows[i]["pool_i"]) in done:
            return
        c, mk = find_cut(cur[i]["ids"])
        c = min(c, HORIZON)
        chain = tok.decode(cur[i]["ids"][:c], clean_up_tokenization_spaces=False)
        chain = G.trim_answer_sentence(chain, EVAL_TASK)
        c = len(G.chain_ids(tok, prompts[i], chain)[1])
        own = G.parse_own_fixed(chain, EVAL_TASK, rows[i].get("options"))
        ok = bool(G.ans_eq_fixed(own, rows[i]["gold"], EVAL_TASK))
        hit = bool(mk is None)
        # a chain that ran into the horizon never finished, so it is not a correct chain whatever
        # its text parses to: it is dropped from the kept pool and counted in the meta
        row = {"i": i, "pool_i": rows[i].get("pool_i"), "src": TASK, "eval_task": EVAL_TASK,
               "question": rows[i]["question"], "gold": rows[i]["gold"],
               "options": rows[i].get("options"), "chain": chain, "n_chain": c,
               "own_answer": own, "answer_correct": ok,
               "kept": bool(ok and not hit) if cfg["harvest_correct_only"] else bool(not hit),
               "stop_marker": mk, "hit_horizon": hit, "horizon": HORIZON,
               "prompt": prompt_kind, "chain_tag": TAGC}
        ap.write(row)
        done[int(rows[i]["pool_i"])] = row
        written.add(i)

    for T_next in G.generation_waves(HORIZON):
        stuck = 0
        while True:
            todo = [i for i in todo0 if not cur[i]["done"] and len(cur[i]["ids"]) < T_next]
            if not todo or stuck > 2:
                break
            Tn = min(len(cur[i]["ids"]) for i in todo)
            at_T = sorted([i for i in todo if len(cur[i]["ids"]) == Tn], key=lambda i: plen[i])
            before = sum(len(cur[i]["ids"]) for i in todo0)
            b, gi = BATCH, 0
            while gi < len(at_T):
                grp = at_T[gi:gi + b]
                nb, _ = batch_for(K, max(plen[i] for i in grp) + T_next + 16)
                if nb < len(grp):
                    b = min(b, nb)
                    grp = at_T[gi:gi + b]
                try:
                    g, _dt = decode(model, tok, [enc[i] + cur[i]["ids"] for i in grp],
                                    T_next - Tn, PAD, CF, K, [tok.eos_token_id], pieces, stops)
                except torch.OutOfMemoryError as e:
                    print("[OOM] b=%d T=%d->%d: %s"
                          % (len(grp), Tn, T_next, str(e).split("\n")[0]), flush=True)
                    traceback.clear_frames(e.__traceback__)
                    e.__traceback__ = None
                    gc.collect(); torch.cuda.empty_cache(); gc.collect()
                    if b == 1:
                        raise
                    b = max(1, b // 2)
                    continue
                g = strip_tail(g, [tok.eos_token_id])
                for j, i in enumerate(grp):
                    cur[i]["ids"] = cur[i]["ids"] + g[j]
                    c, mk = find_cut(cur[i]["ids"])
                    cur[i]["done"] = bool((mk is not None) or len(cur[i]["ids"]) >= HORIZON)
                    if cur[i]["done"]:
                        emit(i)
                gi += len(grp)
                gc.collect(); torch.cuda.empty_cache()
            stuck = stuck + 1 if sum(len(cur[i]["ids"]) for i in todo0) == before else 0
        if all(cur[i]["done"] for i in todo0):
            break
    for i in todo0:
        if not cur[i]["done"]:
            raise RuntimeError("harvest generation did not finish; leave the row pending for resume")
        emit(i)
    ap.close()

    kept = [r for r in done.values() if r["kept"]]
    lens = sorted(r["n_chain"] for r in kept)
    meta = {"task": TASK, "eval_task": EVAL_TASK, "prompt": prompt_kind, "chain_tag": TAGC,
            "prefix_source": prefix_src,
            "k": K, "n_questions": len(done), "n_kept": len(kept),
            "kept_frac": len(kept) / max(1, len(done)),
            "horizon": HORIZON,
            "n_hit_horizon": sum(1 for r in done.values() if r["hit_horizon"]),
            "horizon_hit_share": sum(1 for r in done.values() if r["hit_horizon"])
                                 / max(1, len(done)),
            "n_correct_but_unfinished": sum(1 for r in done.values()
                                            if r.get("answer_correct") and r["hit_horizon"]),
            "len_mean": (sum(lens) / len(lens)) if lens else None,
            "len_median": lens[len(lens) // 2] if lens else None,
            "len_p10": lens[int(0.1 * len(lens))] if lens else None,
            "len_p90": lens[int(0.9 * len(lens))] if lens else None,
            "len_min_max": [lens[0], lens[-1]] if lens else None,
            "share_le_64": (sum(1 for x in lens if x <= 64) / len(lens)) if lens else None,
            "share_le_128": (sum(1 for x in lens if x <= 128) / len(lens)) if lens else None,
            "prefix_tokens": len(tok(prefix, add_special_tokens=False)["input_ids"]),
            "prompt_tokens_mean": sum(plen) / max(1, len(plen)),
            "seconds": round(time.time() - T0, 1),
            "peak_gb": round(torch.cuda.max_memory_allocated() / 1024 ** 3, 3)}
    G.jdump(meta, os.path.join(P["artifacts"], "harvest_meta_%s_%s.json" % (TASK, TAGC)))
    print("DONE harvest %s: kept %d/%d (%.3f) at horizon %d, %d hit it (%d of them parsed "
          "correctly and were dropped), len mean %s median %s, %.0fs"
          % (TAG, meta["n_kept"], meta["n_questions"], meta["kept_frac"], HORIZON,
             meta["n_hit_horizon"], meta["n_correct_but_unfinished"], meta["len_mean"],
             meta["len_median"], meta["seconds"]), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
