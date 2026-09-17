"""Evaluate cell policies on paired prompts; report accuracy gains in percentage points and costs in layer-token passes."""
import numpy as np

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


def _budget_mean(values):
    """Return the equal-weight mean of budget-wise prompt means, retaining missing prompt slots."""
    return _nanmean([_nanmean(row) for row in values])


# ---------------------------------------------------------------- gain over normal
def gain_over_normal(cells, ranking="lookup", n_labels=None, c_gate=0.0, promptfree=False,
                     n_budgets=pol.N_BUDGETS, n_boot=2000, n_cal_draws=100, seed=7,
                     min_normal_feasible=0.9, gate_draws=40):
    """Return gains in percentage points over the budgets at which normal operation is
    affordable for at least `min_normal_feasible` of the prompts.

    `gain_mean_pts` is the headline: the equal-weight mean over those budgets of the mean paired
    difference (policy minus normal) over prompts. `pooled_gain_mean_pts` averages that difference
    over every feasible (prompt, budget) pair instead, so budgets with more affordable prompts
    weigh more; it is reported alongside because it is the older convention.
    """
    rng = np.random.default_rng(seed)
    cost = pol.cost_of(cells, promptfree)
    ev, cal = cells.select("eval"), cells.select("cal")
    if len(ev) == 0 or len(cal) == 0:
        raise ValueError("%s/%s: need both splits (eval %d, cal %d)"
                         % (cells.name, cells.task, len(ev), len(cal)))
    Pm, Rm = pol.median_point(cells, ev)
    cmat = pol.cost_matrix(cells, cost, Pm, Rm)
    Xs = pol.budget_grid(cmat, n_budgets)
    order, extra = make_order(cells, cal, cost, Pm, Rm, ranking, n_labels)
    resamples = calibration_resamples(cal, n_labels, n_cal_draws, seed)
    gate = None
    if c_gate and c_gate > 0:
        gate, _ = gate_for(cells, cal, n_labels=n_labels, c_gate=c_gate,
                           resamples=resamples)
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
           "c_gate": float(c_gate), "promptfree": bool(promptfree),
           "n_eval": int(len(ev)), "n_cal": int(len(cal)),
           "median_prompt_tokens": Pm, "median_reserve": Rm,
           "budgets": [float(x) for x in Xs], "per_budget": per_budget,
           "Bstar": bstar, "Blow": blow, "range_meta": rmeta,
           "order_top5": [list(c) for c in order[:5]]}
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
    for sel, label_sel in resamples:
        od, _ = make_order(cells, cal, cost, Pm, Rm, ranking, n_labels,
                           boot_sel=sel, label_sel=label_sel)
        draw_gate = None
        if gate is not None:
            draw_hat, _ = surface(cells, cal[sel], label_pos=cal[label_sel])
            draw_gate = pol.Gate(draw_hat, gate.sd, c_gate)
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
             promptfree=False, n_budgets=pol.N_BUDGETS, n_boot=2000, seed=7, gate_draws=40):
    """Return the paired difference cells_a minus cells_b in percentage points.

    `cells_b` is the REFERENCE: its median prompt, its own cost function and its cost matrix fix
    the budget grid and the two budget ranges, so both checkpoints are read at one fixed set of
    budgets whichever of them is the cheaper to run. Each checkpoint still prices its own prompts
    with its own layer counts. Complete case: a prompt missing an accuracy at any budget of the
    range leaves every budget, so the mean is over one fixed set of prompts.
    """
    assert_paired(cells_a, cells_b)
    rng = np.random.default_rng(seed)
    ca = pol.cost_of(cells_a, promptfree)
    cb = pol.cost_of(cells_b, promptfree)
    ev_a, cal_a = cells_a.select("eval"), cells_a.select("cal")
    ev_b, cal_b = cells_b.select("eval"), cells_b.select("cal")
    Pm, Rm = pol.median_point(cells_b, ev_b)
    Xs = pol.budget_grid(pol.cost_matrix(cells_b, cb, Pm, Rm), n_budgets)
    bstar, blow, _m = pol.budget_ranges(cells_b, cb, Xs, Pm, Rm)
    rng_idx = bstar if which == "Bstar" else blow
    if not rng_idx:
        return {"range": which, "empty": True, "reference": cells_b.name}
    Xr = [Xs[i] for i in rng_idx]
    oa, _ = make_order(cells_a, cal_a, ca, Pm, Rm, ranking, n_labels)
    ob, _ = make_order(cells_b, cal_b, cb, Pm, Rm, ranking, n_labels)
    ga = gb = None
    if c_gate and c_gate > 0:
        ga, _ = gate_for(cells_a, cal_a, n_labels, c_gate, gate_draws, seed)
        gb, _ = gate_for(cells_b, cal_b, n_labels, c_gate, gate_draws, seed)
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
            "reference": cells_b.name, "budgets": [float(x) for x in Xr],
            "n_budgets": len(rng_idx), "n_eval": int(n),
            "n_eval_dropped_incomplete": int(np.sum(~ok)),
            "mean_pts": 100 * float(D.mean()),
            "lo95_pts": 100 * float(np.percentile(boots, 2.5)),
            "hi95_pts": 100 * float(np.percentile(boots, 97.5))}


