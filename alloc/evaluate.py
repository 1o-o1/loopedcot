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
def split_calibration(cells, cal_pos, n_select=None, n_verify=None):
    """Return (selection positions, verification positions, sizes) from the calibration split.

    The calibration questions are taken IN ID ORDER: the first `n_select` ids fit the ranking and
    the multiplier, the next `n_verify` measure the margin of what was fitted. Id order rather than
    a seeded shuffle, so the same question is in the same half whatever else the run changes, and
    two checkpoints of one task verify on the same questions.

    v5: both counts default to None, which takes `GATE_SELECT_FRAC` of however many questions
    calibrate -- 70 percent to select, the rest to verify. The calibration size is itself a
    function of the grid's size (cells.n_cal_for), so at the frozen 100 this returns the frozen 70
    and 30 and nothing about these grids moves, while a larger calibration split grows both halves
    instead of leaving the verification margin measured on 30 questions for ever. Passing the two
    counts overrides the proportion.

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
    proportional = n_select is None and n_verify is None
    if proportional:
        n_select = max(1, int(round(pol.GATE_SELECT_FRAC * len(order))))
        n_verify = max(0, len(order) - n_select)
    elif n_select is None or n_verify is None:
        raise ValueError("pass both selection and verification counts, or neither for the "
                         "%.0f/%.0f proportion of the calibration split"
                         % (100 * pol.GATE_SELECT_FRAC, 100 * (1 - pol.GATE_SELECT_FRAC)))
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
                 n_select=None, n_verify=None):
    """Return (gate, the positions the ranking may be fitted on, the split sizes).

    `split`  the order is fitted on the selection half and the gate MEASURES the margin of the cell
             it picked against the fallback on the verification half's own labels, paired, with a
             paired bootstrap SD over those questions. The cells the order chose are scored on
             labels that had no part in choosing them, and by those labels rather than by the
             equation's prediction of them.
    `whole`  the old rule, kept for comparison: one set fits and measures, and the margin it reads
             is the predicted one, off the fitted surface.
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
    return measured_gate(cells, ver, c_gate=c_gate, seed=seed), sel, sizes


def measured_gate(cells, ver_pos, c_gate=pol.DEFAULT_C_GATE, seed=7, gate_boot=pol.GATE_BOOT):
    """Return the gate that reads the VERIFICATION questions' own labels.

    The margin between two cells is the paired accuracy difference over those questions and its SD
    a paired bootstrap over them, so no part of the decision comes from the fitted surface. The
    surface predicts; only the labels can say whether the prediction was right, and on a task where
    the equation's assumption fails -- where the early answer is scored better than it is -- the
    predicted margin is the wrong sign and the gate opens on a deviation that loses points.
    """
    ver = np.asarray(ver_pos, dtype=int)
    return pol.MeasuredGate(cells.acc[:, :, ver], c_gate=c_gate, n_boot=gate_boot, seed=seed,
                            pos=ver)


def _budget_mean(values):
    """Return the equal-weight mean of budget-wise prompt means, retaining missing prompt slots."""
    return _nanmean([_nanmean(row) for row in values])


# ---------------------------------------------------------------- structured deviation families
# FROZEN ON. The setting of record is the ten Ouro-1.4B base production grids at horizon 4096 and
# full N; the ten S33 spike grids run a 512 horizon over 400 questions and are not. On the ten
# production grids, at 1.0x of the default cost over both gated arms:
#
#   n_cal  eval  split    deviations  false   gain@1.0x            oracle gap@1.0x
#    100    300  70/30     6  -> 9      0     +0.07 -> +0.12        2.11 -> 2.06
#    150    250  105/45    7  -> 10     0     +0.41 -> +0.73        2.32 -> 1.94
#    200    200  140/60    7  -> 9      0     +0.25 -> +0.77        2.55 -> 1.95
#
# (v4's free set alone -> the families; 150 and 200 emulated by promoting evaluation ids.) The
# families win at every calibration size, carry no false deviation at any of them, and close the
# oracle gap wherever v4's free set widens it. Four grids gain a deviation the free set could not
# earn -- BBH +0.7, CSQA +2.3, StrategyQA +1.3, and HellaSwag's genuine cap-0 optimum, worth +5.6
# at n_cal 150 and +7.5 at 200, which v4 never finds at any size. `--no-families` restores the free
# set alone for comparison.
DEFAULT_FAMILIES = True


