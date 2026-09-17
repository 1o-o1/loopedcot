"""The average budget: hold the MEAN price over prompts at X instead of capping every prompt.

Every other arm applies one budget X to every prompt, so at X set to the default's own mean cost it
can buy the default's cell only for the prompts priced below that mean (0.71 on GSM8K, 0.76 on
MATH500) and is read against `default_at_budget`, not against the default itself. The average
budget is the like-for-like constraint: the default cell for every prompt is then one feasible
policy, so the allocator has a floor to beat, and it beats it by taking a cheaper cell wherever the
score says the cheaper cell is as good and spending the saving where depth is worth buying.

The policy is Lagrangian. For a multiplier lambda >= 0 prompt i takes the cell maximising
score(k,T) - lambda * price_i(k,T); the spend falls as lambda rises, so the multiplier wanted is
the SMALLEST one whose mean price over the CALIBRATION prompts fits X, and bisection finds it.
That multiplier is then applied unchanged to the evaluation prompts, whose realised mean price is
therefore a measurement: it can land over X when the prompts either side of the threshold split
differently in the two halves, and `over_budget` says when it ran more than 2 percent over.
"""
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np                                    # noqa: E402

from alloc import cells as C                          # noqa: E402
from alloc import cli                                 # noqa: E402
from alloc import evaluate as E                       # noqa: E402
from alloc import policy as P                         # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S33 = os.path.join(ROOT, "s33_anytime", "artifacts")
# The column of Table 1 at 1.0 of the default cost, located by value: the default fraction set
# grew a 0.75 point and a fixed index would have silently read the wrong budget.
ONE = E.BUDGET_FRACTIONS.index(1.0)


KS = [1, 2, 4]
CAPS = [64, 512]
STOP = 400                     # every chain stops here, so cap 512 is the natural-stop column

# Two planted surfaces. TIE holds one cheap cell at the same score as a dearer one, so the policy
# must take the cheap one and spend what it saves. BEAT puts the best score on a cell cheaper than
# the default cell, so at X = the default cost the policy has somewhere better to spend.
TIE = {(1, 64): 0.3, (1, 512): 0.3, (2, 64): 0.7, (2, 512): 0.7, (4, 64): 0.9, (4, 512): 0.9}
BEAT = {(1, 64): 0.3, (1, 512): 0.4, (2, 64): 0.5, (2, 512): 0.96, (4, 64): 0.6, (4, 512): 0.95}
_CACHE = {}


def two_clusters(i):
    """Return a prompt length: half the prompts are short and cheap to run deep, half are long.

    Without a spread in the prompt length every prompt faces the same price and the average
    constraint collapses onto the per-prompt one; the jitter inside each cluster lets the
    multiplier's threshold cut through a cluster instead of flipping all of it at once.
    """
    return (100 + 20 * (i % 5)) if i % 2 == 0 else (1600 + 200 * (i % 5))


def planted_rows(acc, lengths=two_clusters, n=300, n_cal=100, task="gsm8k", suffix=4):
    """Return rows whose accuracy at each cell is the planted fraction and whose read-out commits
    only at the largest cap, so the equation surface reconstructs the planted one exactly."""
    budget = C.answer_budget(task)
    out = []
    for i in range(n):
        p = lengths(i)
        for k in KS:
            for T in CAPS:
                right = (i % 100) < int(round(100 * acc[(k, T)]))
                out.append({"idx": i, "k": k, "B": T, "split": "cal" if i < n_cal else "eval",
                            "task": task, "correct": right, "correct_v2": right,
                            "pred": ("A%d" % k) if T == CAPS[-1] else ("B%d" % k),
                            "gold": ("A%d" % k) if right else "Z",
                            "trace_answer": None, "trace_correct": False,
                            "n_cut": min(T, STOP), "natural_stop": STOP,
                            "n_generated": min(T, STOP) + budget,
                            "n_prompt_tokens": p, "n_suffix_tokens": suffix,
                            "n_answer_tokens": budget})
    return out


def planted(acc, **kw):
    return C.Cells(planted_rows(acc, **kw), "gsm8k", name="planted", ks=KS, caps=CAPS)