def noninferiority(cells_a, cells_b, ranking="lookup", n_labels=None, c_gate=0.0,
                   promptfree=False, n_budgets=pol.N_BUDGETS, n_boot=2000, seed=7,
                   margin_pts=NI_MARGIN_PTS, gate_draws=40):
    """Return paired top-three-budget differences and one-sided 95% bound in percentage points, with power at zero true effect."""
    assert_paired(cells_a, cells_b)
    rng = np.random.default_rng(seed)
    ca, cb = pol.cost_of(cells_a, promptfree), pol.cost_of(cells_b, promptfree)
    ev_a, cal_a = cells_a.select("eval"), cells_a.select("cal")
    ev_b, cal_b = cells_b.select("eval"), cells_b.select("cal")
    Pm, Rm = pol.median_point(cells_b, ev_b)
    Xs = pol.budget_grid(pol.cost_matrix(cells_b, cb, Pm, Rm), n_budgets)
    bstar, _bl, _m = pol.budget_ranges(cells_b, cb, Xs, Pm, Rm)
    if not bstar:
        return {"empty": True}
    top = bstar[-3:]
    Xr = [Xs[i] for i in top]
    oa, _ = make_order(cells_a, cal_a, ca, Pm, Rm, ranking, n_labels)
    ob, _ = make_order(cells_b, cal_b, cb, Pm, Rm, ranking, n_labels)
    ga = gb = None
    if c_gate and c_gate > 0:
        ga, _ = gate_for(cells_a, cal_a, n_labels, c_gate, gate_draws, seed)
        gb, _ = gate_for(cells_b, cal_b, n_labels, c_gate, gate_draws, seed)
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
            "verdict": verdict, "n_budgets": len(top), "n_eval": int(n),
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
def default_cap_index(cells, pos):
    """Per question: the index of the smallest cap that did not truncate the chain at the deepest
    depth (the default's own uncapped cell), or the last cap for a chain that hit the horizon."""
    ki = len(cells.ks) - 1
    out = []
    for n in pos:
        nstop, ncut = cells.nstop[ki, :, n], cells.ncut[ki, :, n]
        ok = [j for j in range(len(cells.caps))
              if not (np.isnan(nstop[j]) or np.isnan(ncut[j])) and ncut[j] >= nstop[j] - 1e-9]
        out.append(min(ok, key=lambda j: cells.caps[j]) if ok else len(cells.caps) - 1)
    return np.array(out, int)


