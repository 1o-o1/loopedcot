"""Table 1: default operation against the allocator at matched compute.

  python -m prod.analyze.table1 --cells=artifacts --models=ouro_1_4b_base,ouro_1_4b_think \
      --tasks=gsm8k,math500 [--fractions=0.25,0.5,1.0] [--accounting=prompt|promptfree|both] \
      [--trained=<model name>] [--out=artifacts/table1]

Rows per (checkpoint, dataset, budget fraction), all on the EVALUATION split, protocol v2:

  default uncapped     the checkpoint's own operating point: its deepest depth (Ouro 4) at the horizon,
                       i.e. every problem's complete self-terminated chain; reported once per grid with
                       the share of problems that ran into the horizon (the only ones the cap touches)
  default at budget    normal operation under the budget: the deepest depth with the largest cap the
                       PROMPT's own cost allows (allocate.pick_default per prompt); a prompt that cannot
                       afford even cap 0 at that depth is infeasible
  allocator            the calibration-ranked cell (allocate.rank_from_cal on the calibration rows)
                       that the prompt's budget allows, the first feasible in rank order
  trained + allocator  the same rule on the trained checkpoint's grid (--trained), paired by row id

The budget is `fraction x default cost`, and a policy is priced by the CAP it commits to,
(L_fixed + k L)(P_i + B + R_i), the convention of every allocation number in the package (the rule
constrains the cap cost; the realised spend, what the rows actually generated, is reported beside
every row as `realised_mean_passes`). With --budget-basis=prompt (the default) each prompt's default
cost is the cap cost of the default's OWN uncapped cell: the deepest depth at the smallest cap that did
not truncate that prompt's chain (the horizon for a prompt that ran into it). At 100 percent normal
operation therefore lands on exactly that cell and the "default at budget" row equals the uncapped
baseline by construction (the table's anchor); at 50 and 25 percent both policies get that share of
the same prompt-level budget. With --budget-basis=mean the budget is one number per grid, the MEAN
REALISED default cost (allocate.default_cost, what `budget_fractions` in config.yaml refers to), and
long-chain prompts are starved even at 100 percent. Prompt-inclusive by default, prompt-free with
--accounting.

Uncertainty: the gain (allocator minus default at budget) carries a paired bootstrap over the
evaluation questions where BOTH are feasible (2000 draws); the allocator's own accuracy carries a
calibration-draw bootstrap (100 re-draws of the calibration rows, each re-ranking the cells: the
selection noise, reported as sd and the share of draws with a positive gain). Nothing here uses the
test-grid optimum as a policy; that number is labelled oracle in the cards, not here.
"""
import argparse
import json
import os

import numpy as np

from ..common import ART, save_json
from ..cost import model_shapes
from ..score import load_grid
from .allocate import Grid, default_cost, per_prompt_cost, rank_from_cal

N_BOOT = 2000
N_CAL_DRAWS = 100


def _grid_of(cells, name, shapes):
    return Grid(name, cells.ks, cells.Bs, cells.idx, cells.acc, cells.ptok, shapes["layers_per_loop"],
                cells.reserve, list(cells.split), shapes["layers_fixed"])


def _per_prompt(grid, sel, cost, X, order, passes=None):
    """Per evaluation question: (allocator accuracy, default-at-budget accuracy, allocator realised
    passes, default realised passes), NaN = infeasible. `X` is one budget for every question, or an
    array of budgets aligned with `sel` (NaN = no budget defined for that question, which makes both
    policies infeasible there). `passes` is cells.passes (or passes_pf) indexed [k, B, question]."""
    ki = {k: i for i, k in enumerate(grid.ks)}
    bi = {b: i for i, b in enumerate(grid.Bs)}
    kmax = grid.ks[-1]
    Xs = np.broadcast_to(np.asarray(X, float), (len(sel),))
    pv, nv, ps, ns = [], [], [], []
    for X, n in zip(Xs, sel):
        if np.isnan(X):
            pv.append(np.nan)
            nv.append(np.nan)
            ps.append(np.nan)
            ns.append(np.nan)
            continue
        p, r = grid.ptok[n], grid.reserve[n]
        feas = [c for c in order if cost(c[0], c[1], p, r) <= X]
        if feas:
            a, b = ki[feas[0][0]], bi[feas[0][1]]
            pv.append(grid.acc[a, b, n])
            ps.append(passes[a, b, n] if passes is not None else np.nan)
        else:
            pv.append(np.nan)
            ps.append(np.nan)
        nf = [B for B in grid.Bs if cost(kmax, B, p, r) <= X]
        if nf:
            a, b = ki[kmax], bi[max(nf)]
            nv.append(grid.acc[a, b, n])
            ns.append(passes[a, b, n] if passes is not None else np.nan)
        else:
            nv.append(np.nan)
            ns.append(np.nan)
    return (np.array(pv, float), np.array(nv, float), np.array(ps, float), np.array(ns, float))


