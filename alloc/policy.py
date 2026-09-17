"""Rank calibration cells and choose affordable cells per prompt; costs are layer-token passes and accuracy is a fraction."""
import numpy as np

from . import cells as cellsmod

# Require a predicted margin of half a calibration standard deviation by default.
DEFAULT_C_GATE = 0.5
N_BUDGETS = 16
BUDGET_TOL = 1e-9

# The three ways to price a cell. `cap` and `expected` are decision-time prices; `realised` needs
# the generation it is pricing and is an audit number only (see Cost).
ACCOUNTINGS = ("cap", "realised", "expected")


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
    """Return a pricing function (k,T,P,R[,n]) -> (L_fixed+k*L)*(P+T+R) in layer-token passes; promptfree omits P.

    The trailing prompt position is accepted and ignored, so every pricing function in this module
    has one signature whatever its accounting.
    """
    if promptfree:
        return lambda k, T, p, r, n=None: (L_fixed + k * L) * (T + r)
    return lambda k, T, p, r, n=None: (L_fixed + k * L) * (p + T + r)


class Cost(object):
    """Price cell (k, T) for one prompt in layer-token passes under one of three accountings.

    `cap`       (L_fixed + k L) (P + T + R): the chain is charged its whole cap. Known before
                generating, but it charges a cell that stops early for a length it never writes, so
                a natural-stop cell (T at the horizon) is unaffordable at any budget a natural-stop
                run actually costs.
    `expected`  (L_fixed + k L) (P + E_cal[min(len_k, T)] + R): the cap is replaced by the mean
                length the CALIBRATION prompts realised at that cell. Still a decision-time price,
                because the table is fixed before any evaluation prompt is generated, and it prices
                a natural-stop cell at what natural stop costs on average.
    `realised`  the prompt's own measured layer passes at that cell. An audit price, NOT available
                at decision time: it needs the generation it is pricing.

    Where no prompt is named (the median-prompt cost matrix, the budget grid, ranking tie-breaks)
    `cap` and `expected` price the median prompt they are passed, and `realised` answers with the
    median measured cost of that cell.
    """

    def __init__(self, cells, accounting="cap", promptfree=False, expected=None):
        if accounting not in ACCOUNTINGS:
            raise ValueError("unknown accounting %r; expected one of %s"
                             % (accounting, ", ".join(ACCOUNTINGS)))
        self.cells, self.accounting = cells, accounting
        self.promptfree = bool(promptfree)
        self.L, self.L_fixed = cells.L, cells.L_fixed
        self._ki = {k: i for i, k in enumerate(cells.ks)}
        self._bi = {b: i for i, b in enumerate(cells.caps)}
        self.expected = None
        self.realised = self.median_realised = None
        if accounting == "expected":
            self.expected = (cellsmod.expected_lengths(cells) if expected is None
                             else np.asarray(expected, float))
        elif accounting == "realised":
            self.realised = cells.passes_pf if self.promptfree else cells.passes
            self.median_realised = np.nanmedian(self.realised, axis=2)

    def generated_tokens(self, k, T):
        """Return the chain length in tokens this accounting charges cell (k,T), before the reserve."""
        if self.accounting == "expected":
            return float(self.expected[self._ki[k], self._bi[T]])
        if T < 0:
            raise ValueError("cap accounting cannot price the no-cap cell %r: it has no "
                             "worst-case length; use expected accounting" % (T,))
        return float(T)

    def __call__(self, k, T, p, r, n=None):
        a, c = self._ki[k], self._bi[T]
        if self.accounting == "realised":
            v = np.nan if n is None else float(self.realised[a, c, n])
            return float(self.median_realised[a, c]) if np.isnan(v) else v
        w = self.L_fixed + k * self.L
        gen = self.generated_tokens(k, T)
        return w * (gen + r) if self.promptfree else w * (p + gen + r)


def cost_of(cells, promptfree=False, accounting="cap"):
    """Return the pricing function of `cells` under one accounting; see Cost."""
    return Cost(cells, accounting=accounting, promptfree=promptfree)


def accounting_of(cost):
    """Return the accounting name a pricing function carries, or "cap" for a plain formula."""
    return getattr(cost, "accounting", "cap")


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
        if gate_passes(margin, s, self.c_gate):
            return pick, False
        return normal, True