def family_order(cells, order, family):
    """Return `order` cut down to the cells of one structured deviation family, same ranking.

    The family restricts WHICH cells the allocator may deviate to; the ranking still decides which
    of them it takes. An empty result means the family has no cell on this grid and is skipped.
    """
    want = set(pol.family_cells(cells.ks, cells.caps, family))
    return [c for c in order if c in want]


def _fill_from_normal(pv, nv):
    """Return the policy vector with prompts no family cell could buy run normally instead.

    A family is a restriction on the DEVIATION, not on the run: a prompt that cannot afford any of
    the family's cells still runs normal operation, exactly as it would with no gate at all.
    """
    pv, nv = np.asarray(pv, float), np.asarray(nv, float)
    return np.where(np.isnan(pv) & ~np.isnan(nv), nv, pv)


def family_score(cells, score, family):
    """Return the score surface with every cell outside one family set to NaN, or None.

    `avg_picks` never chooses a cell it cannot score, so blanking the rest is how an average-budget
    policy is restricted to a family. None means the family has no scored cell on this grid.
    """
    want = set(pol.family_cells(cells.ks, cells.caps, family))
    S = np.asarray(score, float)
    mask = np.array([[(k, T) in want for T in cells.caps] for k in cells.ks], bool)
    out = np.where(mask, S, np.nan)
    return None if not np.isfinite(out).any() else out


def family_margin(cells, ver_pos, cost, X, order_f, seed=7, gate_boot=pol.GATE_BOOT):
    """Return (paired mean margin, paired bootstrap SD) of one family's policy over normal
    operation, measured on the VERIFICATION questions' own labels at one budget.

    The margin is between two whole policies, not two cells: the family's order is walked for each
    verification question exactly as it would be for an evaluation question, and the difference is
    taken question by question against normal operation at the same budget.
    """
    Pv, _rev = pol.policy_vectors(cells, ver_pos, cost, [X], order_f, gate=None)
    arm, ref = Pv[0]
    arm = _fill_from_normal(arm, ref)
    return (_nanmean(arm - ref),
            pol.paired_margin_sd(arm, ref, n_boot=gate_boot, seed=seed))


