"""Validate prompt bytes, token masks, visit boundaries, execution depth, pool membership and the realised draw weights before training."""
import json, os, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import targets as G

# V10's tolerance: the realised T and depth histograms may sit this far, in shares, from the
# weights stage 0 intended. Only dropped draws can move them apart.
V10_TOL = 0.05


def upd(CK, **kw):
    """Merge keyword results into the shared checks JSON at CK."""
    d = G.jload(CK, {}) or {}
    d.update(kw)
    G.jdump(d, CK)


def get_tok(cfg):
    """Return the base tokenizer with a pad token guaranteed."""
    from transformers import AutoTokenizer
    t = AutoTokenizer.from_pretrained(cfg["base_repo"], trust_remote_code=True)
    if t.pad_token is None:
        t.pad_token = t.eos_token
    return t


def load_arrays(cfg, P, arm):
    """Return one arm's block arrays keyed by block length, plus its visit spans; padding is included in the arrays and excluded by every span."""
    D = G.data_dir(P, arm)
    arrays = {}
    for name in sorted(os.listdir(D)):
        if name.startswith("blocks_") and name.endswith(".npy"):
            L = int(name[len("blocks_"):-len(".npy")])
            arrays[L] = {"blocks": np.load(os.path.join(D, name)),
                         "mask": np.load(os.path.join(D, "mask_%d.npy" % L)),
                         "depth": np.load(os.path.join(D, "bdepth_%d.npy" % L)),
                         "visit": np.load(os.path.join(D, "bvisit_%d.npy" % L))}
    spans = [json.loads(l) for l in open(os.path.join(D, "spans.jsonl"), encoding="utf-8")]
    return arrays, spans


# ================================================================= V4 (GPU)
def run_v4(cfg, P, arm, CK, wait=False):
    """Check on GPU that a batched forward at one depth equals the same blocks forwarded singly, and that another depth differs; waits for an idle GPU only when asked; returns a process exit code."""
    import torch
    from s3_patch import patch_universal_cache
    # the preflight is a two-minute job: it waits only under the shared-box policy, never on a
    # scheduled job and never when --no-wait says the caller has the GPU already
    waited = G.wait_for_gpu(os.path.join(P["logs"], "gpu_wait.log")) if wait else {"waited_s": 0}
    arrays, _spans = load_arrays(cfg, P, arm)
    sched = json.load(open(os.path.join(G.data_dir(P, arm), "schedule.json"), encoding="utf-8"))
    from s32_common import load_base
    tok, model = load_base()
    patch_universal_cache(model)
    model.eval()
    res, worst = {}, 0.0
    with torch.no_grad():
        for mb in sched[:3]:
            d, L, idx = int(mb["depth"]), int(mb["seq_len"]), mb["blocks"]
            x = torch.tensor(arrays[L]["blocks"][idx], dtype=torch.long, device=G.DEV)
            with G.execution_depth(model, d):
                a = model(input_ids=x).logits.float()
                b = torch.cat([model(input_ids=x[i:i + 1]).logits.float()
                               for i in range(x.shape[0])], 0)
            m = float((a - b).abs().max())
            res["depth_%d_L%d_batch_vs_rows" % (d, L)] = m
            worst = max(worst, m)
            with G.execution_depth(model, 1 if d != 1 else 4):
                c = model(input_ids=x).logits.float()
            res["depth_%d_L%d_vs_other_depth" % (d, L)] = float((a - c).abs().max())
            del a, b, c, x
            torch.cuda.empty_cache()
    res["max_abs_diff"] = worst
    res["waited_for_gpu"] = bool(wait)
    res["gpu_wait"] = waited
    res["depth_switch_is_effective"] = bool(
        all(v > 0 for k, v in res.items() if k.endswith("vs_other_depth")))
    G.jdump(res, os.path.join(P["gates"], "v4_preflight.json"))
    upd(CK, V4=worst, V4_detail=res)
    print(json.dumps(res, indent=2), flush=True)
    assert worst == 0.0, worst
    assert res["depth_switch_is_effective"], res
    print("V4 OK", flush=True)
    return 0