def gate_passes(margin, sd, c_gate=DEFAULT_C_GATE):
    """Return whether a predicted accuracy margin clears c_gate times its own calibration SD.

    One rule, shared by the per-prompt gate above and by the average-budget gate, which measures
    its margin between two whole policies rather than between two cells.
    """
    return bool(float(margin) > float(c_gate) * float(sd))


# ---------------------------------------------------------------- per-prompt policy
def policy_vectors(cells, ev_pos, cost, Xs, order, gate=None):
    """Return paired policy/normal accuracy vectors and reversion fractions per layer-token budget; preserve infeasible prompts as NaN."""
    ki = {k: i for i, k in enumerate(cells.ks)}
    bi = {b: i for i, b in enumerate(cells.caps)}
    kmax = cells.ks[-1]
    order_idx = [(ki[k], bi[T], k, T) for k, T in order]
    out, reverted = [], []
    for X in Xs:
        pv, nv, rev = [], [], 0
        for n in ev_pos:
            p, r = cells.ptok[n], cells.reserve[n]
            nf = [T for T in cells.caps if affordable(cost(kmax, T, p, r, n), X)]
            normal = (ki[kmax], bi[max(nf)]) if nf else None
            pick = None
            for a, c, k, T in order_idx:
                if affordable(cost(k, T, p, r, n), X):
                    pick = (a, c)
                    break
            if gate is not None:
                pick, did = gate.choose(pick, normal)
                rev += int(did)
            pv.append(cells.acc[pick[0], pick[1], n] if pick is not None else np.nan)
            nv.append(cells.acc[normal[0], normal[1], n] if normal is not None else np.nan)
        out.append((np.array(pv, float), np.array(nv, float)))
        reverted.append(rev / max(1, len(ev_pos)))
    return out, reverted


# ---------------------------------------------------------------- the average budget
# `avg_lookup` and `avg_equation` answer a different question from the arms above. Those obey a
# HARD per-prompt cap: every prompt must be priced at or below X, so at X set to the default's own
# mean cost they can buy the default's cell only for the prompts priced under that mean. The
# average budget asks instead that the MEAN price over prompts be at most X. Under that constraint
# "the default cell for every prompt" is itself one feasible policy, so the comparison against the
# uncapped default row is like for like, and the allocator is free to take a cheaper cell where it
# scores the same and spend the saving where depth is worth buying.
AVG_RANKINGS = ("avg_lookup", "avg_equation", "avg_gated_lookup")
# Which ranking supplies the per-cell score of each average-budget arm. `avg_gated_lookup` scores
# like `avg_lookup` and then has to clear a gate against running the default cell for every prompt.
AVG_BASE = {"avg_lookup": "lookup", "avg_equation": "equation", "avg_gated_lookup": "lookup"}
AVG_GATED = "avg_gated_lookup"
AVG_TOL = 0.02          # the realised mean price may run this far over X before it is flagged
AVG_ITERS = 80          # bisection steps: the spend is a step function of the multiplier


def price_tensor(cells, pos, cost):
    """Return the (depth, cap, prompt) price of every cell for the given prompts, in layer-token passes."""
    pos = np.asarray(pos, dtype=int)
    return np.array([[[cost(k, T, cells.ptok[n], cells.reserve[n], n) for n in pos]
                      for T in cells.caps] for k in cells.ks], float)


def avg_picks(score, prices, lam):
    """Return per-prompt (depth index, cap index) arrays maximising score - lam*price.

    A tie in the objective goes to the lower price, and a tie in both to the lower depth and cap,
    so the pick is deterministic. A cell with no score, or no price, is never picked.
    """
    S, Pr = np.asarray(score, float), np.asarray(prices, float)
    nk, nb, nq = Pr.shape
    fin = (np.isfinite(S)[:, :, None] & np.isfinite(Pr)).reshape(nk * nb, nq)
    J = np.where(fin, (S[:, :, None] - float(lam) * Pr).reshape(nk * nb, nq), -np.inf)
    Pf = np.where(fin, Pr.reshape(nk * nb, nq), np.inf)
    best = J.max(0)
    tie = np.maximum(1.0, np.abs(np.where(np.isfinite(best), best, 0.0))) * 1e-12
    flat = np.where(J >= best - tie, Pf, np.inf).argmin(0)
    return flat // nb, flat % nb


