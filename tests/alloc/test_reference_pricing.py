"""The average-budget gate's reference must be priced with the RUN'S OWN ACCOUNTING.

The invariant this pins. The reference -- "normal operation at this budget, the deepest depth at
the largest cap it affords" -- must not be read off `policy.avg_picks` at a multiplier fitted to the
budget. A Lagrangian pick can only ever name a cell on the UPPER CONVEX HULL of (price, cap), and at
the hull's own slope `avg_picks` breaks the tie to the cheaper cell. Under `cap` accounting the cap
ladder is geometric and every cap sits on that hull, so such a pick reads the largest affordable cap
and agrees. Under `expected` accounting every cap past the mean natural length costs the SAME, so
the middle of the ladder falls off the hull and the pick returns the cheapest cap of the depth --
the worst-case-cap answer, whatever the run is priced under.

On mcleish_llama32_r32/svamp at 1.0x, expected accounting, that reference is depth 8 at cap 0: nine
points, where the same budget affords cap 64 at 67.5. The gated arms then measure a verified +47
against it, open, and land at 51.5 -- sixteen points BELOW the `default_at_budget` row of their own
table, and 17.5 below the uncapped default. Same cause on ouro_1_4b_base/bbh at 0.5x (49.6 against
60.9), ouro_1_4b_base/svamp at 0.5x (44.5 against 53.0) and ouro_2_6b_base/bbh at 1.0x (78.4 against
81.7).

The rule (evaluate.normal_at_budget): three candidates, each priced with the same `policy.Cost`
as the arm, the best of them on the calibration split, and `reference_rule` records which -- the
default cell where its mean price fits, the deepest depth at the largest cap whose MEAN PRICE fits,
and the per-prompt hard cap Table 1 reports as `default_at_budget`. The last of the three is what
makes the invariant below hold: a gated arm may not land below `default_at_budget` by more than the
paired bootstrap interval.

  python -m pytest tests/alloc/test_reference_pricing.py -q
"""
import os
import sys
import unittest
import warnings

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np                                    # noqa: E402

from alloc import cells as C                          # noqa: E402
from alloc import evaluate as E                       # noqa: E402
from alloc import policy as P                         # noqa: E402

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
ARTIFACTS = os.path.join(REPO, "artifacts")
MODEL_CONFIG = os.path.join(REPO, "prod", "config.yaml")

ONE = E.BUDGET_FRACTIONS.index(1.0)

# ---------------------------------------------------------------- the planted grid
# The cap ladder starts at 64, so under `expected` accounting -- where every cap from 256 up costs
# the mean natural length of 200 tokens -- the only cells on the upper convex hull of (price, cap)
# are cap 0 and the natural-stop cap. The natural-stop cap is over the budget at 1.0x because the
# CALIBRATION questions run 200 tokens and the EVALUATION questions, which set the default cost, run
# 150; so the hull leaves cap 0, which a multiplier pick returns at three of the four budgets.
KS = [1, 2, 4]
CAPS = [0, 64, 128, 256, 512, 1024, 2048, 4096]
TASK = "gsm8k"
N, N_CAL, N_SEL = 300, 100, 70
STOP_CAL, STOP_EV = 200, 150
DEEP = KS[-1]

# The trap: on the 70 selection questions cap 64 is the best cell on the grid, and from question 70
# on -- the verification half and every evaluation question -- cap 128 and up are 20 points better.
# A score fitted on the selection half therefore buys cap 64 at every budget it can afford it.
ACC_SELECT = {0: 0.1, 64: 0.9, 128: 0.3, 256: 0.3, 512: 0.3, 1024: 0.3, 2048: 0.3, 4096: 0.3}
ACC_AFTER = {0: 0.1, 64: 0.5, 128: 0.7, 256: 0.7, 512: 0.7, 1024: 0.7, 2048: 0.7, 4096: 0.7}