def gated_vectors(cells, ev_pos, cost, Xs, order, gate, families=DEFAULT_FAMILIES, seed=7,
                  gate_boot=pol.GATE_BOOT, picks=None):
    """Return (per-budget (policy, normal) vectors, reverted fractions, family per budget, records).

    `picks`, when a list, receives per budget the (pick depth, pick cap, normal depth, normal
    cap) index arrays the vectors were read at (policy.policy_vectors); a prompt no family cell
    could buy is recorded at normal operation, which is what it ran.

    The structured families are tried IN ORDER, smallest first. F0, F1 and F2 are each tested as a
    WHOLE POLICY on the verification questions against normal operation at that budget, and the
    first whose margin clears `c_gate` times its own paired bootstrap SD is run, ungated: it has
    already earned the deviation on labels that took no part in choosing it, and testing one cell
    or one depth carries far less of a winner's curse than testing all forty.

    F3 is the free set and v4's behaviour exactly: the ranking's first affordable cell, gated cell
    pair by cell pair against that prompt's own normal operation. It is reached only when every
    smaller family has failed, so v5 can add deviations the structured test earns but never removes
    one v4 kept.

    `families=False` skips F0 to F2 and leaves the v4 path alone.
    """
    if gate is None or not isinstance(gate, pol.MeasuredGate) or gate.pos is None:
        P, rev = pol.policy_vectors(cells, ev_pos, cost, Xs, order, gate=gate, picks=picks)
        return P, rev, [None] * len(Xs), []
    ver = gate.pos
    fams = pol.DEVIATION_FAMILIES[:-1] if families else ()
    out, reverted, opened, records = [], [], [], []
    for X in Xs:
        chosen = None
        for fam in fams:
            order_f = family_order(cells, order, fam)
            if not order_f:
                continue
            margin, sd = family_margin(cells, ver, cost, X, order_f, seed=seed,
                                       gate_boot=gate_boot)
            passed = pol.gate_passes(margin, sd, gate.c_gate)
            records.append({"X": float(X), "family": fam, "n_cells": len(order_f),
                            "margin_pts": (100 * margin if margin == margin else None),
                            "sd_pts": (100 * sd if sd == sd else None),
                            "bar_pts": (100 * gate.c_gate * sd if sd == sd else None),
                            "opened": bool(passed), "n_verification": int(len(ver))})
            if passed:
                chosen = (fam, order_f)
                break
        if chosen is not None:
            fp = []
            Pe, _r = pol.policy_vectors(cells, ev_pos, cost, [X], chosen[1], gate=None, picks=fp)
            pv, nv = Pe[0]
            filled = _fill_from_normal(pv, nv)
            if picks is not None:
                pa, pb, na, nb = fp[0]
                run_normal = (pa < 0) & (na >= 0)
                picks.append((np.where(run_normal, na, pa), np.where(run_normal, nb, pb), na, nb))
            # A prompt that could buy no cell of the family ran normally, which is a reversion.
            rev = float(np.mean(np.isnan(pv) & ~np.isnan(nv)))
            out.append((filled, nv))
            reverted.append(rev)
            opened.append(chosen[0])
            continue
        gate.reset_counts()
        Pe, rv = pol.policy_vectors(cells, ev_pos, cost, [X], order, gate=gate, picks=picks)
        out.append(Pe[0])
        reverted.append(rv[0])
        opened.append("F3" if gate.n_opened else None)
    return out, reverted, opened, records