def realised_price(cells, pos, picks, promptfree=False):
    """Mean realised layer-pass cost of the chosen cells over the questions where a cell was chosen:
    the rows' own stored cost (prompt + chain actually generated + read-out), prompt-free when asked."""
    vals = []
    for pk, n in zip(picks, pos):
        if pk is None:
            continue
        a, c = pk
        v = cells.passes[a, c, n]
        if v != v:
            continue
        if promptfree:
            v -= (cells.L_fixed + cells.ks[a] * cells.L) * cells.ptok[n]
        vals.append(float(v))
    return float(np.mean(vals)) if vals else float("nan")


def table1(cells, promptfree=False, fractions=BUDGET_FRACTIONS, c_gate=pol.DEFAULT_C_GATE,
           n_labels_grid=(30, 100), seed=7, gate_draws=40, basis="prompt"):
    """Return each arm's accuracy in percentage points at budgets set to `fractions` of the default
    cost, with the mean realised price of what each arm actually ran.

    basis="prompt" (the default): each question's budget is the fraction of the CAP cost of the
    default's own uncapped cell for that question (deepest depth, smallest cap that did not truncate
    its chain), the way every policy is priced. At fraction 1.0 normal operation lands on exactly that
    cell, so `default_at_budget` equals `default` by construction and anchors the table; below 1.0
    both arms get the same share of the same question-level spend.
    basis="mean": one budget per grid, the fraction of the MEAN realised default cost; a question
    whose chain was longer than average is then starved even at 1.0.

    The `default` row is the unbudgeted run: it costs its whole default cost and cannot be bought at a
    fraction below 1.0; its `feasible` flags say so and its accuracy there is NaN.
    """
    cost = pol.cost_of(cells, promptfree)
    ev, cal = cells.select("eval"), cells.select("cal")
    Pm, Rm = pol.median_point(cells, ev)
    dc = default_cost(cells, promptfree)
    if dc["mean"] is None:
        return {"task": cells.task, "grid": cells.name, "empty": True}
    if basis == "prompt":
        jdef = default_cap_index(cells, ev)
        kmax = cells.ks[-1]
        dpp = np.array([cost(kmax, cells.caps[j], cells.ptok[n], cells.reserve[n])
                        for j, n in zip(jdef, ev)], float)
        Xs = [f * dpp for f in fractions]
        budgets = [{"per_question": True, "mean": float(np.nanmean(x))} for x in Xs]
    else:
        Xs = [f * dc["mean"] for f in fractions]
        budgets = [float(x) for x in Xs]
    dacc = default_accuracy(cells)

    arms = [("lookup", dict(ranking="lookup")),
            ("equation", dict(ranking="equation")),
            ("gated_equation", dict(ranking="equation", gate=True))]
    for nl in n_labels_grid:
        arms.insert(-1, ("equation_n%d" % nl, dict(ranking="equation", n_labels=nl)))

    gate = None
    if c_gate and c_gate > 0:
        gate, _ = gate_for(cells, cal, c_gate=c_gate, n_draws=gate_draws, seed=seed)

    default_acc_pts = 100 * float(np.nanmean(dacc))
    default_feasible = [bool(f >= 1.0 - 1e-9) for f in fractions]
    dprice = realised_price(cells, ev, [(len(cells.ks) - 1, int(j)) for j in default_cap_index(cells, ev)],
                            promptfree)
    rows = {"default": {"note": "max depth, natural stop, uncapped",
                        "acc_pts": [default_acc_pts if f else float("nan")
                                    for f in default_feasible],
                        "feasible": default_feasible,
                        "unbudgeted_acc_pts": default_acc_pts,
                        "price_layer_passes": [dprice if f else float("nan") for f in default_feasible],
                        "cost_layer_passes": [dc["mean"]] * len(fractions)}}
    normal_done = False
    for name, spec in arms:
        order, _ = make_order(cells, cal, cost, Pm, Rm, spec["ranking"], spec.get("n_labels"))
        g = gate if spec.get("gate") else None
        P, rev, picks = pol.policy_vectors(cells, ev, cost, Xs, order, gate=g, with_picks=True)
        rows[name] = {"acc_pts": [100 * _nanmean(P[j][0]) for j in range(len(Xs))],
                      "feasible_frac": [float(np.mean(~np.isnan(P[j][0]))) for j in range(len(Xs))],
                      "price_layer_passes": [realised_price(cells, ev, [p[0] for p in picks[j]], promptfree)
                                             for j in range(len(Xs))],
                      "gate_reverted_frac": list(rev)}
        if not normal_done:
            rows["default_at_budget"] = {
                "note": "normal operation: k_max at its largest affordable cap",
                "acc_pts": [100 * _nanmean(P[j][1]) for j in range(len(Xs))],
                "feasible_frac": [float(np.mean(~np.isnan(P[j][1]))) for j in range(len(Xs))],
                "price_layer_passes": [realised_price(cells, ev, [p[1] for p in picks[j]], promptfree)
                                       for j in range(len(Xs))]}
            normal_done = True
    return {"task": cells.task, "grid": cells.name, "promptfree": bool(promptfree),
            "budget_basis": basis, "fractions": list(fractions), "budgets": budgets,
            "default_cost": dc, "n_eval": int(len(ev)), "c_gate": float(c_gate), "rows": rows}


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


