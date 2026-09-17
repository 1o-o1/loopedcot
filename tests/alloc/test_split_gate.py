"""Split-calibration verification: the gate may not measure its margin on the data that chose the cell.

The old gate picked the best of many cells on one set of calibration labels and then measured that
cell's margin over the default cell on the SAME labels. The maximum of many noisy estimates sits
above the truth by roughly the noise spread times how many cells were in the running, so the margin
the gate read was not the margin the policy had, and `c_gate = 0.5` sd did not cover the gap. That
is the winner's curse, and on the cluster tables it opened the gate on cells that then lost 2 to 5
points while saving 30 to 55 percent of the cost.

The repair cuts the calibration questions in ID ORDER into the first `n_select`, which fit the
ranking and the multiplier, and the next `n_verify`, which measure the margin of what was fitted and
take no part in choosing it. The margin is the paired accuracy difference over those verification
questions against the default cell, and its SD is a paired bootstrap over them.

The grids below plant the two cases the gate has to tell apart:

NULL   eighteen cheap cells whose TRUE accuracy is exactly the default cell's, each measured with
       its own independent noise. Every deviation here is false: the winner is a noise winner.
TRUE   the cheap cap-0 cells are genuinely better, the shape a task like HellaSwag has, where the
       chain buys nothing and the cheapest cell is the right answer. The deviation must survive.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np                                    # noqa: E402

from alloc import cells as C                          # noqa: E402
from alloc import evaluate as E                       # noqa: E402
from alloc import policy as P                         # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S33 = os.path.join(ROOT, "s33_anytime", "artifacts")
ONE = E.BUDGET_FRACTIONS.index(1.0)

KS = [1, 2, 3, 4, 5, 6]
CAPS = [0, 8, 16, 512]
STOP = 400
TASK = "csqa"
DEFAULT_CELL = (KS[-1], CAPS[-1])
N_CAL = 100
_CACHE = {}


def null_surface():
    """Return true accuracies with 18 cheap cells tied to the default cell: every win is noise."""
    s = {(k, T): 0.60 for k in KS for T in CAPS if T != CAPS[-1]}
    s.update({(k, CAPS[-1]): 0.50 for k in KS})
    s[DEFAULT_CELL] = 0.60
    return s


def true_surface():
    """Return true accuracies where cap 0 really is the best cell, by 15 points over the default."""
    s = null_surface()
    for k in KS:
        s[(k, 0)] = 0.75
    return s


def noisy_rows(acc, n=300, n_cal=N_CAL, seed=3, task=TASK):
    """Return rows whose correctness is an INDEPENDENT coin per (question, cell).

    Independence is the point: a planted surface whose tied cells share one deterministic pattern
    has no winner's curse to remove, because every tied cell then measures identically.
    """
    rng = np.random.default_rng(seed)
    budget = C.answer_budget(task)
    out = []
    for i in range(n):
        p = 300 + 20 * (i % 9)
        for k in KS:
            for T in CAPS:
                right = bool(rng.random() < acc[(k, T)])
                out.append({"idx": i, "k": k, "B": T, "split": "cal" if i < n_cal else "eval",
                            "task": task, "correct": right, "correct_v2": right,
                            "pred": ("A%d" % k) if T == CAPS[-1] else ("B%d_%d" % (k, T)),
                            "gold": ("A%d" % k) if right else "Z",
                            "trace_answer": None, "trace_correct": False,
                            "n_cut": min(T, STOP), "natural_stop": STOP,
                            "n_generated": min(T, STOP) + budget,
                            "n_prompt_tokens": p, "n_suffix_tokens": 4,
                            "n_answer_tokens": budget})
    return out


def planted(acc, **kw):
    return C.Cells(noisy_rows(acc, **kw), TASK, name="planted", ks=KS, caps=CAPS)


def table(which, gate_mode, one_se=False, c_gate=P.DEFAULT_C_GATE, n_select=50, n_verify=50):
    key = (which, gate_mode, one_se, c_gate, n_select, n_verify)
    if key not in _CACHE:
        surf = null_surface() if which == "null" else true_surface()
        _CACHE[key] = E.table1(planted(surf), accounting="expected", avg_budget=True,
                               n_labels_grid=(30,), gate_draws=10, n_boot=50, c_gate=c_gate,
                               gate_mode=gate_mode, one_se=one_se, n_select=n_select,
                               n_verify=n_verify)
    return _CACHE[key]


class TestTheSplit(unittest.TestCase):
    """The partition: the first n_select calibration ids fit, the next n_verify verify."""

    def setUp(self):
        self.cs = planted(null_surface(), n=160, n_cal=60)
        self.cal = self.cs.select("cal")

    def test_the_halves_are_the_requested_sizes_and_are_disjoint(self):
        sel, ver, sizes = E.split_calibration(self.cs, self.cal, 40, 15)
        self.assertEqual((sizes["n_selection"], sizes["n_verification"]), (40, 15))
        self.assertFalse(sizes["truncated"])
        self.assertEqual(len(set(sel) & set(ver)), 0)
        self.assertEqual(sizes["n_calibration"], 60)

    def test_the_split_is_taken_in_id_order(self):
        sel, ver, _ = E.split_calibration(self.cs, self.cal, 40, 15)
        ids = [self.cs.idx[n] for n in list(sel) + list(ver)]
        self.assertEqual(ids, sorted(ids))
        self.assertEqual([self.cs.idx[n] for n in sel], list(range(40)))
        self.assertEqual([self.cs.idx[n] for n in ver], list(range(40, 55)))

    def test_both_halves_hold_only_calibration_questions(self):
        sel, ver, _ = E.split_calibration(self.cs, self.cal, 40, 15)
        for pos in list(sel) + list(ver):
            self.assertEqual(self.cs.split[pos], "cal")

    def test_a_short_calibration_split_is_used_entire_and_says_so(self):
        sel, ver, sizes = E.split_calibration(self.cs, self.cal, 100, 20)
        self.assertTrue(sizes["truncated"])
        self.assertEqual(sizes["n_selection"] + sizes["n_verification"], 60)
        self.assertEqual(sizes["requested"], [100, 20])
        self.assertEqual(sizes["n_selection"], 50)       # the 100:20 proportion, kept
        self.assertEqual(len(ver), 10)
        self.assertGreater(len(sel), 0)

    def test_sizes_that_cannot_verify_are_refused(self):
        with self.assertRaises(ValueError):
            E.split_calibration(self.cs, self.cal, 40, 1)
        with self.assertRaises(ValueError):
            E.split_calibration(self.cs, self.cal, 0, 10)
        with self.assertRaises(ValueError):
            E.split_calibration(self.cs, self.cal[:2], 40, 10)


class TestTheVerificationMargin(unittest.TestCase):
    """The margin SD is a PAIRED bootstrap over the verification questions."""

    def test_an_identical_pair_has_no_margin_and_no_spread(self):
        v = np.array([1.0, 0.0, 1.0, 1.0, 0.0] * 8)
        self.assertEqual(P.paired_margin_sd(v, v, n_boot=200, seed=1), 0.0)

    def test_a_real_difference_has_a_positive_spread_and_is_deterministic(self):
        rng = np.random.default_rng(0)
        arm, ref = rng.random(120) < 0.7, rng.random(120) < 0.5
        sd = P.paired_margin_sd(arm, ref, n_boot=300, seed=1)
        self.assertGreater(sd, 0.0)
        self.assertEqual(sd, P.paired_margin_sd(arm, ref, n_boot=300, seed=1))

    def test_too_few_questions_give_no_spread_and_the_gate_stays_shut(self):
        self.assertTrue(np.isnan(P.paired_margin_sd([1.0], [0.0])))
        self.assertFalse(P.gate_passes(0.5, float("nan"), 0.5))

    def test_the_default_is_two_thousand_resamples(self):
        self.assertEqual(P.GATE_BOOT, 2000)

    def test_one_standard_error_raises_the_bar_to_a_whole_sd(self):
        self.assertEqual(P.gate_constant(0.5, one_se=False), 0.5)
        self.assertEqual(P.gate_constant(0.5, one_se=True), 1.0)
        self.assertEqual(P.gate_constant(2.0, one_se=True), 1.0)


class TestTheWinnersCurse(unittest.TestCase):
    """The planted null: 18 cheap cells tie the default cell, so every deviation is false."""

    def test_the_old_gate_opens_on_a_margin_that_is_not_there(self):
        row = table("null", "whole")["rows"][P.AVG_GATED]
        self.assertFalse(row["gate_reverted"][ONE])
        self.assertGreater(row["gate_margin_pts"][ONE], 0.5 * row["gate_sd_pts"][ONE])
        self.assertGreater(row["gate_margin_pts"][ONE], 3.0)          # the bias it reads

    def test_the_split_gate_reverts_to_the_default_cell(self):
        t1 = table("null", "split")
        row = t1["rows"][P.AVG_GATED]
        self.assertTrue(row["gate_reverted"][ONE])
        self.assertLessEqual(row["gate_margin_pts"][ONE], 0.5 * row["gate_sd_pts"][ONE])
        self.assertEqual(list(row["cells_used"][ONE]), ["k%d_T%d" % DEFAULT_CELL])
        self.assertAlmostEqual(row["acc_pts"][ONE], t1["rows"]["default"]["acc_pts"][ONE])

    def test_the_verification_margin_is_far_below_the_whole_set_one(self):
        whole = table("null", "whole")["rows"][P.AVG_GATED]["gate_margin_pts"][ONE]
        split = table("null", "split")["rows"][P.AVG_GATED]["gate_margin_pts"][ONE]
        self.assertLess(split, whole - 3.0)

    def test_the_old_gate_is_still_reachable_under_the_flag(self):
        self.assertEqual(table("null", "whole")["rows"][P.AVG_GATED]["gate_mode"], "whole")
        self.assertEqual(table("null", "split")["rows"][P.AVG_GATED]["gate_mode"], "split")
        self.assertEqual(P.DEFAULT_GATE_MODE, "split")

    def test_an_unknown_mode_is_refused(self):
        cs = planted(null_surface(), n=120, n_cal=60)
        with self.assertRaises(ValueError):
            E.gate_and_fit(cs, cs.select("cal"), None, 0.5, 4, 7, "half")
        with self.assertRaises(ValueError):
            E.table1(cs, avg_budget=True, gate_mode="half", n_labels_grid=(10,), gate_draws=2)


class TestATrueDeviationSurvives(unittest.TestCase):
    """The planted cap-0 optimum: the cheap cell really is 15 points better and must be kept."""

    def test_both_gates_keep_it(self):
        for mode in ("whole", "split"):
            row = table("true", mode)["rows"][P.AVG_GATED]
            self.assertFalse(row["gate_reverted"][ONE], mode)
            self.assertGreater(row["gate_margin_pts"][ONE], 0.5 * row["gate_sd_pts"][ONE], mode)

    def test_the_kept_deviation_buys_the_cheap_cell_and_beats_the_default(self):
        t1 = table("true", "split")
        row = t1["rows"][P.AVG_GATED]
        self.assertTrue(all(key.endswith("_T0") for key in row["cells_used"][ONE]),
                        row["cells_used"][ONE])
        self.assertGreater(row["acc_pts"][ONE], t1["rows"]["default"]["acc_pts"][ONE] + 5.0)
        self.assertGreater(row["cost_saving_pct"][ONE], 30.0)

    def test_the_selection_draws_agree_with_the_verdict(self):
        """A diagnostic, not a second gate: each draw refits on a resample of the SELECTION half
        and remeasures the same verification margin, so the share positive says how much of the
        verdict rests on that half's own luck. A majority here, not a certainty, because fifty
        verification questions measure any one cell loosely."""
        row = table("true", "split")["rows"][P.AVG_GATED]
        self.assertGreater(row["gate_draw_frac_positive"][ONE], 0.5)
        self.assertIsNone(row["gate_draw_frac_positive"][0])   # no fallback, so nothing to draw

    def test_one_standard_error_still_keeps_a_fifteen_point_margin(self):
        row = table("true", "split", one_se=True)["rows"][P.AVG_GATED]
        self.assertFalse(row["gate_reverted"][ONE])
        self.assertEqual(row["gate_c"], 1.0)

    def test_one_standard_error_also_closes_the_null(self):
        row = table("null", "split", one_se=True)["rows"][P.AVG_GATED]
        self.assertTrue(row["gate_reverted"][ONE])


class TestTheHalvesAreReported(unittest.TestCase):
    """Both halves' sizes travel with the row, and the markdown says why the gate opened."""

    def test_the_row_carries_both_sizes(self):
        t1 = table("true", "split")
        for name in (P.AVG_GATED, "gated_equation"):
            row = t1["rows"][name]
            self.assertEqual(row["gate_mode"], "split")
            self.assertEqual(row["gate_n_selection"], 50)
            self.assertEqual(row["gate_n_verification"], 50)
            self.assertFalse(row["gate_split_truncated"])

    def test_the_whole_set_row_reports_one_set_and_no_verification_half(self):
        row = table("true", "whole")["rows"][P.AVG_GATED]
        self.assertEqual(row["gate_mode"], "whole")
        self.assertEqual(row["gate_n_verification"], 0)
        self.assertEqual(row["gate_n_selection"], N_CAL)

    def test_the_markdown_prints_the_margin_and_its_sd_beside_the_saving(self):
        md = E.table1_markdown(table("true", "split"))
        line = [l for l in md.split("\n") if l.startswith("- `%s` at 1.00x" % P.AVG_GATED)
                and "margin" in l]
        self.assertEqual(len(line), 1, md)
        self.assertIn("Verification margin", line[0])
        self.assertIn("sd", line[0])
        self.assertIn("cost saving", line[0])
        self.assertIn("verification questions, the ids after the", line[0])
        self.assertIn("deviated from the default cell", line[0])

    def test_a_reverted_row_says_so_with_the_same_two_numbers(self):
        md = E.table1_markdown(table("null", "split"))
        line = [l for l in md.split("\n") if l.startswith("- `%s` at 1.00x" % P.AVG_GATED)
                and "margin" in l]
        self.assertEqual(len(line), 1, md)
        self.assertIn("reverted to the default cell", line[0])
        self.assertIn("Verification margin", line[0])

    def test_the_table_records_the_mode_it_was_built_under(self):
        t1 = table("true", "split")
        self.assertEqual(t1["gate_mode"], "split")
        self.assertFalse(t1["one_se"])
        self.assertEqual(t1["gate_c"], 0.5)
        self.assertEqual(t1["gate_sizes"]["n_verification"], 50)