# ---------------------------------------------------------------- gain over normal
def gain_over_normal(cells, ranking="lookup", n_labels=None, c_gate=0.0, promptfree=False,
                     n_budgets=pol.N_BUDGETS, n_boot=2000, n_cal_draws=100, seed=7,
                     min_normal_feasible=0.9, gate_draws=40, accounting="cap",
                     gate_mode=pol.DEFAULT_GATE_MODE, one_se=False,
                     n_select=None, n_verify=None, families=DEFAULT_FAMILIES):
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
    P, reverted, fam_opened, fam_records = gated_vectors(cells, ev, cost, Xs, order, gate,
                                                         families=families, seed=seed)
    # Snapshot before the bootstrap below asks the gate about further pairs: these are the pairs the
    # reported policy was ruled on, each with the margin and SD its verification questions measured.
    gate_decisions = gate.decisions() if isinstance(gate, pol.MeasuredGate) else None
    bstar, blow, rmeta = pol.budget_ranges(cells, cost, Xs, Pm, Rm)

    gains, per_budget = [], []
    for xi, X in enumerate(Xs):
        pv, nv = P[xi]
        feas = ~np.isnan(nv)
        rec = {"X": float(X), "normal_feasible_frac": float(feas.mean()),
               "policy_acc": _nanmean(pv), "normal_acc": _nanmean(nv),
               "gate_reverted_frac": reverted[xi],
               "deviation_family": fam_opened[xi],
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
           "gate_sizes": gate_sizes, "gate_decisions": gate_decisions,
           "families": bool(families), "family_decisions": fam_records,
           "deviation_family_per_budget": list(fam_opened),
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
            # The gate keeps reading the VERIFICATION half's labels (or, under `whole`, the surface
            # refitted on the draw); only the order is redrawn, which is what this bootstrap
            # measures. Under `split` that is the same gate object, so its margins stay cached.
            draw_gate = (gate if gate_mode == "split" else
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
             n_select=None, n_verify=None):
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
                   n_select=None, n_verify=None):
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
           n_select=None, n_verify=None, families=DEFAULT_FAMILIES):
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

    `families` (v5, on by default) tries the structured deviation families F0 to F2 before the free
    set F3, smallest first, and each gated row records which one opened at each budget. The table
    also carries an ORACLE GAP: the best single evaluation cell's accuracy minus each arm's at
    1.0x. That number reads the evaluation labels, so it is a diagnostic -- the price of
    calibration noise -- and never a policy result; no arm may consume it.
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
    dki, dbi = list(cells.ks).index(dk), list(cells.caps).index(dT)
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

    # Every arm's per-prompt picks, so the policies the rows were read at can be run live
    # (prod.live_check) without a second implementation of any of them.
    picks_out = {}
    normal_done, normal_vecs = False, None
    for name, spec in arms:
        gated = bool(spec.get("gate")) and gate is not None
        # A gated arm is fitted on the SELECTION half only, so the cells its order chose are
        # scored by the gate on labels that had no part in choosing them.
        fit_pos = gate_fit if gated else cal
        order, _ = make_order(cells, fit_pos, cost, Pm, Rm, spec["ranking"], spec.get("n_labels"))
        g = gate if gated else None
        arm_picks = []
        P, rev, fams, frecs = gated_vectors(cells, ev, cost, Xs, order, g, families=families,
                                            seed=seed, picks=arm_picks)
        picks_out[name] = [
            {"fraction": float(fractions[j]), "budget": float(Xs[j]),
             "gate": (_gate_decision(fams[j], frecs, Xs[j]) if gated else None),
             "picks": _pick_records(cells, ev, cost, arm_picks[j][0], arm_picks[j][1])}
            for j in range(len(Xs))]
        for j, e in enumerate(picks_out[name]):
            e["mean_price"] = _mean_price(e["picks"])
        rows[name] = {"acc_pts": [100 * _nanmean(P[j][0]) for j in range(len(Xs))],
                      "feasible_frac": [float(np.mean(~np.isnan(P[j][0]))) for j in range(len(Xs))],
                      "gate_reverted_frac": list(rev),
                      "deviation_family": list(fams),
                      "vs_default": [_paired_vs_default(P[j][0], dacc, rng, n_boot)
                                     for j in range(len(Xs))],
                      # The arm against ITS OWN FALLBACK -- normal operation at the same budget,
                      # which is what the gate reverts to. A deviation whose interval here sits
                      # wholly below zero is a FALSE deviation: it was earned on the verification
                      # questions and lost on the evaluation questions.
                      "vs_fallback": [_paired_vs_default(P[j][0], P[j][1], rng, n_boot)
                                      for j in range(len(Xs))],
                      "fallback": "default_at_budget"}
        if gated:
            rows[name].update(_gate_fields(gate_mode, c, gate_sizes))
            rows[name]["family_decisions"] = frecs
            if isinstance(gate, pol.MeasuredGate):
                rows[name]["gate_decisions"] = gate.decisions()
        if not normal_done:
            picks_out["default_at_budget"] = [
                {"fraction": float(fractions[j]), "budget": float(Xs[j]), "gate": None,
                 "picks": _pick_records(cells, ev, cost, arm_picks[j][2], arm_picks[j][3])}
                for j in range(len(Xs))]
            for e in picks_out["default_at_budget"]:
                e["mean_price"] = _mean_price(e["picks"])
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
                                  one_se=one_se, n_select=n_select, n_verify=n_verify,
                                  families=families)
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
            "deviation_family": [v.get("deviation_family") for v in V],
            "gate_margin_pts": [v.get("gate_margin_pts") for v in V],
            "gate_sd_pts": [v.get("gate_sd_pts") for v in V],
            "gate_draw_frac_positive": [v.get("gate_draw_frac_positive") for v in V],
            # gain over normal is not defined for an average budget: normal operation is a
            # per-prompt cap policy and the two are not priced the same way. The paired
            # differences below are what stands in its place.
            "vs_default": [_paired_vs_default(V[j]["acc"], dacc, rng, n_boot)
                           for j in range(len(Xs))],
            "vs_default_at_budget": [_paired_vs_default(V[j]["acc"], normal_vecs[j], rng, n_boot)
                                     for j in range(len(Xs))],
            # The average-budget arms revert to the DEFAULT CELL run for every prompt, so that is
            # the fallback a deviation of theirs has to beat, and the interval below is what says
            # whether it did on the evaluation questions.
            "vs_fallback": [_paired_vs_default(V[j]["acc"], cells.acc[dki, dbi, ev], rng, n_boot)
                            for j in range(len(Xs))],
            "fallback": "default_cell"}
        if name == pol.AVG_GATED:
            rows[name].update(_gate_fields(gate_mode, c,
                                           V[0].get("gate_sizes") if V else gate_sizes))
        picks_out[name] = [
            {"fraction": float(fractions[j]), "budget": float(Xs[j]),
             "gate": ({"family": v.get("deviation_family"),
                       "margin_pts": v.get("gate_margin_pts"), "sd_pts": v.get("gate_sd_pts"),
                       "opened": v.get("deviation_family") is not None,
                       "reverted": bool(v.get("gate_reverted", False))}
                      if name == pol.AVG_GATED else None),
             "mean_price": float(v["mean_price"]),
             "picks": _pick_records(cells, ev, cost, v["k_idx"], v["cap_idx"], v["price"])}
            for j, v in enumerate(V)]
    orc = oracle_cell(cells, ev)
    one = list(fractions).index(1.0) if 1.0 in fractions else len(fractions) - 1
    for name, r in rows.items():
        v = r["acc_pts"][one]
        r["oracle_gap_pts"] = None if v != v else float(orc["acc_pts"] - v)
    return {"task": cells.task, "grid": cells.name, "promptfree": bool(promptfree),
            "accounting": accounting, "fractions": list(fractions), "avg_budget": avg_on,
            "budgets": [float(x) for x in Xs],
            "default_cost": dc, "n_eval": int(len(ev)), "c_gate": float(c_gate),
            "gate_mode": gate_mode, "one_se": bool(one_se), "gate_c": float(c),
            "families": bool(families), "oracle": orc, "oracle_gap_fraction": float(fractions[one]),
            "gate_sizes": gate_sizes, "rows": rows,
            "picks": {"n_eval": int(len(ev)), "evaluation_ids": [int(cells.idx[n]) for n in ev],
                      "arms": picks_out}}


