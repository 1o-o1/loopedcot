"""Evaluate cell policies on paired prompts; report accuracy gains in percentage points and costs in layer-token passes."""
import numpy as np

from . import cells as C
from . import mechanism as mech
from . import policy as pol

BUDGET_FRACTIONS = (0.25, 0.5, 0.75, 1.0)
NI_MARGIN_PTS = 2.0


def _nanmean(x):
    return pol._nanmean(x)


# ---------------------------------------------------------------- the surface and the order
def surface(cells, cal_pos, n_labels=None, label_pos=None):
    """Return fitted accuracy surface and diagnostics using calibration read-outs and the first n_labels calibration labels."""
    cal_pos = np.asarray(cal_pos, dtype=int)
    if not len(cal_pos) or any(cells.split[n] != "cal" for n in cal_pos):
        raise ValueError("surface fitting requires calibration prompts only")
    if n_labels is not None and int(n_labels) <= 0:
        raise ValueError("n_labels must be positive")
    if label_pos is None:
        label_pos = cal_pos if n_labels is None else cal_pos[:int(n_labels)]
    if not len(label_pos) or any(cells.split[n] != "cal" for n in label_pos):
        raise ValueError("surface fitting requires calibration labels only")
    m = mech.mechanism(cells, cal_pos, np.asarray(label_pos, dtype=int))
    return mech.a_hat_matrix(m), m


def make_order(cells, cal_pos, cost, Pm, Rm, ranking="lookup", n_labels=None, boot_sel=None, label_sel=None):
    """Return a lookup/equation cell order and optional fitted surface from calibration positions and optional resampled positions."""
    if ranking == "lookup":
        order, _ = pol.rank_lookup(cells, cal_pos, cost, Pm, Rm, boot_sel=boot_sel)
        return order, None
    if ranking == "equation":
        ids = np.asarray(cal_pos)[boot_sel] if boot_sel is not None else np.asarray(cal_pos)
        lab = ids if n_labels is None else np.asarray(cal_pos)[:int(n_labels)]
        if label_sel is not None:
            lab = np.asarray(cal_pos)[label_sel]
        A_hat, m = surface(cells, ids, label_pos=lab)
        order, _ = pol.rank_equation(cells, A_hat, cost, Pm, Rm)
        return order, (A_hat, m)
    if ranking in pol.AVG_RANKINGS:
        raise ValueError("%r is an average-budget policy and not a cell order: it has no one "
                         "sequence of cells to walk, because the cell a prompt takes depends on "
                         "that prompt's own price. Use cell_scores() with "
                         "policy.avg_budget_vectors()" % ranking)
    raise ValueError("unknown ranking %r" % ranking)


def cell_scores(cells, cal_pos, ranking, cost, Pm, Rm, n_labels=None):
    """Return the (depth, cap) value the average-budget policy maximises: calibration accuracy for
    `lookup`, predicted accuracy for `equation`, both fractions.

    An `avg_` prefix is accepted, so an arm name passes straight through. A cell the ranking cannot
    score stays NaN, and the policy never picks one.
    """
    base = pol.AVG_BASE.get(ranking, ranking)
    if base == "lookup":
        _order, acc = pol.rank_lookup(cells, cal_pos, cost, Pm, Rm)
        return np.array([[acc[(k, T)] for T in cells.caps] for k in cells.ks], float)
    if base == "equation":
        return surface(cells, cal_pos, n_labels=n_labels)[0]
    raise ValueError("unknown ranking %r" % ranking)


def calibration_resamples(cal_pos, n_labels, n_draws, seed):
    """Return shared (read-out positions, label positions) bootstrap indices; units are prompts."""
    cal = np.asarray(cal_pos, dtype=int)
    nl = len(cal) if n_labels is None else min(int(n_labels), len(cal))
    if len(cal) == 0 or nl <= 0:
        raise ValueError("calibration requires at least one labelled prompt")
    rng = np.random.default_rng(seed)
    draws = []
    for _ in range(n_draws):
        gs = rng.integers(0, len(cal), len(cal))
        ls = gs if nl == len(cal) else rng.integers(0, nl, nl)
        draws.append((gs, ls))
    return draws


def gate_for(cells, cal_pos, n_labels=None, c_gate=pol.DEFAULT_C_GATE, n_draws=40, seed=7,
             resamples=None):
    """Return gate and fitted surface; margin SD uses supplied prompt resamples in accuracy units."""
    A_hat, m = surface(cells, cal_pos, n_labels=n_labels)
    cal = np.asarray(cal_pos, dtype=int)
    plan = calibration_resamples(cal, n_labels, n_draws, seed) if resamples is None else resamples
    if not plan:
        raise ValueError("the gate requires calibration resamples")
    draws = [surface(cells, cal[gs], label_pos=cal[ls])[0] for gs, ls in plan]
    sd = pol.margin_sd(np.stack(draws))
    return pol.Gate(A_hat, sd, c_gate), m


# ---------------------------------------------------------------- split calibration
def split_calibration(cells, cal_pos, n_select=pol.DEFAULT_N_SELECT,
                      n_verify=pol.DEFAULT_N_VERIFY):
    """Return (selection positions, verification positions, sizes) from the calibration split.

    The calibration questions are taken IN ID ORDER: the first `n_select` ids fit the ranking and
    the multiplier, the next `n_verify` measure the margin of what was fitted. Id order rather than
    a seeded shuffle, so the same question is in the same half whatever else the run changes, and
    two checkpoints of one task verify on the same questions.

    Nothing about the verification half may touch the fit. That is the whole repair: the old gate
    chose the best of many cells on one set of labels and then measured that cell's margin over the
    default cell on the SAME labels, so it read the maximum's upward bias as if it were the
    policy's advantage.

    A calibration split shorter than `n_select + n_verify` is used entire, keeping the requested
    proportion, and the returned sizes say so with `truncated`. Two verification questions are the
    minimum: below that the margin has no measurable spread.
    """
    cal = np.asarray(cal_pos, dtype=int)
    ids = np.asarray([cells.idx[int(n)] for n in cal])
    order = cal[np.argsort(ids, kind="stable")]
    ns, nv = int(n_select), int(n_verify)
    if ns < 1 or nv < 2:
        raise ValueError("the split needs at least 1 selection and 2 verification questions, "
                         "got %d and %d" % (ns, nv))
    if len(order) < 3:
        raise ValueError("a calibration split of %d cannot be halved into a selection and a "
                         "verification half" % len(order))
    want = ns + nv
    truncated = len(order) < want
    if truncated:
        ns = min(max(1, int(round(len(order) * ns / float(want)))), len(order) - 2)
        nv = len(order) - ns
    sel, ver = order[:ns], order[ns:ns + nv]
    sizes = {"n_selection": int(len(sel)), "n_verification": int(len(ver)),
             "n_calibration": int(len(order)), "requested": [int(n_select), int(n_verify)],
             "truncated": bool(truncated)}
    return sel, ver, sizes