def parts(cells, ranking="avg_lookup", accounting="expected"):
    """Return the pieces the average-budget policy needs: the price, both splits and the scores."""
    cost = P.cost_of(cells, accounting=accounting)
    ev, cal = cells.select("eval"), cells.select("cal")
    Pm, Rm = P.median_point(cells, ev)
    return cost, ev, cal, E.cell_scores(cells, cal, ranking, cost, Pm, Rm)


def uniform_price(cells, cost, pos, k, T):
    """Return the mean price of running one cell for every one of those prompts."""
    return float(np.mean([cost(k, T, cells.ptok[n], cells.reserve[n], n) for n in pos]))


def real(task, ckpt="A0"):
    if (task, ckpt) not in _CACHE:
        _CACHE[(task, ckpt)] = C.load(S33, task, ckpt, L=24, L_fixed=0)
    return _CACHE[(task, ckpt)]


def real_table(task):
    if ("t1", task) not in _CACHE:
        _CACHE[("t1", task)] = E.table1(real(task), accounting="expected", avg_budget=True,
                                        n_labels_grid=(30,), gate_draws=5, n_boot=50)
    return _CACHE[("t1", task)]


class TestThePick(unittest.TestCase):
    """The per-prompt rule: maximise score - lambda * price, ties to the cheaper cell."""

    SCORE = np.array([[0.5, 0.5], [0.9, 0.9]])
    PRICE = np.array([[[10.0, 20.0], [30.0, 40.0]],      # (depth, cap, prompt)
                      [[50.0, 60.0], [70.0, 80.0]]])

    def test_a_tie_in_score_goes_to_the_cheaper_cell(self):
        a, b = P.avg_picks(self.SCORE, self.PRICE, 0.0)
        np.testing.assert_array_equal(a, [1, 1])         # the higher score, at either price
        np.testing.assert_array_equal(b, [0, 0])         # and the cheaper of its two tied cells
        a, b = P.avg_picks(self.SCORE, self.PRICE, 1.0)  # price now swamps the score
        np.testing.assert_array_equal((a, b), ([0, 0], [0, 0]))

    def test_a_cell_without_a_score_is_never_picked(self):
        score = self.SCORE.copy()
        score[1, 0] = np.nan                             # the cell the tie-break would have taken
        a, b = P.avg_picks(score, self.PRICE, 0.0)
        np.testing.assert_array_equal((a, b), ([1, 1], [1, 1]))

    def test_the_spend_falls_as_the_multiplier_rises(self):
        spends = [P.avg_spend(self.SCORE, self.PRICE, lam)
                  for lam in (0.0, 0.001, 0.01, 0.02, 0.05, 1.0)]
        self.assertTrue(all(spends[i + 1] <= spends[i] + 1e-12 for i in range(len(spends) - 1)),
                        spends)
        self.assertAlmostEqual(spends[0], 55.0)          # cell (1,0): (50 + 60) / 2
        self.assertAlmostEqual(spends[-1], 15.0)         # cell (0,0): (10 + 20) / 2

    def test_a_budget_below_the_cheapest_allocation_is_reported_not_hidden(self):
        lam, spend, met = P.lambda_for_budget(self.SCORE, self.PRICE, 5.0)
        self.assertFalse(met)
        self.assertAlmostEqual(spend, 15.0)              # the cheapest cell for every prompt
        self.assertGreater(lam, 0.0)

    def test_an_audit_price_is_refused(self):
        cs = planted(TIE)
        cost = P.cost_of(cs, accounting="realised")
        with self.assertRaises(ValueError):
            P.avg_budget_vectors(cs, cs.select("eval"), cs.select("cal"), cost, [1e6],
                                 np.zeros((len(KS), len(CAPS))))

    def test_an_average_budget_arm_is_not_a_cell_order(self):
        cs = planted(TIE)
        cost, ev, cal, _s = parts(cs)
        Pm, Rm = P.median_point(cs, ev)
        for name in P.AVG_RANKINGS:
            with self.assertRaises(ValueError):
                E.make_order(cs, cal, cost, Pm, Rm, ranking=name)