# ---------------------------------------------------------------- the picks record
def _pick_records(cells, ev, cost, a, b, price=None):
    """Return one {row_idx, k, cap, price} per evaluation prompt for index arrays (a, b); a
    prompt with no pick (index -1) carries None for the cell and the price."""
    out = []
    for i, n in enumerate(ev):
        if int(a[i]) < 0 or int(b[i]) < 0:
            out.append({"row_idx": int(cells.idx[n]), "k": None, "cap": None, "price": None})
            continue
        k, T = int(cells.ks[int(a[i])]), int(cells.caps[int(b[i])])
        pr = float(price[i]) if price is not None else float(cost(k, T, cells.ptok[n], cells.reserve[n], n))
        out.append({"row_idx": int(cells.idx[n]), "k": k, "cap": T, "price": pr})
    return out


def _mean_price(recs):
    """Return the mean price over the prompts that have a pick, or None when none has."""
    pr = [r["price"] for r in recs if r["price"] is not None]
    return float(np.mean(pr)) if pr else None


def _gate_decision(family, records, X):
    """Return the gate decision of a per-prompt gated arm at budget X: the family that opened,
    with the verification margin and SD its record carries (None on the free set, where the
    gate rules cell pair by cell pair and `gate_decisions` on the row holds those)."""
    out = {"family": family, "margin_pts": None, "sd_pts": None, "opened": family is not None}
    for r in records:
        if r.get("family") == family and r.get("opened") and abs(float(r["X"]) - float(X)) <= 1e-9 * max(1.0, abs(float(X))):
            out["margin_pts"], out["sd_pts"] = r.get("margin_pts"), r.get("sd_pts")
            break
    return out


