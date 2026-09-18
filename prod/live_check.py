"""Run the allocator's picks END TO END and compare them with the grid at the same picks.

  python -m prod.live_check --model=ouro_1_4b_base --task=gsm8k --cells=artifacts \\
      --alloc-dir=artifacts/alloc_v5_gsm8k_ouro_1_4b_base --arm avg_gated_lookup \\
      --budget-fraction=0.5 [--accounting expected] [--n=20] [--no-generate] [--out=FILE] \\
      [--preflight]

`--preflight` generates ONE prompt at cap 0 first and exits 3 with the child's stderr if that fails,
so a broken model path or python is caught before any pick is run. Every generation's stdout and
stderr tail is kept on its run record; a failed generation writes `live_<...>.FAILED.json` with
those tails, no result file, and exits 2.

Every number in the paper's allocation section comes from a GRID: the cell (k, B) is looked up in a
table of rows that were generated for every cell. That is a legitimate way to score a policy, but it
is not the thing the paper claims a user would do. This script does the thing itself:

  1. read the picks `alloc.cli` recorded for this arm and budget fraction (results.json["picks"]):
     the cell every evaluation prompt was scored at when Table 1 was read, plus the calibration
     ids the policy was fitted on. alloc is the ONLY source of picks; nothing is re-ranked here.
  2. refuse to run unless the cells directory carries the split alloc calibrated from: the
     grid's own calibration ids, the ids alloc promoted out of the evaluation split, and the
     evaluation ids left, must all agree
  3. GENERATE ONCE at each recorded (k, B), with the forced read-out, and score protocol v2
  4. compare the live accuracy with the grid's label at the same picks, and the realised price
     with the budget

The difference is reported in points. It should be zero up to bf16 batch-composition noise, because
step 3 regenerates a row the grid already holds; a non-zero difference is either that noise (the row
is now decoded in a batch of differently-chosen cells, LEDGER 2026-09-04 S5) or a bug. Both are
worth knowing before a claim is made, which is why this is a gate and not an analysis.

The generation reuses `prod.generate`'s own machinery through a subprocess per distinct chosen cell,
so the live path is byte-for-byte the production path -- there is no second decoder to keep in sync.
"""
import argparse
import collections
import glob
import json
import os
import subprocess
import sys
import tempfile
import threading
import time

import numpy as np

from . import config as cfgmod
from .common import ART, DATA, load_json, read_jsonl, save_json

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_YAML = os.path.join(REPO_ROOT, "prod", "config.yaml")
#: the install record: repo, pinned revision and local snapshot per model name
REVISIONS_FILE = os.path.join(DATA, "model_revisions.json")
# The arms the live check can run: every one is read out of alloc.cli's picks block, so adding
# one here needs no other logic. avg_gated_equation_resolved is the arm of record (alloc v6).
ARMS = ("lookup", "avg_gated_lookup", "equation_resolved", "avg_gated_equation_resolved")
#: lines of each subprocess's stdout and stderr kept on the run record
TAIL_LINES = 40


# ---------------------------------------------------------------- alloc's picks
def load_picks(alloc_dir, arm, fraction, accounting="expected"):
    """Return (the picks entry, the calibration record, the whole results.json) for one arm at
    one budget fraction under one accounting, from `alloc.cli`'s output directory.

    Every failure is a refusal with the reason: no results.json, a results.json written before
    the picks record existed, an accounting or arm the run did not tabulate, or a fraction it did
    not price. Nothing is recomputed here.
    """
    path = os.path.join(alloc_dir, "results.json")
    if not os.path.exists(path):
        raise SystemExit("%s: no results.json; run alloc.cli on this pair first" % alloc_dir)
    res = load_json(path)
    block = res.get("picks")
    if not block or not block.get("by_accounting"):
        raise SystemExit("%s has no picks block: it was written by an alloc.cli older than the picks "
                         "record; rerun alloc.cli" % path)
    acc = block["by_accounting"].get(accounting)
    if not acc:
        raise SystemExit("%s: no %s accounting in the picks (have %s)"
                         % (path, accounting, ", ".join(sorted(k for k, v in block["by_accounting"].items() if v))))
    arms = acc.get("arms") or {}
    if arm not in arms:
        raise SystemExit("%s: arm %s not in the picks (have %s)" % (path, arm, ", ".join(sorted(arms))))
    for e in arms[arm]:
        if abs(float(e["fraction"]) - float(fraction)) < 1e-9:
            return e, block["calibration"], res
    raise SystemExit("%s: fraction %s not priced for %s (have %s)"
                     % (path, fraction, arm, ", ".join(str(e["fraction"]) for e in arms[arm])))


