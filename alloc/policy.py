"""Rank calibration cells and choose affordable cells per prompt; costs are layer-token passes and accuracy is a fraction."""
import numpy as np

from . import cells as cellsmod

# Require a predicted margin of half a calibration standard deviation by default.
DEFAULT_C_GATE = 0.5
N_BUDGETS = 16
BUDGET_TOL = 1e-9

# The cell orders a per-prompt policy can walk.
#   `lookup`             calibration accuracy, measured cell by cell.
#   `equation`           the POOLED commitment identity: one c_k and one l_k per depth.
#   `equation_resolved`  the identity RESOLVED BY SETTLE TIME: c_k(j) per settle cap, l_k(T) per
#                        cap (mechanism.resolved_mechanism). The pooled surface rises with T
#                        wherever c_k > l_k, so it can never rank the first cap first; the resolved
#                        one can, which is what the class sets need.
# Every one of them is ranked the same way by `rank_lookup`/`rank_equation`: by score, then by the
# median prompt's price, then by depth and cap, so a tie is broken toward the cheaper cell.
RANKINGS = ("lookup", "equation", "equation_resolved")
# The two that are fitted surfaces rather than measured cell means.
EQUATION_RANKINGS = ("equation", "equation_resolved")

# How the gate measures its margin.
#   `split`  the calibration questions are halved once, by seed: the SELECTION half fits the
#            ranking and the multiplier, the VERIFICATION half measures the margin of what was
#            fitted. The two halves are independent, so the margin is unbiased.
#   `whole`  the old rule: fit and measure on all of the calibration questions. The policy is the
#            argmax over many cells of the same labels the margin is then read on, so the margin
#            carries the maximum's upward bias -- the winner's curse -- and c_gate * sd does not
#            cover it. Kept under a flag so the two can be compared.
GATE_MODES = ("split", "whole")
DEFAULT_GATE_MODE = "split"

# How many FOLDS of the split the gate must be cleared on.
#   1  one direction: fit on the selection half, verify on the verification half. The comparison
#      setting now, and the only count the `whole` gate can have.
#   2  the FROZEN default (2026-09-18). Both directions: fit on the selection half and verify on the
#      verification half, then fit on the verification half and verify on the selection half, and
#      deviate only when BOTH verified margins clear c_gate * sd. A one-fold verification of 30
#      questions can read a large margin that the evaluation half does not repay -- StrategyQA's F0
#      deviation verified +13.3 +/- 5.5 and then lost 2.7 points over 1,990 evaluation questions --
#      and a deviation that is real has to show in both halves. Nothing about one fold moves: the
#      arm that RUNS is always the fold-1 policy, and the extra fold can only withhold a deviation.
#
# Frozen on the 60-pair run of work/analysis_2026-09-18: equation_v6 (one fold) against
# equation_v6_folds2 (two), expected accounting, 1.0x of the default cost. The second fold removed
# every FALSE deviation -- one whose paired evaluation interval sits wholly below its own
# fallback -- for both gated arms, and the deviations it kept are worth more per point of compute:
#
#   arm                          deviations   false at two folds   gain@1.0x      saving@1.0x
#   avg_gated_lookup             31 -> 22     0                    1.22 -> 1.45   42% -> 35%
#   avg_gated_equation_resolved  34 -> 25     0                    0.95 -> 1.13   42% -> 35%
GATE_FOLDS = 2
GATE_FOLD_CHOICES = (1, 2)


def resolve_gate_folds(gate_mode=DEFAULT_GATE_MODE, folds=None):
    """Return the fold count for a run: an explicit request unchanged, else the mode's own default.

    `None` means the default, which is GATE_FOLDS under a split and 1 under `whole`: that mode has
    one set that both fits and measures, so it has no second direction to verify in. An explicit 2
    under `whole` comes back unchanged and is refused where it would be used, because asking for a
    verification the mode cannot do is a mistake and not something to satisfy silently.
    """
    if folds is not None:
        return int(folds)
    return 1 if gate_mode == "whole" else GATE_FOLDS