# ---------------------------------------------------------------- the oracle gap
def oracle_cell(cells, ev_pos=None):
    """Return the best SINGLE cell on the evaluation questions, and its accuracy in points.

    This reads the evaluation labels. It is therefore a diagnostic and not a policy: no allocator
    can choose this cell, because choosing it needs the labels it is being scored on. Its distance
    from an arm at 1.0x of the default cost is the PRICE OF CALIBRATION NOISE -- what the arm gives
    up by having to find the cell from a hundred-odd calibration questions instead of being told
    it. Ties go to the lower depth and then the lower cap, so the cell named is deterministic.
    """
    ev = cells.select("eval") if ev_pos is None else np.asarray(ev_pos, dtype=int)
    best, cell = float("-inf"), None
    for a, k in enumerate(cells.ks):
        for b, T in enumerate(cells.caps):
            v = _nanmean(cells.acc[a, b, ev])
            if v == v and v > best:
                best, cell = v, (int(k), int(T))
    if cell is None:
        return {"cell": None, "acc_pts": float("nan"), "n_eval": int(len(ev)),
                "note": "no cell has an evaluation label; a diagnostic, not a policy result"}
    return {"cell": list(cell), "acc_pts": 100.0 * best, "n_eval": int(len(ev)),
            "note": "best single cell on the EVALUATION labels: a diagnostic ceiling, not a "
                    "policy result. The gap below it is the price of calibration noise."}


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
                "k_idx": np.full(len(ev), ki, int), "cap_idx": np.full(len(ev), bi, int),
                "mean_price_over_X_pct": 100.0 * (mean_price / float(X) - 1.0),
                "over_budget": bool(mean_price > float(X) * (1.0 + pol.AVG_TOL)),
                "cells_used": {"k%d_T%d" % default_kt: int(len(ev))},
                "gate_reverted": True})


