"""One (model, task, depth, shard) generation job.

  python -m prod.generate --model=ouro_1_4b_base --task=gsm8k --k=4 \
      [--protocol=natural|forced] [--n=N] [--shard=0 --shards=1] [--adapter=DIR] \
      [--caps=0,16,32,64,128,256,512] [--extra-caps=48,96,192,384] [--horizon=512] \
      [--batch-cap=32] [--mem-fraction=0.85] [--tag-loops --tag-tokens] [--out=DIR] \
      [--batch-width=N] [--no-mask] [--wall-clock] [--resume-from-chains]

Protocol (natural stop), ported from s32_run.py and s28_common:
  generate once at the horizon with the model's own stop rule, then cut(B) = trace[:min(B, natural
  stop)] and run ONE forced read-out per DISTINCT cut length, serving every budget that shares it.
  Both parses are stored per cap, and protocol v2 is computed from the stored fields (decision D1).

Protocol (forced continuation), ported from s13_common.decode(stopper=...) / make_stopper:
  no row ever stops; a token that would stop is replaced by the "Wait," tokens, so every row emits
  exactly `horizon` tokens. GSM8K and MATH500 on the Ouro checkpoints only.

Pinned by the rulings on PP2 protocol decisions (PLAN.md, 2026-09-12):
  * batch width 16 in every production run (Q6 clause iv), stored per row as `batch_width` with the
    actual group size of the generation and of the read-out beside it. `--batch-width=0` restores the
    adaptive KV-ceiling width and exists for the gates, which reproduce spikes that ran that way.
  * the forced read-out is truncated at its eos, KEEPING the eos token, in every family (Q8 option
    O1: the rule of S13, S26, S32 and of every analysis of record). Where the strip removed text, the
    row also carries `nostrip` = what the answer would have been without it, so gate G1 can attribute
    a mismatch against the S9a-family spikes to the strip rule with no second generation.
  * forced continuation defaults to the spike's N (GSM8K 300, MATH500 500; Q2 option O1) and `--n`
    overrides it. The full-N forced block is priced separately (protocol decision Q15).

Every hyperparameter above is an argument; nothing is hard-coded in a driver.
Resumable at (problem, cut) granularity: traces and cells are append-only jsonl, re-read on start.
"""
import argparse
import gc
import json
import os
import sys
import time
import traceback

import torch

from . import config as cfgmod
from .common import (ART, Appender, BATCH_WIDTH, CAPS_EXTRA, CAPS_STANDARD, FORCED_BUDGETS,
                     FORCED_HORIZON, FORCED_N, HORIZON, env_report, gpu_procs, load_ckpt, nvsmi,
                     read_jsonl, save_json, sha256_text)
from .models import depths_for, get
from .tasks import (ans_eq, build_prompts, data_hashes, make_find_cut, parse_forced, parse_own,
                    row_kind, row_n_answer, rows as task_rows_of, split_labels, task_cfg)


# ------------------------------------------------------------------ protocol v2 (decision D1)
def score_v2(row):
    """s32_common.score_v2, verbatim: the model's own answer if it parses inside the cut, else the
    forced read-out. Computed from stored fields only."""
    if row.get("trace_answer") is not None:
        return bool(row["trace_correct"])
    return bool(row["correct"])


