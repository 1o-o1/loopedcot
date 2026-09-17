"""Run the allocation rule END TO END and compare it with the offline policy value (dec. 7).

  python -m prod.live_check --model=ouro_1_4b_base --task=gsm8k --cells=artifacts \\
      --budget-index=8 --n=20 [--promptfree] [--out=FILE]
  python -m prod.live_check ... --budget=2.4e7          # an explicit budget in layer-token passes

Every number in the paper's allocation section comes from a GRID: the cell (k, B) is looked up in a
table of rows that were generated for every cell. That is a legitimate way to score a policy, but it
is not the thing the paper claims a user would do. This script does the thing itself:

  1. read the calibration rows out of the cells files and rank the cells by calibration accuracy,
     ties broken by cost at the task's median prompt length   (allocate.rank_from_cal, verbatim)
  2. for each EVALUATION prompt, compute feasibility from ITS OWN token count
     (allocate.per_prompt_cost: (L_fixed + k L) (p_i + B + r_i) <= X, the family's own passes per
     token) and take the first feasible ranked cell
  3. GENERATE ONCE at that loop count and cap, with the forced read-out, and score protocol v2
  4. compare the live accuracy with the offline policy value from the grid at the same budget

The difference is reported in points. It should be zero up to bf16 batch-composition noise, because
step 3 regenerates a row the grid already holds; a non-zero difference is either that noise (the row
is now decoded in a batch of differently-chosen cells, LEDGER 2026-09-04 S5) or a bug in the
allocator. Both are worth knowing before the cluster run, which is why this is a gate and not an
analysis.

The generation reuses `prod.generate`'s own machinery through a subprocess per distinct chosen cell,
so the live path is byte-for-byte the production path -- there is no second decoder to keep in sync.

The ranking grid must be COMPLETE. A missing cell is NaN, and NaN is not a small number: it can be
ranked first by `rank_from_cal` (a mean over a calibration column that is partly NaN) and it scores
as neither right nor wrong, so an incomplete grid silently produces a policy nobody measured.
`choose` refuses to rank on one unless `--allow-incomplete` says the caller knows.
"""
import argparse
import json
import os
import subprocess
import sys
import time

import numpy as np

from . import config as cfgmod
from .analyze.allocate import (Grid, budget_grid, default_cost, per_prompt_cost, policy_vectors,
                               rank_from_cal)
from .common import ART, load_json, read_jsonl, save_json
from .cost import model_shapes
from .score import load_grid

CONFIG_YAML = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "prod", "config.yaml")


# ---------------------------------------------------------------- the average-budget gated arm
def avg_gated_picks(cells_dir, model, task, budget_fraction, c_gate=0.5, gate_draws=40, seed=7,
                    protocol="natural"):
    """The `avg_gated_lookup` arm exactly as `alloc.cli --accounting expected --avg-budget` picks
    it: cells loaded by alloc.cells.load (geometry from prod/config.yaml), budget = fraction x
    alloc.evaluate.default_cost, the lookup score on the calibration rows, the multiplier fitted on
    the calibration prompts (alloc.policy.avg_budget_vectors), the gate (c_gate) fitted on the
    calibration resamples (alloc.evaluate.avg_gated_vectors). Returns (cells, X, record,
    {row_idx: (k, B)}, eval positions), where the record is alloc's own for this budget.
    """
    from alloc import cells as C, evaluate as E, policy as P
    L, L_fixed = C.model_geometry(model, CONFIG_YAML)
    cs = C.load(cells_dir, task, model, L=L, L_fixed=L_fixed, protocol=protocol)
    cost = P.cost_of(cs, promptfree=False, accounting="expected")
    ev, cal = cs.select("eval"), cs.select("cal")
    if not len(ev) or not len(cal):
        raise SystemExit("%s/%s: need both splits (eval %d, cal %d)" % (model, task, len(ev), len(cal)))
    Pm, Rm = P.median_point(cs, ev)
    dc = E.default_cost(cs, promptfree=False)
    if dc["mean"] is None:
        raise SystemExit("%s/%s: no uncapped realisation of the default point" % (model, task))
    X = float(budget_fraction) * float(dc["mean"])
    score = E.cell_scores(cs, cal, P.AVG_GATED, cost, Pm, Rm)
    dk, dT = E.default_cell(cs)
    rec = E.avg_gated_vectors(cs, ev, cal, cost, [X], score, (dk, dT), c_gate=c_gate,
                              n_draws=gate_draws, seed=seed)[0]
    if rec.get("gate_reverted"):
        a = np.full(len(ev), list(cs.ks).index(dk), int)
        b = np.full(len(ev), list(cs.caps).index(dT), int)
    else:
        a, b = P.avg_picks(np.asarray(score, float), P.price_tensor(cs, ev, cost), rec["lambda"])
    chosen = {int(cs.idx[n]): (int(cs.ks[i]), int(cs.caps[j])) for n, i, j in zip(ev, a, b)}
    return cs, X, rec, chosen, ev, dc