def avg_gated_vectors(cells, ev_pos, cal_pos, cost, Xs, score, default_kt,
                      c_gate=pol.DEFAULT_C_GATE, n_draws=40, seed=7, n_labels=None,
                      gate_mode=pol.DEFAULT_GATE_MODE, one_se=False,
                      n_select=None, n_verify=None, families=DEFAULT_FAMILIES,
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

    `families` (v5) tries the structured deviation families F0 to F2 first, smallest first, each
    one a Lagrangian policy restricted to that family's cells and each tested the same way against
    the default cell on the verification questions. The first to clear the bar is run and the row
    records it. F3, the free set, is the test below and v4's behaviour exactly, so a family can
    only add a deviation the structured test earned, never take one away.
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
                        "gate_sd_pts": None, "gate_reverted": False, "deviation_family": None,
                        "family_decisions": [],
                        "gate_draw_frac_positive": None, "gate_sizes": sizes})
            if not on or not pol.affordable(float(cal_prices[ki, bi, :].mean()), X):
                continue
            hit = None
            for fam in (pol.DEVIATION_FAMILIES[:-1] if families else ()):
                Sf = family_score(cells, S, fam)
                if Sf is None:
                    continue
                lam_f, _sp, _met = pol.lambda_for_budget(Sf, sel_prices, X)
                af, bf = pol.avg_picks(Sf, ver_prices, lam_f)
                arm_f = np.asarray(cells.acc[af, bf, ver], float)
                m_f = _nanmean(arm_f - ref)
                sd_f = pol.paired_margin_sd(arm_f, ref, n_boot=gate_boot, seed=seed)
                passed = pol.gate_passes(m_f, sd_f, c)
                rec["family_decisions"].append(
                    {"family": fam, "n_cells": int(np.isfinite(Sf).sum()),
                     "margin_pts": (100 * m_f if m_f == m_f else None),
                     "sd_pts": (100 * sd_f if sd_f == sd_f else None),
                     "bar_pts": (100 * c * sd_f if sd_f == sd_f else None),
                     "opened": bool(passed), "n_verification": int(len(ver))})
                if passed:
                    hit = (fam, Sf, m_f, sd_f)
                    break
            if hit is not None:
                fam, Sf, m_f, sd_f = hit
                # The same selection-half diagnostic the free set carries: each draw refits the
                # score and the multiplier INSIDE the family on a resample of the selection half
                # and remeasures the same verification margin.
                fpos = []
                for dsel, _lab in plan:
                    Sd = family_score(cells, cell_scores_boot(cells, sel, cost, Pm, Rm, dsel), fam)
                    if Sd is None:
                        continue
                    lam_d, _sp, _met = pol.lambda_for_budget(Sd, sel_prices[:, :, dsel], X)
                    ad, bd = pol.avg_picks(Sd, ver_prices, lam_d)
                    fpos.append(_nanmean(np.asarray(cells.acc[ad, bd, ver], float) - ref) > 0)
                keep = {k: rec[k] for k in ("gate_mode", "gate_c", "gate_sizes",
                                            "family_decisions")}
                rec.update(pol.avg_budget_vectors(cells, ev, sel, cost, [X], Sf)[0])
                rec.update(keep)
                rec.update({"gate_margin_pts": 100 * m_f, "gate_sd_pts": 100 * sd_f,
                            "gate_reverted": False, "deviation_family": fam,
                            "gate_draw_frac_positive": (float(np.mean(fpos)) if fpos else None)})
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
                rec["deviation_family"] = "F3"
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
                    "gate_sd_pts": None, "gate_reverted": False, "deviation_family": None,
                    "family_decisions": [],
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
            rec["deviation_family"] = "F3"
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
        fam = (r.get("deviation_family") or [None] * len(t1["fractions"]))[j]
        verdict = ("reverted to the default cell for every question"
                   if r["gate_reverted"][j] else
                   "deviated from the default cell on family %s" % fam if fam
                   else "deviated from the default cell")
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
           "| arm | %s | oracle gap @%.2fx |" % (head, t1.get("oracle_gap_fraction", 1.0)),
           "|---|" + "---|" * (len(t1["fractions"]) + 1)]
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
        gap = r.get("oracle_gap_pts")
        out.append("| %s | %s | %s |"
                   % (name, " | ".join(cell(r, j) for j in range(len(t1["fractions"]))),
                      "n/a" if gap is None else "%+.1f" % gap))
    orc = t1.get("oracle")
    if orc and orc.get("cell"):
        fams = sorted({f for n in pol.AVG_RANKINGS + ("gated_equation",)
                       for f in (t1["rows"].get(n, {}).get("deviation_family") or []) if f})
        out += ["", "The ORACLE GAP is the best single evaluation cell (depth %d at cap %d, %.1f "
                "points over %d questions) minus each arm at %.2fx. It reads the EVALUATION "
                "labels, so it is a diagnostic and never a policy result: no allocator can pick "
                "that cell, because picking it needs the labels it is scored on. The gap is the "
                "price of calibration noise -- what the arm gives up by having to find the cell "
                "from the calibration questions. A negative gap means the arm beat every single "
                "cell by varying the cell per question."
                % (orc["cell"][0], orc["cell"][1], orc["acc_pts"], orc["n_eval"],
                   t1.get("oracle_gap_fraction", 1.0))]
        if t1.get("families"):
            out += ["", "Deviation families opened at some budget: %s."
                    % (", ".join(fams) if fams else "none")]
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