def gate_and_fit(cells, cal_pos, n_labels, c_gate, n_draws, seed,
                 gate_mode=pol.DEFAULT_GATE_MODE, resamples=None,
                 n_select=pol.DEFAULT_N_SELECT, n_verify=pol.DEFAULT_N_VERIFY):
    """Return (gate, the positions the ranking may be fitted on, the split sizes).

    `split`  the order is fitted on the selection half and the gate's surface and margin SD come
             from the verification half alone, so the cells the order chose are scored on labels
             that had no part in choosing them.
    `whole`  the old rule, kept for comparison: one set fits and measures.
    """
    if gate_mode not in pol.GATE_MODES:
        raise ValueError("unknown gate mode %r; expected one of %s"
                         % (gate_mode, ", ".join(pol.GATE_MODES)))
    cal = np.asarray(cal_pos, dtype=int)
    if gate_mode == "whole":
        gate, _m = gate_for(cells, cal, n_labels=n_labels, c_gate=c_gate, n_draws=n_draws,
                            seed=seed, resamples=resamples)
        return gate, cal, {"n_selection": int(len(cal)), "n_verification": 0,
                           "n_calibration": int(len(cal)), "requested": None, "truncated": False}
    sel, ver, sizes = split_calibration(cells, cal, n_select, n_verify)
    gate, _m = gate_for(cells, ver, n_labels=n_labels, c_gate=c_gate, n_draws=n_draws, seed=seed)
    return gate, sel, sizes


def _budget_mean(values):
    """Return the equal-weight mean of budget-wise prompt means, retaining missing prompt slots."""
    return _nanmean([_nanmean(row) for row in values])


# ---------------------------------------------------------------- gain over normal
def gain_over_normal(cells, ranking="lookup", n_labels=None, c_gate=0.0, promptfree=False,
                     n_budgets=pol.N_BUDGETS, n_boot=2000, n_cal_draws=100, seed=7,
                     min_normal_feasible=0.9, gate_draws=40, accounting="cap",
                     gate_mode=pol.DEFAULT_GATE_MODE, one_se=False,
                     n_select=pol.DEFAULT_N_SELECT, n_verify=pol.DEFAULT_N_VERIFY):
    """Return gains in percentage points over the budgets at which normal operation is
    affordable for at least `min_normal_feasible` of the prompts.

    `gain_mean_pts` is the headline: the equal-weight mean over those budgets of the mean paired
    difference (policy minus normal) over prompts. `pooled_gain_mean_pts` averages that difference
    over every feasible (prompt, budget) pair instead, so budgets with more affordable prompts
    weigh more; it is reported alongside because it is the older convention.

    `accounting` prices the policy, normal operation AND the budget grid the same way, so the
    comparison stays internal to one accounting (see policy.Cost).
    """
    rng = np.random.default_rng(seed)
    cost = pol.cost_of(cells, promptfree, accounting=accounting)
    ev, cal = cells.select("eval"), cells.select("cal")
    if len(ev) == 0 or len(cal) == 0:
        raise ValueError("%s/%s: need both splits (eval %d, cal %d)"
                         % (cells.name, cells.task, len(ev), len(cal)))
    Pm, Rm = pol.median_point(cells, ev)
    cmat = pol.cost_matrix(cells, cost, Pm, Rm)
    Xs = pol.budget_grid(cmat, n_budgets)
    c = pol.gate_constant(c_gate, one_se)
    gate, fit_pos, gate_sizes = None, cal, None
    if c_gate and c_gate > 0 and gate_mode == "split":
        # Under a split the order is fitted on the selection half and the gate reads the other
        # half, so the two cannot share one resample plan: the selection draws below resample the
        # selection half, the gate its own.
        gate, fit_pos, gate_sizes = gate_and_fit(cells, cal, n_labels, c, gate_draws, seed,
                                                 gate_mode="split", n_select=n_select,
                                                 n_verify=n_verify)
    resamples = calibration_resamples(fit_pos, n_labels, n_cal_draws, seed)
    if c_gate and c_gate > 0 and gate is None:
        gate, fit_pos, gate_sizes = gate_and_fit(cells, cal, n_labels, c, gate_draws, seed,
                                                 gate_mode=gate_mode, resamples=resamples)
    order, extra = make_order(cells, fit_pos, cost, Pm, Rm, ranking, n_labels)
    P, reverted = pol.policy_vectors(cells, ev, cost, Xs, order, gate=gate)
    bstar, blow, rmeta = pol.budget_ranges(cells, cost, Xs, Pm, Rm)

    gains, per_budget = [], []
    for xi, X in enumerate(Xs):
        pv, nv = P[xi]
        feas = ~np.isnan(nv)
        rec = {"X": float(X), "normal_feasible_frac": float(feas.mean()),
               "policy_acc": _nanmean(pv), "normal_acc": _nanmean(nv),
               "gate_reverted_frac": reverted[xi],
               "in_Bstar": xi in bstar, "in_Blow": xi in blow}
        if feas.mean() >= min_normal_feasible and (~np.isnan(pv) & feas).sum() > 0:
            d = pv - nv                       # NaN wherever either arm is infeasible, kept IN PLACE
            rec["gain"] = _nanmean(d)
            gains.append(d)
        per_budget.append(rec)

    out = {"grid": cells.name, "task": cells.task, "ranking": ranking, "n_labels": n_labels,
           "c_gate": float(c_gate), "promptfree": bool(promptfree), "accounting": accounting,
           "n_eval": int(len(ev)), "n_cal": int(len(cal)),
           "median_prompt_tokens": Pm, "median_reserve": Rm,
           "budgets": [float(x) for x in Xs], "per_budget": per_budget,
           "Bstar": bstar, "Blow": blow, "range_meta": rmeta,
           "gate_mode": gate_mode, "one_se": bool(one_se), "gate_c": float(c),
           "gate_sizes": gate_sizes,
           "order_top5": [list(cc) for cc in order[:5]]}
    if extra is not None:
        out["mechanism"] = extra[1]
    if not gains:
        out["gain_mean_pts"] = None
        out["gain_ci95_pts"] = None
        out["pooled_gain_mean_pts"] = None
        out["pooled_gain_ci95_pts"] = None
        return out
    G = np.stack(gains)
    nq = G.shape[1]
    per_b = np.array([_nanmean(G[i]) for i in range(G.shape[0])])
    pooled_boots, budget_boots = [], []
    for _ in range(n_boot):
        cols = rng.integers(0, nq, nq)        # ONE resample of the questions, shared by every budget
        pooled = _nanmean(G[:, cols])
        equal = _budget_mean(G[:, cols])
        if not np.isnan(pooled):
            pooled_boots.append(pooled)
        if not np.isnan(equal):
            budget_boots.append(equal)
    out.update({"gain_mean_pts": 100 * _budget_mean(G),
                "gain_aggregation": "equal weight per budget",
                "gain_ci95_pts": ([100 * float(np.percentile(budget_boots, 2.5)),
                                   100 * float(np.percentile(budget_boots, 97.5))]
                                  if budget_boots else None),
                "pooled_gain_mean_pts": 100 * _nanmean(G),
                "pooled_gain_aggregation": "every feasible prompt-budget pair",
                "pooled_gain_ci95_pts": ([100 * float(np.percentile(pooled_boots, 2.5)),
                                          100 * float(np.percentile(pooled_boots, 97.5))]
                                         if pooled_boots else None),
                "gain_worst_budget_pts": 100 * float(np.nanmin(per_b)),
                "gain_per_budget_pts": [100 * float(v) for v in per_b],
                "n_budgets_with_normal": int(G.shape[0]), "n_eval_in_gain": int(nq)})

    draws = []
    fit = np.asarray(fit_pos, dtype=int)
    for sel, label_sel in resamples:
        od, _ = make_order(cells, fit, cost, Pm, Rm, ranking, n_labels,
                           boot_sel=sel, label_sel=label_sel)
        draw_gate = None
        if gate is not None:
            # The gate surface stays the one the VERIFICATION half fitted (or the whole set under
            # `whole`); only the order is redrawn, which is what this bootstrap measures.
            draw_gate = (pol.Gate(gate.A_hat, gate.sd, c) if gate_mode == "split" else
                         pol.Gate(surface(cells, fit[sel], label_pos=fit[label_sel])[0],
                                  gate.sd, c))
        Pd, _rev = pol.policy_vectors(cells, ev, cost, Xs, od, gate=draw_gate)
        gs = []
        for xi in range(len(Xs)):
            pv, nv = Pd[xi]
            feas = ~np.isnan(nv)
            if feas.mean() >= min_normal_feasible and (~np.isnan(pv) & feas).sum() > 0:
                gs.append(float(np.nanmean(pv[feas] - nv[feas])))
        if gs:
            draws.append(float(np.mean(gs)))
    if draws:
        out.update({"gain_cal_draw_mean_pts": 100 * float(np.mean(draws)),
                    "gain_cal_draw_sd_pts": 100 * float(np.std(draws)),
                    "gain_cal_draw_frac_positive": float(np.mean([g > 0 for g in draws]))})
    return out