def default_cap_index(cells, sel):
    """Per question of `sel`: the index of the smallest cap that did not truncate the chain at the
    deepest depth (the default's own uncapped cell), or the last cap for a chain that hit the horizon."""
    ki = len(cells.ks) - 1
    out = []
    for n in sel:
        nstop, ncut = cells.nstop[ki, :, n], cells.ncut[ki, :, n]
        ok = [j for j in range(len(cells.Bs))
              if not (np.isnan(nstop[j]) or np.isnan(ncut[j])) and ncut[j] >= nstop[j] - 1e-9]
        out.append(min(ok, key=lambda j: cells.Bs[j]) if ok else len(cells.Bs) - 1)
    return np.array(out, int)


def _boot_mean_diff(d, rng, n_boot=N_BOOT):
    n = len(d)
    if n == 0:
        return None
    boots = [float(d[rng.integers(0, n, n)].mean()) for _ in range(n_boot)]
    return [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]


def run_horizon(paths, default):
    """The horizon the deepest-depth job actually generated to, from its meta file (a Huginn job clamps
    the horizon below the largest cap because its rotary table is bounded); `default` if unknown."""
    hs = []
    for p in paths:
        m = p.replace("cells_", "meta_", 1)
        m = m[:-len(".jsonl")] + ".json" if m.endswith(".jsonl") else m
        if os.path.exists(m):
            try:
                d = json.load(open(m, encoding="utf-8"))
                h = (d.get("passes") or {}).get("single", {}).get("horizon")
                if h:
                    hs.append(int(h))
            except (OSError, ValueError):
                continue
    return min(hs) if hs else int(default)


def horizon_hit_frac(cells, sel, horizon):
    """Share of evaluation problems whose natural stop reached the run's horizon at the deepest depth."""
    ki = len(cells.ks) - 1
    bj = len(cells.Bs) - 1
    ns = cells.nstop[ki, bj, sel]
    ok = ~np.isnan(ns)
    return float(np.mean(ns[ok] >= horizon)) if ok.any() else None


