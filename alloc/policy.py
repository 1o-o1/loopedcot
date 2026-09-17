"""Rank calibration cells and choose affordable cells per prompt; costs are layer-token passes and accuracy is a fraction."""
import numpy as np

# Require a predicted margin of half a calibration standard deviation by default.
DEFAULT_C_GATE = 0.5
N_BUDGETS = 16
BUDGET_TOL = 1e-9


def affordable(price, X):
    """Return whether a cell priced at `price` layer-token passes fits budget X layer-token passes.

    The comparison carries a relative tolerance because a budget grid point is built by
    exponentiating a logarithm, so the budget that is meant to be exactly one cell's price can land
    an ulp below it; without the tolerance that cell would be unaffordable at its own budget.
    """
    return price <= X * (1 + BUDGET_TOL)


def _nanmean(x):
    """Return the mean of defined numeric entries, or NaN if none exist; output units match input units."""
    v = np.asarray(x, float)
    m = ~np.isnan(v)
    return float(v[m].mean()) if m.any() else float("nan")


# ---------------------------------------------------------------- cost
def per_prompt_cost(L, promptfree=False, L_fixed=0):
    """Return a pricing function (k,T,P,R) -> (L_fixed+k*L)*(P+T+R) in layer-token passes; promptfree omits P."""
    if promptfree:
        return lambda k, T, p, r: (L_fixed + k * L) * (T + r)
    return lambda k, T, p, r: (L_fixed + k * L) * (p + T + r)


def cost_of(cells, promptfree=False):
    return per_prompt_cost(cells.L, promptfree, cells.L_fixed)


def median_point(cells, pos):
    """Return median prompt length and reserve from the selected prompt positions, both in tokens."""
    return (float(np.median(cells.ptok[pos])), float(np.median(cells.reserve[pos])))


def cost_matrix(cells, cost, Pm, Rm):
    return np.array([[cost(k, T, Pm, Rm) for T in cells.caps] for k in cells.ks], float)


def budget_grid(cmat, n=N_BUDGETS):
    """Return n logarithmically spaced layer-token budgets from the cheapest to the dearest entry
    of the median-prompt cost matrix; the endpoints are those two prices, not a margin above them."""
    return np.exp(np.linspace(np.log(cmat.min()), np.log(cmat.max()), n))