# ---------------------------------------------------------------- contrasts
def assert_paired(cells_a, cells_b):
    """Assert identical ordered evaluation prompt IDs for two grids and return True; pairing uses prompt positions."""
    ia, ib = cells_a.ids("eval"), cells_b.ids("eval")
    if ia != ib:
        only_a, only_b = sorted(set(ia) - set(ib)), sorted(set(ib) - set(ia))
        raise AssertionError(
            "%s and %s are not paired: %d vs %d evaluation questions, %d only in %s, %d only in %s"
            % (cells_a.name, cells_b.name, len(ia), len(ib), len(only_a), cells_a.name,
               len(only_b), cells_b.name))
    return True


def contrast(cells_a, cells_b, which="Bstar", ranking="lookup", n_labels=None, c_gate=0.0,
             promptfree=False, n_budgets=pol.N_BUDGETS, n_boot=2000, seed=7, gate_draws=40,
             accounting="cap", gate_mode=pol.DEFAULT_GATE_MODE, one_se=False,
             n_select=pol.DEFAULT_N_SELECT, n_verify=pol.DEFAULT_N_VERIFY):
    """Return the paired difference cells_a minus cells_b in percentage points.

    `cells_b` is the REFERENCE: its median prompt, its own cost function and its cost matrix fix
    the budget grid and the two budget ranges, so both checkpoints are read at one fixed set of
    budgets whichever of them is the cheaper to run. Each checkpoint still prices its own prompts
    with its own layer counts. Complete case: a prompt missing an accuracy at any budget of the
    range leaves every budget, so the mean is over one fixed set of prompts.
    """
    assert_paired(cells_a, cells_b)
    rng = np.random.default_rng(seed)
    ca = pol.cost_of(cells_a, promptfree, accounting=accounting)
    cb = pol.cost_of(cells_b, promptfree, accounting=accounting)
    ev_a, cal_a = cells_a.select("eval"), cells_a.select("cal")
    ev_b, cal_b = cells_b.select("eval"), cells_b.select("cal")
    Pm, Rm = pol.median_point(cells_b, ev_b)
    Xs = pol.budget_grid(pol.cost_matrix(cells_b, cb, Pm, Rm), n_budgets)
    bstar, blow, _m = pol.budget_ranges(cells_b, cb, Xs, Pm, Rm)
    rng_idx = bstar if which == "Bstar" else blow
    if not rng_idx:
        return {"range": which, "empty": True, "reference": cells_b.name}
    Xr = [Xs[i] for i in rng_idx]
    ga = gb = None
    fa, fb = cal_a, cal_b
    if c_gate and c_gate > 0:
        c = pol.gate_constant(c_gate, one_se)
        ga, fa, _sa = gate_and_fit(cells_a, cal_a, n_labels, c, gate_draws, seed, gate_mode,
                                   n_select=n_select, n_verify=n_verify)
        gb, fb, _sb = gate_and_fit(cells_b, cal_b, n_labels, c, gate_draws, seed, gate_mode,
                                   n_select=n_select, n_verify=n_verify)
    oa, _ = make_order(cells_a, fa, ca, Pm, Rm, ranking, n_labels)
    ob, _ = make_order(cells_b, fb, cb, Pm, Rm, ranking, n_labels)
    Pa, _ra = pol.policy_vectors(cells_a, ev_a, ca, Xr, oa, gate=ga)
    Pb, _rb = pol.policy_vectors(cells_b, ev_b, cb, Xr, ob, gate=gb)
    D = np.stack([Pa[j][0] - Pb[j][0] for j in range(len(rng_idx))])
    ok = ~np.isnan(D).any(0)
    D = D[:, ok]
    n = D.shape[1]
    if n == 0:
        return {"range": which, "empty": True, "n_eval": 0, "reference": cells_b.name,
                "budgets": [float(x) for x in Xr],
                "n_eval_dropped_incomplete": int(np.sum(~ok))}
    boots = [float(D[:, rng.integers(0, n, n)].mean()) for _ in range(n_boot)]
    return {"range": which, "a": cells_a.name, "b": cells_b.name, "ranking": ranking,
            "reference": cells_b.name, "accounting": accounting,
            "budgets": [float(x) for x in Xr],
            "n_budgets": len(rng_idx), "n_eval": int(n),
            "n_eval_dropped_incomplete": int(np.sum(~ok)),
            "mean_pts": 100 * float(D.mean()),
            "lo95_pts": 100 * float(np.percentile(boots, 2.5)),
            "hi95_pts": 100 * float(np.percentile(boots, 97.5))}