def table_for(cells_dir, model, task, protocol, label, fractions, promptfree, trained=None,
              seed=7, basis="prompt"):
    rng = np.random.default_rng(seed)
    cells, paths = load_grid(cells_dir, model, task, protocol, label)
    if not cells.complete():
        raise SystemExit("%s/%s/%s: %d missing cells; Table 1 needs a complete grid"
                         % (model, task, protocol, len(cells.missing())))
    sh = model_shapes(model)
    grid = _grid_of(cells, "%s/%s/%s" % (model, task, protocol), sh)
    cost = per_prompt_cost(grid.L, promptfree, grid.L_fixed)
    ev, cal = grid.select("eval"), grid.select("cal")
    if len(ev) == 0 or len(cal) == 0:
        raise SystemExit("%s/%s: need both splits (eval %d, cal %d)" % (model, task, len(ev), len(cal)))
    Pm = float(np.median(grid.ptok[ev]))
    Rm = float(np.median(grid.reserve[ev]))
    dc = default_cost(cells, promptfree=promptfree)
    if dc["mean"] is None:
        raise SystemExit("%s/%s: no uncapped realisation of the default point; widen the caps" % (model, task))
    # each prompt's default budget = the CAP cost of the default's own uncapped cell
    jdef = default_cap_index(cells, ev)
    dpp = np.array([cost(grid.ks[-1], grid.Bs[j], grid.ptok[n], grid.reserve[n])
                    for j, n in zip(jdef, ev)], float)
    passes = cells.passes_pf if promptfree else cells.passes
    order = rank_from_cal(grid, cal, cost, Pm, Rm)
    kmax_i, bmax_i = len(grid.ks) - 1, len(grid.Bs) - 1
    unc = grid.acc[kmax_i, bmax_i, ev]
    # the cell at the horizon cap and the default's own uncapped cell are the same read-out for every
    # question (one read-out per distinct cut), so their labels must agree question by question
    unc_j = np.array([grid.acc[kmax_i, j, n] for j, n in zip(jdef, ev)], float)
    if not np.array_equal(np.nan_to_num(unc, nan=-1), np.nan_to_num(unc_j, nan=-1)):
        raise SystemExit("%s/%s: the horizon-cap labels and the uncapped-cell labels differ on %d "
                         "question(s); the grid is not internally consistent"
                         % (model, task, int(np.sum(unc != unc_j))))
    horizon = run_horizon(paths, grid.Bs[-1])
    out = {"model": model, "task": task, "protocol": protocol, "label": label,
           "accounting": "promptfree" if promptfree else "prompt-inclusive", "files": paths,
           "budget_basis": basis,
           "n_eval": int(len(ev)), "n_cal": int(len(cal)),
           "layers_per_loop": grid.L, "layers_fixed": grid.L_fixed,
           "default_depth": int(grid.ks[-1]), "horizon": int(horizon), "largest_cap": int(grid.Bs[-1]),
           "default_cost_mean": dc["mean"], "default_cost_n": dc["n"],
           "default_uncapped_acc": float(np.nanmean(unc)),
           "default_uncapped_realised_mean_passes": float(np.nanmean(
               [passes[len(grid.ks) - 1, j, n] for j, n in zip(jdef, ev)])),
           "default_cap_cost_mean": float(np.nanmean(dpp)),
           "horizon_hit_frac": horizon_hit_frac(cells, ev, horizon),
           "policy_order_top5": [list(c) for c in order[:5]], "rows": []}

    tgrid = None
    if trained:
        tcells, tpaths = load_grid(cells_dir, trained, task, protocol, label)
        if not tcells.complete():
            raise SystemExit("%s/%s: %d missing cells" % (trained, task, len(tcells.missing())))
        tgrid = _grid_of(tcells, "%s/%s/%s" % (trained, task, protocol), model_shapes(trained))
        out["trained"] = {"model": trained, "files": tpaths, "n_eval": int(len(tgrid.select("eval")))}

    for f in fractions:
        X = float(f) * (dpp if basis == "prompt" else float(dc["mean"]))
        pv, nv, ps, ns = _per_prompt(grid, ev, cost, X, order, passes)
        both = ~np.isnan(pv) & ~np.isnan(nv)
        row = {"fraction": float(f),
               "budget": (float(X) if np.ndim(X) == 0 else
                          {"per_prompt": True, "mean": float(np.nanmean(X)),
                           "n_defined": int(np.sum(~np.isnan(X)))}),
               "default_at_budget": {"acc": float(np.nanmean(nv)) if (~np.isnan(nv)).any() else None,
                                     "feasible_frac": float(np.mean(~np.isnan(nv))),
                                     "realised_mean_passes": float(np.nanmean(ns)) if (~np.isnan(ns)).any() else None},
               "allocator": {"acc": float(np.nanmean(pv)) if (~np.isnan(pv)).any() else None,
                             "feasible_frac": float(np.mean(~np.isnan(pv))),
                             "realised_mean_passes": float(np.nanmean(ps)) if (~np.isnan(ps)).any() else None},
               "n_paired": int(both.sum())}
        if both.any():
            d = pv[both] - nv[both]
            row["gain"] = {"mean": float(d.mean()), "ci95": _boot_mean_diff(d, rng),
                           "allocator_acc_paired": float(pv[both].mean()),
                           "default_acc_paired": float(nv[both].mean())}
        # selection noise: re-draw the calibration rows, re-rank, re-score the allocator
        draws = []
        for di in range(N_CAL_DRAWS):
            bs = rng.integers(0, len(cal), len(cal)) if di else np.arange(len(cal))
            od = rank_from_cal(grid, cal, cost, Pm, Rm, boot_sel=bs)
            pvd, nvd, _a, _b = _per_prompt(grid, ev, cost, X, od)
            m = ~np.isnan(pvd) & ~np.isnan(nvd)
            if m.any():
                draws.append(float((pvd[m] - nvd[m]).mean()))
        if draws:
            row["gain_cal_draws"] = {"sd": float(np.std(draws)), "frac_positive": float(np.mean([g > 0 for g in draws])),
                                     "n_draws": len(draws)}
        if tgrid is not None:
            tev = tgrid.select("eval")
            tcal = tgrid.select("cal")
            tcost = per_prompt_cost(tgrid.L, promptfree, tgrid.L_fixed)
            torder = rank_from_cal(tgrid, tcal, tcost, Pm, Rm)
            # pair by row id with the original grid's evaluation rows; the trained grid is given
            # each prompt's budget from the ORIGINAL default (the budget is the original's spend)
            gi = {grid.idx[n]: i for i, n in enumerate(ev)}
            ti = {tgrid.idx[n]: i for i, n in enumerate(tev)}
            common = sorted(set(gi) & set(ti))
            Xt = np.array([X[gi[tgrid.idx[n]]] if (np.ndim(X) and tgrid.idx[n] in gi) else
                           (np.nan if np.ndim(X) else float(X)) for n in tev], float)
            tpv, _tnv, _c, _d = _per_prompt(tgrid, tev, tcost, Xt, torder)
            a = np.array([tpv[ti[r]] for r in common], float)
            b = np.array([nv[gi[r]] for r in common], float)
            m = ~np.isnan(a) & ~np.isnan(b)
            row["trained_allocator"] = {"acc": float(np.nanmean(tpv)) if (~np.isnan(tpv)).any() else None,
                                        "feasible_frac": float(np.mean(~np.isnan(tpv))),
                                        "n_paired_with_default": int(m.sum())}
            if m.any():
                d2 = a[m] - b[m]
                row["trained_allocator"]["gain_over_default"] = {"mean": float(d2.mean()),
                                                                 "ci95": _boot_mean_diff(d2, rng)}
        out["rows"].append(row)
    return out