# The one-standard-error rule: demand a whole SD of margin instead of c_gate of one.
ONE_SE_C_GATE = 1.0
# The split is by COUNT, not by fraction, and it is taken in id order: the first N_SELECT
# calibration ids fit, the next N_VERIFY verify. A count keeps the verification half the same size
# whatever the task's calibration split happens to be, so the margin's SD is comparable across
# tasks; a fraction would not be.
#
# 70/30 is the FROZEN default, re-swept under the MEASURED rule over {50/50, 50/30, 70/30} x
# c_gate {0.5, 1.0} on twenty grids: the ten Ouro-1.4B base production grids at horizon 4096 (ten
# tasks, 100 calibration and 300 evaluation questions) and the ten S33 spike grids (five tasks, two
# checkpoints), both gated arms, expected accounting, 1.0x of the default cost. Objective, in
# order: no deviation that loses to its fallback beyond the paired evaluation interval, then the
# largest mean gain at 1.0x, then the largest mean cost saving.
#
#   setting      deviations  false  gain@1.0x  saving@1.0x  worst row
#   50/50 c0.5       19        0      +0.56      12.77%      -10.0
#   50/50 c1.0       16        0      +0.67      10.35%      -10.0
#   50/30 c0.5       22        1      +0.64      12.64%      -10.0
#   50/30 c1.0       19        1      +0.73      11.41%      -10.0
#   70/30 c0.5       17        0      +0.83      11.10%       -2.0   <- frozen
#   70/30 c1.0       17        0      +0.80      11.10%       -2.0
#
# The single false deviation at 50/30, at both bars, is HellaSwag: its 30 verification questions
# (ids 50-79) read +6.7 points for the depth-3 deviation against an SD of 6.5, and it then loses
# 5.7 points over the 300 evaluation questions. Moving the cut to 70 changes both halves -- a
# policy fitted on 70 questions, verified on ids 70-99 -- and that pair measures +0.0, so the gate
# reverts. 70/30 also carries the best worst row of the six and the highest mean gain; 50/50 saves
# more but gains less, and saving is the third criterion, not the first two.
DEFAULT_N_SELECT = 70
DEFAULT_N_VERIFY = 30
GATE_BOOT = 2000                # resamples of the verification questions behind the margin SD

# v5: the split is 70/30 OF the calibration size, which is itself a function of how many questions
# the grid holds (cells.n_cal_for). At n_cal = 100 that is the frozen 70 and 30 above, so nothing
# about the production grids here moves; at a larger n_cal both halves grow and the verification
# margin's sampling error falls, which is the constraint the whole gate rests on. `n_select` and
# `n_verify` left at None take this proportion; passed as counts they override it, as before.
GATE_SELECT_FRAC = 0.7

# ---------------------------------------------------------------- structured deviation families
# v5. The gate's bar has to cover the winner's curse of whatever set the deviating cell was chosen
# from, and that bias grows with how many cells were in the running. The free set is 40 cells on
# these grids, so a real 5-point edge can sit under the bar. These families are tested IN ORDER,
# SMALLEST FIRST, and the first whose verified margin over the fallback clears the bar wins:
#
#   F0  the deepest depth at cap 0            1 cell   -- "the chain buys nothing" (HellaSwag)
#   F1  the deepest depth at any cap          |caps|   -- "the chain is worth less than its length"
#   F2  one depth shallower, at any cap       |caps|   -- "the last loop pass buys nothing" (MATH500)
#   F3  the free set                          all      -- v4's behaviour, and the last resort
#
# The order is a fixed, pre-registered sequence, not a search: F0 and F2 name the two shapes the
# twenty grids actually show, and a family is only reached when every smaller one has failed.
DEVIATION_FAMILIES = ("F0", "F1", "F2", "F3")


def family_cells(ks, caps, family):
    """Return the cells a structured deviation family may pick from, in depth then cap order.

    An empty list means the family does not exist on this grid -- no cap 0 for F0, one depth only
    for F2 -- and such a family is skipped rather than standing in for another.
    """
    ks, caps = list(ks), list(caps)
    if family not in DEVIATION_FAMILIES:
        raise ValueError("unknown deviation family %r; expected one of %s"
                         % (family, ", ".join(DEVIATION_FAMILIES)))
    if family == "F0":
        return [(ks[-1], 0)] if 0 in caps else []
    if family == "F1":
        return [(ks[-1], T) for T in caps]
    if family == "F2":
        return [(ks[-2], T) for T in caps] if len(ks) > 1 else []
    return [(k, T) for k in ks for T in caps]

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
    """Return whether a predicted accuracy margin clears c_gate times its own SD.

    One rule, shared by the per-prompt gate above and by the average-budget gate, which measures
    its margin between two whole policies rather than between two cells. A margin or an SD that is
    not a number never passes, so a margin the data cannot support leaves normal operation alone.
    """
    m, s = float(margin), float(sd)
    if np.isnan(m) or np.isnan(s):
        return False
    return bool(m > float(c_gate) * s)


def gate_constant(c_gate=DEFAULT_C_GATE, one_se=False):
    """Return the number of SDs of margin the gate demands: c_gate, or 1.0 under one_se.

    The one-standard-error rule is the conventional conservative choice: it asks the deviation to
    be a whole standard error clear of the fallback before it is taken, rather than half of one.
    """
    return ONE_SE_C_GATE if one_se else float(c_gate)


