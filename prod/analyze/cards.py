"""The card per checkpoint, to the operational definition of PLAN.md "Framework of record" rule 1.

  python -m prod.analyze.cards --cells=artifacts --model=ouro_1_4b_base [--tasks=gsm8k,math500]
                               [--label=v2] [--out=FILE]

Rule 1, field by field (the brief's own list, in order):
  supported depths           what the code accepts (the adapter's `depths`)
  trained depth k_t          from the card or the paper (the adapter's `trained_depth`)
  measured saturation depth  the smallest k whose T=512 accuracy is within the paired CI of the
                             maximum over k
  raw contrasts              A(k=4) - A(k=2) at T in {64, 128, 256, 512}
  oracle frontier V(X)       at the 16 budgets on the TEST grid, labelled oracle (rule 2)
  dip cells                  T in {16, 32, 64} against T=0, per k (LEDGER 2026-09-05 S9a: "a short
                             chain of thought is worse than none ... accuracy drops from 17% at zero
                             tokens to 12% at 8 tokens")
  natural-stop distribution  per k
  cost model                 layer passes, FLOPs, KV bytes per token, wall clock
  G / c / l                  with the COMMITMENT definition (LEDGER "Agreed 2026-09-11")
  fitted a / m / g           LAST, with fit quality, never without the raw contrasts
"""
import argparse
import os

import numpy as np

from ..common import save_json
from ..cost import cell_costs, model_shapes
from ..models import depths_for, get
from ..score import load_grid
from .allocate import Grid, budget_grid, default_cost, per_prompt_cost, pick
from .tests import card_fit_block