def check_split(cells, calibration):
    """Refuse unless `cells` carries the split alloc calibrated from.

    The grid's own calibration ids must be exactly the ids alloc started from, every id alloc
    promoted must be one of the grid's evaluation ids, and what is left must be the evaluation ids
    the picks were read on. Returns the evaluation ids, in the recorded order.
    """
    cal_now = sorted(int(cells.idx[n]) for n in cells.select("cal"))
    ev_now = set(int(cells.idx[n]) for n in cells.select("eval"))
    before = sorted(int(i) for i in calibration["ids_before_promotion"])
    promoted = [int(i) for i in calibration.get("promoted_ids", [])]
    ev_rec = [int(i) for i in calibration["evaluation_ids"]]
    if cal_now != before:
        raise SystemExit("the cells' calibration split (%d ids) is not the one alloc calibrated from "
                         "(%d ids): these picks belong to another grid" % (len(cal_now), len(before)))
    if not set(promoted) <= ev_now:
        raise SystemExit("alloc promoted %d ids that are not evaluation ids of these cells"
                         % len(set(promoted) - ev_now))
    if sorted(ev_now - set(promoted)) != sorted(ev_rec):
        raise SystemExit("the evaluation ids left after promotion (%d) are not the %d the picks "
                         "were read on" % (len(ev_now - set(promoted)), len(ev_rec)))
    return ev_rec


def load_cells(cells_dir, model, task):
    """The grid, loaded by alloc's own loader with the model's geometry from prod/config.yaml."""
    from alloc import cells as C
    L, L_fixed = C.model_geometry(model, CONFIG_YAML)
    return C.load(cells_dir, task, model, L=L, L_fixed=L_fixed)


# ---------------------------------------------------------------- the generation path
def generate_cmd(model, task, k, B, out_dir, row_ids_path=None, horizon=None, python=None,
                 adapter=None, extra=None, n=None):
    """The `prod.generate` command one live cell -- or the preflight -- is run with.

    One builder for both, so the preflight proves the command the picks will be run with and a test
    can stand a stub in its place without a second copy of the argument list.
    """
    cmd = [python or sys.executable, "-m", "prod.generate", "--model=%s" % model,
           "--task=%s" % task, "--k=%d" % int(k), "--caps=%d" % int(B), "--no-extra-caps",
           "--horizon=%d" % int(horizon or 1), "--out=%s" % out_dir]
    if row_ids_path:
        cmd.append("--only-rows=%s" % row_ids_path)
    if n is not None:
        cmd.append("--n=%d" % int(n))
    if adapter:
        cmd.append("--adapter=%s" % adapter)
    cmd += list(extra or [])
    return cmd


def _pump(stream, sink, keep):
    """Echo a child stream line by line and keep its last `keep.maxlen` lines."""
    for line in iter(stream.readline, ""):
        keep.append(line.rstrip("\n"))
        try:
            sink.write(line)
            sink.flush()
        except (ValueError, OSError):                          # a closed sink is not a run failure
            pass
    stream.close()


def _call(cmd, cwd=None, tail=TAIL_LINES):
    """Run one command and return (rc, stdout tail, stderr tail, seconds).

    Both streams are ECHOED as they arrive, so a long generation still prints as it goes, AND their
    last `tail` lines are kept: a generation that dies in two seconds used to leave nothing but its
    rc on the record, which is why 129 of 201 cluster live files could not be diagnosed at all.
    """
    t0 = time.time()
    p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         text=True, bufsize=1, errors="replace")
    keep = (collections.deque(maxlen=int(tail)), collections.deque(maxlen=int(tail)))
    th = [threading.Thread(target=_pump, args=(p.stdout, sys.stdout, keep[0]), daemon=True),
          threading.Thread(target=_pump, args=(p.stderr, sys.stderr, keep[1]), daemon=True)]
    for t in th:
        t.start()
    rc = p.wait()
    for t in th:
        t.join(timeout=30)
    return (rc, "\n".join(keep[0]) or None, "\n".join(keep[1]) or None,
            round(time.time() - t0, 1))