class TestTheGatedEquationArm(unittest.TestCase):
    """`gated_equation` is fitted on the selection half and gated on the verification half."""

    def test_the_order_is_fitted_on_the_selection_half_only(self):
        cs = planted(null_surface())
        cal = cs.select("cal")
        sel, ver, _ = E.split_calibration(cs, cal, 50, 50)
        gate, fit_pos, sizes = E.gate_and_fit(cs, cal, None, 0.5, 8, 7, "split",
                                              n_select=50, n_verify=50)
        np.testing.assert_array_equal(fit_pos, sel)
        self.assertEqual(sizes["n_verification"], len(ver))
        # the gate's surface is the verification half's, not the whole set's
        np.testing.assert_allclose(gate.A_hat, E.surface(cs, ver)[0], equal_nan=True)

    def test_the_whole_mode_fits_and_measures_on_everything(self):
        cs = planted(null_surface())
        cal = cs.select("cal")
        gate, pos, sizes = E.gate_and_fit(cs, cal, None, 0.5, 8, 7, "whole")
        np.testing.assert_array_equal(pos, cal)
        self.assertEqual(sizes["n_verification"], 0)
        np.testing.assert_allclose(gate.A_hat, E.surface(cs, cal)[0], equal_nan=True)

    def test_the_arm_still_reports_an_accuracy_at_every_budget(self):
        row = table("null", "split")["rows"]["gated_equation"]
        self.assertEqual(len(row["acc_pts"]), len(E.BUDGET_FRACTIONS))
        self.assertEqual(len(row["gate_reverted_frac"]), len(E.BUDGET_FRACTIONS))

    def test_gain_over_normal_carries_the_mode_and_the_sizes(self):
        cs = planted(null_surface(), n=160, n_cal=60)
        g = E.gain_over_normal(cs, ranking="equation", c_gate=0.5, n_boot=5, n_cal_draws=2,
                               gate_draws=3, n_select=30, n_verify=20)
        self.assertEqual(g["gate_mode"], "split")
        self.assertEqual(g["gate_sizes"]["n_selection"], 30)
        self.assertEqual(g["gate_sizes"]["n_verification"], 20)