def paired_margin_sd(arm, ref, n_boot=GATE_BOOT, seed=7):
    """Return the bootstrap SD of the PAIRED mean accuracy margin arm - ref, in accuracy fractions.

    The questions are resampled with replacement and both arms are read on the same resample, so
    the spread is the spread of the difference and not the sum of two independent spreads. A pair
    with fewer than two defined differences has no measurable spread and comes back NaN, which
    `gate_passes` refuses.
    """
    d = np.asarray(arm, float) - np.asarray(ref, float)
    d = d[~np.isnan(d)]
    if len(d) < 2:
        return float("nan")
    rng = np.random.default_rng(int(seed))
    idx = rng.integers(0, len(d), (int(n_boot), len(d)))
    return float(d[idx].mean(axis=1).std())


class MeasuredGate(object):
    """Choose the candidate cell only when its MEASURED margin over the fallback clears the bar.

    The margin is the paired accuracy difference between the two cells over the VERIFICATION
    questions -- those questions' own labels -- and the bar is c_gate times a paired bootstrap SD
    of that same difference. Nothing here is predicted: `Gate` above reads its margin off the
    fitted surface A_hat, so where the equation's assumption fails the gate is told the deviation
    is worth points it does not have, and opens. This gate can only be told what the questions
    measured.

    `acc` is (depth, cap, verification question) measured accuracy, 1 or 0 per question, NaN where
    a question has no label at that cell. A pair with fewer than two defined differences has no
    measurable spread, `paired_margin_sd` returns NaN, and `gate_passes` refuses it, so the
    fallback stands.
    """

    def __init__(self, acc, c_gate=DEFAULT_C_GATE, n_boot=GATE_BOOT, seed=7, pos=None, folds=()):
        self.acc = np.asarray(acc, float)
        # The verification POSITIONS behind `acc`, when the caller has them. The structured
        # deviation families need to run a whole policy over those same questions, which needs
        # their prompt lengths and prices, not only their labels.
        self.pos = None if pos is None else np.asarray(pos, dtype=int)
        # Extra FOLDS a deviation must also clear (GATE_FOLDS). Each is another MeasuredGate over a
        # disjoint set of questions -- under two folds, the selection half's own labels -- and
        # `choose` opens only where every one of them clears the bar. The cell pair being ruled on
        # comes from the fold-1 order, so the extra fold tightens the bar; it never loosens it.
        self.folds = [(f if isinstance(f, MeasuredGate)
                       else MeasuredGate(f[0], c_gate=c_gate, n_boot=n_boot, seed=seed,
                                         pos=(f[1] if len(f) > 1 else None)))
                      for f in folds]
        self.n_calls = 0
        self.n_opened = 0
        if self.acc.ndim != 3:
            raise ValueError("the measured gate needs a (depth, cap, question) accuracy block, "
                             "got shape %r" % (self.acc.shape,))
        if self.acc.shape[2] < 2:
            raise ValueError("the measured gate needs at least two verification questions, got %d"
                             % self.acc.shape[2])
        self.c_gate = float(c_gate)
        self.n_boot = int(n_boot)
        self.seed = int(seed)
        self.seen = {}

    @property
    def n_verification(self):
        """Return how many verification questions every margin below is measured on."""
        return int(self.acc.shape[2])

    def measure(self, pick, normal):
        """Return (paired mean margin, paired bootstrap SD) for one cell pair, accuracy fractions.

        Cached: the per-prompt policy asks about the same handful of pairs once per prompt and
        budget, and the bootstrap behind each SD is the expensive part.
        """
        key = (tuple(pick), tuple(normal))
        if key not in self.seen:
            arm = self.acc[pick[0], pick[1]]
            ref = self.acc[normal[0], normal[1]]
            self.seen[key] = (_nanmean(arm - ref),
                              paired_margin_sd(arm, ref, n_boot=self.n_boot, seed=self.seed))
        return self.seen[key]

    def reset_counts(self):
        """Zero the decision counters, so a caller can read one budget's decisions on their own."""
        self.n_calls = self.n_opened = 0

    def choose(self, pick, normal):
        """Return a chosen (depth index,cap index) pair and reversion flag; same contract as `Gate`."""
        if normal is None:
            return pick, False
        if pick is None or pick == normal:
            return normal, False
        self.n_calls += 1
        margin, sd = self.measure(pick, normal)
        ok = gate_passes(margin, sd, self.c_gate)
        for g in self.folds:
            ok = ok and gate_passes(*g.measure(pick, normal), c_gate=self.c_gate)
        if ok:
            self.n_opened += 1
            return pick, False
        return normal, True

    @property
    def n_folds(self):
        """Return how many disjoint question sets a deviation has to clear."""
        return 1 + len(self.folds)

    def decisions(self):
        """Return one record per cell pair the gate ruled on, margins and SDs in percentage points.

        Under more than one fold the record carries each further fold's own margin and SD beside the
        first's, and `opened` is the conjunction: every fold had to clear its own bar.
        """
        out = []
        for (p, n), (m, s) in sorted(self.seen.items()):
            ok = gate_passes(m, s, self.c_gate)
            folds = []
            for g in self.folds:
                fm, fs = g.measure(p, n)
                ok = ok and gate_passes(fm, fs, self.c_gate)
                folds.append({"margin_pts": (100 * fm if fm == fm else None),
                              "sd_pts": (100 * fs if fs == fs else None),
                              "bar_pts": (100 * self.c_gate * fs if fs == fs else None),
                              "opened": bool(gate_passes(fm, fs, self.c_gate)),
                              "n_verification": g.n_verification})
            out.append({"pick": list(p), "normal": list(n),
                        "margin_pts": (100 * m if m == m else None),
                        "sd_pts": (100 * s if s == s else None),
                        "bar_pts": (100 * self.c_gate * s if s == s else None),
                        "opened": bool(ok), "n_verification": self.n_verification,
                        "n_folds": self.n_folds,
                        "folds": (folds or None)})
        return out