def noninferiority(cells_a, cells_b, ranking="lookup", n_labels=None, c_gate=0.0,
                   promptfree=False, n_budgets=pol.N_BUDGETS, n_boot=2000, seed=7,
                   margin_pts=NI_MARGIN_PTS, gate_draws=40, accounting="cap",
                   gate_mode=pol.DEFAULT_GATE_MODE, one_se=False,
                   n_select=pol.DEFAULT_N_SELECT, n_verify=pol.DEFAULT_N_VERIFY):
    """Return paired top-three-budget differences and one-sided 95% bound in percentage points, with power at zero true effect."""
    assert_paired(cells_a, cells_b)
    rng = np.random.default_rng(seed)
    ca = pol.cost_of(cells_a, promptfree, accounting=accounting)
    cb = pol.cost_of(cells_b, promptfree, accounting=accounting)
    ev_a, cal_a = cells_a.select("eval"), cells_a.select("cal")
    ev_b, cal_b = cells_b.select("eval"), cells_b.select("cal")
    Pm, Rm = pol.median_point(cells_b, ev_b)
    Xs = pol.budget_grid(pol.cost_matrix(cells_b, cb, Pm, Rm), n_budgets)
    bstar, _bl, _m = pol.budget_ranges(cells_b, cb, Xs, Pm, Rm)
    if not bstar:
        return {"empty": True}
    top = bstar[-3:]
    Xr = [Xs[i] for i in top]
    ga = gb = None
    fa, fb = cal_a, cal_b
    if c_gate and c_gate > 0:
        c = pol.gate_constant(c_gate, one_se)
        ga, fa, _sa = gate_and_fit(cells_a, cal_a, n_labels, c, gate_draws, seed, gate_mode,
                                   n_select=n_select, n_verify=n_verify)
        gb, fb, _sb = gate_and_fit(cells_b, cal_b, n_labels, c, gate_draws, seed, gate_mode,
                                   n_select=n_select, n_verify=n_verify)
    oa, _ = make_order(cells_a, fa, ca, Pm, Rm, ranking, n_labels)
    ob, _ = make_order(cells_b, fb, cb, Pm, Rm, ranking, n_labels)
    Pa, _ = pol.policy_vectors(cells_a, ev_a, ca, Xr, oa, gate=ga)
    Pb, _ = pol.policy_vectors(cells_b, ev_b, cb, Xr, ob, gate=gb)
    D = np.stack([Pa[j][0] - Pb[j][0] for j in range(len(top))])
    D = D[:, ~np.isnan(D).any(0)]
    n = D.shape[1]
    if n < 2:
        return {"empty": True}
    boots = np.array([D[:, rng.integers(0, n, n)].mean() for _ in range(n_boot)])
    lo95 = float(np.percentile(boots, 5))
    m = float(D.mean())
    per_prompt = D.mean(0)
    se = float(per_prompt.std(ddof=1) / np.sqrt(n))
    from math import erf, sqrt
    power = (1.0 if se == 0 else
             float(0.5 * (1 + erf(((margin_pts / 100.0) / se - 1.6449) / sqrt(2)))))
    verdict = ("non-inferior" if 100 * lo95 > -margin_pts else
               ("inconclusive" if 100 * m > -margin_pts else "inferior"))
    return {"mean_pts": 100 * m, "lo95_pts": 100 * lo95, "margin_pts": -margin_pts,
            "verdict": verdict, "accounting": accounting, "n_budgets": len(top), "n_eval": int(n),
            "se_pts": 100 * se, "power_at_zero_effect": power}


# ---------------------------------------------------------------- default cost
def default_cost(cells, promptfree=False, k=None, split="eval"):
    """Return mean realised layer-token cost at the selected depth and natural stop, counting capped observations at the horizon and reporting their share."""
    ks = list(cells.ks)
    kk = k if (k is not None and k in ks) else ks[-1]
    ki = ks.index(kk)
    sel = cells.select(split)
    field = cells.passes_pf if promptfree else cells.passes
    vals, n_hor = [], 0
    for n in sel:
        nstop, ncut = cells.nstop[ki, :, n], cells.ncut[ki, :, n]
        ok = [j for j in range(len(cells.caps))
              if not (np.isnan(nstop[j]) or np.isnan(ncut[j])) and ncut[j] >= nstop[j] - 1e-9]
        if ok:
            j = min(ok, key=lambda j: cells.caps[j])       # the cheapest UNCAPPED realisation
        else:
            j = len(cells.caps) - 1                        # the horizon: counted, not skipped
            n_hor += 1
        v = field[ki, j, n]
        if not np.isnan(v):
            vals.append(float(v))
    return {"k": int(kk), "n": len(vals), "mean": (float(np.mean(vals)) if vals else None),
            "promptfree": bool(promptfree), "n_at_horizon": n_hor,
            "horizon_share": (n_hor / max(1, len(sel)))}


def default_accuracy(cells, k=None, split="eval"):
    """Return prompt-level accuracy fractions at natural stop for the selected depth, using the horizon when an uncapped observation is unavailable."""
    ks = list(cells.ks)
    kk = k if (k is not None and k in ks) else ks[-1]
    ki = ks.index(kk)
    sel = cells.select(split)
    out = []
    for n in sel:
        nstop, ncut = cells.nstop[ki, :, n], cells.ncut[ki, :, n]
        ok = [j for j in range(len(cells.caps))
              if not (np.isnan(nstop[j]) or np.isnan(ncut[j])) and ncut[j] >= nstop[j] - 1e-9]
        j = min(ok, key=lambda j: cells.caps[j]) if ok else len(cells.caps) - 1
        out.append(cells.acc[ki, j, n])
    return np.array(out, float)


# ---------------------------------------------------------------- Table 1
def default_cell(cells):
    """Return the (depth, cap) cell that IS the default operating point: the deepest depth at the
    cap standing for natural stop, which is the cell an allocator would have to buy to match it."""
    return cells.ks[-1], cells.caps[C.natural_stop_cap_index(cells)]