def choose(cells_dir, model, task, budget=None, budget_index=None, promptfree=False,
           label="v2", n_budgets=None, budget_fraction=None, allow_incomplete=False):
    """Steps 1 and 2: the ranked cells, the budget, and the cell chosen for every eval prompt.

    `budget_fraction` (decision 7, config.yaml's `budget_fractions`, e.g. 0.25/0.5/1.0) is an
    alternative to `budget`/`budget_index`: it names X as a fraction of the DEFAULT cost -- the MEAN
    REALISED layer-pass cost of the default operating point (allocate.default_cost: the max measured
    depth, at each problem's own natural stop, uncapped, read off the cells) -- not the grid's
    largest (k, B) CAP cell at the median prompt, which is a synthetic (L_fixed + k L)(P+B) number
    no row is guaranteed to ever actually realise. 1.0 is that mean cost exactly; 0.25 a quarter.

    The grid must be complete: `allow_incomplete` is the only way to rank on one that is not, and it
    is there for a deliberate smoke run, never for a result.
    """
    cells, paths = load_grid(cells_dir, model, task, "natural", label)
    miss = cells.missing()
    if miss and not allow_incomplete:
        raise SystemExit("%s/%s: the ranking grid has %d missing cell(s) (first %s); a missing cell "
                         "is NaN, which can rank first and scores as neither right nor wrong. "
                         "Finish the grid, or pass --allow-incomplete to rank on what is there."
                         % (model, task, len(miss), miss[:3]))
    sh = model_shapes(model)
    # passes per token are layers_fixed + k * layers_per_loop (cost.model_shapes): 0 fixed layers
    # for Ouro, prelude + coda for a raven family
    grid = Grid("%s/%s" % (model, task), cells.ks, cells.Bs, cells.idx, cells.acc, cells.ptok,
                sh["layers_per_loop"], cells.reserve, list(cells.split), sh["layers_fixed"])
    cost = per_prompt_cost(grid.L, promptfree, grid.L_fixed)
    ev, cal = grid.select("eval"), grid.select("cal")
    if len(cal) == 0:
        raise SystemExit("%s/%s has no calibration rows; the allocator has nothing to read"
                         % (model, task))
    Pm = float(np.median(grid.ptok[ev]))
    Rm = float(np.median(grid.reserve[ev]))
    cmat = np.array([[cost(k, B, Pm, Rm) for B in grid.Bs] for k in grid.ks])
    Xs = budget_grid(cmat, n_budgets or 16)
    dc = default_cost(cells, promptfree, split="eval")
    if budget:
        X = float(budget)
    elif budget_fraction is not None:
        if dc["mean"] is None:
            raise SystemExit("%s/%s: no eval row reached an uncapped natural stop at k=%s in the "
                             "cells; widen the caps grid before using --budget-fraction"
                             % (model, task, dc["k"]))
        X = float(budget_fraction) * float(dc["mean"])
    else:
        X = float(Xs[int(budget_index if budget_index is not None else len(Xs) // 2)])
    order = rank_from_cal(grid, cal, cost, Pm, Rm)
    chosen = {}
    for n in ev:
        p, r = grid.ptok[n], grid.reserve[n]
        feas = [c for c in order if cost(c[0], c[1], p, r) <= X]
        chosen[int(grid.idx[n])] = (tuple(feas[0]) if feas else None)
    return grid, cells, order, X, Xs, chosen, ev, cost, Pm, Rm, paths, dc


def offline_value(grid, ev, cost, X, order):
    """Step 4's reference: the grid's own policy value at this budget (allocate.policy_vectors)."""
    pv, nv = policy_vectors(grid, ev, cost, [X], order)[0]
    return (float(np.nanmean(pv)) if np.any(~np.isnan(pv)) else None,
            float(np.nanmean(nv)) if np.any(~np.isnan(nv)) else None)


def run_live(model, task, chosen, row_ids, out_dir, python=None, adapter=None, horizon=None,
             extra=None):
    """Step 3: ONE generation per distinct chosen cell, over exactly the prompts that chose it."""
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
        save_json(os.path.join(tagdir, "row_ids.json"), sorted(ids))
        # The live request spends B tokens, so it generates AT MOST B: a trace that has not
        # stopped by B is truncated at B either way, so cut = min(natural stop, B) is identical to
        # the grid's and the generation is B-bounded instead of horizon-bounded. `horizon` is only
        # the ceiling, and is never below 1 (a B=0 request still needs one decode step to exist).
        cmd = [python or sys.executable, "-m", "prod.generate", "--model=%s" % model,
               "--task=%s" % task, "--k=%d" % k, "--caps=%d" % B, "--no-extra-caps",
               "--horizon=%d" % max(1, min(int(B) or 1, int(horizon or B or 1))),
               "--out=%s" % tagdir, "--only-rows=%s" % os.path.join(tagdir, "row_ids.json")]
        if adapter:
            cmd.append("--adapter=%s" % adapter)
        cmd += list(extra or [])
        t0 = time.time()
        rc = subprocess.call(cmd, cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        runs.append({"k": k, "B": B, "n": len(ids), "rc": rc,
                     "seconds": round(time.time() - t0, 1), "dir": tagdir,
                     "cmd": " ".join(cmd)})
        print("[live] k=%d B=%d n=%d rc=%d %.0fs" % (k, B, len(ids), rc, runs[-1]["seconds"]),
              flush=True)
    return runs


def collect_live(runs, chosen):
    """The live protocol-v2 label per row, from the cells the live generations wrote."""
    live = {}
    for r in runs:
        for fn in sorted(os.listdir(r["dir"])):
            if not (fn.startswith("cells_") and fn.endswith(".jsonl")):
                continue
            for row in read_jsonl(os.path.join(r["dir"], fn)):
                rid = int(row.get("row_idx", row["idx"]))
                if chosen.get(rid) == (int(row["k"]), int(row["B"])):
                    live[rid] = bool(row["correct_v2"])
    return live


def main(argv=None):
    p = argparse.ArgumentParser(prog="prod.live_check")
    p.add_argument("--model", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--cells", default=None, help="the grid's cells directory (default artifacts/)")
    p.add_argument("--budget", type=float, default=None)
    p.add_argument("--budget-index", dest="budget_index", type=int, default=None)
    p.add_argument("--budget-fraction", dest="budget_fraction", type=float, default=None,
                   help="X as a fraction of the DEFAULT cost (decision 7; config.yaml's "
                        "budget_fractions, e.g. 0.25/0.5/1.0), instead of --budget or --budget-index")
    p.add_argument("--n", type=int, default=None, help="use only the first N evaluation prompts")
    p.add_argument("--promptfree", action="store_true")
    p.add_argument("--label", default="v2")
    p.add_argument("--adapter", default=None)
    p.add_argument("--python", default=None)
    p.add_argument("--out", default=None)
    p.add_argument("--out-dir", dest="out_dir", default=None)
    p.add_argument("--no-generate", dest="generate", action="store_false", default=True,
                   help="rank and choose, report the plan, run nothing on the GPU")
    p.add_argument("--allow-incomplete", dest="allow_incomplete", action="store_true",
                   help="rank on a grid with missing cells (a smoke run only: a missing cell is "
                        "NaN, which can rank first and scores as neither right nor wrong)")
    p.add_argument("--extra", default="")
    p.add_argument("--arm", default="lookup", choices=("lookup", "avg_gated_lookup"),
                   help="lookup: the calibration-ranked first affordable cell per prompt (unchanged); "
                        "avg_gated_lookup: alloc's average-budget lookup policy with the gate, under "
                        "the expected accounting, budget = --budget-fraction x the default cost")
    p.add_argument("--c-gate", dest="c_gate", type=float, default=0.5)
    cfgmod.add_args(p)
    a = p.parse_args(argv)
    cfg = cfgmod.from_args(a)
    cells_dir = a.cells or ART
    if a.arm == "avg_gated_lookup":
        return main_avg(a, cfg, cells_dir)

    grid, cells, order, X, Xs, chosen, ev, cost, Pm, Rm, paths, dc = choose(
        cells_dir, a.model, a.task, a.budget, a.budget_index, a.promptfree, a.label,
        budget_fraction=a.budget_fraction, allow_incomplete=a.allow_incomplete)
    print("default cost (k=%s, n=%d, promptfree=%s): %s" % (dc["k"], dc["n"], dc["promptfree"],
                                                             dc["mean"]), flush=True)
    row_ids = [int(grid.idx[n]) for n in ev]
    if a.n:
        row_ids = row_ids[:a.n]
        ev = ev[:a.n]
    off_pol, off_norm = offline_value(grid, ev, cost, X, order)
    hist = {}
    for rid in row_ids:
        hist["k%s_B%s" % chosen[rid] if chosen[rid] else "infeasible"] = \
            hist.get("k%s_B%s" % chosen[rid] if chosen[rid] else "infeasible", 0) + 1

    out = {"model": a.model, "task": a.task, "cells": paths, "budget": X,
           "grid_complete": bool(cells.complete()), "n_missing_cells": len(cells.missing()),
           "allow_incomplete": bool(a.allow_incomplete),
           "layers_per_loop": grid.L, "layers_fixed": grid.L_fixed,
           "budget_index": a.budget_index, "budget_fraction": a.budget_fraction,
           "default_cost": dc, "budgets": [float(x) for x in Xs],
           "promptfree": bool(a.promptfree), "n_eval_used": len(row_ids),
           "n_cal": int(len(grid.select("cal"))), "median_prompt_tokens": Pm,
           "median_reserve": Rm, "ranked_top5": [list(c) for c in order[:5]],
           "chosen_histogram": hist,
           "offline_policy_acc": off_pol, "offline_normal_acc": off_norm,
           "config": cfg, "config_sha256": cfgmod.digest(cfg)}

    if not a.generate:
        out["live"] = "skipped (--no-generate)"
        dest = a.out or os.path.join(cells_dir, "live_check_%s_%s.json"
                                     % (a.model.replace("+", "-"), a.task))
        save_json(dest, out)
        print(json.dumps({k: out[k] for k in ("budget", "chosen_histogram",
                                              "offline_policy_acc", "offline_normal_acc")},
                         indent=2))
        print("wrote", dest)
        return out

    out_dir = a.out_dir or os.path.join(cells_dir, "live_check_%s_%s"
                                        % (a.model.replace("+", "-"), a.task))
    os.makedirs(out_dir, exist_ok=True)
    runs = run_live(a.model, a.task, chosen, row_ids, out_dir, a.python, a.adapter,
                    cfg["horizon"], [x for x in a.extra.split() if x])
    live = collect_live(runs, chosen)
    have = [r for r in row_ids if r in live]
    # the grid's own label for the SAME rows and the SAME cells, so the comparison is paired
    ki = {k: i for i, k in enumerate(grid.ks)}
    bi = {b: i for i, b in enumerate(grid.Bs)}
    ni = {int(v): i for i, v in enumerate(grid.idx)}
    grid_lab = {r: bool(grid.acc[ki[chosen[r][0]], bi[chosen[r][1]], ni[r]]) for r in have}
    live_acc = float(np.mean([live[r] for r in have])) if have else None
    grid_acc = float(np.mean([grid_lab[r] for r in have])) if have else None
    flips = [{"row_idx": r, "cell": list(chosen[r]), "grid": grid_lab[r], "live": live[r]}
             for r in have if grid_lab[r] != live[r]]
    out.update({"runs": runs, "n_live_rows": len(have),
                "live_acc": live_acc, "grid_acc_same_rows": grid_acc,
                "offline_policy_acc_same_rows": grid_acc,
                "delta_pp": (None if live_acc is None or grid_acc is None
                             else round(100.0 * (live_acc - grid_acc), 3)),
                "n_flips": len(flips), "flips": flips[:50],
                "missing_rows": [r for r in row_ids if r not in live]})
    dest = a.out or os.path.join(cells_dir, "live_check_%s_%s.json"
                                 % (a.model.replace("+", "-"), a.task))
    save_json(dest, out)
    print("live %.4f vs offline %.4f on %d rows -> delta %.2f pp (%d flips)"
          % (live_acc or 0, grid_acc or 0, len(have), out["delta_pp"] or 0.0, len(flips)))
    print("wrote", dest)
    return out


def main_avg(a, cfg, cells_dir):
    """The avg_gated_lookup arm end to end: alloc's picks, one generation per chosen cell, protocol
    v2, live against the grid at the same picks, realised price against the budget."""
    if a.budget_fraction is None:
        raise SystemExit("--arm avg_gated_lookup needs --budget-fraction")
    cs, X, rec, chosen, ev, dc = avg_gated_picks(cells_dir, a.model, a.task, a.budget_fraction,
                                                 c_gate=a.c_gate)
    row_ids = [int(cs.idx[n]) for n in ev]
    if a.n:
        row_ids = row_ids[:a.n]
    hist = {}
    for rid in row_ids:
        key = "k%d_B%d" % chosen[rid]
        hist[key] = hist.get(key, 0) + 1
    ki = {k: i for i, k in enumerate(cs.ks)}
    bi = {b: i for i, b in enumerate(cs.caps)}
    ni = {int(v): i for i, v in enumerate(cs.idx)}
    out = {"model": a.model, "task": a.task, "arm": "avg_gated_lookup", "accounting": "expected",
           "budget_fraction": a.budget_fraction, "budget": X, "default_cost": dc,
           "c_gate": a.c_gate, "lambda": rec["lambda"], "gate_reverted": bool(rec.get("gate_reverted")),
           "gate_margin_pts": rec.get("gate_margin_pts"), "gate_sd_pts": rec.get("gate_sd_pts"),
           "grid_mean_price_layer_passes": rec["mean_price"],
           "n_eval_used": len(row_ids), "n_cal": int(len(cs.select("cal"))),
           "chosen_histogram": hist, "layers_per_loop": cs.L, "layers_fixed": cs.L_fixed,
           "config": cfg, "config_sha256": cfgmod.digest(cfg)}
    grid_lab = {r: bool(cs.acc[ki[chosen[r][0]], bi[chosen[r][1]], ni[r]]) for r in row_ids}
    out["grid_acc_at_picks"] = float(np.mean([grid_lab[r] for r in row_ids]))
    if not a.generate:
        out["live"] = "skipped (--no-generate)"
        dest = a.out or os.path.join(cells_dir, "live_check_%s_%s_avg.json"
                                     % (a.model.replace("+", "-"), a.task))
        save_json(dest, out)
        print(json.dumps({k: out[k] for k in ("budget", "lambda", "gate_reverted",
                                              "chosen_histogram", "grid_acc_at_picks")}, indent=2))
        print("wrote", dest)
        return out
    out_dir = a.out_dir or os.path.join(cells_dir, "live_check_%s_%s_avg"
                                        % (a.model.replace("+", "-"), a.task))
    os.makedirs(out_dir, exist_ok=True)
    runs = run_live(a.model, a.task, chosen, row_ids, out_dir, a.python, a.adapter,
                    cfg["horizon"], [x for x in a.extra.split() if x])
    live, live_price = {}, {}
    for r in runs:
        for fn in sorted(os.listdir(r["dir"])):
            if not (fn.startswith("cells_") and fn.endswith(".jsonl")):
                continue
            for row in read_jsonl(os.path.join(r["dir"], fn)):
                rid = int(row.get("row_idx", row["idx"]))
                if chosen.get(rid) == (int(row["k"]), int(row["B"])):
                    live[rid] = bool(row["correct_v2"])
                    live_price[rid] = float(row.get("layer_passes") or float("nan"))
    have = [r for r in row_ids if r in live]
    live_acc = float(np.mean([live[r] for r in have])) if have else None
    grid_acc = float(np.mean([grid_lab[r] for r in have])) if have else None
    grid_price = float(np.nanmean([cs.passes[ki[chosen[r][0]], bi[chosen[r][1]], ni[r]] for r in have])) if have else None
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
                "missing_rows": [r for r in row_ids if r not in live]})
    dest = a.out or os.path.join(cells_dir, "live_check_%s_%s_avg.json"
                                 % (a.model.replace("+", "-"), a.task))
    save_json(dest, out)
    print("%s %s avg_gated_lookup @%.2f: n=%d live %.4f grid %.4f delta %+.2f pp | realised price "
          "%.0f vs budget %.0f (%+.1f%%)%s"
          % (a.model, a.task, a.budget_fraction, len(have), live_acc or 0, grid_acc or 0,
             out["delta_pp"] or 0.0, mean_live_price or 0, X, out["price_over_budget_pct"] or 0.0,
             " [gate reverted to the default cell]" if out["gate_reverted"] else ""))
    print("wrote", dest)
    return out


if __name__ == "__main__":
    main()