class TestTheSavingIsSpent(unittest.TestCase):
    """The planted tie: one cheap cell scores what a dearer cell scores, on the TIE surface."""

    def setUp(self):
        self.cs = planted(TIE)
        self.cost, self.ev, self.cal, _ = parts(self.cs)
        # The budget is what running the dear tie cell for every prompt would cost.
        self.X = uniform_price(self.cs, self.cost, self.ev, 2, 512)

    def _run(self, ranking):
        _c, _e, _l, score = parts(self.cs, ranking)
        return P.avg_budget_vectors(self.cs, self.ev, self.cal, self.cost, [self.X], score)[0]

    def test_the_tie_is_taken_cheap_and_the_saving_buys_depth_elsewhere(self):
        for ranking in P.AVG_RANKINGS:
            v = self._run(ranking)
            self.assertNotIn("k2_T512", v["cells_used"], ranking)   # the dearer half of the tie
            self.assertIn("k4_T64", v["cells_used"], ranking)       # bought with what was saved
            self.assertIn("k2_T64", v["cells_used"], ranking)
            self.assertLessEqual(v["mean_price"], self.X * (1 + P.AVG_TOL), ranking)
            self.assertFalse(v["over_budget"], ranking)

    def test_the_depth_goes_to_the_prompts_it_is_cheap_for(self):
        """Depth is bought where it is cheap: every short prompt gets it, and not every long one.

        The threshold is on the price, not on the cluster, so it cuts inside the long cluster: the
        shorter long prompts still clear it. What must hold is the direction -- the prompts that
        get depth are the cheaper ones.
        """
        _c, _e, _l, score = parts(self.cs)
        prices = P.price_tensor(self.cs, self.ev, self.cost)
        lam = self._run("avg_lookup")["lambda"]
        a, _b = P.avg_picks(score, prices, lam)
        deep = np.array([self.cs.ks[i] for i in a]) == 4
        short = self.cs.ptok[self.ev] < 1000
        self.assertTrue(bool(np.all(deep[short])), "every short prompt must get depth 4")
        self.assertTrue(bool((~deep).any()), "the long prompts cannot all afford depth 4")
        self.assertLess(float(self.cs.ptok[self.ev][deep].mean()),
                        float(self.cs.ptok[self.ev][~deep].mean()))

    def test_it_beats_every_single_cell_that_fits_the_same_average(self):
        got = float(np.nanmean(self._run("avg_lookup")["acc"]))
        best = max(float(np.nanmean(self.cs.acc[self.cs.ks.index(k), self.cs.caps.index(T),
                                                self.ev]))
                   for k in KS for T in CAPS
                   if uniform_price(self.cs, self.cost, self.ev, k, T) <= self.X)
        self.assertAlmostEqual(best, 0.70)               # the tie cell is the best one X can buy
        self.assertGreater(got, best + 0.05)

    def test_lambda_is_monotone_in_the_budget(self):
        _c, _e, _l, score = parts(self.cs)
        Xs = np.linspace(0.2, 2.0, 13) * self.X
        V = P.avg_budget_vectors(self.cs, self.ev, self.cal, self.cost, Xs, score)
        lams = [v["lambda"] for v in V]
        self.assertTrue(all(lams[i + 1] <= lams[i] + 1e-18 for i in range(len(lams) - 1)), lams)
        self.assertGreater(lams[0], 0.0)
        self.assertEqual(lams[-1], 0.0)                  # a budget wide enough needs no multiplier
        spends = [v["mean_price"] for v in V]
        self.assertTrue(all(spends[i + 1] >= spends[i] - 1e-9 for i in range(len(spends) - 1)),
                        spends)