def _gate_fields(gate_mode, c, sizes):
    """Return the gate columns every gated row carries: the mode, the bar, and both half sizes."""
    sizes = sizes or {"n_selection": 0, "n_verification": 0, "truncated": False}
    return {"gate_mode": gate_mode, "gate_c": float(c),
            "gate_n_selection": int(sizes.get("n_selection", 0)),
            "gate_n_verification": int(sizes.get("n_verification", 0)),
            "gate_n_calibration": int(sizes.get("n_calibration", 0)),
            "gate_split_truncated": bool(sizes.get("truncated", False))}


def _paired_vs_default(arm, ref, rng, n_boot):
    """Return the paired arm-minus-reference accuracy difference in percentage points with a
    bootstrap interval over prompts; prompts either side cannot afford drop out of the pair.

    The reference is the unbudgeted `default` accuracy for most rows, and normal operation at the
    same budget (`default_at_budget`) for the average-budget rows, which are read against both.
    """
    d = np.asarray(arm, float) - np.asarray(ref, float)
    v = d[~np.isnan(d)]
    if len(v) < 2:
        return {"mean_pts": None, "lo95_pts": None, "hi95_pts": None, "n": int(len(v))}
    boots = [float(v[rng.integers(0, len(v), len(v))].mean()) for _ in range(n_boot)]
    return {"mean_pts": 100 * float(v.mean()),
            "lo95_pts": 100 * float(np.percentile(boots, 2.5)),
            "hi95_pts": 100 * float(np.percentile(boots, 97.5)), "n": int(len(v))}


def table1(cells, promptfree=False, fractions=BUDGET_FRACTIONS, c_gate=pol.DEFAULT_C_GATE,
           n_labels_grid=(30, 100), seed=7, gate_draws=40, accounting="cap", n_boot=400,
           avg_budget=False, gate_mode=pol.DEFAULT_GATE_MODE, one_se=False,
           n_select=pol.DEFAULT_N_SELECT, n_verify=pol.DEFAULT_N_VERIFY):
    """Return each arm's accuracy in percentage points at budgets set to `fractions` of the default
    cost (the mean realised layer-token cost of the deepest depth run to its natural stop).

    The budgets are the same under every accounting, because the default cost is a measured
    statistic and not a price. What changes with `accounting` is what each arm is CHARGED, so the
    three tables answer three questions with one budget column (see policy.Cost and the README).

    The `default` row is the unbudgeted run itself, so it costs the whole default cost and cannot
    be bought at a fraction below 1.0; its `feasible` flags say so and its accuracy there is NaN,
    rather than repeating the unbudgeted number as if it had been affordable. The `default_cell`
    row is that same operating point priced per prompt as a cell of the grid: under `cap` it is
    charged its whole cap and is unaffordable at 1.0x, under `expected` it is charged the mean
    realised length and becomes a cell the allocator can actually choose.

    `avg_budget` adds the two average-budget arms, which hold the MEAN price over prompts at or
    below the budget instead of capping every prompt. Under that constraint the default cell for
    every prompt is itself a feasible policy, so those rows are the like-for-like comparison with
    the `default` row; each carries its realised mean price beside the budget it was fitted to.
    They need a decision-time price and are therefore skipped under `realised` accounting.

    `gate_mode` decides where the two gated arms measure their margin. Under `split` the
    calibration questions are cut in id order into `n_select` that fit the ranking and the
    multiplier and `n_verify` that measure the margin of what was fitted; under `whole` one set
    does both, which is the rule that let the winner curse through. `one_se` raises the bar from
    c_gate standard errors to one whole standard error.
    """
    rng = np.random.default_rng(seed)
    cost = pol.cost_of(cells, promptfree, accounting=accounting)
    ev, cal = cells.select("eval"), cells.select("cal")
    Pm, Rm = pol.median_point(cells, ev)
    dc = default_cost(cells, promptfree)
    if dc["mean"] is None:
        return {"task": cells.task, "grid": cells.name, "empty": True}
    Xs = [f * dc["mean"] for f in fractions]
    dacc = default_accuracy(cells)

    arms = [("lookup", dict(ranking="lookup")),
            ("equation", dict(ranking="equation")),
            ("gated_equation", dict(ranking="equation", gate=True))]
    for nl in n_labels_grid:
        arms.insert(-1, ("equation_n%d" % nl, dict(ranking="equation", n_labels=nl)))

    c = pol.gate_constant(c_gate, one_se)
    gate, gate_fit, gate_sizes = None, cal, None
    if c_gate and c_gate > 0:
        gate, gate_fit, gate_sizes = gate_and_fit(cells, cal, None, c, gate_draws, seed,
                                                  gate_mode=gate_mode, n_select=n_select,
                                                  n_verify=n_verify)

    default_acc_pts = 100 * float(np.nanmean(dacc))
    default_feasible = [bool(pol.affordable(dc["mean"], X)) for X in Xs]
    rows = {"default": {"note": "max depth, natural stop, uncapped",
                        "acc_pts": [default_acc_pts if f else float("nan")
                                    for f in default_feasible],
                        "feasible": default_feasible,
                        "unbudgeted_acc_pts": default_acc_pts,
                        "cost_layer_passes": [dc["mean"]] * len(fractions)}}

    dk, dT = default_cell(cells)
    dprice = np.array([cost(dk, dT, cells.ptok[n], cells.reserve[n], n) for n in ev], float)
    dfeas = [np.array([pol.affordable(v, X) for v in dprice]) for X in Xs]
    rows["default_cell"] = {
        "note": "the default operating point priced as a cell of the grid: depth %d at cap %d, "
                "per prompt, under %s accounting" % (dk, dT, accounting),
        "cell": [int(dk), int(dT)],
        "acc_pts": [100 * _nanmean(np.where(f, dacc, np.nan)) for f in dfeas],
        "feasible_frac": [float(f.mean()) for f in dfeas],
        "median_price_layer_passes": float(np.median(dprice)),
        "mean_price_layer_passes": float(np.mean(dprice)),
        # A hard per-prompt cap and an average budget are two different questions. The flag below
        # answers the second one: whether the default operating point fits the budget ON AVERAGE
        # over the evaluation prompts, which is how the default cost itself was measured.
        "affordable_on_average": [bool(pol.affordable(float(np.mean(dprice)), X)) for X in Xs]}

    normal_done, normal_vecs = False, None
    for name, spec in arms:
        gated = bool(spec.get("gate")) and gate is not None
        # A gated arm is fitted on the SELECTION half only, so the cells its order chose are
        # scored by the gate on labels that had no part in choosing them.
        fit_pos = gate_fit if gated else cal
        order, _ = make_order(cells, fit_pos, cost, Pm, Rm, spec["ranking"], spec.get("n_labels"))
        g = gate if gated else None
        P, rev = pol.policy_vectors(cells, ev, cost, Xs, order, gate=g)
        rows[name] = {"acc_pts": [100 * _nanmean(P[j][0]) for j in range(len(Xs))],
                      "feasible_frac": [float(np.mean(~np.isnan(P[j][0]))) for j in range(len(Xs))],
                      "gate_reverted_frac": list(rev),
                      "vs_default": [_paired_vs_default(P[j][0], dacc, rng, n_boot)
                                     for j in range(len(Xs))]}
        if gated:
            rows[name].update(_gate_fields(gate_mode, c, gate_sizes))
        if not normal_done:
            normal_vecs = [P[j][1] for j in range(len(Xs))]
            rows["default_at_budget"] = {
                "note": "normal operation: k_max at its largest affordable cap",
                "acc_pts": [100 * _nanmean(P[j][1]) for j in range(len(Xs))],
                "feasible_frac": [float(np.mean(~np.isnan(P[j][1]))) for j in range(len(Xs))],
                "vs_default": [_paired_vs_default(P[j][1], dacc, rng, n_boot)
                               for j in range(len(Xs))]}
            normal_done = True

    avg_on = bool(avg_budget) and accounting != "realised"
    for name in (pol.AVG_RANKINGS if avg_on else ()):
        score = cell_scores(cells, cal, name, cost, Pm, Rm)
        if name == pol.AVG_GATED:
            V = avg_gated_vectors(cells, ev, cal, cost, Xs, score, (dk, dT), c_gate=c_gate,
                                  n_draws=gate_draws, seed=seed, gate_mode=gate_mode,
                                  one_se=one_se, n_select=n_select, n_verify=n_verify)
        else:
            V = pol.avg_budget_vectors(cells, ev, cal, cost, Xs, score)
        rows[name] = {
            "note": "average budget: every prompt takes the cell maximising score - lambda * "
                    "price, lambda fitted on the calibration prompts so that THEIR mean price is "
                    "at most X, then applied unchanged; no per-prompt cap",
            "acc_pts": [100 * _nanmean(v["acc"]) for v in V],
            "lambda": [v["lambda"] for v in V],
            "mean_price_layer_passes": [v["mean_price"] for v in V],
            "cal_mean_price_layer_passes": [v["cal_mean_price"] for v in V],
            "mean_price_over_X_pct": [v["mean_price_over_X_pct"] for v in V],
            "over_budget": [v["over_budget"] for v in V],
            "constraint_met_on_calibration": [v["constraint_met_on_calibration"] for v in V],
            "cells_used": [v["cells_used"] for v in V],
            # Underspend is the efficiency claim, not a defect: where the multiplier reaches 0 the
            # budget never binds, so the arm bought its best cell outright and the row is the same
            # accuracy for less compute.
            "cost_saving_pct": [100.0 * (1.0 - v["mean_price"] / v["X"]) for v in V],
            "pct_of_default_cost": [100.0 * v["mean_price"] / dc["mean"] for v in V],
            "gate_reverted": [bool(v.get("gate_reverted", False)) for v in V],
            "gate_margin_pts": [v.get("gate_margin_pts") for v in V],
            "gate_sd_pts": [v.get("gate_sd_pts") for v in V],
            "gate_draw_frac_positive": [v.get("gate_draw_frac_positive") for v in V],
            # gain over normal is not defined for an average budget: normal operation is a
            # per-prompt cap policy and the two are not priced the same way. The paired
            # differences below are what stands in its place.
            "vs_default": [_paired_vs_default(V[j]["acc"], dacc, rng, n_boot)
                           for j in range(len(Xs))],
            "vs_default_at_budget": [_paired_vs_default(V[j]["acc"], normal_vecs[j], rng, n_boot)
                                     for j in range(len(Xs))]}
        if name == pol.AVG_GATED:
            rows[name].update(_gate_fields(gate_mode, c,
                                           V[0].get("gate_sizes") if V else gate_sizes))
    return {"task": cells.task, "grid": cells.name, "promptfree": bool(promptfree),
            "accounting": accounting, "fractions": list(fractions), "avg_budget": avg_on,
            "budgets": [float(x) for x in Xs],
            "default_cost": dc, "n_eval": int(len(ev)), "c_gate": float(c_gate),
            "gate_mode": gate_mode, "one_se": bool(one_se), "gate_c": float(c),
            "gate_sizes": gate_sizes, "rows": rows}