# ---------------------------------------------------------------- per-prompt policy
def policy_vectors(cells, ev_pos, cost, Xs, order, gate=None, picks=None):
    """Return paired policy/normal accuracy vectors and reversion fractions per layer-token budget; preserve infeasible prompts as NaN.

    `picks`, when a list is passed, receives one tuple per budget of four int arrays over
    `ev_pos`: the picked (depth index, cap index) after the gate, then normal operation's,
    -1 where that prompt could afford no cell. These are the picks the accuracy vectors were
    read at, so a caller that records them records the policy exactly.
    """
    ki = {k: i for i, k in enumerate(cells.ks)}
    bi = {b: i for i, b in enumerate(cells.caps)}
    kmax = cells.ks[-1]
    order_idx = [(ki[k], bi[T], k, T) for k, T in order]
    out, reverted = [], []
    for X in Xs:
        pv, nv, rev = [], [], 0
        pa, pb, na, nb = [], [], [], []
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
            pa.append(pick[0] if pick is not None else -1)
            pb.append(pick[1] if pick is not None else -1)
            na.append(normal[0] if normal is not None else -1)
            nb.append(normal[1] if normal is not None else -1)
        out.append((np.array(pv, float), np.array(nv, float)))
        reverted.append(rev / max(1, len(ev_pos)))
        if picks is not None:
            picks.append((np.array(pa, int), np.array(pb, int), np.array(na, int), np.array(nb, int)))
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
# The resolved-identity average-budget arms, kept in their own tuple so the frozen v5 set above
# still names exactly the three arms it named. `AVG_ARMS` is what a table reports.
AVG_RANKINGS_RESOLVED = ("avg_equation_resolved", "avg_gated_equation_resolved")
# Ruling of record (2026-09-18): the RANKING OF RECORD is the settle-time-resolved commitment
# identity. Over the 60 pairs of work/analysis_2026-09-18/equation_v6 it is statistically
# indistinguishable from the lookup on 58 of them, and it is the one the mechanism justifies: the
# lookup is a table of measured cell means with no account of WHEN a question commits, so it can only
# repeat what the calibration labels happened to say. The lookup stays as the LABEL-ONLY BASELINE
# the resolved arm is read against, so those two lead every report, in that order, and every other
# arm is still available.
RANKING_OF_RECORD = "equation_resolved"
AVG_ARM_OF_RECORD = "avg_gated_equation_resolved"
AVG_ARM_BASELINE = "avg_gated_lookup"
# The reporting ORDER of the average-budget arms; neither set above moves.
AVG_ARMS = (AVG_ARM_OF_RECORD, AVG_ARM_BASELINE) + tuple(
    n for n in AVG_RANKINGS + AVG_RANKINGS_RESOLVED
    if n not in (AVG_ARM_OF_RECORD, AVG_ARM_BASELINE))
# Which ranking supplies the per-cell score of each average-budget arm. `avg_gated_lookup` scores
# like `avg_lookup` and then has to clear a gate against running the default cell for every prompt.
AVG_BASE = {"avg_lookup": "lookup", "avg_equation": "equation", "avg_gated_lookup": "lookup",
            "avg_equation_resolved": "equation_resolved",
            "avg_gated_equation_resolved": "equation_resolved"}
AVG_GATED = "avg_gated_lookup"
# Every average-budget arm whose deviation has to clear the gate before it is run.
AVG_GATED_ARMS = ("avg_gated_lookup", "avg_gated_equation_resolved")
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
                    # the picks the two vectors above were read at, so a record IS the policy
                    "k_idx": np.asarray(a, int), "cap_idx": np.asarray(b, int),
                    "cells_used": counts})
    return out