def _fmt(x, pct=True):
    if x is None:
        return "--"
    return "%.1f" % (100 * x) if pct else "%.3g" % x


def markdown(tables):
    lines = ["| checkpoint | dataset | acct | basis | budget | default uncapped | default at budget (feasible) | "
             "allocator (feasible) | paired: default / allocator (n) | gain [95% CI] | cal-draw sd / P(gain>0) | "
             "trained + allocator |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for t in tables:
        first = True
        for r in t["rows"]:
            g = r.get("gain") or {}
            cd = r.get("gain_cal_draws") or {}
            ta = r.get("trained_allocator") or {}
            ci = g.get("ci95")
            lines.append("| %s | %s | %s | %s | %d%% | %s%s | %s (%s) | %s (%s) | %s | %s%s | %s | %s%s |" % (
                t["model"], t["task"], "pf" if t["accounting"] == "promptfree" else "pi",
                t.get("budget_basis", "prompt"), round(100 * r["fraction"]),
                _fmt(t["default_uncapped_acc"]) if first else "",
                (" (horizon hit %s)" % _fmt(t["horizon_hit_frac"])) if first and t["horizon_hit_frac"] is not None else "",
                _fmt(r["default_at_budget"]["acc"]), _fmt(r["default_at_budget"]["feasible_frac"]),
                _fmt(r["allocator"]["acc"]), _fmt(r["allocator"]["feasible_frac"]),
                ("%s / %s (%d)" % (_fmt(g["default_acc_paired"]), _fmt(g["allocator_acc_paired"]), r["n_paired"])) if g else "--",
                ("%+.1f" % (100 * g["mean"])) if g else "--",
                (" [%+.1f, %+.1f]" % (100 * ci[0], 100 * ci[1])) if ci else "",
                ("%.1f / %.2f" % (100 * cd["sd"], cd["frac_positive"])) if cd else "--",
                _fmt(ta.get("acc")) if ta else "--",
                (" (%+.1f)" % (100 * ta["gain_over_default"]["mean"])) if ta.get("gain_over_default") else ""))
            first = False
    return "\n".join(lines) + "\n"


def main(argv=None):
    p = argparse.ArgumentParser(prog="prod.analyze.table1")
    p.add_argument("--cells", default=None)
    p.add_argument("--models", required=True)
    p.add_argument("--tasks", required=True)
    p.add_argument("--protocol", default="natural")
    p.add_argument("--label", default="v2")
    p.add_argument("--fractions", default="0.25,0.5,1.0")
    p.add_argument("--accounting", default="prompt", choices=("prompt", "promptfree", "both"))
    p.add_argument("--trained", default=None, help="model name of the trained checkpoint's grid")
    p.add_argument("--budget-basis", dest="basis", default="prompt", choices=("prompt", "mean"),
                   help="fraction of each prompt's own default cost (default) or of the grid's mean")
    p.add_argument("--out", default=None)
    a = p.parse_args(argv)
    cells_dir = a.cells or ART
    fractions = [float(x) for x in a.fractions.split(",") if x.strip()]
    accts = [False, True] if a.accounting == "both" else [a.accounting == "promptfree"]
    tables = []
    for model in [m.strip() for m in a.models.split(",") if m.strip()]:
        for task in [t.strip() for t in a.tasks.split(",") if t.strip()]:
            for pf in accts:
                tables.append(table_for(cells_dir, model, task, a.protocol, a.label, fractions, pf,
                                        trained=a.trained, basis=a.basis))
    out = a.out or os.path.join(cells_dir, "table1_%s_%s_%s" % (a.protocol, a.accounting, a.basis))
    save_json(out + ".json", {"tables": tables, "fractions": fractions, "protocol": a.protocol,
                              "budget_basis": a.basis,
                              "label": a.label, "n_boot": N_BOOT, "n_cal_draws": N_CAL_DRAWS})
    md = markdown(tables)
    with open(out + ".md", "w", encoding="utf-8", newline="\n") as f:
        f.write(md)
    print(md)
    print("wrote %s.json and %s.md" % (out, out))
    return tables


if __name__ == "__main__":
    main()