class TestAtTheDefaultCost(unittest.TestCase):
    """Fraction 1.0: the default cell for every prompt is feasible, so the policy must match it."""

    def _table(self, cells, avg_budget=True):
        return E.table1(cells, accounting="expected", avg_budget=avg_budget,
                        n_labels_grid=(10,), gate_draws=3, n_boot=50)

    def test_the_policy_is_never_below_the_default_row_at_one_times(self):
        for surface in (TIE, BEAT):
            t1 = self._table(planted(surface))
            default = t1["rows"]["default"]["acc_pts"][ONE]
            for arm in P.AVG_RANKINGS:
                self.assertGreaterEqual(t1["rows"][arm]["acc_pts"][ONE], default - 1e-9,
                                        "%s on %s" % (arm, sorted(surface.items())[:1]))

    def test_a_cheaper_cell_that_scores_better_is_bought_instead(self):
        t1 = self._table(planted(BEAT))
        row = t1["rows"]["avg_lookup"]
        self.assertGreater(row["acc_pts"][ONE], t1["rows"]["default"]["acc_pts"][ONE])
        self.assertEqual(list(row["cells_used"][ONE]), ["k2_T512"])
        self.assertLess(row["mean_price_layer_passes"][ONE], t1["budgets"][ONE])
        self.assertEqual(row["lambda"][ONE], 0.0)        # the budget never binds here
        self.assertGreater(row["cost_saving_pct"][ONE], 1.0)

    def test_the_rows_carry_both_paired_comparisons(self):
        t1 = self._table(planted(BEAT))
        for arm in P.AVG_RANKINGS:
            row = t1["rows"][arm]
            self.assertIsNotNone(row["vs_default"][ONE]["mean_pts"])
            self.assertIsNotNone(row["vs_default_at_budget"][ONE]["mean_pts"])
            self.assertNotIn("gain_mean_pts", row)       # gain over normal is not defined here

    def test_the_arms_appear_only_when_they_are_asked_for(self):
        cs = planted(BEAT)
        off = self._table(cs, avg_budget=False)
        self.assertFalse(off["avg_budget"])
        for arm in P.AVG_RANKINGS:
            self.assertNotIn(arm, off["rows"])
        self.assertNotIn("avg_lookup", E.table1_markdown(off))
        on = self._table(cs)
        self.assertTrue(on["avg_budget"])
        md = E.table1_markdown(on)
        self.assertIn("| avg_lookup |", md)
        self.assertIn("Realised mean price", md)

    def test_an_audit_price_leaves_the_rows_out(self):
        t1 = E.table1(planted(BEAT), accounting="realised", avg_budget=True,
                      n_labels_grid=(10,), gate_draws=3, n_boot=20)
        self.assertFalse(t1["avg_budget"])
        self.assertNotIn("avg_lookup", t1["rows"])


class TestCli(unittest.TestCase):
    @staticmethod
    def _run(argv):
        with contextlib.redirect_stdout(io.StringIO()):
            return cli.main(argv)

    def _write(self, d):
        for k in KS:
            with open(os.path.join(d, "cells_gsm8k_SYN_k%d.jsonl" % k), "w",
                      encoding="utf-8") as fh:
                for r in planted_rows(BEAT, n=120, n_cal=40):
                    if r["k"] == k:
                        fh.write(json.dumps(r) + "\n")

    def test_the_flag_adds_the_rows_and_nothing_else_does(self):
        with tempfile.TemporaryDirectory() as d:
            self._write(d)
            base = ["--cells", d, "--task", "gsm8k", "--checkpoint", "SYN",
                    "--layers-per-loop", "24", "--fixed-layers", "0",
                    "--accounting", "expected", "--boot", "5", "--cal-draws", "1"]
            off = self._run(base + ["--out", os.path.join(d, "off")])
            self.assertFalse(off["avg_budget"])
            self.assertNotIn("avg_lookup", off["table1"]["rows"])
            out = os.path.join(d, "on")
            on = self._run(base + ["--out", out, "--avg-budget"])
            self.assertTrue(on["avg_budget"])
            for arm in P.AVG_RANKINGS:
                row = on["table1"]["rows"][arm]
                self.assertEqual(len(row["acc_pts"]), len(E.BUDGET_FRACTIONS))
                self.assertEqual(len(row["mean_price_over_X_pct"]), len(E.BUDGET_FRACTIONS))
            with open(os.path.join(out, "table1_expected.md"), encoding="utf-8") as fh:
                self.assertIn("| avg_equation |", fh.read())