class TestTheWholeSetPathIsUnchanged(unittest.TestCase):
    """The old gate is kept for comparison, so its numbers must not move."""

    def test_the_whole_set_gate_matches_the_old_helper(self):
        cs = planted(null_surface(), n=120, n_cal=60)
        cal = cs.select("cal")
        old, _m = E.gate_for(cs, cal, n_labels=None, c_gate=0.5, n_draws=6, seed=7)
        new, pos, _sizes = E.gate_and_fit(cs, cal, None, 0.5, 6, 7, "whole")
        np.testing.assert_allclose(new.A_hat, old.A_hat, equal_nan=True)
        np.testing.assert_allclose(new.sd, old.sd)
        np.testing.assert_array_equal(pos, cal)

    def test_an_ungated_run_is_untouched_by_the_split(self):
        """c_gate = 0 turns the gate off, so no half is taken and the order sees every question."""
        cs = planted(null_surface(), n=120, n_cal=60)
        a = E.gain_over_normal(cs, ranking="lookup", c_gate=0.0, n_boot=3, n_cal_draws=1)
        b = E.gain_over_normal(cs, ranking="lookup", c_gate=0.0, n_boot=3, n_cal_draws=1,
                               gate_mode="whole")
        self.assertEqual(a["gain_mean_pts"], b["gain_mean_pts"])
        self.assertIsNone(a["gate_sizes"])