# ================================================================= V1, V2, V3-CONTEXT, V9, V10 (CPU)
def run_cpu(cfg, P, arm, CK):
    """Run the CPU gates (V1 prompt parity, V2 masks, V3-CONTEXT with its negative control, V9 pool membership, V10 draw weights) and stop on the first failure; returns a process exit code."""
    tok = get_tok(cfg)
    from s32_common import build_prompts
    A = cfg.arm(arm)
    with_line = bool(A["budget_line"])

    # V9 argues about a named set of screened questions, so the pool is pinned by content and
    # every gate run re-checks it before reading a single row
    pool_sha256 = G.check_pool(cfg)
    pool = {}
    with open(os.path.expanduser(cfg["pool_jsonl"]), encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            pool.setdefault(r["src"], []).append(r)

    # ---------------------------------------------------------------- V1
    v1 = {"arm": arm, "budget_line_present": with_line, "n_checked": 0, "diffs": 0, "detail": [],
          "by_task": {}}
    for src in cfg.sources:
        et = cfg.eval_task(src)
        rows = pool[src][:20]
        s32rows = [{"idx": i, "input": r["question"], "target": r["gold"],
                    "options": r.get("options")} for i, r in enumerate(rows)]
        ref, _S, _st, _eos, extra = build_prompts(tok, et, s32rows, "A0", 4, None,
                                                  tag_override="")
        nd = 0
        for T in cfg.budget_grid_for(src):      # every budget THIS source can draw, no others
            bl = G.budget_line(cfg, T, with_line)
            ap = G.task_bits(et)[1]
            for i, r in enumerate(rows):
                mine = G.eval_prompt(cfg, tok, et, r["question"], T, with_line)
                v1["n_checked"] += 1
                if with_line and mine.count(bl) != 1:
                    nd += 1
                    v1["detail"].append({"task": src, "T": str(T), "i": i,
                                         "reason": "budget line appears %d times"
                                                   % mine.count(bl)})
                    continue
                stripped = mine.replace(bl, "", 1) if with_line else mine
                if stripped != ref[i]:
                    nd += 1
                    v1["detail"].append({"task": src, "T": str(T), "i": i,
                                         "reason": "prompt differs from the harness once the "
                                                   "budget line is removed",
                                         "mine_len": len(stripped), "ref_len": len(ref[i])})
                    continue
                if str(cfg["budget_line_position"]) != "after_question_before_answer_prefix":
                    raise AssertionError("unsupported budget_line_position %r"
                                         % cfg["budget_line_position"])
                if not mine.endswith(bl + ap):
                    nd += 1
                    v1["detail"].append({"task": src, "T": str(T), "i": i,
                                         "reason": "budget line is not immediately before the "
                                                   "answer prefix"})
        v1["by_task"][src] = {"diffs": nd, "tag_line": extra.get("tag_line"),
                              "budget_line_tokens": {
                                  str(T): len(tok(G.budget_line(cfg, T, with_line),
                                                  add_special_tokens=False)["input_ids"])
                                  for T in cfg.budget_grid_for(src)},
                              "harvest_horizon": cfg.horizon(src)}
        v1["diffs"] += nd
    v1["detail"] = v1["detail"][:20]
    G.jdump(v1, os.path.join(P["gates"], "v1_parity.json"))
    print("[V1] %d prompts checked, %d diffs" % (v1["n_checked"], v1["diffs"]), flush=True)

    # ---------------------------------------------------------------- V2
    visits = [json.loads(l) for l in open(os.path.join(G.data_dir(P, arm), "visits.jsonl"),
                                          encoding="utf-8")]
    records, _hs = G.load_records(cfg, P)
    bykey = {(r["src"], r["pool_i"]): r for r in records}
    arrays, spans = load_arrays(cfg, P, arm)
    L_ = ["# V2: loss masks", "",
          "20 visits rebuilt from data/visits.jsonl, every token printed with the supervised ones",
          "marked. The prompt, the budget line, the forced suffix and the PADDING must never be",
          "supervised; the chain, the answer sentence and one EOS must be.", ""]
    rng = np.random.default_rng(int(cfg["seed"]))
    sel = rng.choice(len(visits), size=min(20, len(visits)), replace=False)
    v2_ok = True
    for si in sel:
        v = visits[int(si)]
        r = bykey[(v["src"], v["record"])]
        T = v["T"]
        ids, msk, info = G.build_target(cfg, tok, arm, r["src"], r["question"], r["gold"], T,
                                        r["chain_A"], r["chain_B"],
                                        fullplus=(v["kind"] == "CHAIN_PLUS"),
                                        fallback_chain_A=r.get("fallback_chain_A"))
        et = cfg.eval_task(r["src"])
        prompt = G.eval_prompt(cfg, tok, et, r["question"], T, with_line)
        n_p = len(tok(prompt, add_special_tokens=False)["input_ids"])
        n_s = info["n_suffix"]
        bad = []
        if ids is None:
            bad.append("visit no longer builds")
        else:
            if any(msk[:n_p]):
                bad.append("a prompt or budget-line token is supervised")
            if info["kind"] in ("DIRECT", "FALLBACK", "CHAIN_PLUS"):
                st = n_p + (info["n_chain"] if info["kind"] != "DIRECT" else 0)
                if any(msk[st:st + n_s]):
                    bad.append("a suffix token is supervised")
            if msk[-1] != 1:
                bad.append("EOS not supervised")
            if info["kind"] in ("CHAIN", "CHAIN_PLUS") and not any(msk[n_p:n_p + info["n_chain"]]):
                bad.append("chain not supervised")
            if info["n_supervised"] != v["n_supervised"]:
                bad.append("supervised count %d != manifest %d"
                           % (info["n_supervised"], v["n_supervised"]))
        if bad:
            v2_ok = False
        L_ += ["## visit %d  src=%s T=%s kind=%s chain=%s n_sup=%s  %s"
               % (si, r["src"], T, v["kind"], v["chain_used"], v["n_supervised"],
                  ("BAD: " + "; ".join(bad)) if bad else "ok"), "",
               "prompt tokens %d (budget line %s), suffix %d, block %d"
               % (n_p, v["budget_line_tokens"], n_s, v["block_len"]), "```"]
        if ids is not None:
            for j in range(max(0, n_p - 6), len(ids)):
                L_.append("%5d %s %r" % (j, "*" if msk[j] else ".",
                                         tok.decode([ids[j]],
                                                    clean_up_tokenization_spaces=False)))
        L_ += ["```", ""]

    # whole-array padding clause: every block is a visit of n_tokens followed by padding, and no
    # padded position may be supervised anywhere in the data set
    pad_bad = 0
    n_pad = 0
    for s in spans:
        m = arrays[s["L"]]["mask"][s["block"]]
        n_pad += int(s["L"] - s["end"])
        if m[s["end"]:].any():
            pad_bad += 1
    v2_ok = v2_ok and pad_bad == 0
    L_ += ["## padding", "",
           "%d padded positions across %d blocks; supervised padded positions: %d"
           % (n_pad, len(spans), pad_bad), ""]
    open(os.path.join(P["gates"], "v2_loss_mask.txt"), "w", encoding="utf-8").write("\n".join(L_))
    print("[V2] %s (padding: %d bad blocks)" % ("OK" if v2_ok else "FAILED", pad_bad), flush=True)

    # ---------------------------------------------------------------- V3-CONTEXT
    v3 = G.v3_context(arrays, spans, pad_id=tok.pad_token_id)
    # negative control: the SAME visits packed the old way must fail, or the gate is vacuous
    demo = []
    for s in spans[:64]:
        b, st, en = s["block"], s["start"], s["end"]
        demo.append({"ids": arrays[s["L"]]["blocks"][b, st:en].tolist(),
                     "mask": arrays[s["L"]]["mask"][b, st:en].tolist(),
                     "n_prompt": int(s["visit_prompt_len"])})
    ctrl = {"ran": False}
    if demo:
        la, ls = G.legacy_pack(demo, 512)
        ctrl = G.v3_context(la, ls)
        ctrl["ran"] = True
    v3_out = {"real": v3, "legacy_control": ctrl,
              "split_detected": bool(ctrl.get("ran") and not ctrl["ok"])}
    G.jdump(v3_out, os.path.join(P["gates"], "v3_context.json"))
    print("[V3-CONTEXT] real ok=%s (%d supervised tokens); legacy control detected=%s"
          % (v3["ok"], v3["n_supervised_tokens"], v3_out["split_detected"]), flush=True)

    # ---------------------------------------------------------------- V9
    # The s33 screening record (drop_near and the overlap counts) ships with the package; the
    # spike read it from the Spark's ~/latent-loop/s33, kept as the fallback.
    s33_v9 = (G.jload(os.path.join(HERE, "data", "v9_contamination.json"), {})
              or G.jload(os.path.expanduser("~/latent-loop/s33/gates/v9_contamination.json"), {})
              or {})
    poolq = {G.norm_q(r["question"]) for src in pool for r in pool[src]}
    missing = n_h = 0
    for src in cfg.sources:
        for tag in ("A", "B"):
            p = os.path.join(P["artifacts"], "harvest_%s_%s_k%d.jsonl"
                             % (src, tag, int(cfg["k_harvest"])))
            if not os.path.exists(p):
                continue
            with open(p, encoding="utf-8") as f:
                for line in f:
                    h = json.loads(line)
                    n_h += 1
                    if G.norm_q(h["question"]) not in poolq:
                        missing += 1
    # the MATH shot helper falls back to evaluation rows when no training split is reachable
    shots = (G.math_shot_source()
             if any(cfg.eval_task(s) in ("math", "math500") for s in cfg.sources) else None)
    G.check_exemplar_source(shots)
    man = G.jload(os.path.join(P["artifacts"], "target_manifest_%s.json" % arm), {}) or {}
    G.check_exemplars(tok, cfg, man.get("exemplar_sha256"))
    v9 = {"n_harvest_questions": n_h, "not_in_pool": missing,
          "pool_jsonl": cfg["pool_jsonl"], "pool_sha256": pool_sha256,
          "exemplar_sha256": G.exemplar_fingerprints(tok, cfg), "math_exemplar_source": shots,
          "s33_v9_exact_overlaps_left_in_pool": s33_v9.get("V9_overlap"),
          "s33_v9_near_duplicates_dropped": s33_v9.get("n_near_duplicates"),
          "s33_v9_drop_near": s33_v9.get("drop_near"),
          "s33_v9_pool_after": s33_v9.get("n_pool_after"),
          "argument": ("every harvest question comes from the screened pool, which was checked "
                       "against GSM8K test, MATH500, SVAMP test, AQuA test, CSQA validation, the "
                       "two BBH files and the five calibration sets, with every exact overlap and "
                       "every near-duplicate dropped. This recipe introduces no new question.")}
    G.jdump(v9, os.path.join(P["gates"], "v9_contamination.json"))
    print("[V9] %d harvest questions, %d not in the pool" % (n_h, missing), flush=True)

    # ---------------------------------------------------------------- V10
    # The two draws ARE the objective. The manifest carries both the table stage 0 wrote and the
    # histogram the draw realised, so this gate is the one place the objective on disk is checked
    # against the objective on paper. Drops (a visit longer than the longest bucket, a question
    # with no correct chain) are the only way the two can part, and they are counted per T, so a
    # gap over the tolerance names the T or the depth that went missing.
    tw_sha = G.check_theory_weights(cfg)        # re-pinned here, as V9 re-pins the pool
    v10 = G.v10_draw_weights(man, tol=V10_TOL)
    v10["theory_weights_sha256_on_disk"] = tw_sha
    v10["ok"] = bool(v10["ok"] and man.get("theory_weights_sha256") == tw_sha)
    G.jdump(v10, os.path.join(P["gates"], "v10_draw_weights.json"))
    print("[V10] draw=%s, worst |realised - intended| = %.4f over %d tables (tol %.2f)"
          % (v10.get("draw"), v10["worst"], len(v10["by_source"]), V10_TOL), flush=True)

    upd(CK, arm=arm, V1=int(v1["diffs"]), V1_n_checked=int(v1["n_checked"]), V2=bool(v2_ok),
        V2_padding_bad_blocks=int(pad_bad), V3_CONTEXT=bool(v3["ok"]),
        V3_CONTEXT_split_detected=bool(v3_out["split_detected"]),
        V3_CONTEXT_supervised_tokens=int(v3["n_supervised_tokens"]), V9=int(missing),
        V9_detail=v9, V10=bool(v10["ok"]), V10_worst_dev=float(v10["worst"]), V10_detail=v10)
    assert v1["diffs"] == 0, v1["detail"][:3]
    assert v2_ok, "see gates/v2_loss_mask.txt"
    assert v3["ok"], v3
    assert v3_out["split_detected"], "V3-CONTEXT did not detect a deliberately split stream"
    assert missing == 0, missing
    assert s33_v9.get("drop_near") is True, s33_v9
    assert v10["ok"], {k: v for k, v in v10["by_source"].items() if not v["within_tol"]}
    print("V1 V2 V3-CONTEXT V9 V10 OK", flush=True)
    return 0


def main(argv):
    """Dispatch to the CPU gates or the GPU preflight for one arm; returns a process exit code."""
    mode = "--v4" if "--v4" in argv else "--cpu"
    cfg_path, root, arm, sources = G.DEFAULT_CONFIG, None, None, None
    for a in argv:
        k, _, v = a.lstrip("-").partition("=")
        if k == "config":
            cfg_path = v
        elif k == "root":
            root = v
        elif k == "arm":
            arm = v
        elif k == "sources":
            sources = v
    G.require_root(root, "gates.py")
    cfg = G.load_config(cfg_path, sources)
    arm = arm or cfg["default_arm"]
    P = G.paths(root)
    G.ensure_dirs(P)
    CK = os.path.join(P["gates"], "checks.json")
    if mode != "--v4":
        return run_cpu(cfg, P, arm, CK)
    return run_v4(cfg, P, arm, CK, wait=G.should_wait_for_gpu(argv))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