def resolved_model(model):
    """What `prod.generate` will load for this name: repo, pinned revision and local snapshot.

    Read from the install record, so a failure says WHICH path was looked for instead of only that
    the child exited 1.
    """
    base = str(model).split("+", 1)[0]
    m = (load_json(REVISIONS_FILE, {}).get("models") or {}).get(base) or {}
    out = {"name": model, "base": base, "repo": m.get("repo"), "revision": m.get("revision"),
           "local_dir": m.get("local_dir"), "local_dir_exists": None,
           "revisions_file": REVISIONS_FILE}
    if out["local_dir"]:
        out["local_dir_exists"] = os.path.isdir(out["local_dir"])
    return out


def _n_rows(out_dir):
    """Cells rows (header lines excluded) under one generation's output directory."""
    n = 0
    for path in sorted(glob.glob(os.path.join(out_dir, "**", "cells_*.jsonl"), recursive=True)):
        n += len(read_jsonl(path))
    return n


def preflight(model, task, python=None, adapter=None, extra=None, out_dir=None):
    """Prove the generation path works for this (model, task) BEFORE a single pick is run.

    One prompt, cap 0, horizon 1: the cheapest generation the harness can make. It must exit 0 and
    write one row. What is printed is what a failure needs -- the resolved model path and revision,
    the adapter, HF_HUB_OFFLINE and HF_HOME, the working directory and the python. A failure exits
    3, with the child's stderr tail, before any GPU time is spent on the picks.
    """
    tmp = out_dir or tempfile.mkdtemp(prefix="live_preflight_")
    os.makedirs(tmp, exist_ok=True)
    info = {"model": model, "task": task, "adapter": adapter,
            "python": python or sys.executable, "cwd": REPO_ROOT, "out_dir": tmp,
            "hf_hub_offline": os.environ.get("HF_HUB_OFFLINE"),
            "hf_home": os.environ.get("HF_HOME"),
            "model_path": resolved_model(model)}
    print("[preflight] " + json.dumps(info, indent=1, default=str), flush=True)
    cmd = generate_cmd(model, task, 1, 0, tmp, None, horizon=1, python=python, adapter=adapter,
                       extra=extra, n=1)
    rc, otail, etail, secs = _call(cmd, cwd=REPO_ROOT)
    rows = _n_rows(tmp)
    info.update({"cmd": " ".join(cmd), "rc": rc, "seconds": secs, "n_rows": rows,
                 "stdout_tail": otail, "stderr_tail": etail})
    if rc != 0 or rows < 1:
        print("preflight FAILED: rc=%d, %d rows written under %s. The picks were NOT run. "
              "stderr tail:" % (rc, rows, tmp), flush=True)
        print(etail or "(the generation wrote nothing to stderr)", flush=True)
        sys.exit(3)
    print("[preflight] ok: %d row in %.1fs at %s" % (rows, secs, tmp), flush=True)
    return info


def check_writable(path):
    """Refuse now if the result could not be written after the generations.

    The probe leaves nothing behind: a path that did not exist does not exist afterwards, because a
    failed run must leave no result file at all.
    """
    d = os.path.dirname(os.path.abspath(path)) or "."
    if os.path.isdir(path):
        raise SystemExit("--out %s is a directory, not a file" % path)
    try:
        os.makedirs(d, exist_ok=True)
    except OSError as e:
        raise SystemExit("--out %s is not writable: %r" % (path, e))
    existed = os.path.exists(path)
    try:
        with open(path, "a", encoding="utf-8"):
            pass
    except OSError as e:
        raise SystemExit("--out %s is not writable: %r" % (path, e))
    if not existed:
        try:
            os.remove(path)
        except OSError:
            pass
    return True