def budget_ranges(cells, cost, Xs, Pm, Rm):
    """Return budget indices where depth 2 and maximum depth fit at cap 64, and the lower-depth-only range; costs are layer-token passes."""
    kmax = cells.ks[-1]
    k2 = 2 if 2 in cells.ks else cells.ks[min(1, len(cells.ks) - 1)]
    T = 64 if 64 in cells.caps else cells.caps[len(cells.caps) // 2]
    bstar = [i for i, X in enumerate(Xs)
             if affordable(cost(k2, T, Pm, Rm), X) and affordable(cost(kmax, T, Pm, Rm), X)]
    blow = [i for i, X in enumerate(Xs)
            if not affordable(cost(kmax, T, Pm, Rm), X)
            and affordable(cost(cells.ks[0], T, Pm, Rm), X)]
    return bstar, blow, {"k2": k2, "kmax": kmax, "T": T, "L": cells.L, "L_fixed": cells.L_fixed}


# ---------------------------------------------------------------- rankings
def rank_lookup(cells, cal_pos, cost, Pm, Rm, boot_sel=None):
    """Return cells sorted by calibration accuracy fraction, then median layer-token cost, depth, and token cap; NaN scores sort last."""
    if any(cells.split[n] != "cal" for n in cal_pos) or not len(cal_pos):
        raise ValueError("rankings require calibration positions only")
    ids = cal_pos if boot_sel is None else np.asarray(cal_pos)[boot_sel]
    order = [(k, T) for k in cells.ks for T in cells.caps]
    ki = {k: i for i, k in enumerate(cells.ks)}
    bi = {b: i for i, b in enumerate(cells.caps)}
    acc = {c: _nanmean(cells.acc[ki[c[0]], bi[c[1]], ids]) for c in order}
    return sorted(order, key=lambda c: (not np.isfinite(acc[c]), -acc[c] if np.isfinite(acc[c]) else 0, cost(c[0], c[1], Pm, Rm), c)), acc


def rank_equation(cells, A_hat, cost, Pm, Rm):
    """Return cells sorted by supplied predicted accuracy fraction, then median layer-token cost, depth, and token cap; NaNs sort last."""
    order = [(k, T) for k in cells.ks for T in cells.caps]
    ki = {k: i for i, k in enumerate(cells.ks)}
    bi = {b: i for i, b in enumerate(cells.caps)}
    pred = {c: float(A_hat[ki[c[0]], bi[c[1]]]) for c in order}
    return sorted(order, key=lambda c: (not np.isfinite(pred[c]), -pred[c] if np.isfinite(pred[c]) else 0, cost(c[0], c[1], Pm, Rm), c)), pred


# ---------------------------------------------------------------- the gate
def margin_sd(A_hat_draws):
    """Return population SD of each cell-pair accuracy margin from (draw,depth,cap) surfaces, in accuracy-fraction units."""
    D = np.asarray(A_hat_draws, float)
    d, nk, nb = D.shape
    F = D.reshape(d, nk * nb)
    M = F[:, :, None] - F[:, None, :]           # (draws, cell_a, cell_b)
    return M.std(0).reshape(nk, nb, nk, nb)


class Gate(object):
    """Choose the candidate only when its predicted accuracy margin exceeds c_gate times the calibration margin SD."""

    def __init__(self, A_hat, sd, c_gate=DEFAULT_C_GATE):
        self.A_hat = np.asarray(A_hat, float)
        self.sd = np.asarray(sd, float)
        self.c_gate = float(c_gate)

    def choose(self, pick, normal):
        """Return a chosen (depth index,cap index) pair and reversion flag from candidate and normal pairs, either possibly None."""
        if normal is None:
            return pick, False
        if pick is None or pick == normal:
            return normal, False
        margin = self.A_hat[pick] - self.A_hat[normal]
        s = self.sd[pick[0], pick[1], normal[0], normal[1]]
        if margin > self.c_gate * s:
            return pick, False
        return normal, True


# ---------------------------------------------------------------- per-prompt policy
def policy_vectors(cells, ev_pos, cost, Xs, order, gate=None, with_picks=False):
    """Return paired policy/normal accuracy vectors and reversion fractions per layer-token budget; preserve infeasible prompts as NaN.

    Each entry of `Xs` is one budget for every question, or an array of budgets aligned with
    `ev_pos` (a per-question budget; NaN = no budget defined there, both arms infeasible).
    `with_picks=True` also returns, per budget, the chosen (depth index, cap index) of the policy
    and of normal operation per question (None where infeasible), so a caller can price them.
    """
    ki = {k: i for i, k in enumerate(cells.ks)}
    bi = {b: i for i, b in enumerate(cells.caps)}
    kmax = cells.ks[-1]
    order_idx = [(ki[k], bi[T], k, T) for k, T in order]
    out, reverted, picks = [], [], []
    for X in Xs:
        Xq = np.broadcast_to(np.asarray(X, float), (len(ev_pos),))
        pv, nv, rev, pk = [], [], 0, []
        for X, n in zip(Xq, ev_pos):
            if X != X:                                   # NaN budget
                pv.append(np.nan)
                nv.append(np.nan)
                pk.append((None, None))
                continue
            p, r = cells.ptok[n], cells.reserve[n]
            nf = [T for T in cells.caps if affordable(cost(kmax, T, p, r), X)]
            normal = (ki[kmax], bi[max(nf)]) if nf else None
            pick = None
            for a, c, k, T in order_idx:
                if affordable(cost(k, T, p, r), X):
                    pick = (a, c)
                    break
            if gate is not None:
                pick, did = gate.choose(pick, normal)
                rev += int(did)
            pv.append(cells.acc[pick[0], pick[1], n] if pick is not None else np.nan)
            nv.append(cells.acc[normal[0], normal[1], n] if normal is not None else np.nan)
            pk.append((pick, normal))
        out.append((np.array(pv, float), np.array(nv, float)))
        reverted.append(rev / max(1, len(ev_pos)))
        picks.append(pk)
    if with_picks:
        return out, reverted, picks
    return out, reverted