# ---------------------------------------------------------------- the average budget, gated
def cell_scores_boot(cells, cal_pos, cost, Pm, Rm, boot_sel):
    """Return the lookup score surface on one bootstrap resample of the given calibration prompts."""
    _order, acc = pol.rank_lookup(cells, cal_pos, cost, Pm, Rm, boot_sel=boot_sel)
    return np.array([[acc[(k, T)] for T in cells.caps] for k in cells.ks], float)


def _revert_to_default(rec, cells, ev, cost, default_kt, ki, bi, X):
    """Overwrite one record with the fallback: the default cell run for every evaluation prompt."""
    price = np.array([cost(default_kt[0], default_kt[1], cells.ptok[n], cells.reserve[n], n)
                      for n in ev], float)
    mean_price = float(price.mean())
    rec.update({"acc": cells.acc[ki, bi, ev], "price": price, "mean_price": mean_price,
                "mean_price_over_X_pct": 100.0 * (mean_price / float(X) - 1.0),
                "over_budget": bool(mean_price > float(X) * (1.0 + pol.AVG_TOL)),
                "cells_used": {"k%d_T%d" % default_kt: int(len(ev))},
                "gate_reverted": True})


def avg_gated_vectors(cells, ev_pos, cal_pos, cost, Xs, score, default_kt,
                      c_gate=pol.DEFAULT_C_GATE, n_draws=40, seed=7, n_labels=None,
                      gate_mode=pol.DEFAULT_GATE_MODE, one_se=False,
                      n_select=pol.DEFAULT_N_SELECT, n_verify=pol.DEFAULT_N_VERIFY,
                      gate_boot=pol.GATE_BOOT):
    """Return the records of `avg_gated_lookup`: the average-budget lookup policy, kept only where
    it is measured to beat running the DEFAULT CELL for every prompt by more than its own noise.

    Under `split` (the default) the calibration questions are cut in id order into a SELECTION half
    and a VERIFICATION half. The ranking and the multiplier are fitted on the selection half alone.
    The margin is then the paired accuracy difference, over the VERIFICATION questions, between the
    cells that policy picks for them and the default cell, and its SD is a paired bootstrap over
    those same questions. Neither number can be inflated by the choice of cell, because the labels
    that chose the cell are in the other half.

    Under `whole` the old rule is restored for comparison: the policy is scored, and its margin
    measured, on all of the calibration questions in the ranking own score units, with the SD taken
    over calibration resamples that re-score and refit. That margin is the maximum of many noisy
    cells read on the data that maximised it, so it runs optimistic by roughly the noise spread
    times how many cells were in the running -- the winner curse this repair removes.

    `one_se` replaces c_gate with a whole standard error. The fallback exists only where the
    default cell fits the budget ON AVERAGE over the calibration prompts; below that there is
    nothing to revert to and the Lagrangian policy stands.
    """
    if gate_mode not in pol.GATE_MODES:
        raise ValueError("unknown gate mode %r; expected one of %s"
                         % (gate_mode, ", ".join(pol.GATE_MODES)))
    ev, cal = np.asarray(ev_pos, dtype=int), np.asarray(cal_pos, dtype=int)
    Pm, Rm = pol.median_point(cells, ev)
    ki = list(cells.ks).index(default_kt[0])
    bi = list(cells.caps).index(default_kt[1])
    c = pol.gate_constant(c_gate, one_se)
    cal_prices = pol.price_tensor(cells, cal, cost)
    on = bool(c_gate) and float(c_gate) > 0

    if gate_mode == "split":
        sel, ver, sizes = split_calibration(cells, cal, n_select, n_verify)
        S = cell_scores(cells, sel, pol.AVG_GATED, cost, Pm, Rm, n_labels=n_labels)
        sel_prices = pol.price_tensor(cells, sel, cost)
        ver_prices = pol.price_tensor(cells, ver, cost)
        ref = np.asarray(cells.acc[ki, bi, ver], float)
        # The multiplier is fitted on the selection half, so that is the half the arm is fitted
        # to; the evaluation mean price stays a measurement, as it is for the ungated arms.
        out = pol.avg_budget_vectors(cells, ev, sel, cost, Xs, S)
        plan = calibration_resamples(sel, n_labels, n_draws, seed) if on else []
        for j, X in enumerate(Xs):
            rec = out[j]
            rec.update({"gate_mode": "split", "gate_c": c, "gate_margin_pts": None,
                        "gate_sd_pts": None, "gate_reverted": False,
                        "gate_draw_frac_positive": None, "gate_sizes": sizes})
            if not on or not pol.affordable(float(cal_prices[ki, bi, :].mean()), X):
                continue
            a, b = pol.avg_picks(S, ver_prices, rec["lambda"])
            arm = np.asarray(cells.acc[a, b, ver], float)
            margin = _nanmean(arm - ref)
            sd = pol.paired_margin_sd(arm, ref, n_boot=gate_boot, seed=seed)
            # The selection half is bootstrapped in its turn: each draw refits the score and the
            # multiplier on a resample of it and remeasures the same verification margin, so the
            # share positive says how much of the verdict is the selection half own luck.
            pos = []
            for dsel, _lab in plan:
                Sd = cell_scores_boot(cells, sel, cost, Pm, Rm, dsel)
                lam_d, _sp, _met = pol.lambda_for_budget(Sd, sel_prices[:, :, dsel], X)
                ad, bd = pol.avg_picks(Sd, ver_prices, lam_d)
                pos.append(_nanmean(np.asarray(cells.acc[ad, bd, ver], float) - ref) > 0)
            rec["gate_margin_pts"], rec["gate_sd_pts"] = 100 * margin, 100 * sd
            rec["gate_draw_frac_positive"] = float(np.mean(pos)) if pos else None
            if pol.gate_passes(margin, sd, c):
                continue
            _revert_to_default(rec, cells, ev, cost, default_kt, ki, bi, X)
        return out

    S = np.asarray(score, float)
    sizes = {"n_selection": int(len(cal)), "n_verification": 0, "n_calibration": int(len(cal)),
             "requested": None, "truncated": False}
    out = pol.avg_budget_vectors(cells, ev, cal, cost, Xs, S)
    plan = calibration_resamples(cal, n_labels, n_draws, seed) if on else []
    draw_scores = [cell_scores_boot(cells, cal, cost, Pm, Rm, sel) for sel, _lab in plan]
    for j, X in enumerate(Xs):
        rec = out[j]
        rec.update({"gate_mode": "whole", "gate_c": c, "gate_margin_pts": None,
                    "gate_sd_pts": None, "gate_reverted": False,
                    "gate_draw_frac_positive": None, "gate_sizes": sizes})
        if not on or not pol.affordable(float(cal_prices[ki, bi, :].mean()), X):
            continue
        a, b = pol.avg_picks(S, cal_prices, rec["lambda"])
        margin = float(np.nanmean(S[a, b]) - S[ki, bi])
        draws = []
        for (sel, _lab), Sd in zip(plan, draw_scores):
            pd = cal_prices[:, :, sel]
            lam_d, _spend, _met = pol.lambda_for_budget(Sd, pd, X)
            ad, bd = pol.avg_picks(Sd, pd, lam_d)
            draws.append(float(np.nanmean(Sd[ad, bd]) - Sd[ki, bi]))
        sd = float(np.std(draws)) if draws else 0.0
        rec["gate_margin_pts"], rec["gate_sd_pts"] = 100 * margin, 100 * sd
        rec["gate_draw_frac_positive"] = (float(np.mean([d > 0 for d in draws]))
                                          if draws else None)
        if pol.gate_passes(margin, sd, c):
            continue
        _revert_to_default(rec, cells, ev, cost, default_kt, ki, bi, X)
    return out


