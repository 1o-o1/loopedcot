"""Allocation: the calibration cost curve, gain over normal operation, and the bootstraps.

Every allocation policy is built on calibration questions and scored on disjoint evaluation
questions; the test-grid optimum is labelled ORACLE and never reported as a policy result. The
headline comparison is the allocator against NORMAL OPERATION (the deepest depth with its largest
feasible cap), paired per prompt, with the prompt's own token count and answer reserve.

Ported, with the source named at each function:
  Grid / build_grid / cost_cap / pick / pick_default   b1t.py and b1t_v3.py
  rank_from_cal / policy_matrix / contrast / non-inferiority / gain over normal
                                                       v5_s32_analysis.py
  v1 bootstrap (c, l, G, reconstruction RMSE) and the calibration-draw bootstrap
                                                       v3_bootstrap.py

Two cost conventions are kept apart on purpose and never mixed in one table:
  CAP cost      (L_fixed + k L) (P_mean + B)  -- b1t / S28's budget axis, one number per (k, B)
  PER-PROMPT    (L_fixed + k L) (P_i + B + R_i)
                                              -- the headline, one number per (k, B, question);
                `promptfree=True` drops P_i (the prompt-inclusive / prompt-free pair)

L is the layers INSIDE the loop and L_fixed the layers executed once per token whatever k is, so the
passes per token are L_fixed + k L. Ouro runs every layer inside the recurrence (L_fixed = 0, the
default, which is why every pre-existing caller and the frozen G3 reproduction are unchanged); the
raven families do not (Huginn prelude 2 + k * 4 + coda 2, so L = 4 and L_fixed = 4; McLeish
4 + k * 6 + 4, so L = 6 and L_fixed = 8). `cost.model_shapes` is the single source of both numbers
(`layers_per_loop`, `layers_fixed`) and the callers read them from there.

`default_cost` is a third quantity, not a cost FORMULA but a cost STATISTIC read off the cells: the
mean realised layer-pass cost of the default operating point (max measured depth, natural stop,
uncapped). `config.yaml`'s `budget_fractions` (0.25/0.5/1.0) are fractions of THIS, not of the
grid's largest CAP cell (`cmat.max()`).
"""
import numpy as np

N_BUDGETS = 16
BAD_REGRET = 0.05           # b1t_v3.BAD: a "bad selection" is a regret above 5 points


def _nanmean(x):
    """The mean over the defined entries, NaN when there are none.

    np.nanmean warns on an all-NaN slice; a bootstrap draw can select only questions that are
    infeasible at one budget, so the empty case is expected here and is not worth a warning.
    """
    v = np.asarray(x, float)
    m = ~np.isnan(v)
    return float(v[m].mean()) if m.any() else float("nan")


# ------------------------------------------------------------------ grids (b1t.py)
class Grid(object):
    """(ks, Bs, idx, acc[k, B, question], prompt tokens, layers per loop, layers executed once).

    `L_fixed` is 0 by default: Ouro runs every layer inside the recurrence, so the pre-existing
    callers and the frozen G3 tables are untouched. A raven family passes its prelude + coda.
    """

    def __init__(self, name, ks, Bs, idx, acc, ptok, L, reserve=None, split=None, L_fixed=0):
        self.name, self.ks, self.Bs, self.idx = name, list(ks), list(Bs), list(idx)
        self.acc, self.ptok, self.L = acc, np.asarray(ptok, float), L
        self.L_fixed = L_fixed
        self.reserve = (np.zeros(len(idx)) if reserve is None else np.asarray(reserve, float))
        self.split = list(split) if split is not None else ["eval"] * len(idx)
        self.P = float(np.mean(self.ptok))

    def restrict_B(self, Bs):
        bi = [self.Bs.index(b) for b in Bs]
        return Grid(self.name, self.ks, list(Bs), self.idx, self.acc[:, bi], self.ptok, self.L,
                    self.reserve, self.split, self.L_fixed)

    def mean_acc(self, sel=None):
        a = self.acc if sel is None else self.acc[:, :, sel]
        return a.mean(2)

    def cost_cap(self):
        """b1t.Grid.cost_cap, with the family's fixed layers: (L_fixed + k L) (mean prompt + B).

        L_fixed = 0 reduces to b1t's k * L * (P + B) verbatim, which is the Ouro case the frozen
        b1t / S28 numbers were measured on.
        """
        k = np.array(self.ks, float)[:, None]
        B = np.array(self.Bs, float)[None, :]
        return (self.L_fixed + k * self.L) * (self.P + B)

    def select(self, split):
        if split == "all":
            return np.arange(len(self.idx))
        return np.array([i for i, s in enumerate(self.split) if s == split], dtype=int)