def plant_rows():
    """Rows for the grid above; correctness is a fixed pattern per block of ten ids, so every
    accuracy below is exact on the selection half, the verification half and the evaluation split."""
    reserve = C.answer_budget(TASK)
    out = []
    for i in range(N):
        stop = STOP_CAL if i < N_CAL else STOP_EV
        table = ACC_SELECT if i < N_SEL else ACC_AFTER
        for k in KS:
            for T in CAPS:
                acc = table[T] if k == DEEP else 0.1
                right = (i % 10) < int(round(10 * acc))
                ncut = min(T, stop)
                out.append({"idx": i, "k": k, "B": T,
                            "split": "cal" if i < N_CAL else "eval", "task": TASK,
                            "correct": right, "correct_v2": right,
                            "pred": ("A%d" % k) if T == CAPS[-1] else ("B%d_%d" % (k, T)),
                            "gold": ("A%d" % k) if right else "Z",
                            "trace_answer": None, "trace_correct": False,
                            "n_cut": ncut, "natural_stop": stop,
                            "n_generated": ncut + reserve,
                            "n_prompt_tokens": 150, "n_suffix_tokens": 4,
                            "n_answer_tokens": reserve})
    return out


_CACHE = {}


def grid():
    if "cells" not in _CACHE:
        _CACHE["cells"] = C.Cells(plant_rows(), TASK, name="planted_pricing", ks=KS, caps=CAPS)
    return _CACHE["cells"]


def table(accounting):
    key = ("t1", accounting)
    if key not in _CACHE:
        _CACHE[key] = E.table1(grid(), promptfree=True, accounting=accounting, avg_budget=True,
                               n_labels_grid=(10,), gate_draws=4, n_boot=200)
    return _CACHE[key]


def hull_reference(cs, fit_prices, X):
    """Return the cap the OLD rule returned: the deepest depth's caps scored by the tokens they buy
    and picked at a multiplier fitted to X, which is `policy.avg_picks` on the convex hull."""
    limits = C.cap_limits(cs)
    rank = np.empty(len(cs.caps), float)
    rank[np.argsort(limits, kind="stable")] = np.arange(len(cs.caps), dtype=float)
    S = np.full((len(cs.ks), len(cs.caps)), np.nan)
    S[len(cs.ks) - 1, :] = rank
    lam, _spend, _met = P.lambda_for_budget(S, fit_prices, X)
    _a, b = P.avg_picks(S, fit_prices, lam)
    return sorted({int(cs.caps[j]) for j in b})


def largest_cap_whose_mean_price_fits(cs, fit_prices, X):
    """Return the cap the rule must return: the largest at the deepest depth whose MEAN price fits."""
    d = len(cs.ks) - 1
    for j in list(np.argsort(C.cap_limits(cs), kind="stable"))[::-1]:
        if P.affordable(float(fit_prices[d, int(j)].mean()), X):
            return int(cs.caps[int(j)])
    return None


def fitting_prices(cs, accounting):
    """Return (selection positions, their price tensor, the four budgets) for the planted grid."""
    cost = P.cost_of(cs, promptfree=True, accounting=accounting)
    sel, _ver, _sizes = E.split_calibration(cs, cs.select("cal"), None, None)
    dc = E.default_cost(cs, True)
    return sel, P.price_tensor(cs, sel, cost), [f * dc["mean"] for f in E.BUDGET_FRACTIONS]