@unittest.skipUnless(os.path.isdir(S33), "the cell files are not on this machine")
class TestRealGrids(unittest.TestCase):
    """GSM8K and MATH500 A0, 24 layers per loop and no fixed layers, expected accounting."""

    TASKS = ("gsm8k", "math500")
    # One row runs over the 2 percent bar. The multiplier is fitted so that the CALIBRATION mean
    # price is as close under X as a step function allows, so whether the evaluation mean lands
    # over or under X is decided by how the prompts either side of the threshold split between the
    # two halves; at 0.25x on MATH500 the two cells in play are 24 and 48 layers per token with a
    # 512-token chain between them, so one prompt crossing moves the mean by about a percent.
    OVER_TWO_PERCENT = {("math500", "avg_equation", 0.25): 2.30,
                        ("math500", "avg_gated_lookup", 0.25): 2.30}

    def test_the_mean_price_holds_within_two_percent_or_is_flagged(self):
        for task in self.TASKS:
            t1 = real_table(task)
            for arm in P.AVG_RANKINGS:
                row = t1["rows"][arm]
                for j, f in enumerate(t1["fractions"]):
                    pct, key = row["mean_price_over_X_pct"][j], (task, arm, f)
                    if key in self.OVER_TWO_PERCENT:
                        self.assertTrue(row["over_budget"][j], key)
                        self.assertAlmostEqual(pct, self.OVER_TWO_PERCENT[key], delta=0.3)
                    else:
                        self.assertLessEqual(pct, 100 * P.AVG_TOL, key)
                        self.assertFalse(row["over_budget"][j], key)

    def test_the_calibration_constraint_is_met_exactly(self):
        """What the multiplier is fitted to is a guarantee, not a measurement."""
        for task in self.TASKS:
            t1 = real_table(task)
            for arm in P.AVG_RANKINGS:
                row = t1["rows"][arm]
                for j in range(len(t1["fractions"])):
                    self.assertTrue(row["constraint_met_on_calibration"][j], (task, arm, j))
                    self.assertTrue(P.affordable(row["cal_mean_price_layer_passes"][j],
                                                 t1["budgets"][j]), (task, arm, j))

    def test_lambda_is_monotone_in_the_budget(self):
        for task in self.TASKS:
            cs = real(task)
            cost, ev, cal, score = parts(cs)
            Xs = np.linspace(0.15, 1.2, 12) * E.default_cost(cs)["mean"]
            lams = [v["lambda"] for v in P.avg_budget_vectors(cs, ev, cal, cost, Xs, score)]
            self.assertTrue(all(lams[i + 1] <= lams[i] + 1e-18 for i in range(len(lams) - 1)),
                            "%s: %s" % (task, lams))

    def test_the_gated_arm_is_not_below_the_default_row_at_one_times(self):
        """At X = the default cost the arm either beats the default row or falls back onto it."""
        for task in self.TASKS:
            t1 = real_table(task)
            row = t1["rows"][P.AVG_GATED]
            default = t1["rows"]["default"]["acc_pts"][ONE]
            self.assertGreaterEqual(row["vs_default"][ONE]["hi95_pts"], 0.0, task)
            self.assertGreaterEqual(row["acc_pts"][ONE], default - 1e-9, task)

    def test_the_gate_reverts_where_the_margin_is_noise_and_not_where_it_is_not(self):
        """Measured on the VERIFICATION half, the 30 calibration ids after the 50 that fit.

        GSM8K: the policy's cheaper cell is 10 points BEHIND the default cell on questions that
        took no part in choosing it, so the arm goes back to the default. MATH500: depth 3 is 16.7
        points ahead of the default cell there against a 7-point SD, so the policy stands and the
        row keeps the accuracy it bought.
        """
        gsm = real_table("gsm8k")["rows"][P.AVG_GATED]
        self.assertTrue(gsm["gate_reverted"][ONE])
        self.assertLessEqual(gsm["gate_margin_pts"][ONE], 0.5 * gsm["gate_sd_pts"][ONE])
        math = real_table("math500")["rows"][P.AVG_GATED]
        self.assertFalse(math["gate_reverted"][ONE])
        self.assertGreater(math["gate_margin_pts"][ONE], 0.5 * math["gate_sd_pts"][ONE])
        self.assertGreater(math["acc_pts"][ONE], real_table("math500")["rows"]["default"]
                           ["acc_pts"][ONE])
        for row in (gsm, math):
            self.assertEqual((row["gate_n_selection"], row["gate_n_verification"]),
                             (P.DEFAULT_N_SELECT, P.DEFAULT_N_VERIFY))

    def test_the_underspend_at_one_times_is_a_saving_not_a_shortfall(self):
        for task in self.TASKS:
            row = real_table(task)["rows"]["avg_equation"]
            self.assertEqual(row["lambda"][ONE], 0.0)
            self.assertGreater(row["cost_saving_pct"][ONE], 1.0, task)
            self.assertAlmostEqual(row["pct_of_default_cost"][ONE],
                                   100.0 - row["cost_saving_pct"][ONE], places=6)

    def test_the_average_budget_beats_the_capped_arms_at_one_times(self):
        """At X = the default cost the average constraint is what makes the comparison fair."""
        for task in self.TASKS:
            t1 = real_table(task)
            capped = t1["rows"]["lookup"]["acc_pts"][ONE]
            normal = t1["rows"]["default_at_budget"]["acc_pts"][ONE]
            avg = t1["rows"]["avg_lookup"]["acc_pts"][ONE]
            self.assertGreater(avg, normal, task)
            if task == "gsm8k":
                self.assertGreater(avg, capped, task)