def run_live(model, task, chosen, row_ids, out_dir, python=None, adapter=None, horizon=None,
             extra=None, fail_path=None, context=None):
    """Step 3: ONE generation per distinct chosen cell, over exactly the prompts that chose it.

    Each run's record carries its rc, its seconds AND the last TAIL_LINES lines of its stdout and
    stderr. If any run failed, every failure's stderr tail is printed, `fail_path` (if given)
    receives `context` plus the run records as the FAILED json, no result is written, and the exit
    is 2.
    """
    by_cell = {}
    for rid in row_ids:
        c = chosen.get(int(rid))
        if c is None:
            continue
        by_cell.setdefault(c, []).append(int(rid))
    runs = []
    for (k, B), ids in sorted(by_cell.items()):
        tagdir = os.path.join(out_dir, "live_k%d_B%d" % (k, B))
        os.makedirs(tagdir, exist_ok=True)
        rows_path = os.path.join(tagdir, "row_ids.json")
        save_json(rows_path, sorted(ids))
        # An only-rows file that is missing or empty does NOT run these prompts: `prod.generate`
        # would fall back to the whole shard. Checked here, before the GPU is asked for anything.
        if not os.path.exists(rows_path) or os.path.getsize(rows_path) < 3:
            raise SystemExit("live check FAILED: %s is missing or empty, so the generation would "
                             "run the whole shard instead of these %d prompts"
                             % (rows_path, len(ids)))
        # The live request spends B tokens, so it generates AT MOST B: a trace that has not
        # stopped by B is truncated at B either way, so cut = min(natural stop, B) is identical to
        # the grid's and the generation is B-bounded instead of horizon-bounded. `horizon` is only
        # the ceiling, and is never below 1 (a B=0 request still needs one decode step to exist).
        cmd = generate_cmd(model, task, k, B, tagdir, rows_path,
                           horizon=max(1, min(int(B) or 1, int(horizon or B or 1))),
                           python=python, adapter=adapter, extra=extra)
        rc, otail, etail, secs = _call(cmd, cwd=REPO_ROOT)
        runs.append({"k": k, "B": B, "n": len(ids), "rc": rc, "seconds": secs, "dir": tagdir,
                     "cmd": " ".join(cmd), "tail_lines": TAIL_LINES,
                     "stdout_tail": otail, "stderr_tail": etail})
        print("[live] k=%d B=%d n=%d rc=%d %.0fs" % (k, B, len(ids), rc, secs), flush=True)
    bad = [r for r in runs if r["rc"] != 0]
    if bad:
        for r in bad:
            print("[live] FAILED k=%d B=%d rc=%d after %.1fs. stderr tail:"
                  % (r["k"], r["B"], r["rc"], r["seconds"]), flush=True)
            print(r["stderr_tail"] or "(the generation wrote nothing to stderr)", flush=True)
        if fail_path:
            rec = dict(context or {})
            rec.update({"failed": True, "n_failed": len(bad), "n_runs": len(runs), "runs": runs,
                        "reason": "%d of %d generations exited non-zero" % (len(bad), len(runs))})
            save_json(fail_path, rec)
            print("wrote", fail_path, flush=True)
        print("live check FAILED: %d of %d generations exited non-zero (first: k=%d B=%d rc=%d); the "
              "result would be partial, so none is written" % (len(bad), len(runs), bad[0]["k"],
                                                                 bad[0]["B"], bad[0]["rc"]), flush=True)
        sys.exit(2)
    return runs


def collect_live(runs, chosen):
    """The live protocol-v2 label and realised layer passes per row, from the cells the live
    generations wrote."""
    live, price = {}, {}
    for r in runs:
        for fn in sorted(os.listdir(r["dir"])):
            if not (fn.startswith("cells_") and fn.endswith(".jsonl")):
                continue
            for row in read_jsonl(os.path.join(r["dir"], fn)):
                rid = int(row.get("row_idx", row["idx"]))
                if chosen.get(rid) == (int(row["k"]), int(row["B"])):
                    live[rid] = bool(row["correct_v2"])
                    price[rid] = float(row.get("layer_passes") or float("nan"))
    return live, price