def paired_ci(x, y, n_boot=2000, seed=11):
    """95% paired bootstrap interval for mean(x) - mean(y) over questions."""
    rng = np.random.default_rng(seed)
    d = np.asarray(x, float) - np.asarray(y, float)
    n = len(d)
    bs = [float(d[rng.integers(0, n, n)].mean()) for _ in range(n_boot)]
    return float(d.mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def saturation_depth(cells, sel, cap=512):
    """The smallest k whose accuracy at `cap` is within the paired CI of the maximum over k."""
    if cap not in cells.Bs:
        cap = cells.Bs[-1]
    j = cells.Bs.index(cap)
    per_k = [cells.acc[i, j, sel] for i in range(len(cells.ks))]
    best = int(np.argmax([v.mean() for v in per_k]))
    for i in range(len(cells.ks)):
        m, lo, hi = paired_ci(per_k[i], per_k[best])
        if lo <= 0.0 <= hi or i == best:
            return {"cap": cap, "depth": cells.ks[i], "best_depth": cells.ks[best],
                    "delta_vs_best_pp": 100 * m, "ci_pp": [100 * lo, 100 * hi]}
    return {"cap": cap, "depth": cells.ks[best], "best_depth": cells.ks[best],
            "delta_vs_best_pp": 0.0, "ci_pp": [0.0, 0.0]}


def dip_cells(cells, sel, caps=(16, 32, 64)):
    """Per k, the accuracy at each short cap minus the accuracy at T=0, with a paired interval."""
    if 0 not in cells.Bs:
        return None
    j0 = cells.Bs.index(0)
    out = []
    for i, k in enumerate(cells.ks):
        row = {"k": k}
        for T in caps:
            if T not in cells.Bs:
                continue
            m, lo, hi = paired_ci(cells.acc[i, cells.Bs.index(T), sel], cells.acc[i, j0, sel])
            row["T%d" % T] = {"delta_pp": 100 * m, "ci_pp": [100 * lo, 100 * hi],
                              "is_dip": bool(hi < 0)}
        out.append(row)
    return out


def natural_stop_distribution(cells, sel, cap=512):
    j = cells.Bs.index(cap) if cap in cells.Bs else len(cells.Bs) - 1
    out = []
    for i, k in enumerate(cells.ks):
        v = cells.nstop[i, j, sel]
        v = v[~np.isnan(v)]
        out.append({"k": k, "n": int(len(v)), "mean": float(v.mean()) if len(v) else None,
                    "quantiles": ([float(np.percentile(v, q)) for q in (10, 25, 50, 75, 90)]
                                  if len(v) else None),
                    "frac_at_cap": float(np.mean(v >= cap)) if len(v) else None})
    return out


def oracle_frontier(grid, promptfree=False, n_budgets=16):
    """V(X) on the TEST grid at 16 log-spaced budgets. Labelled ORACLE (measurement rule 2): this is
    the ceiling, never a policy result."""
    cost = per_prompt_cost(grid.L, promptfree)
    ev = grid.select("eval")
    Pm = float(np.median(grid.ptok[ev]))
    Rm = float(np.median(grid.reserve[ev]))
    cmat = np.array([[cost(k, B, Pm, Rm) for B in grid.Bs] for k in grid.ks])
    Xs = budget_grid(cmat, n_budgets)
    A = grid.mean_acc(ev)
    out = []
    for X in Xs:
        c = pick(A, cmat, X)
        out.append({"X": float(X), "oracle_cell": None if c is None else [grid.ks[c[0]],
                                                                         grid.Bs[c[1]]],
                    "oracle_acc": None if c is None else float(A[c])})
    return {"label": "oracle (test-grid optimum; never a policy result)",
            "promptfree": bool(promptfree), "median_prompt_tokens": Pm,
            "median_reserve": Rm, "points": out}


def card(cells_dir, model, task, protocol="natural", label="v2", shapes=None):
    cells, paths = load_grid(cells_dir, model, task, protocol, label)
    sel_ev = cells.select("eval")
    sel_all = cells.select("all")
    A = cells.mean_acc(sel_ev)
    ad = get(model)
    sh = shapes if shapes is not None else model_shapes(
        model if model in ("huginn_0125", "mcleish_llama32_r32") or model.startswith("ouro")
        else model)
    L_per_loop = sh["layers_per_loop"]
    grid = Grid("%s/%s/%s" % (model, task, protocol), cells.ks, cells.Bs, cells.idx,
                cells.acc, cells.ptok, L_per_loop, cells.reserve, list(cells.split))
    out = {
        "model": model, "task": task, "protocol": protocol, "label": label, "files": paths,
        "n_eval": int(len(sel_ev)), "n_cal": int(len(cells.select("cal"))),
        "complete": cells.complete(), "n_missing": len(cells.missing()),
        # rule 1, in the brief's order
        "supported_depths": list(ad.depths),
        "depths_of_record": list(depths_for(model, task)),
        "depths_measured": cells.ks,
        "trained_depth": ad.trained_depth,
        "measured_saturation_depth": saturation_depth(cells, sel_ev),
        "raw_contrasts": card_fit_block(A, cells.ks, cells.Bs)["raw_contrasts"],
        "oracle_frontier": oracle_frontier(grid),
        "oracle_frontier_promptfree": oracle_frontier(grid, promptfree=True),
        # Fix 2 (PP3b, decision 7): the mean realised cost of the default operating point --
        # `budget_fractions` (config.yaml) are fractions of THIS, not of the grid's largest CAP cell.
        "default_cost": default_cost(cells, promptfree=False),
        "default_cost_promptfree": default_cost(cells, promptfree=True),
        "dip_cells": dip_cells(cells, sel_ev),
        "natural_stop": natural_stop_distribution(cells, sel_ev),
        "cost_model": {"layers_per_loop": L_per_loop, "layers_fixed": sh["layers_fixed"],
                       "d_model": sh["d_model"], "n_nonembed": sh["n_nonembed"],
                       "cells": cell_costs(cells, sh)},
        "mechanism_commitment": cells.mechanism("eval"),
        "mechanism_commitment_strict": cells.mechanism("eval", strict=True),
        # fitted quantities LAST (rule 1: never without the raw contrasts, which are above)
        "surface": card_fit_block(A, cells.ks, cells.Bs),
        "parse_rate_forced": np.round(cells.parse_rate(), 6).tolist(),
        "acc_table": np.round(A, 6).tolist(),
        "acc_table_all_splits": np.round(cells.mean_acc(sel_all), 6).tolist(),
    }
    return out


def main(argv=None):
    p = argparse.ArgumentParser(prog="prod.analyze.cards")
    p.add_argument("--cells", required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--tasks", default="gsm8k")
    p.add_argument("--protocol", default="natural")
    p.add_argument("--label", default="v2")
    p.add_argument("--out", default=None)
    a = p.parse_args(argv)
    shapes = model_shapes(a.model)
    out = {}
    for t in a.tasks.split(","):
        out[t] = card(a.cells, a.model, t, a.protocol, a.label, shapes=shapes)
        c = out[t]
        print("%s / %s: n_eval=%d saturation k=%s (best %s) rank-one energy %.3f, raw k%d-k%d "
              "contrasts %s"
              % (a.model, t, c["n_eval"], c["measured_saturation_depth"]["depth"],
                 c["measured_saturation_depth"]["best_depth"],
                 c["surface"]["rank_one"]["energy_rank_one"],
                 c["raw_contrasts"]["k_hi"], c["raw_contrasts"]["k_lo"],
                 {k: round(v, 1) for k, v in c["raw_contrasts"]["contrast_pp"].items()}))
        dc, dcp = c["default_cost"], c["default_cost_promptfree"]
        print("  default cost (decision 7): k=%s n=%d mean=%s | promptfree mean=%s"
              % (dc["k"], dc["n"], dc["mean"], dcp["mean"]))
    dest = a.out or os.path.join(a.cells, "card_%s.json" % a.model.replace("+", "-"))
    save_json(dest, out)
    print("wrote", dest)
    return out


if __name__ == "__main__":
    main()