# ---------------------------------------------------------------- the gate's constant
def gate_selection(cells_by_task, c_grid=(0.0, 0.5, 1.0, 1.5, 2.0), worst_floor_pts=-1.0,
                   ranking="equation", n_labels=None, n_boot=50, seed=7):
    """Return the gate coefficient maximizing calibration-held-out mean gain subject to a worst-budget floor, measured in percentage points."""
    from copy import copy
    per = {}
    for task, source in cells_by_task.items():
        cs = copy(source)
        cal = source.select("cal")
        if len(cal) < 2:
            raise ValueError("gate selection requires at least two calibration prompts")
        cs.split = np.full(len(source.idx), "unused", dtype=object)
        cs.split[cal[:len(cal) // 2]] = "cal"
        cs.split[cal[len(cal) // 2:]] = "eval"
        for c in c_grid:
            g = gain_over_normal(cs, ranking=ranking, n_labels=n_labels, c_gate=c,
                                 n_boot=n_boot, n_cal_draws=40, seed=seed)
            per[(task, c)] = (g["gain_mean_pts"], g["gain_worst_budget_pts"])
    tasks = sorted(cells_by_task)

    def best_over(sub):
        ok = [c for c in c_grid if min(per[(t, c)][1] for t in sub) >= worst_floor_pts]
        if not ok:
            return None
        return max(ok, key=lambda c: float(np.mean([per[(t, c)][0] for t in sub])))

    chosen = best_over(tasks)
    loo = {t: best_over([x for x in tasks if x != t]) for t in tasks}
    return {"c_grid": list(c_grid), "worst_floor_pts": worst_floor_pts,
            "chosen": chosen, "leave_one_out": loo,
            "stable": all(v == chosen for v in loo.values()),
            "mean_gain_pts": (float(np.mean([per[(t, chosen)][0] for t in tasks]))
                              if chosen is not None else None),
            "worst_loss_pts": (float(min(per[(t, chosen)][1] for t in tasks))
                               if chosen is not None else None),
            "per_task": {"%s|%s" % (t, c): {"mean_pts": per[(t, c)][0],
                                            "worst_pts": per[(t, c)][1]} for (t, c) in per}}


def _gate_lines(t1, name, r):
    """Return the gate note for each budget where the arm had a fallback to deviate from.

    At 1.0x the note carries the VERIFICATION margin and its SD beside the cost saving, so a reader
    can see what the deviation was measured to be worth and on how many held-out questions, rather
    than only that the gate opened.
    """
    mode = r.get("gate_mode", t1.get("gate_mode", "whole"))
    c = r.get("gate_c", t1.get("c_gate"))
    where = ("%d verification questions, the ids after the %d that fit, out of %d calibration"
             % (r.get("gate_n_verification", 0), r.get("gate_n_selection", 0),
                r.get("gate_n_calibration", 0))
             if mode == "split" else
             "all %d calibration questions, which both fit and measure"
             % r.get("gate_n_selection", 0))
    lines = []
    for j, f in enumerate(t1["fractions"]):
        m, sd = r["gate_margin_pts"][j], r["gate_sd_pts"][j]
        if m is None or sd is None:
            continue                       # no fallback at this budget: nothing to gate against
        verdict = ("reverted to the default cell for every question"
                   if r["gate_reverted"][j] else "deviated from the default cell")
        lines.append("- `%s` at %.2fx: %s. %s margin %+.1f points, sd %.1f, bar %.2f sd (%s); "
                     "cost saving %.1f%% of the budget, %.1f%% of the default cost."
                     % (name, f, verdict, "Verification" if mode == "split" else "Calibration",
                        m, sd, c, where, r["cost_saving_pct"][j], r["pct_of_default_cost"][j]))
    return lines


def table1_markdown(t1):
    if t1.get("empty"):
        return "# Table 1\n\n(no uncapped realisation in these cells; nothing to report)\n"
    order = ["default", "default_cell", "default_at_budget", "lookup", "equation"]
    order += [k for k in t1["rows"] if k.startswith("equation_n")]
    order += ["gated_equation"]
    order += [k for k in pol.AVG_RANKINGS if k in t1["rows"]]
    head = " | ".join("%.2f x default" % f for f in t1["fractions"])
    acc = t1.get("accounting", "cap")
    out = ["# Table 1 -- %s (%s), %s accounting" % (t1["task"], t1["grid"], acc), "",
           "Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max "
           "depth at its natural stop, uncapped: %.0f layer passes over %d questions "
           "(%.1f%% of them counted at the horizon). The budgets do not depend on the accounting; "
           "what each arm is CHARGED does."
           % (t1["default_cost"]["mean"], t1["default_cost"]["n"],
              100 * t1["default_cost"]["horizon_share"]), "",
           "| arm | %s |" % head, "|---|" + "---|" * len(t1["fractions"])]
    def cell(r, j):
        feasible = r.get("feasible")
        if feasible is not None and not feasible[j]:
            return "not feasible"      # the arm costs more than this budget; nothing is substituted
        v = r["acc_pts"][j]
        if v != v:                     # NaN: no cell of that arm is affordable at that budget
            return "n/a"
        f = r.get("feasible_frac")
        return "%.1f" % v if f is None or f[j] >= 0.999 else "%.1f (%.0f%%)" % (v, 100 * f[j])

    for name in order:
        r = t1["rows"].get(name)
        if not r:
            continue
        out.append("| %s | %s |"
                   % (name, " | ".join(cell(r, j) for j in range(len(t1["fractions"])))))
    dcell = t1["rows"].get("default_cell")
    if dcell:
        avg = ", ".join("%.2fx %s" % (f, "yes" if ok else "no")
                        for f, ok in zip(t1["fractions"], dcell["affordable_on_average"]))
        out += ["", "`default_cell` is the default operating point (depth %d at cap %d) priced per "
                "prompt under %s accounting: the share in brackets is how often the allocator "
                "could buy the default's own operating point at that budget, and the accuracy "
                "above it is over those questions only, which are the cheaper -- and so the "
                "easier -- ones. Affordable ON AVERAGE over the questions: %s."
                % (dcell["cell"][0], dcell["cell"][1], acc, avg)]
    avg = [n for n in pol.AVG_RANKINGS if n in t1["rows"]]
    if avg:
        out += ["", "`avg_lookup` and `avg_equation` hold the MEAN price over questions at or "
                "below the budget instead of capping every question, so the default cell for "
                "every question is one feasible policy and these rows are comparable with the "
                "`default` row itself. Realised mean price over the evaluation questions, against "
                "the budget the multiplier was fitted to:", "",
                "| arm | %s |" % head, "|---|" + "---|" * len(t1["fractions"])]
        for n in avg:
            r = t1["rows"][n]
            out.append("| %s | %s |" % (n, " | ".join(
                "%.0f vs %.0f (%+.1f%%)" % (r["mean_price_layer_passes"][j], t1["budgets"][j],
                                            r["mean_price_over_X_pct"][j])
                for j in range(len(t1["fractions"])))))
    for n in avg:
        r = t1["rows"][n]
        for j, f in enumerate(t1["fractions"]):
            if (r["lambda"][j] == 0.0 and r["cost_saving_pct"][j] >= 1.0
                    and not r["gate_reverted"][j]):
                out.append("- `%s` at %.2fx: the multiplier is 0, so the budget never binds. The "
                           "row is the same %.1f points at %.1f%% of the default cost, %.1f%% "
                           "under the budget it was given."
                           % (n, f, r["acc_pts"][j], r["pct_of_default_cost"][j],
                              r["cost_saving_pct"][j]))
        out += _gate_lines(t1, n, r)
    out += ["", "`not feasible` = the arm itself costs more than that budget, so it cannot be run "
            "there at all. `n/a` = the arm could run in principle but no question can afford any "
            "of its cells at that budget. A percentage in brackets is the share of questions that "
            "could afford the arm, and the mean above it is over those questions only."]
    return "\n".join(out) + "\n"