@unittest.skipUnless(os.path.isdir(S33), "the cell files are not on this machine")
class TestTheRealGrids(unittest.TestCase):
    """S33 cells, 24 layers per loop and no fixed layers, expected accounting, at 1.0x.

    MATH500 A0 is the true deviation: the lookup ranking puts depth 3 at the top and that cheaper
    cell is genuinely better, so its margin survives being measured on labels that did not choose
    it. The reverts are the false deviations the whole-set gate opened.
    """
    TASKS = ("gsm8k", "math500", "svamp", "aqua", "csqa")

    def _table(self, task, ckpt, mode):
        key = ("real", task, ckpt, mode)
        if key not in _CACHE:
            cs = C.load(S33, task, ckpt, L=24, L_fixed=0)
            _CACHE[key] = E.table1(cs, accounting="expected", avg_budget=True,
                                   n_labels_grid=(30,), gate_draws=5, n_boot=30, gate_mode=mode)
        return _CACHE[key]

    def test_math500_a0_keeps_its_deviation_under_both_gates(self):
        for mode in ("whole", "split"):
            row = self._table("math500", "A0", mode)["rows"][P.AVG_GATED]
            self.assertFalse(row["gate_reverted"][ONE], mode)
            self.assertGreater(row["gate_margin_pts"][ONE], 0.5 * row["gate_sd_pts"][ONE], mode)

    def test_the_kept_deviation_is_the_cheaper_depth_three_cell(self):
        row = self._table("math500", "A0", "split")["rows"][P.AVG_GATED]
        self.assertTrue(any(key.startswith("k3_") for key in row["cells_used"][ONE]),
                        row["cells_used"][ONE])
        self.assertGreater(row["cost_saving_pct"][ONE], 10.0)

    def test_a_reverted_grid_lands_exactly_on_the_default_cell(self):
        for task in self.TASKS:
            for ckpt in ("A0", "s33"):
                t1 = self._table(task, ckpt, "split")
                row = t1["rows"][P.AVG_GATED]
                if row["gate_reverted"][ONE]:
                    self.assertEqual(len(row["cells_used"][ONE]), 1, (task, ckpt))
                    self.assertEqual(list(row["cells_used"][ONE])[0],
                                     "k%d_T%d" % tuple(t1["rows"]["default_cell"]["cell"]),
                                     (task, ckpt))

    def test_a_budget_the_default_cell_cannot_buy_has_no_margin_to_report(self):
        """Below the default cell there is no fallback, so the Lagrangian policy stands ungated.

        GSM8K s33 is that case at 1.0x: the default cell does not fit the budget on average, the
        row carries no margin, and the arm is the plain `avg_lookup` policy.
        """
        t1 = self._table("gsm8k", "s33", "split")
        row = t1["rows"][P.AVG_GATED]
        self.assertIsNone(row["gate_margin_pts"][ONE])
        self.assertFalse(row["gate_reverted"][ONE])
        self.assertFalse(t1["rows"]["default_cell"]["affordable_on_average"][ONE])

    def test_the_split_gate_never_opens_where_the_whole_set_gate_shut(self):
        """The verification margin is the stricter reading, so it can only close deviations."""
        for task in self.TASKS:
            for ckpt in ("A0", "s33"):
                whole = self._table(task, ckpt, "whole")["rows"][P.AVG_GATED]
                split = self._table(task, ckpt, "split")["rows"][P.AVG_GATED]
                if whole["gate_reverted"][ONE]:
                    self.assertTrue(split["gate_reverted"][ONE], (task, ckpt))

    def test_every_split_row_reports_the_frozen_two_sizes(self):
        for task in self.TASKS:
            row = self._table(task, "A0", "split")["rows"][P.AVG_GATED]
            self.assertEqual(row["gate_n_selection"], P.DEFAULT_N_SELECT)
            self.assertEqual(row["gate_n_verification"], P.DEFAULT_N_VERIFY)
            self.assertFalse(row["gate_split_truncated"])

    def test_the_frozen_split_is_fifty_and_thirty(self):
        """Swept over 50/50, 100/20 and 50/30 on these ten grids: 100/20 cannot run (every grid
        has exactly 100 calibration ids) and 50/50 closes the MATH500 A0 deviation, which is the
        one true gain in the set."""
        self.assertEqual((P.DEFAULT_N_SELECT, P.DEFAULT_N_VERIFY), (50, 30))
        for task in self.TASKS:
            self.assertEqual(len(C.load(S33, task, "A0", L=24, L_fixed=0).select("cal")), 100)

    def test_fifty_fifty_is_the_setting_that_loses_math500(self):
        cs = C.load(S33, "math500", "A0", L=24, L_fixed=0)
        t1 = E.table1(cs, accounting="expected", avg_budget=True, n_labels_grid=(30,),
                      gate_draws=5, n_boot=30, gate_mode="split", n_select=50, n_verify=50)
        self.assertTrue(t1["rows"][P.AVG_GATED]["gate_reverted"][ONE])


if __name__ == "__main__":
    unittest.main()