# ------------------------------------------------------------------ argument parsing
def build_parser():
    p = argparse.ArgumentParser(prog="prod.generate")
    p.add_argument("--model", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--k", type=int, required=True)
    p.add_argument("--protocol", default="natural", choices=("natural", "forced"))
    p.add_argument("--adapter", default=None, help="LoRA adapter directory (S32 tag convention)")
    p.add_argument("--n", type=int, default=None, help="use only the first N rows of the shard")
    p.add_argument("--shard", type=int, default=0)
    p.add_argument("--shards", type=int, default=1)
    p.add_argument("--only-rows", dest="only_rows", default=None,
                   help="a JSON file holding a list of row_idx values; generate exactly those "
                        "rows, in the task's own order (prod.live_check uses it to regenerate the "
                        "prompts the allocator chose a given cell for)")
    p.add_argument("--extra-caps", dest="extra_caps", default=",".join(str(c) for c in CAPS_EXTRA))
    p.add_argument("--no-extra-caps", dest="extra_caps", action="store_const", const="")
    p.add_argument("--mem-fraction", dest="mem_fraction", type=float, default=None)
    # every protocol default (caps, horizon, batch width, seed, forced block, depths, datasets)
    # comes from prod/config.py and is overridable here (PP3 decision 2)
    cfgmod.add_args(p)
    p.add_argument("--no-mask", dest="no_mask", action="store_true",
                   help="raven families only: never install the padding mask (batch-1 control)")
    p.add_argument("--tag-loops", dest="tag_loops", action="store_true",
                   help="S32 tag convention: prepend 'Loops: k.'")
    p.add_argument("--tag-tokens", dest="tag_tokens", action="store_true",
                   help="S32 tag convention: prepend 'Loops: k. Tokens: T.' (one pass per cap)")
    p.add_argument("--suffix", default=None, help="override the task's forced read-out suffix")
    p.add_argument("--out", default=None, help="artifacts directory (default prod artifacts/)")
    p.add_argument("--wall-clock", dest="wall_clock", action="store_true",
                   help="also write a wall-clock row for cost.py")
    p.add_argument("--resume-from-chains", dest="resume_from_chains", action="store_true",
                   help="forced protocol only (Fix 1, PP3b): when chains_<model>_<task>_k<k>.jsonl "
                        "(written by a prior natural-stop job on the same model/task/k) exists, "
                        "re-prefill prompt + its stored chain_ids instead of regenerating that span, "
                        "then apply the existing Wait injection and continue to the horizon; falls "
                        "back to full generation for a row missing from the file")
    p.add_argument("--save-traces", dest="save_traces", default="1")
    p.add_argument("--no-eos-cut", dest="eos_cut", action="store_false", default=True,
                   help="use the older S9a cut rule with no eos branch, which S9c and S9f "
                        "copied; gate G1 needs it to reproduce those two spikes exactly")
    return p


def tag_line(k, T=None, loops=False, tokens=False):
    """s32_common.tag_line: the one control line between the few-shot prompt and the question."""
    if tokens and T is not None:
        return "Loops: %d. Tokens: %d.\n" % (int(k), int(T))
    if loops or tokens:
        return "Loops: %d.\n" % int(k)
    return ""


# ------------------------------------------------------------------ chains (Fix 1, PP3b)
# A sidecar per (model, task, k) -- not per tag, so every shard of a run resumes the SAME file and
# rows are keyed by the task-global problem id (`idx`), which is stable across shards; a shard's
# local row number is not. Written once by a natural-stop job; read by a later forced job's
# `--resume-from-chains`. Greedy decoding is deterministic, so the natural pass's trace up to (and
# including) its own stop marker is byte-identical to what a forced pass would produce up to that
# same point -- storing it lets the forced job skip regenerating that span.
def chain_path(out_dir, model, task, k):
    return os.path.join(out_dir, "chains_%s_%s_k%d.jsonl" % (model.replace("+", "-"), task, int(k)))


def write_chains(out_dir, model, task, k, rws, enc, cur, st, bw):
    """One row per problem, appended once, resumable exactly like the cells file (skip a problem
    already present). `chain_ids` = cur[i]['ids'][:c] where c = st[i][0] (the cut find_cut found --
    the tokens up to and including the stop marker, or the whole trace when it never found one,
    i.e. the horizon). `prompt_sha256` fingerprints the encoded prompt (enc[i], the token ids), so a
    later resume can detect a prompt that changed underneath it (a different suffix, tag line, or
    tokenizer) and fall back to full generation instead of silently continuing the wrong context."""
    path = chain_path(out_dir, model, task, k)
    have = load_ckpt(path, lambda r: int(r["idx"]))
    ap = Appender(path)
    n = 0
    try:
        for i, r in enumerate(rws):
            ridx = int(r["idx"])
            if ridx in have or not cur[i].get("done"):
                continue            # a truncated trace (unrecoverable OOM) is never a chain
            c = st[i][0]
            c = len(cur[i]["ids"]) if c is None else int(c)
            ap.write({"idx": ridx, "natural_stop": (None if st[i][0] is None else int(st[i][0])),
                     "n_prompt_tokens": len(enc[i]),
                     "chain_ids": [int(x) for x in cur[i]["ids"][:c]],
                     "prompt_sha256": sha256_text(json.dumps(enc[i])), "batch_width": int(bw or 0)})
            n += 1
    finally:
        ap.close()
    return n, path


def seed_from_chain(chain_row, pieces, tail_window):
    """The prefill-and-continue bookkeeping `--resume-from-chains` needs: the resumed trace, and the
    tail-window seed a forced state's stopper requires (the last up-to-`tail_window` decoded pieces
    of the chain) so a pattern straddling the chain/continuation boundary (e.g. a '####' line split
    across the two) is still seen whole by the stopper on the very first newly generated token.
    Positions fall out for free: the caller sets fstate['off'] = len(cur[i]['ids']) exactly as it
    already does for a fresh row (generate.py, the wave loop), so an absolute position computed as
    off + len(gen[b]) is correct whether the trace started empty or from a stored chain."""
    ids = [int(x) for x in chain_row["chain_ids"]]
    tail_seed = [pieces[t] for t in ids[-tail_window:]] if pieces is not None else []
    return ids, tail_seed


# ------------------------------------------------------------------ the job
def main(argv=None):
    a = build_parser().parse_args(argv)
    cfg = cfgmod.from_args(a)
    forced = a.protocol == "forced"
    caps = sorted(set(cfg["forced_budgets"] if forced else cfg["caps"]))
    extra = [] if forced else sorted({int(x) for x in (a.extra_caps or "").split(",")
                                      if x.strip() != ""})
    # The pinned production width (rulings Q6 (iv)). 0 means "adaptive", the pre-pin behaviour.
    # Ruling Q12: when the caller did not pass an explicit --batch-width, the per-(model, k) table
    # in config.yaml applies (a.batch_width is the RAW cli value, None when the flag was omitted, so
    # an explicit --batch-width=N -- including the queue's own, which the launcher always sets from
    # this same table -- still wins).
    bw = int(cfg["batch_width"]) if a.batch_width is not None \
        else cfgmod.batch_width_for(a.model, a.k, cfg)
    bw = None if bw <= 0 else bw
    if forced:
        fn = cfg["forced_block"].get("n")
        if a.n is None and isinstance(fn, dict) and a.task in fn:
            a.n = int(fn[a.task])
        elif a.n is None and isinstance(fn, int):
            a.n = int(fn)
        # PP3 decision 4: fn None means FULL N, which is the default of record.
    all_caps = sorted(set(caps) | set(extra))
    horizon = int(cfg["forced_horizon"] if forced else cfg["horizon"])
    # A cap above the horizon cannot be honoured: its cut would be the horizon, and the row would
    # claim a budget it never spent. Drop it loudly rather than write a mislabelled row. (Under the
    # natural-stop protocol a trace that STOPS before a cap is a different matter: the cut is the
    # natural stop and the row is correct at every cap above it.)
    over = [c for c in all_caps if c > horizon]
    if over and forced:
        print("[warn] dropping caps above the horizon %d: %s" % (horizon, over), flush=True)
        caps = [c for c in caps if c <= horizon]
        extra = [c for c in extra if c <= horizon]
        all_caps = sorted(set(caps) | set(extra))
    out_dir = a.out or ART
    os.makedirs(out_dir, exist_ok=True)

    tcfg = task_cfg(a.task)
    if forced and not tcfg["forced"]:
        raise SystemExit("task %s has no forced-continuation protocol of record" % a.task)
    if a.k not in depths_for(a.model, a.task):
        print("[warn] depth %d is not in the depth set of record for %s on %s (%s)"
              % (a.k, a.model, a.task, depths_for(a.model, a.task)), flush=True)

    kw = {}
    if cfg.get("batch_cap"):
        kw["batch_cap"] = int(cfg["batch_cap"])
    if a.mem_fraction:
        kw["mem_fraction"] = a.mem_fraction
    ad = get(a.model, adapter_dir=a.adapter, **kw)
    if forced and ad.family != "ouro":
        raise SystemExit("forced continuation is of record for the Ouro checkpoints only "
                         "(Brief PP2); %s is %s" % (a.model, ad.family))

    # ---- rows, split, shard
    all_rows = task_rows_of(a.task)
    labels = split_labels(a.task, len(all_rows), cfg["split_seed"], cfg["n_cal"])
    sel = list(range(a.shard, len(all_rows), a.shards)) if a.shards > 1 else list(
        range(len(all_rows)))
    if a.only_rows:
        with open(a.only_rows, encoding="utf-8") as f:
            want = set(int(x) for x in json.load(f))
        sel = [i for i in sel if int(all_rows[i].get("row_idx", all_rows[i].get("idx", i))) in want]
    if a.n:
        sel = sel[:a.n]
    rws = [all_rows[i] for i in sel]
    spl = [labels[i] for i in sel]
    N = len(rws)

    tagged = bool(a.tag_tokens)
    tagstr = ("_tagT" if a.tag_tokens else ("_tagK" if a.tag_loops else ""))
    shardstr = "" if a.shards == 1 else "_s%dof%d" % (a.shard, a.shards)
    if a.only_rows:
        shardstr += "_sub%d" % N
    tag = "%s_%s_%s_k%d%s%s" % (a.model.replace("+", "-"), a.task, a.protocol, a.k, tagstr,
                                shardstr)
    t0 = time.time()
    print("[%s] N=%d caps=%s horizon=%d | %s | %s"
          % (tag, N, all_caps, horizon, nvsmi(), gpu_procs()), flush=True)

    from .models.ouro import strip_tail    # s9a_common.strip_tail, family-agnostic (Q8)
    gen_widths, ro_widths = {}, {}
    _t_load = time.time()
    ad.load()
    tok = ad.tok
    dinfo = ad.set_depth(a.k)
    load_seconds = round(time.time() - _t_load, 1)
    ast = bool(getattr(ad, "add_special_tokens", False))
    # PP3: pooled BBH mixes answer kinds, and word_sorting writes a list, so the forced read-out
    # length is a PER-ROW quantity. A read-out group decodes max(n_answer) new tokens; the extra
    # tokens on a short-answer row are truncated at its eos and never enter the accounting, which
    # stores len(o[j]) after the strip.
    nans_row = [row_n_answer(a.task, r) for r in rws]
    nans = max(nans_row) if nans_row else task_cfg(a.task)["n_answer"]

    meta_path = os.path.join(out_dir, "meta_%s.json" % tag)
    meta = json.load(open(meta_path, encoding="utf-8")) if os.path.exists(meta_path) else {}
    meta.update({"tag": tag, "model": a.model, "task": a.task, "k": a.k, "protocol": a.protocol,
                 "adapter": a.adapter, "caps": caps, "extra_caps": extra, "horizon": horizon,
                 "n_problems": N, "shard": a.shard, "shards": a.shards,
                 "n_eval": sum(1 for s in spl if s == "eval"),
                 "n_cal": sum(1 for s in spl if s == "cal"),
                 "cut_rule": "min(natural stop, B)" if not forced else "B tokens of a forced trace",
                 "n_answer_tokens": nans, "add_special_tokens": ast,
                 "config": cfg, "config_sha256": cfgmod.digest(cfg),
                 "tag_loops": bool(a.tag_loops), "tag_tokens": bool(a.tag_tokens),
                 "only_rows": a.only_rows,
                 "model_meta": ad.meta(), "depth_info": dinfo, "env": env_report(),
                 "data_hashes": data_hashes(), "argv": list(sys.argv),
                 "passes_per_token": ad.passes_per_token(a.k),
                 "kv_bytes_per_token": ad.kv_bytes_per_token(a.k),
                 "load_seconds": load_seconds,
                 "batch_width_pinned": bw or "adaptive (KV ceiling)",
                 "strip_at_eos": True, "eos_cut": bool(a.eos_cut),
                 "resume_from_chains": bool(a.resume_from_chains)})
    meta.setdefault("oom_events", [])
    meta.setdefault("errors", {})
    meta.setdefault("passes", {})

    def save_meta():
        save_json(meta_path, meta)

    cells_path = os.path.join(out_dir, "cells_%s.jsonl" % tag)
    done = load_ckpt(cells_path, lambda r: (int(r["idx"]), int(r["B"])))
    fresh = not os.path.exists(cells_path)
    apc = Appender(cells_path)
    if fresh:
        # PP3 decision 2: the effective config is the FIRST LINE of every cells file. Every reader
        # in the package skips a row with `_header` (common.read_jsonl / load_ckpt / count_cells).
        apc.write(cfgmod.header_row(cfg, tag, {"model": a.model, "task": a.task, "k": a.k,
                                               "protocol": a.protocol, "n_problems": N,
                                               "horizon": horizon, "caps": all_caps,
                                               "data_hashes": data_hashes()}))

    # ---------------------------------------------------------------- phase A: traces
    def gen_pass(T_cap, hor, key):
        """Generate traces for one pass. Returns (enc, cur, plen, stop_table, suffix_ids)."""
        tl = tag_line(a.k, T_cap, a.tag_loops, a.tag_tokens)
        prompts, suf, stops, eos_ids, extra_meta = build_prompts(
            tok, a.task, rws, chat_template=ad.chat_template, suffix_text=a.suffix)
        if tl:
            # the tag line goes between the few-shot prompt and the question (s32_common)
            prompts = [_insert_tag(p, tl, a.task, ad.chat_template) for p in prompts]
            extra_meta["tag_line"] = tl
        find_cut = make_find_cut(tok, stops or [], eos_ids, chat_template=ad.chat_template,
                                 eos_cut=bool(a.eos_cut))
        if ad.family in ("huginn", "mcleish"):
            # the family's stop ids of record (S9c: end_text, end_turn, begin_text for Huginn) join
            # the tokenizer eos, for the decoder, the cut rule and the strip alike
            eos_ids = sorted(set(eos_ids) | set(ad.stop_ids()))
            find_cut = make_find_cut(tok, stops or [], eos_ids, chat_template=ad.chat_template,
                                     eos_cut=bool(a.eos_cut))
        enc = [tok(p, add_special_tokens=ast)["input_ids"] for p in prompts]
        plen = [len(e) for e in enc]
        maxpos = getattr(ad, "max_positions", None)
        if maxpos:
            # Huginn indexes a rotary table of block_size (4096) entries by absolute position, so
            # prompt + trace + suffix + read-out must stay below it or the forward raises
            room = int(maxpos) - max(plen) - len(suf) - nans - 1
            if room < hor:
                print("[warn] %s: horizon %d clamped to %d (positions limited to %d; longest prompt "
                      "%d, read-out %d)" % (key, hor, max(16, room), maxpos, max(plen),
                                           len(suf) + nans), flush=True)
                hor = max(16, room)
        meta["passes"][key] = {"tag_line": tl, "horizon": hor, "horizon_requested": horizon,
                               "max_positions": maxpos, "suffix_text":
                               extra_meta["suffix_text"], "stop_strings": stops,
                               "eos_ids": eos_ids,
                               "prompt_tokens_mean": sum(plen) / max(1, len(plen)),
                               "prompt_tokens_min_max": [min(plen), max(plen)]}
        tp = os.path.join(out_dir, "trace_%s_%s.jsonl" % (tag, key))
        cur = {i: {"ids": [], "done": False} for i in range(N)}
        for i, r in load_ckpt(tp, lambda r: int(r["idx"])).items():
            if i < N:
                cur[i] = {"ids": r["ids"], "done": bool(r["done"])}
        apt = Appender(tp) if a.save_traces != "0" else None
        gen_tokens, gen_seconds = 0, 0.0

        if forced:
            from .models.ouro import TAIL_WINDOW, make_stopper, new_forced_states
            pieces = ad._pieces                     # noqa: SLF001  (the adapter's own table)
            stopper = make_stopper(ad.chat_template, pieces, eos_ids, a.task)
            wait = ad.wait_ids()
            meta["passes"][key].update({"wait_ids": wait, "wait_text": tok.decode(wait)})
            # ---- Fix 1 (PP3b): resume from a stored natural-stop chain instead of regenerating it.
            # A row whose OWN trace checkpoint already has ids (a resumed/incomplete forced job) is
            # left alone -- the chain is only for a row this forced job has not touched yet.
            chains_loaded, cpath = 0, chain_path(out_dir, a.model, a.task, a.k)
            if a.resume_from_chains and os.path.exists(cpath):
                chain_by_idx = {int(r["idx"]): r for r in read_jsonl(cpath)}
                for i in range(N):
                    if cur[i]["ids"]:
                        continue
                    cr = chain_by_idx.get(int(rws[i]["idx"]))
                    if cr is None:
                        continue
                    if cr.get("prompt_sha256") != sha256_text(json.dumps(enc[i])):
                        print("[warn] chain prompt mismatch idx=%s (%s); full generation"
                              % (rws[i]["idx"], key), flush=True)
                        continue
                    ids, tail_seed = seed_from_chain(cr, pieces, TAIL_WINDOW)
                    cur[i] = {"ids": ids, "done": len(ids) >= hor, "_tail_seed": tail_seed}
                    chains_loaded += 1
            meta["passes"][key].update({"resume_from_chains_requested": bool(a.resume_from_chains),
                                        "chains_path": cpath, "chains_file_found": os.path.exists(cpath),
                                        "chains_loaded": chains_loaded})

        waves = [w for w in (128, 256, 512, 1024, 2048) if w < hor] + [hor]
        for T_next in waves:
            stuck = 0
            while True:
                todo = [i for i in range(N) if not cur[i]["done"]
                        and len(cur[i]["ids"]) < T_next]
                if not todo or stuck > 2:
                    break
                Tn = min(len(cur[i]["ids"]) for i in todo)
                at_T = sorted([i for i in todo if len(cur[i]["ids"]) == Tn],
                              key=lambda i: plen[i])
                before = sum(len(cur[i]["ids"]) for i in range(N))
                b = bw or ad.batch_cap
                gi = 0
                while gi < len(at_T):
                    grp = at_T[gi:gi + b]
                    max_seq = max(plen[i] for i in grp) + T_next + len(suf) + nans
                    if bw is None:
                        nb, _ = ad.batch_for(a.k, max_seq)
                        if nb < len(grp):
                            b = nb
                            grp = at_T[gi:gi + b]
                    try:
                        seqs = [enc[i] + cur[i]["ids"] for i in grp]
                        if forced:
                            # s13_common carries the stopper state ACROSS segments, so the decoded
                            # tail is not cleared at a segment boundary and a stop pattern spanning
                            # it cannot be missed. The state lives on the problem, not the call.
                            for i in grp:
                                if "fstate" not in cur[i]:
                                    cur[i]["fstate"] = new_forced_states(1)[0]
                                    cur[i]["fstate"]["off"] = len(cur[i]["ids"])
                                    # Fix 1: a row resumed from a stored chain seeds the tail deque
                                    # with the chain's own trailing pieces, so the stopper sees a
                                    # pattern straddling the chain/continuation boundary whole.
                                    seed = cur[i].pop("_tail_seed", None)
                                    if seed:
                                        cur[i]["fstate"]["tail"].extend(seed)
                            states = [cur[i]["fstate"] for i in grp]
                            g, states, dt = ad.decode(
                                seqs, T_next - Tn, a.k, eos_ids, stop_strings=None,
                                row_ids=[rws[i]["idx"] for i in grp],
                                stopper=stopper, wait_ids=wait, states=states)
                        else:
                            kwd = {}
                            if ad.family in ("huginn", "mcleish") and a.no_mask:
                                kwd["use_mask"] = False
                            g, dt = ad.decode(seqs, T_next - Tn, a.k, eos_ids,
                                              stop_strings=stops,
                                              row_ids=[rws[i]["idx"] for i in grp], **kwd)
                    except torch.OutOfMemoryError as e:
                        line = "OOM A %s b=%d %d->%d: %s" % (key, len(grp), Tn, T_next,
                                                             str(e).split("\n")[0])
                        meta["oom_events"].append(line)
                        print("[OOM] " + line, flush=True)
                        traceback.clear_frames(e.__traceback__)
                        e.__traceback__ = None
                        gc.collect()
                        torch.cuda.empty_cache()
                        gc.collect()
                        if b == 1:
                            meta["errors"]["A_%s" % key] = line
                            save_meta()
                            break
                        b = max(1, b // 2)
                        continue
                    gen_seconds += dt
                    # Q8 (rulings, option O1): strip at the eos, KEEPING the eos token, in EVERY
                    # family. Both decoders already stop a row at its eos, so this is belt and
                    # braces rather than a second rule; it makes the rule explicit and uniform
                    # instead of Ouro-only. A forced trace is never stripped: it has no eos to stop
                    # at, by construction (s13_common suppresses every stop).
                    gen_widths.setdefault(len(grp), 0)
                    gen_widths[len(grp)] += 1
                    if not forced:
                        g = strip_tail(g, eos_ids)
                    for j, i in enumerate(grp):
                        cur[i]["width"] = max(cur[i].get("width") or 0, len(grp))
                        cur[i]["ids"] = cur[i]["ids"] + g[j]
                        gen_tokens += len(g[j])
                        c, mk = find_cut(cur[i]["ids"])
                        cur[i]["done"] = bool(forced is False and (mk is not None)) or \
                            len(cur[i]["ids"]) >= hor
                        if apt is not None:
                            apt.write({"idx": i, "row_idx": rws[i]["idx"], "ids": cur[i]["ids"],
                                       "done": cur[i]["done"], "natural_stop": c, "marker": mk,
                                       "wave": T_next})
                    gi += len(grp)
                    gc.collect()
                    torch.cuda.empty_cache()
                stuck = stuck + 1 if sum(len(cur[i]["ids"]) for i in range(N)) == before else 0
            if all(cur[i]["done"] for i in cur):
                break
        if apt is not None:
            apt.close()
        st = {}
        for i in range(N):
            if forced:
                # S13's semantics for a forced trace: `natural_stop` is the position of the FIRST
                # suppressed stop (the stopper's `natural_stop_pos`), not a cut-rule position -- the
                # forced trace never stops, so the cut rule has nothing to find. s13_merge.py writes
                # natural_stop == natural_stop_pos for exactly this reason.
                fs = cur[i].get("fstate") or {}
                st[i] = (fs.get("natural_stop_pos"), fs.get("natural_stop_reason"))
            else:
                c, mk = find_cut(cur[i]["ids"])
                st[i] = (min(c, hor), mk)
        nat = [st[i][0] for i in range(N) if st[i][0] is not None]
        meta["passes"][key].update({
            "natural_stop_mean": (sum(nat) / len(nat)) if nat else None,
            "natural_stop_min_max": [min(nat), max(nat)] if nat else None,
            "natural_stop_hit_frac": sum(1 for i in st if st[i][1] is not None) / max(1, N),
            "trace_tokens": sum(len(cur[i]["ids"]) for i in cur),
            "generated_tokens": gen_tokens, "generate_seconds": round(gen_seconds, 2),
            "tokens_per_s": (gen_tokens / gen_seconds) if gen_seconds > 0 else None})
        save_meta()
        print("  pass %s: natural stop mean %s hit %.3f, %d tokens in %.0fs (%.1f tok/s) [%.0fs]"
              % (key, ("%.1f" % meta["passes"][key]["natural_stop_mean"])
                 if meta["passes"][key]["natural_stop_mean"] is not None else "n/a",
                 meta["passes"][key]["natural_stop_hit_frac"], gen_tokens, gen_seconds,
                 meta["passes"][key]["tokens_per_s"] or 0.0, time.time() - t0), flush=True)
        return enc, cur, plen, st, suf, eos_ids, find_cut

    # ---------------------------------------------------------------- phase B: forced read-out
    def readout_pass(enc, cur, plen, st, suf, eos_ids, jobs, key):
        jobs = [(i, c, bs) for (i, c, bs) in jobs if any((i, B) not in done for B in bs)]
        jobs.sort(key=lambda t: plen[t[0]] + t[1])
        b = bw or ad.batch_cap
        gi, nrows = 0, 0
        while gi < len(jobs):
            grp = jobs[gi:gi + b]
            max_seq = max(plen[i] + c for (i, c, _x) in grp) + len(suf) + nans
            if bw is None:
                nb, _ = ad.batch_for(a.k, max_seq)
                if nb < len(grp):
                    b = nb
                    grp = jobs[gi:gi + b]
            try:
                kwd = {}
                if ad.family in ("huginn", "mcleish") and a.no_mask:
                    kwd["use_mask"] = False
                o, dt = ad.decode([enc[i] + cur[i]["ids"][:c] + suf for (i, c, _x) in grp],
                                  nans, a.k, eos_ids, stop_strings=None,
                                  row_ids=[rws[i]["idx"] for (i, _c, _x) in grp], **kwd)
            except torch.OutOfMemoryError as e:
                line = "OOM B %s b=%d: %s" % (key, len(grp), str(e).split("\n")[0])
                meta["oom_events"].append(line)
                print("[OOM] " + line, flush=True)
                traceback.clear_frames(e.__traceback__)
                e.__traceback__ = None
                gc.collect()
                torch.cuda.empty_cache()
                gc.collect()
                if b == 1:
                    meta["errors"]["B_%s" % key] = line
                    save_meta()
                    break
                b = max(1, b // 2)
                continue
            raw = [list(x) for x in o]          # before the eos strip, for G1 cause attribution
            o = strip_tail(o, eos_ids)          # Q8 option O1, every family
            ro_widths.setdefault(len(grp), 0)
            ro_widths[len(grp)] += 1
            for j, (i, c, bs) in enumerate(grp):
                # the eos token is KEPT in o[j] for the token accounting (Q8) but must not reach
                # the parsed text: "42<|endoftext|>" is not "42" for the math and free-form parsers
                atxt = tok.decode([t for t in o[j] if t not in eos_ids],
                                  clean_up_tokenization_spaces=False)
                ctxt = tok.decode(cur[i]["ids"][:c], clean_up_tokenization_spaces=False)
                opts = rws[i].get("options") or None
                gold = rws[i]["target"]
                kind = row_kind(a.task, rws[i])
                pred = parse_forced(atxt, a.task, opts, kind)
                own = parse_own(ctxt, a.task, opts, kind)
                # Q8: what the answer would have been WITHOUT the eos strip, stored only when the
                # strip actually removed something. Gate G1 needs it to prove that the strip rule is
                # the whole difference from the S9a-family spikes without a second generation.
                nostrip = None
                if len(raw[j]) != len(o[j]):
                    rtxt = tok.decode([t for t in raw[j] if t not in eos_ids],
                                      clean_up_tokenization_spaces=False)
                    nostrip = {"n_answer_tokens": len(raw[j]),
                               "pred": parse_forced(rtxt, a.task, opts, kind)}
                    nostrip["correct"] = bool(ans_eq(nostrip["pred"], gold, a.task, kind))
                ngen = c + len(o[j])
                ppt = ad.passes_per_token(a.k)
                for B in bs:
                    if (i, B) in done:
                        continue
                    row = {"idx": i, "row_idx": rws[i]["idx"], "split": spl[i],
                           "model": a.model, "adapter": a.adapter, "task": a.task, "k": a.k,
                           "B": B, "extra": bool(B in extra and B not in caps),
                           "protocol": a.protocol, "tag_line": meta["passes"][key]["tag_line"],
                           "pred": pred, "gold": gold, "kind": kind,
                           "subtask": rws[i].get("subtask"),
                           "subject": rws[i].get("subject"),
                           "correct": bool(ans_eq(pred, gold, a.task, kind)),
                           "trace_answer": own,
                           "trace_correct": bool(ans_eq(own, gold, a.task, kind)),
                           "n_cut": c, "natural_stop": st[i][0], "stop_marker": st[i][1],
                           "n_trace": len(cur[i]["ids"]), "n_generated": ngen,
                           "n_prompt_tokens": plen[i], "n_answer_tokens": len(o[j]),
                           "n_suffix_tokens": len(suf),
                           "layer_passes": ppt * (plen[i] + ngen),
                           "layer_passes_promptfree": ppt * ngen,
                           "answer_text": atxt,
                           # rulings Q6 (iv): the width is pinned and STORED PER ROW, because a
                           # per-problem label is only comparable to another taken at the same width
                           # (LEDGER 2026-09-04 S5).
                           "batch_width": bw or 0,
                           "batch_width_readout": len(grp),
                           "batch_width_gen": cur[i].get("width"),
                           "strip_at_eos": True}
                    if nostrip is not None:
                        row["nostrip"] = nostrip
                    if forced and "fstate" in cur[i]:
                        fs = cur[i]["fstate"]
                        row.update({"natural_stop_pos": fs["natural_stop_pos"],
                                    "natural_stop_reason": fs["natural_stop_reason"],
                                    "n_forced_continuations": fs["n_forced_continuations"],
                                    "forced_positions": fs["forced_positions"]})
                        # S13 writes natural_stop == natural_stop_pos on a forced row
                        row["natural_stop"] = fs["natural_stop_pos"]
                        row["stop_marker"] = fs["natural_stop_reason"]
                    row["correct_v2"] = score_v2(row)
                    apc.write(row)
                    done[(i, B)] = row
                    nrows += 1
            gi += len(grp)
            gc.collect()
            torch.cuda.empty_cache()
            if gi % (16 * max(1, b)) == 0 or gi >= len(jobs):
                print("    readout %s %d/%d jobs b=%d rows %d [%.0fs] peak %.2f GB"
                      % (key, gi, len(jobs), len(grp), nrows, time.time() - t0,
                         torch.cuda.max_memory_allocated() / 1024 ** 3), flush=True)
                save_meta()
        return nrows

    # ---------------------------------------------------------------- drive
    if tagged:
        # A tagged arm's prompt contains the cap, so one generation cannot serve every cap
        # (s32_run.py): one pass per cap at that cap's horizon, plus a generation-free B=0 pass.
        prompts0, suf0, _s, eos0, ex0 = build_prompts(tok, a.task, rws,
                                                      chat_template=ad.chat_template,
                                                      suffix_text=a.suffix)
        tl0 = tag_line(a.k, 0, a.tag_loops, a.tag_tokens)
        enc0 = [tok(_insert_tag(p, tl0, a.task, ad.chat_template),
                    add_special_tokens=ast)["input_ids"] for p in prompts0]
        plen0 = [len(e) for e in enc0]
        meta["passes"]["T0"] = {"tag_line": tl0, "horizon": 0, "suffix_text": ex0["suffix_text"],
                                "natural_stop_mean": 0.0,
                                "prompt_tokens_mean": sum(plen0) / max(1, len(plen0)),
                                "note": "Tokens: 0. never appears in the S32 training pool"}
        cur0 = {i: {"ids": [], "done": True} for i in range(N)}
        st0 = {i: (0, None) for i in range(N)}
        readout_pass(enc0, cur0, plen0, st0, suf0, eos0,
                     [(i, 0, [0]) for i in range(N)], "T0")
        for T in [c for c in all_caps if c > 0]:
            enc, cur, plen, st, suf, eos_ids, _fc = gen_pass(T, T, "T%d" % T)
            readout_pass(enc, cur, plen, st, suf, eos_ids,
                         [(i, min(st[i][0], T), [T]) for i in range(N)], "T%d" % T)
    else:
        enc, cur, plen, st, suf, eos_ids, _fc = gen_pass(None, horizon, "single")
        if not forced:
            # Fix 1 (PP3b): the natural-stop pass's own trace is the chain a later forced job on
            # the same (model, task, k) can resume from instead of regenerating it.
            n_chain, chain_p = write_chains(out_dir, a.model, a.task, a.k, rws, enc, cur, st, bw)
            meta["chains_written"] = meta.get("chains_written", 0) + n_chain
            meta["chains_path"] = chain_p
            save_meta()
        jobs = []
        incomplete = {i for i in range(N) if not cur[i]["done"]}
        if incomplete:
            meta["n_incomplete_rows"] = len(incomplete)
            meta["incomplete_row_idx"] = sorted(int(rws[i]["idx"]) for i in incomplete)[:500]
            print("[warn] %d row(s) have truncated traces (OOM or stalled wave) and are left "
                  "unscored; the job will exit 3" % len(incomplete), flush=True)
            save_meta()
        for i in range(N):
            if i in incomplete:
                continue
            m = {}
            for B in all_caps:
                cut = min(st[i][0], B) if not forced else min(len(cur[i]["ids"]), B)
                m.setdefault(cut, []).append(B)
            for c, bs in m.items():
                jobs.append((i, c, bs))
        readout_pass(enc, cur, plen, st, suf, eos_ids, jobs, "single")

    apc.close()
    meta["cells_written"] = len(done)
    meta["cells_expected"] = N * len(all_caps)
    got = {}
    for B in all_caps:
        rowsB = [done[(i, B)] for i in range(N) if (i, B) in done]
        if not rowsB:
            continue
        got[str(B)] = {
            "n": len(rowsB),
            "parse_rate_forced": sum(1 for r in rowsB if r["pred"] is not None) / len(rowsB),
            "parse_rate_own": sum(1 for r in rowsB if r["trace_answer"] is not None) / len(rowsB),
            "acc_forced": sum(r["correct"] for r in rowsB) / len(rowsB),
            "acc_own": sum(r["trace_correct"] for r in rowsB) / len(rowsB),
            "acc_v2": sum(r["correct_v2"] for r in rowsB) / len(rowsB),
            "mean_layer_passes": sum(r["layer_passes"] for r in rowsB) / len(rowsB),
            "mean_n_cut": sum(r["n_cut"] for r in rowsB) / len(rowsB)}
        for sp in ("eval", "cal"):
            sub = [r for r in rowsB if r["split"] == sp]
            if sub:
                got[str(B)]["acc_v2_" + sp] = sum(r["correct_v2"] for r in sub) / len(sub)
                got[str(B)]["n_" + sp] = len(sub)
    meta["by_budget"] = got
    meta["batch_width_histogram"] = {"generation": gen_widths, "readout": ro_widths}
    meta["parse_rate_min"] = min([v["parse_rate_forced"] for v in got.values()] or [None])
    meta["seconds"] = round(time.time() - t0, 1)
    meta["peak_gb"] = round(torch.cuda.max_memory_allocated() / 1024 ** 3, 3) \
        if torch.cuda.is_available() else None
    n_inc = int(meta.get("n_incomplete_rows") or 0)
    if meta["errors"] or n_inc or len(done) < meta["cells_expected"]:
        meta["complete"] = False
        save_meta()
        print("INCOMPLETE %s %d/%d cells (%d row(s) unscored) in %.0fs peak %s GB; errors %s"
              % (tag, len(done), meta["cells_expected"], n_inc, meta["seconds"], meta["peak_gb"],
                 meta["errors"]), flush=True)
        sys.exit(3)
    meta["complete"] = True
    save_meta()
    print("DONE %s %d/%d cells in %.0fs peak %s GB | acc_v2 %s"
          % (tag, len(done), meta["cells_expected"], meta["seconds"], meta["peak_gb"],
             {B: round(v["acc_v2"], 3) for B, v in got.items()}), flush=True)
    return meta


def _insert_tag(prompt, tl, task, chat_template):
    """Insert the S32 control line between the few-shot prompt and the question.

    The question begins at the task's `q_prefix` after the exemplar block, so the insertion point is
    the LAST occurrence of the exemplar block's trailing separator before that prefix. Implemented
    the way s32_common.build_prompts does it: the prompt is rebuilt as prefix + tag + question, so
    here the tag is spliced in front of the final `q_prefix`.
    """
    from .tasks import task_cfg as _cfg
    qp = _cfg(task)["q_prefix"]
    i = prompt.rfind(qp)
    if i < 0:
        return prompt
    return prompt[:i] + tl + prompt[i:]


if __name__ == "__main__":
    main()