def build_grid(name, rows, L, correct_key="correct_v2"):
    """The (k, B, question) accuracy grid from scored rows: the default label is protocol v2, and
    each row's prompt tokens, answer reserve and eval/cal split are carried along for the
    per-prompt cost."""
    ks = sorted({int(r["k"]) for r in rows})
    Bs = sorted({int(r["B"]) for r in rows})
    idx = sorted({int(r.get("row_idx", r["idx"])) for r in rows})
    ki = {k: i for i, k in enumerate(ks)}
    bi = {b: i for i, b in enumerate(Bs)}
    ni = {n: i for i, n in enumerate(idx)}
    acc = np.full((len(ks), len(Bs), len(idx)), np.nan)
    ptok = np.full(len(idx), np.nan)
    res = np.zeros(len(idx))
    spl = ["eval"] * len(idx)
    for r in rows:
        n = ni[int(r.get("row_idx", r["idx"]))]
        v = r[correct_key] if correct_key in r else (
            r["trace_correct"] if r.get("trace_answer") not in (None, "None", "")
            else r["correct"])
        acc[ki[int(r["k"])], bi[int(r["B"])], n] = float(bool(v in (True, "True")))
        ptok[n] = float(r["n_prompt_tokens"])
        res[n] = float(r.get("n_suffix_tokens", 0)) + float(r.get("n_answer_tokens", 0))
        spl[n] = r.get("split", "eval")
    if np.isnan(acc).any():
        w = np.argwhere(np.isnan(acc))
        raise ValueError("%s: %d missing cells, first (k=%s, B=%s, idx=%s)"
                         % (name, len(w), ks[w[0][0]], Bs[w[0][1]], idx[w[0][2]]))
    return Grid(name, ks, Bs, idx, acc, ptok, L, res, spl)


# ------------------------------------------------------------------ picking (b1t_v3.py)
def pick(pred, cost, X):
    """b1t_v3.pick, verbatim: argmax of the predicted surface among cells with cost <= X."""
    feas = cost <= X
    if not feas.any():
        return None
    return np.unravel_index(int(np.argmax(np.where(feas, pred, -np.inf))), pred.shape)


def pick_default(cost, X, ki=None):
    """b1t_v3.pick_default, verbatim: the deepest feasible depth (or the given one) with its largest
    feasible cap. This is NORMAL OPERATION when ki is None."""
    feas = cost <= X
    ks_ok = [i for i in range(cost.shape[0]) if feas[i].any()]
    if not ks_ok:
        return None
    i = max(ks_ok) if ki is None else (ki if feas[ki].any() else None)
    if i is None:
        return None
    return (i, int(np.max(np.where(feas[i])[0])))


def budget_grid(cost, n=N_BUDGETS):
    """b1t_v3: n log-spaced budgets spanning the cost matrix."""
    return np.exp(np.linspace(np.log(cost.min()), np.log(cost.max()), n)) * (1 + 1e-9)