def table1_markdown(t1):
    if t1.get("empty"):
        return "# Table 1\n\n(no uncapped realisation in these cells; nothing to report)\n"
    order = ["default", "default_at_budget", "lookup", "equation"]
    order += [k for k in t1["rows"] if k.startswith("equation_n")]
    order += ["gated_equation"]
    head = " | ".join("%.2f x default" % f for f in t1["fractions"])
    basis = t1.get("budget_basis", "mean")
    acct = "prompt-free" if t1.get("promptfree") else "prompt-inclusive"
    if basis == "prompt":
        why = ("Budget = a fraction of each question's OWN default cost, the cap cost of the deepest "
               "depth at the smallest cap that did not truncate its chain; at 1.00 normal operation is "
               "exactly the default. Mean default cost (realised): %.0f layer passes over %d questions "
               "(%.1f%% of them counted at the horizon)."
               % (t1["default_cost"]["mean"], t1["default_cost"]["n"],
                  100 * t1["default_cost"]["horizon_share"]))
    else:
        why = ("Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max "
               "depth at its natural stop, uncapped: %.0f layer passes over %d questions "
               "(%.1f%% of them counted at the horizon)."
               % (t1["default_cost"]["mean"], t1["default_cost"]["n"],
                  100 * t1["default_cost"]["horizon_share"]))
    out = ["# Table 1 -- %s (%s), %s accounting, budget basis: %s" % (t1["task"], t1["grid"], acct, basis),
           "", why, "",
           "Each cell: accuracy in points [mean realised price of what that arm ran, in thousands of "
           "layer passes]; a bracketed percentage is the share of questions that could afford the arm.",
           "", "| arm | %s |" % head, "|---|" + "---|" * len(t1["fractions"])]
    def cell(r, j):
        feasible = r.get("feasible")
        if feasible is not None and not feasible[j]:
            return "not feasible"      # the arm costs more than this budget; nothing is substituted
        v = r["acc_pts"][j]
        if v != v:                     # NaN: no cell of that arm is affordable at that budget
            return "n/a"
        f = r.get("feasible_frac")
        pr = (r.get("price_layer_passes") or [float("nan")] * (j + 1))[j]
        ptxt = " [%.1fk]" % (pr / 1000.0) if pr == pr else ""
        base = "%.1f" % v if f is None or f[j] >= 0.999 else "%.1f (%.0f%%)" % (v, 100 * f[j])
        return base + ptxt

    for name in order:
        r = t1["rows"].get(name)
        if not r:
            continue
        out.append("| %s | %s |"
                   % (name, " | ".join(cell(r, j) for j in range(len(t1["fractions"])))))
    out += ["", "`not feasible` = the arm itself costs more than that budget, so it cannot be run "
            "there at all. `n/a` = the arm could run in principle but no question can afford any "
            "of its cells at that budget. A percentage in brackets is the share of questions that "
            "could afford the arm, and the mean above it is over those questions only."]
    return "\n".join(out) + "\n"