# ---------------------------------------------------------------- main
def main(argv=None):
    p = argparse.ArgumentParser(prog="prod.live_check")
    p.add_argument("--model", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--cells", default=None, help="the grid's cells directory (default artifacts/)")
    p.add_argument("--alloc-dir", dest="alloc_dir", required=True,
                   help="alloc.cli's output directory for this (task, model): the picks are read "
                        "from its results.json and nothing is re-ranked here")
    p.add_argument("--arm", default="lookup", choices=ARMS,
                   help="lookup: the calibration-ranked first affordable cell per prompt; "
                        "equation_resolved: the same per-prompt rule ranked by the settle-time-resolved "
                        "commitment identity; avg_gated_lookup: the average-budget lookup policy with the "
                        "gate (label-only baseline); avg_gated_equation_resolved: the average-budget arm of "
                        "record, resolved ranking and two-fold verified gate")
    p.add_argument("--budget-fraction", dest="budget_fraction", type=float, required=True,
                   help="X as a fraction of the DEFAULT cost, one of the fractions alloc priced")
    p.add_argument("--accounting", default="expected",
                   help="which accounting's picks to run (alloc tabulated it under --accounting)")
    p.add_argument("--n", type=int, default=None, help="use only the first N evaluation prompts")
    p.add_argument("--adapter", default=None)
    p.add_argument("--python", default=None)
    p.add_argument("--out", default=None)
    p.add_argument("--out-dir", dest="out_dir", default=None)
    p.add_argument("--no-generate", dest="generate", action="store_false", default=True,
                   help="read the picks, report the plan, run nothing on the GPU")
    p.add_argument("--preflight", action="store_true",
                   help="before any pick: generate ONE prompt at cap 0 and horizon 1 for this "
                        "(model, task), assert it writes a row, and print the resolved model path, "
                        "the adapter, HF_HUB_OFFLINE, the working directory and the python. Exits 3 "
                        "with the child's stderr if it fails, so a broken setup costs one prompt "
                        "instead of a whole array element")
    p.add_argument("--extra", default="")
    cfgmod.add_args(p)
    a = p.parse_args(argv)
    cfg = cfgmod.from_args(a)
    cells_dir = a.cells or ART
    extra = [x for x in a.extra.split() if x]

    # Before ANY pick: prove the generation path for this (model, task). A broken model path, a
    # wrong python or an offline cache miss then costs one prompt and exits 3, not an array element.
    pre = preflight(a.model, a.task, a.python, a.adapter, extra) if a.preflight else None

    entry, calib, res = load_picks(a.alloc_dir, a.arm, a.budget_fraction, a.accounting)
    if res.get("task") != a.task or res.get("checkpoint") != a.model:
        raise SystemExit("%s holds %s/%s, not %s/%s" % (a.alloc_dir, res.get("checkpoint"),
                                                        res.get("task"), a.model, a.task))
    cs = load_cells(cells_dir, a.model, a.task)
    ev_ids = check_split(cs, calib)
    X = float(entry["budget"])
    chosen = {int(r["row_idx"]): (int(r["k"]), int(r["cap"])) for r in entry["picks"]
              if r["k"] is not None}
    row_ids = [int(r["row_idx"]) for r in entry["picks"]]
    if sorted(row_ids) != sorted(ev_ids):
        raise SystemExit("the picks cover %d prompts, the evaluation split %d" % (len(row_ids), len(ev_ids)))
    if a.n:
        row_ids = row_ids[:a.n]
    hist = {}
    for rid in row_ids:
        key = "k%d_B%d" % chosen[rid] if rid in chosen else "infeasible"
        hist[key] = hist.get(key, 0) + 1
    ki = {k: i for i, k in enumerate(cs.ks)}
    bi = {b: i for i, b in enumerate(cs.caps)}
    ni = {int(v): i for i, v in enumerate(cs.idx)}
    feasible = [r for r in row_ids if r in chosen]
    grid_lab = {r: bool(cs.acc[ki[chosen[r][0]], bi[chosen[r][1]], ni[r]]) for r in feasible}
    rec_price = [r["price"] for r in entry["picks"] if r["price"] is not None]
    out = {"model": a.model, "task": a.task, "arm": a.arm, "accounting": a.accounting,
           "alloc_dir": a.alloc_dir, "budget_fraction": a.budget_fraction, "budget": X,
           "default_cost": res.get("default_cost"), "gate": entry.get("gate"),
           "alloc_mean_price_layer_passes": entry.get("mean_price"),
           "n_eval_used": len(row_ids), "n_infeasible": len(row_ids) - len(feasible),
           "n_cal": int(calib["n_cal"]), "n_promoted": len(calib.get("promoted_ids", [])),
           "chosen_histogram": hist, "layers_per_loop": cs.L, "layers_fixed": cs.L_fixed,
           "grid_acc_at_picks": (float(np.mean([grid_lab[r] for r in feasible])) if feasible else None),
           "preflight": pre,
           "config": cfg, "config_sha256": cfgmod.digest(cfg)}
    tag = "%s_%s_%s_b%s" % (a.model.replace("+", "-"), a.task, a.arm, a.budget_fraction)
    dest = a.out or os.path.join(cells_dir, "live_check_%s.json" % tag)
    if not a.generate:
        out["live"] = "skipped (--no-generate)"
        save_json(dest, out)
        print(json.dumps({k: out[k] for k in ("budget", "gate", "chosen_histogram",
                                              "grid_acc_at_picks")}, indent=2))
        print("wrote", dest)
        return out

    # Checked before the GPU is asked for anything: a result that cannot be written is a run whose
    # whole cost is lost at the last line.
    check_writable(dest)
    out_dir = a.out_dir or os.path.join(cells_dir, "live_check_%s" % tag)
    os.makedirs(out_dir, exist_ok=True)
    runs = run_live(a.model, a.task, chosen, row_ids, out_dir, a.python, a.adapter,
                    cfg["horizon"], extra,
                    fail_path=os.path.splitext(dest)[0] + ".FAILED.json", context=out)
    live, live_price = collect_live(runs, chosen)
    have = [r for r in feasible if r in live]
    if feasible and not have:
        print("live check FAILED: no live row was generated (every generation exited non-zero; see the "
              "[live] lines above, rc != 0)", flush=True)
        sys.exit(2)
    live_acc = float(np.mean([live[r] for r in have])) if have else None
    grid_acc = float(np.mean([grid_lab[r] for r in have])) if have else None
    grid_price = (float(np.nanmean([cs.passes[ki[chosen[r][0]], bi[chosen[r][1]], ni[r]] for r in have]))
                  if have else None)
    mean_live_price = float(np.nanmean([live_price[r] for r in have])) if have else None
    flips = [{"row_idx": r, "cell": list(chosen[r]), "grid": grid_lab[r], "live": live[r]}
             for r in have if grid_lab[r] != live[r]]
    out.update({"runs": runs, "n_live_rows": len(have), "live_acc": live_acc,
                "grid_acc_same_rows": grid_acc,
                "delta_pp": (None if live_acc is None or grid_acc is None
                             else round(100.0 * (live_acc - grid_acc), 3)),
                "live_mean_price_layer_passes": mean_live_price,
                "grid_mean_price_same_rows": grid_price,
                "price_over_budget_pct": (None if mean_live_price is None
                                          else round(100.0 * (mean_live_price / X - 1.0), 2)),
                "n_flips": len(flips), "flips": flips[:50],
                "missing_rows": [r for r in feasible if r not in live]})
    save_json(dest, out)
    gate = entry.get("gate") or {}
    rule = ((gate.get("reference") or {}).get("rule")) or "default_cell"
    print("%s %s %s @%.2f: n=%d live %.4f grid %.4f delta %+.2f pp | realised price %.0f vs budget "
          "%.0f (%+.1f%%)%s"
          % (a.model, a.task, a.arm, a.budget_fraction, len(have), live_acc or 0, grid_acc or 0,
             out["delta_pp"] or 0.0, mean_live_price or 0, X, out["price_over_budget_pct"] or 0.0,
             (" [gate reverted to %s]" % rule if gate.get("reverted")
              else (" [family %s]" % gate["family"] if gate.get("family") else ""))))
    print("wrote", dest)
    return out


if __name__ == "__main__":
    main()