# ------------------------------------------------------------------ nested regret (b1t_v3)
def nested_regret(grid, rng, n_cal=50, n_rep=20, n_budgets=N_BUDGETS, arms=None):
    """The frozen evaluation protocol of b1t_v3.run_pair for the arms that need NO fitted surface.

    Per draw: permute the questions, take n_cal as calibration, split the rest into a SELECTION half
    and an EVALUATION half; the oracle cell is picked on the selection half and scored on the
    evaluation half, so the reported "oracle" is a nested oracle and not the test-grid optimum.
    Regret = A_ev(oracle cell) - A_ev(arm cell), averaged over budgets and draws.

    Arms here: oracle, R4 (exhaustive on the calibration questions), cal_direct (argmax over the two
    measured rows only, k in {2, kmax}), default_deep (normal operation), default_k1. The transferred
    surfaces R0/R1/R2/R2g/PLt and the in-sample ceilings law_full/PL_full live in b1t_v3.py, which
    owns the fits; `gates/g3_score.py` states that split explicitly.
    """
    arms = arms or ("oracle", "R4", "cal_direct", "default_deep", "default_k1")
    ks = grid.ks
    kmax_i = len(ks) - 1
    kb_i = ks.index(2) if 2 in ks else max(0, kmax_i - 1)
    cost = grid.cost_cap()
    N = len(grid.idx)
    Xs = budget_grid(cost, n_budgets)
    reg = {a: [] for a in arms}
    bad = {a: 0 for a in arms}
    nsel = 0
    for _rep in range(n_rep):
        perm = rng.permutation(N)
        cal, rest = perm[:n_cal], perm[n_cal:]
        sel, ev = rest[:len(rest) // 2], rest[len(rest) // 2:]
        A_cal, A_sel, A_ev = grid.mean_acc(cal), grid.mean_acc(sel), grid.mean_acc(ev)
        cd = np.full_like(A_cal, -np.inf)
        cd[kb_i] = A_cal[kb_i]
        cd[kmax_i] = A_cal[kmax_i]
        for X in Xs:
            o = pick(A_sel, cost, X)
            if o is None:
                continue
            ref = A_ev[o]
            nsel += 1
            for a in arms:
                if a == "oracle":
                    c = o
                elif a == "R4":
                    c = pick(A_cal, cost, X)
                elif a == "cal_direct":
                    c = pick(cd, cost, X)
                    if c is None or not np.isfinite(cd[c]):
                        c = pick_default(cost, X)
                elif a == "default_deep":
                    c = pick_default(cost, X)
                elif a == "default_k1":
                    c = pick_default(cost, X, ki=0)
                else:
                    raise KeyError(a)
                if c is None:
                    continue
                r = float(ref - A_ev[c])
                reg[a].append(r)
                bad[a] += int(r > BAD_REGRET)
    return {"n_selections": nsel, "budgets": int(n_budgets), "n_cal": n_cal, "n_rep": n_rep,
            "regret_mean": {a: float(np.mean(reg[a])) if reg[a] else None for a in arms},
            "bad_selection_frac": {a: (bad[a] / max(1, len(reg[a]))) for a in arms}}


# ------------------------------------------------------------------ per-prompt policy (v5)
def per_prompt_cost(L, promptfree=False, L_fixed=0):
    """The per-prompt cost: (L_fixed + k L) (P_i + B + R_i), or the same prompt-free
    (v5_s32_analysis).

    `L_fixed = 0` is v5's formula verbatim and is right for Ouro; a raven family passes its
    prelude + coda, whose passes per token do not scale with k.
    """
    if promptfree:
        return lambda k, B, p, r: (L_fixed + k * L) * (B + r)
    return lambda k, B, p, r: (L_fixed + k * L) * (p + B + r)


def default_cost(cells, promptfree=False, k=None, split="eval"):
    """Budget as a fraction of the default cost: the MEAN REALISED layer-pass cost of the DEFAULT
    OPERATING POINT -- the checkpoint's max measured depth ("use the max depth present in the
    cells": Ouro 4, Huginn 32, McLeish 32 by card, when the full depth set ran) at the NATURAL
    STOP, UNCAPPED, from the cells themselves (prompt tokens + generated tokens + read-out tokens
    at the smallest B that did not truncate the natural stop for that problem).

    Not X = budget_fraction * cmat.max() ("grid max": the cost of the grid's largest CAP cell at
    the median prompt -- a synthetic k*L*(P+B) number nothing realises end to end, since B is a
    cap, not a length any row is guaranteed to reach).

    `cells` is a score.Cells object (ks, Bs, idx, ncut, nstop, passes, passes_pf, split); `k=None`
    uses the max depth present. Returns {"k", "n", "mean", "promptfree"}; `mean` is None when no
    row in `split` ever reached an uncapped realisation (every cap truncates its natural stop --
    the caps grid needs widening before `--budget-fraction` means anything for that grid).
    """
    ks = list(cells.ks)
    if not ks:
        return {"k": None, "n": 0, "mean": None, "promptfree": bool(promptfree)}
    kk = k if (k is not None and k in ks) else ks[-1]
    per = default_cost_per_prompt(cells, promptfree, kk, split)
    vals = [v for v in per.values() if v is not None]
    return {"k": int(kk), "n": len(vals), "mean": (float(np.mean(vals)) if vals else None),
            "promptfree": bool(promptfree)}


def default_cost_per_prompt(cells, promptfree=False, k=None, split="eval"):
    """The realised cost of the default operating point for EACH question of `split`: {row position
    in cells.idx: cost or None}. None when every cap truncated that question's natural stop."""
    ks = list(cells.ks)
    kk = k if (k is not None and k in ks) else ks[-1]
    ki = ks.index(kk)
    sel = cells.select(split) if hasattr(cells, "select") else np.arange(len(cells.idx))
    field = cells.passes_pf if promptfree else cells.passes
    out = {}
    for n in sel:
        nstop, ncut = cells.nstop[ki, :, n], cells.ncut[ki, :, n]
        ok = [j for j in range(len(cells.Bs))
              if not (np.isnan(nstop[j]) or np.isnan(ncut[j])) and ncut[j] >= nstop[j] - 1e-9]
        if not ok:
            out[int(n)] = None
            continue
        j = min(ok, key=lambda j: cells.Bs[j])          # the cheapest UNCAPPED realisation
        v = field[ki, j, n]
        out[int(n)] = None if np.isnan(v) else float(v)
    return out


def rank_from_cal(grid, cal_sel, cost, Pm, Rm, boot_sel=None):
    """v5_s32_analysis.rank_from_cal, verbatim: rank the cells by calibration accuracy, breaking ties
    by the cheaper cell at the task's median prompt length."""
    cells = [(k, B) for k in grid.ks for B in grid.Bs]
    ki = {k: i for i, k in enumerate(grid.ks)}
    bi = {b: i for i, b in enumerate(grid.Bs)}
    ids = cal_sel if boot_sel is None else cal_sel[boot_sel]
    acc = {c: float(grid.acc[ki[c[0]], bi[c[1]], ids].mean()) for c in cells}
    return sorted(cells, key=lambda c: (-acc[c], cost(c[0], c[1], Pm, Rm)))


def policy_vectors(grid, ev_sel, cost, Xs, order):
    """v5_s32_analysis.policy_matrix, verbatim: per budget, the per-question accuracy of the
    calibration-chosen policy and of normal operation (k_max at its largest feasible cap)."""
    ki = {k: i for i, k in enumerate(grid.ks)}
    bi = {b: i for i, b in enumerate(grid.Bs)}
    kmax = grid.ks[-1]
    out = []
    for X in Xs:
        pv, nv = [], []
        for n in ev_sel:
            p, r = grid.ptok[n], grid.reserve[n]
            feas = [c for c in order if cost(c[0], c[1], p, r) <= X]
            if not feas:
                pv.append(np.nan)
                nv.append(np.nan)
                continue
            c = feas[0]
            pv.append(grid.acc[ki[c[0]], bi[c[1]], n])
            nf = [B for B in grid.Bs if cost(kmax, B, p, r) <= X]
            nv.append(grid.acc[ki[kmax], bi[max(nf)], n] if nf else np.nan)
        out.append((np.array(pv, float), np.array(nv, float)))
    return out


def budget_ranges(grid, cost, Xs, Pm, Rm, L=None, L_fixed=None):
    """B* and B_low, the two budget ranges.

    B*    budgets at which BOTH (k=2, T=64) and (k=k_max, T=64) are feasible at the median prompt
    B_low budgets at which (k_max, 64) is NOT feasible but (k=1, 64) is

    `cost` already prices the cells with the family's fixed layers; `L` and `L_fixed` (default: the
    grid's own) are recorded in the returned meta, so a table states which pass count the ranges
    were priced with. A raven range priced as if L_fixed were 0 is a different question, and the
    meta is where that shows.
    """
    kmax = grid.ks[-1]
    k2 = 2 if 2 in grid.ks else grid.ks[min(1, len(grid.ks) - 1)]
    T = 64 if 64 in grid.Bs else grid.Bs[len(grid.Bs) // 2]
    bstar = [i for i, X in enumerate(Xs)
             if cost(k2, T, Pm, Rm) <= X and cost(kmax, T, Pm, Rm) <= X]
    blow = [i for i, X in enumerate(Xs)
            if cost(kmax, T, Pm, Rm) > X and cost(grid.ks[0], T, Pm, Rm) <= X]
    return bstar, blow, {"k2": k2, "kmax": kmax, "T": T,
                         "L": (grid.L if L is None else L),
                         "L_fixed": (grid.L_fixed if L_fixed is None else L_fixed)}


def gain_over_normal(grid, promptfree=False, n_budgets=N_BUDGETS, n_boot=2000,
                     n_cal_draws=100, seed=7, min_normal_feasible=0.9, L_fixed=None):
    """The headline: the gain of the calibration-chosen policy over normal operation.

    Two bootstraps, both from v3_bootstrap / v5_s32_analysis:
      * paired over evaluation questions (n_boot resamples) -- sampling noise in the SCORE
      * over calibration draws (n_cal_draws resamples of the calibration questions, each re-ranking
        the cells) -- SELECTION noise, reported as the share of draws with a positive mean gain and
        the sd of the mean over draws

    The per-budget gain vectors are kept at FULL LENGTH, one entry per evaluation question, NaN where
    the policy or normal operation is infeasible for that question at that budget, and are stacked
    without truncation. Column j is therefore the same question at every budget, and the paired
    bootstrap resamples QUESTION INDICES (the same columns at every budget) and takes a nanmean per
    draw. Dropping the NaNs per budget and cutting every vector to the shortest would re-index the
    columns: one question infeasible at a low budget would move every later question a place to the
    left, so the paired bootstrap would pair different questions at different budgets.

    `L_fixed` defaults to the grid's own (0 for Ouro, prelude + coda for a raven family).
    """
    rng = np.random.default_rng(seed)
    cost = per_prompt_cost(grid.L, promptfree,
                           grid.L_fixed if L_fixed is None else L_fixed)
    ev, cal = grid.select("eval"), grid.select("cal")
    if len(cal) == 0 or len(ev) == 0:
        raise ValueError("%s: need both splits (eval %d, cal %d)" % (grid.name, len(ev), len(cal)))
    Pm = float(np.median(grid.ptok[ev]))
    Rm = float(np.median(grid.reserve[ev]))
    cmat = np.array([[cost(k, B, Pm, Rm) for B in grid.Bs] for k in grid.ks])
    Xs = budget_grid(cmat, n_budgets)
    order = rank_from_cal(grid, cal, cost, Pm, Rm)
    pol = policy_vectors(grid, ev, cost, Xs, order)
    bstar, blow, rmeta = budget_ranges(grid, cost, Xs, Pm, Rm)

    gains, per_budget = [], []
    for xi, X in enumerate(Xs):
        pv, nv = pol[xi]
        feas = ~np.isnan(nv)
        rec = {"X": float(X), "normal_feasible_frac": float(feas.mean()),
               "policy_acc": float(np.nanmean(pv)) if np.any(~np.isnan(pv)) else None,
               "normal_acc": float(np.nanmean(nv)) if feas.any() else None,
               "in_Bstar": xi in bstar, "in_Blow": xi in blow}
        if feas.mean() >= min_normal_feasible and (~np.isnan(pv) & feas).sum() > 0:
            d = pv - nv                  # NaN wherever either arm is infeasible, kept IN PLACE
            rec["gain"] = _nanmean(d)
            rec["n_questions_in_gain"] = int(np.sum(~np.isnan(d)))
            gains.append(d)
        per_budget.append(rec)

    out = {"grid": grid.name, "promptfree": bool(promptfree), "n_eval": int(len(ev)),
           "n_cal": int(len(cal)), "median_prompt_tokens": Pm, "median_reserve": Rm,
           "budgets": [float(x) for x in Xs], "per_budget": per_budget,
           "Bstar": bstar, "Blow": blow, "range_meta": rmeta,
           "policy_order_top5": [list(c) for c in order[:5]]}
    if not gains:
        out["gain_mean"] = None
        return out
    G = np.stack(gains)              # (budgets with normal operation, evaluation questions)
    nq = G.shape[1]
    per_b = np.array([_nanmean(G[i]) for i in range(G.shape[0])])
    boots = []
    for _ in range(n_boot):
        cols = rng.integers(0, nq, nq)   # ONE resample of the questions, shared by every budget
        b = _nanmean(G[:, cols])
        if not np.isnan(b):
            boots.append(b)
    out.update({"gain_mean": _nanmean(G), "gain_worst_budget": float(np.nanmin(per_b)),
                "gain_ci95": ([float(np.percentile(boots, 2.5)),
                               float(np.percentile(boots, 97.5))] if boots else None),
                "n_budgets_with_normal": int(G.shape[0]),
                "n_eval_in_gain": int(nq),
                "n_gain_cells_defined": int(np.sum(~np.isnan(G))),
                "gain_per_budget": [float(v) for v in per_b]})
    # calibration-draw bootstrap (selection noise)
    draws = []
    for d in range(n_cal_draws):
        sel = rng.integers(0, len(cal), len(cal)) if d else np.arange(len(cal))
        od = rank_from_cal(grid, cal, cost, Pm, Rm, boot_sel=sel)
        pd_ = policy_vectors(grid, ev, cost, Xs, od)
        gs = []
        for xi in range(len(Xs)):
            pv, nv = pd_[xi]
            feas = ~np.isnan(nv)
            if feas.mean() >= min_normal_feasible and (~np.isnan(pv) & feas).sum() > 0:
                gs.append(float(np.nanmean(pv[feas] - nv[feas])))
        if gs:
            draws.append(float(np.mean(gs)))
    if draws:
        out.update({"gain_cal_draw_mean": float(np.mean(draws)),
                    "gain_cal_draw_sd": float(np.std(draws)),
                    "gain_cal_draw_frac_positive": float(np.mean([g > 0 for g in draws])),
                    "gain_cal_draw_ci95": [float(np.percentile(draws, 2.5)),
                                           float(np.percentile(draws, 97.5))]})
    return out


def contrast(grid_a, grid_b, promptfree=False, n_budgets=N_BUDGETS, n_boot=2000, seed=7,
             which="Bstar", L_fixed=None, L_fixed_b=None):
    """v5_s32_analysis's contrast: the mean over a predeclared budget range of the paired difference
    between two arms' calibration-chosen policies, with a 95% paired bootstrap over evaluation
    questions. Used for the training arms (S32/S19) and for any two checkpoints on one task.

    Each grid is PRICED WITH ITS OWN (L, L_fixed): two checkpoints of different families spend
    different numbers of passes per token at the same k. The BUDGET GRID, the median prompt and the
    median reserve come from grid_a alone, so both arms are still read at the same budgets.
    `L_fixed` and `L_fixed_b` override grid_a's and grid_b's own value.

    COMPLETE CASE over questions, on purpose and unlike `gain_over_normal`: a question with a NaN at
    ANY budget of the range leaves every budget, so the mean over the range is a mean over one fixed
    set of questions and the paired bootstrap resamples that set. The price is that a question one
    arm cannot afford at the cheapest budget of the range leaves the comparison entirely;
    `n_eval` and `n_eval_dropped_incomplete` report how many survived and how many went.
    """
    rng = np.random.default_rng(seed)
    cost_a = per_prompt_cost(grid_a.L, promptfree,
                             grid_a.L_fixed if L_fixed is None else L_fixed)
    cost_b = per_prompt_cost(grid_b.L, promptfree,
                             grid_b.L_fixed if L_fixed_b is None else L_fixed_b)
    ev = grid_a.select("eval")
    cal = grid_a.select("cal")
    Pm = float(np.median(grid_a.ptok[ev]))
    Rm = float(np.median(grid_a.reserve[ev]))
    cmat = np.array([[cost_a(k, B, Pm, Rm) for B in grid_a.Bs] for k in grid_a.ks])
    Xs = budget_grid(cmat, n_budgets)
    bstar, blow, _m = budget_ranges(grid_a, cost_a, Xs, Pm, Rm)
    rng_idx = bstar if which == "Bstar" else blow
    if not rng_idx:
        return {"range": which, "empty": True}
    pa = policy_vectors(grid_a, ev, cost_a, [Xs[i] for i in rng_idx],
                        rank_from_cal(grid_a, cal, cost_a, Pm, Rm))
    pb = policy_vectors(grid_b, grid_b.select("eval"), cost_b, [Xs[i] for i in rng_idx],
                        rank_from_cal(grid_b, grid_b.select("cal"), cost_b, Pm, Rm))
    D = np.stack([pa[j][0] - pb[j][0] for j in range(len(rng_idx))])
    ok = ~np.isnan(D).any(0)
    D = D[:, ok]
    n = D.shape[1]
    boots = [float(D[:, rng.integers(0, n, n)].mean()) for _ in range(n_boot)]
    return {"range": which, "n_budgets": len(rng_idx), "n_eval": int(n),
            "n_eval_dropped_incomplete": int(np.sum(~ok)),
            "pricing": {"L_a": grid_a.L,
                        "L_fixed_a": (grid_a.L_fixed if L_fixed is None else L_fixed),
                        "L_b": grid_b.L,
                        "L_fixed_b": (grid_b.L_fixed if L_fixed_b is None else L_fixed_b)},
            "mean": float(D.mean()), "lo95": float(np.percentile(boots, 2.5)),
            "hi95": float(np.percentile(boots, 97.5)),
            "noninferiority_lo95_top3": float(np.percentile(
                [float(D[-3:][:, rng.integers(0, n, n)].mean()) for _ in range(n_boot)], 5))}