class TestThePlantIsTheDefectsShape(unittest.TestCase):
    """Worst-case pricing picks cap 0; expected pricing affords a long cap."""

    def test_the_hull_leaves_only_cap_zero_under_expected_accounting(self):
        cs = grid()
        sel, prices, Xs = fitting_prices(cs, "expected")
        self.assertEqual(hull_reference(cs, prices, Xs[ONE]), [0])
        self.assertEqual(largest_cap_whose_mean_price_fits(cs, prices, Xs[ONE]), 128)
        # and the long cap is worth 60 points more than the cap 0 the hull returned
        i = len(cs.ks) - 1
        ev = cs.select("eval")
        acc = lambda T: 100 * float(np.nanmean(cs.acc[i, list(cs.caps).index(T), ev]))
        self.assertAlmostEqual(acc(0), 10.0, places=6)
        self.assertAlmostEqual(acc(128), 70.0, places=6)

    def test_the_two_rules_agree_under_cap_accounting(self):
        """The geometric cap ladder is its own convex hull, so nothing about a `cap` run moves."""
        cs = grid()
        _sel, prices, Xs = fitting_prices(cs, "cap")
        for j, X in enumerate(Xs):
            self.assertEqual(hull_reference(cs, prices, X),
                             [largest_cap_whose_mean_price_fits(cs, prices, X)], j)

    def test_the_default_cell_does_not_fit_the_calibration_mean_at_one_times(self):
        self.assertFalse(table("expected")["rows"]["default_cell"]
                         ["affordable_on_average"][ONE])


class TestTheReferenceIsPricedWithTheRunsAccounting(unittest.TestCase):
    def test_the_reference_is_the_long_cap_and_not_cap_zero(self):
        cs = grid()
        sel, prices, Xs = fitting_prices(cs, "expected")
        info = E.normal_at_budget(cs, prices, Xs[ONE], E.default_cell(cs), fit_pos=sel)
        ev = cs.select("eval")
        cost = P.cost_of(cs, promptfree=True, accounting="expected")
        _a, _b, rec = E.reference_record(cs, info, ev, P.price_tensor(cs, ev, cost))
        self.assertEqual(rec["reference_cells"], {"k%d_T128" % DEEP: len(ev)})
        self.assertEqual(rec["reference_k"], DEEP)
        self.assertLessEqual(rec["reference_mean_price"], Xs[ONE] * (1 + P.AVG_TOL))
        self.assertIn(rec["reference_rule"], ("deepest_depth_capped", "default_at_budget"))

    def test_the_row_records_which_rule_the_reference_came_from(self):
        row = table("expected")["rows"][P.AVG_GATED]
        for j in range(len(E.BUDGET_FRACTIONS)):
            self.assertIn(row["reference_rule"][j],
                          ("default_cell", "deepest_depth_capped", "shallower_depth",
                           "default_at_budget", "cheapest_over_budget"), j)
            self.assertIsNotNone(row["reference_cells"][j], j)

    def test_the_losing_deviation_no_longer_opens(self):
        """The arm's cell is 20 points behind the properly priced reference on the verification
        half, so the gate reverts; against cap 0 the same cell would measure +40 and open."""
        t1 = table("expected")
        for name in P.AVG_GATED_ARMS:
            row = t1["rows"][name]
            self.assertTrue(row["gate_reverted"][ONE], name)
            self.assertIsNone(row["deviation_family"][ONE], name)
            self.assertLess(row["gate_margin_pts"][ONE], 0.0, name)
            self.assertAlmostEqual(row["acc_pts"][ONE], 70.0, places=6, msg=name)
        # the ungated arm: what stands where nothing checks the pick
        self.assertAlmostEqual(t1["rows"]["avg_lookup"]["acc_pts"][ONE], 50.0, places=6)


class TestAGatedArmNeverFallsBelowDefaultAtBudget(unittest.TestCase):
    """The invariant: a gated average-budget row may not sit below the `default_at_budget` row of
    its own table by more than the paired bootstrap interval over the evaluation prompts."""

    def check(self, t1, where):
        for name in P.AVG_GATED_ARMS:
            row = t1["rows"][name]
            for j, f in enumerate(t1["fractions"]):
                d = row["vs_default_at_budget"][j]
                if d["mean_pts"] is None:
                    continue
                self.assertGreaterEqual(
                    d["hi95_pts"], 0.0,
                    "%s: %s at %.2fx is %.1f points below default_at_budget, interval "
                    "[%.1f, %.1f]" % (where, name, f, -d["mean_pts"], d["lo95_pts"],
                                      d["hi95_pts"]))

    def test_on_the_planted_grid_under_every_accounting(self):
        for accounting in ("cap", "expected"):
            self.check(table(accounting), "planted/%s" % accounting)