class TestTheGatedArm(unittest.TestCase):
    """`avg_gated_lookup`: the same policy, but it must earn the deviation from the default cell.

    The margin is read on the calibration prompts, between two whole policies: the mean score over
    the cells the multiplier picks for those prompts against the score of the default cell run for
    every prompt. c_gate scales the SD of that margin over the calibration resamples, so the two
    ends of the constant are what pin the rule down -- at 0 a positive margin is enough, and a
    constant large enough sends every deviation back to the default cell.
    """

    # These two read the gate CONSTANT at its ends, so they hold the fit fixed and use the
    # whole-set gate. The planted rows make correctness a function of `i % 100`, so the first 50
    # calibration ids saturate every cell scoring 0.5 or better and an id-ordered half of THIS
    # fixture is not representative of it; the split rule is exercised on the independent-noise
    # grids in tests/test_split_gate.py instead.
    def _table(self, c_gate):
        return E.table1(planted(BEAT), accounting="expected", avg_budget=True,
                        n_labels_grid=(10,), gate_draws=8, n_boot=30, c_gate=c_gate,
                        gate_mode="whole")

    def test_a_zero_gate_keeps_the_policy_and_a_large_one_reverts(self):
        keep = self._table(0.0)
        row, plain = keep["rows"][P.AVG_GATED], keep["rows"]["avg_lookup"]
        self.assertEqual(row["acc_pts"][ONE], plain["acc_pts"][ONE])
        self.assertFalse(row["gate_reverted"][ONE])

        back = self._table(10.0)
        row = back["rows"][P.AVG_GATED]
        self.assertTrue(row["gate_reverted"][ONE])
        self.assertAlmostEqual(row["acc_pts"][ONE], back["rows"]["default"]["acc_pts"][ONE])
        self.assertEqual(list(row["cells_used"][ONE]), ["k4_T512"])      # the default cell
        self.assertGreater(row["gate_sd_pts"][ONE], 0.0)
        self.assertLess(row["gate_margin_pts"][ONE], 10.0 * row["gate_sd_pts"][ONE])

    def test_below_the_default_cell_there_is_nothing_to_revert_to(self):
        """The fallback has to be affordable on average before the gate can prefer it."""
        row = self._table(10.0)["rows"][P.AVG_GATED]
        for j in range(ONE):
            self.assertFalse(row["gate_reverted"][j], j)
            self.assertIsNone(row["gate_margin_pts"][j], j)
        self.assertEqual(row["acc_pts"][0], self._table(0.0)["rows"]["avg_lookup"]["acc_pts"][0])

    def test_the_underspend_is_reported_as_a_saving(self):
        t1 = self._table(0.0)
        row = t1["rows"]["avg_lookup"]
        self.assertEqual(row["lambda"][ONE], 0.0)
        self.assertAlmostEqual(row["cost_saving_pct"][ONE], 50.0, delta=0.5)
        self.assertAlmostEqual(row["pct_of_default_cost"][ONE], 50.0, delta=0.5)
        md = E.table1_markdown(t1)
        self.assertIn("% of the default cost", md)
        self.assertIn("the multiplier is 0, so the budget never binds", md)

    def test_every_fraction_is_reported(self):
        self.assertEqual(list(E.BUDGET_FRACTIONS), [0.25, 0.5, 0.75, 1.0])
        row = self._table(0.0)["rows"][P.AVG_GATED]
        self.assertEqual(len(row["acc_pts"]), 4)

if __name__ == "__main__":
    unittest.main()