def avg_spend(score, prices, lam):
    """Return the mean price over prompts of the cells chosen at multiplier `lam`, in layer-token passes."""
    Pr = np.asarray(prices, float)
    a, b = avg_picks(score, Pr, lam)
    return float(Pr[a, b, np.arange(Pr.shape[2])].mean())


def _lambda_ceiling(score, prices):
    """Return a multiplier beyond which price decides alone, so bisection has a bracket.

    A cell can be worth at most the whole spread of the score surface, and buying any dearer cell
    costs at least the smallest positive price step a prompt shows; above that ratio no score
    advantage survives and every prompt takes its cheapest cell.
    """
    S = np.asarray(score, float)
    fin = np.isfinite(S)
    spread = float(S[fin].max() - S[fin].min()) if fin.any() else 1.0
    Pr = np.asarray(prices, float)
    flat = np.sort(Pr.reshape(-1, Pr.shape[2]), axis=0)
    d = np.diff(flat, axis=0)
    d = d[np.isfinite(d) & (d > 0)]
    gap = float(d.min()) if d.size else 1.0
    return 4.0 * max(spread, np.finfo(float).tiny) / gap


def lambda_for_budget(score, prices, X, n_iter=AVG_ITERS):
    """Return (multiplier, the mean price it spends, whether X could be met) for these prompts.

    The spend is a non-increasing step function of the multiplier, so the multiplier wanted is the
    SMALLEST one whose spend fits X: that is the largest feasible spend, and any larger multiplier
    would leave budget unspent. Bisection brackets it between 0, where the best score is bought
    whatever it costs, and a multiplier at which every prompt takes its cheapest cell.
    """
    at_zero = avg_spend(score, prices, 0.0)
    if affordable(at_zero, X):
        return 0.0, at_zero, True
    hi = _lambda_ceiling(score, prices)
    floor_spend = avg_spend(score, prices, hi)
    if not affordable(floor_spend, X):
        # Not even the cheapest cell for every prompt fits X. The multiplier is returned with the
        # spend it cannot get below, so the caller can report by how much the budget was missed.
        return hi, floor_spend, False
    lo = 0.0
    for _ in range(int(n_iter)):
        mid = 0.5 * (lo + hi)
        if affordable(avg_spend(score, prices, mid), X):
            hi = mid
        else:
            lo = mid
    return hi, avg_spend(score, prices, hi), True


def avg_budget_vectors(cells, ev_pos, cal_pos, cost, Xs, score, tol=AVG_TOL):
    """Return one record per budget: the average-budget policy's accuracy over the evaluation
    prompts, its multiplier, and the realised mean price beside the budget X it was fitted to.

    The multiplier is fitted on the CALIBRATION prompts and then applied unchanged, so the
    evaluation prompts' mean price is a measurement and not a constraint imposed on them; it can
    land over X when the prompts either side of the multiplier's threshold split differently in the
    two halves. `over_budget` flags a record that ran more than `tol` over X.
    """
    if accounting_of(cost) == "realised":
        raise ValueError("the average-budget policy needs a decision-time price; `realised` is an "
                         "audit price that needs the generation it is pricing (see policy.Cost)")
    ev, cal = np.asarray(ev_pos, dtype=int), np.asarray(cal_pos, dtype=int)
    if not len(ev) or not len(cal):
        raise ValueError("the average-budget policy needs both splits")
    cal_prices = price_tensor(cells, cal, cost)
    ev_prices = price_tensor(cells, ev, cost)
    idx = np.arange(len(ev))
    out = []
    for X in Xs:
        lam, cal_spend, met = lambda_for_budget(score, cal_prices, X)
        a, b = avg_picks(score, ev_prices, lam)
        price = ev_prices[a, b, idx]
        counts = {}
        for i, j in zip(a, b):
            key = "k%d_T%d" % (cells.ks[i], cells.caps[j])
            counts[key] = counts.get(key, 0) + 1
        mean_price = float(price.mean())
        out.append({"X": float(X), "lambda": float(lam),
                    "constraint_met_on_calibration": bool(met),
                    "cal_mean_price": float(cal_spend),
                    "mean_price": mean_price,
                    "mean_price_over_X_pct": 100.0 * (mean_price / float(X) - 1.0),
                    "over_budget": bool(mean_price > float(X) * (1.0 + tol)),
                    "acc": cells.acc[a, b, ev],
                    "price": price,
                    "cells_used": counts})
    return out