def svamp_available():
    return (os.path.isfile(MODEL_CONFIG) and
            all(os.path.isfile(os.path.join(
                ARTIFACTS, "cells_mcleish_llama32_r32_svamp_natural_k%d.jsonl" % k))
                for k in (1, 2, 4, 8)))


@unittest.skipUnless(svamp_available(), "the production cell files are not on this machine")
class TestTheGridTheDefectWasFoundOn(unittest.TestCase):
    """mcleish_llama32_r32/svamp at 1.0x under `expected` accounting: a hull pick names depth 8 at
    cap 0, nine points, and both gated arms then open against it and land at 51.5. The budget
    affords cap 64, and both the reference and the arms must read at least 67 on evaluation."""

    FLOOR = 67.0

    @classmethod
    def setUpClass(cls):
        L, L_fixed = C.model_geometry("mcleish_llama32_r32", MODEL_CONFIG)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cs = C.load(ARTIFACTS, "svamp", "mcleish_llama32_r32", L=L, L_fixed=L_fixed,
                        protocol="natural")
            n_cal, _why = C.resolve_n_cal(cs, None)
            cs, _rec = C.promote_calibration(cs, n_cal)
            cls.cs = cs
            cls.t1 = E.table1(cs, promptfree=True, accounting="expected", avg_budget=True,
                              n_labels_grid=(30,), gate_draws=8, n_boot=200)

    def test_the_grid_is_the_one_the_cluster_read(self):
        self.assertEqual(list(self.cs.ks), [1, 2, 4, 8])
        self.assertEqual((self.t1["n_eval"], len(self.cs.select("cal"))), (200, 100))

    def test_the_reference_at_one_times_reads_at_least_sixty_seven(self):
        cs = self.cs
        cost = P.cost_of(cs, promptfree=True, accounting="expected")
        sel, _ver, _sizes = E.split_calibration(cs, cs.select("cal"), None, None)
        ev = cs.select("eval")
        X = self.t1["budgets"][ONE]
        info = E.normal_at_budget(cs, P.price_tensor(cs, sel, cost), X, E.default_cell(cs),
                                  fit_pos=sel)
        a, b, rec = E.reference_record(cs, info, ev, P.price_tensor(cs, ev, cost))
        self.assertEqual(rec["reference_k"], 8)
        self.assertNotEqual(rec["reference_cells"], {"k8_T0": len(ev)})   # the low-accuracy cell
        self.assertGreaterEqual(100 * float(np.nanmean(cs.acc[a, b, ev])), self.FLOOR)
        for name in P.AVG_GATED_ARMS:
            self.assertEqual(self.t1["rows"][name]["reference_cells"][ONE],
                             rec["reference_cells"], name)

    def test_both_gated_arms_at_one_times_read_at_least_sixty_seven(self):
        for name in P.AVG_GATED_ARMS:
            self.assertGreaterEqual(self.t1["rows"][name]["acc_pts"][ONE], self.FLOOR, name)

    def test_no_gated_row_sits_below_default_at_budget_beyond_the_interval(self):
        for name in P.AVG_GATED_ARMS:
            row = self.t1["rows"][name]
            for j, f in enumerate(self.t1["fractions"]):
                d = row["vs_default_at_budget"][j]
                if d["mean_pts"] is None:
                    continue
                self.assertGreaterEqual(
                    d["hi95_pts"], 0.0,
                    "%s at %.2fx is %.1f points below default_at_budget, interval [%.1f, %.1f]"
                    % (name, f, -d["mean_pts"], d["lo95_pts"], d["hi95_pts"]))


if __name__ == "__main__":
    unittest.main()
