"""The average-budget gate's reference: NORMAL OPERATION AT THE BUDGET, not only the default cell.

The defect this pins: below the default cell's own mean price the gate did not run at all. The
reference was "the default cell for every prompt", and where that cell is unaffordable ON AVERAGE
there was nothing to revert to, so the average-budget pick stood UNGATED at exactly the budgets
where the deviation is largest. On the cluster that produced five of the seven evaluation losses,
four of them on BBH.

The rule now: the reference at budget X is normal operation at that budget -- the deepest depth at
the largest cap per prompt whose mean price fits X, stepping down a depth if even the cheapest cap
at the deepest depth does not fit. Where the default cell IS affordable on average the same rule
returns the default cell for every prompt, so nothing about a row that already gated changes.

The plant below is the BBH shape: a cheap shallow cell is right on the 70 selection questions and
wrong on everything after them, so the fitted score buys it and the verification half says so.

  python -m pytest tests/alloc/test_gate_reference.py -q
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np                                    # noqa: E402

from alloc import cells as C                          # noqa: E402
from alloc import evaluate as E                       # noqa: E402
from alloc import policy as P                         # noqa: E402

KS = [1, 2, 4]
CAPS = [64, 512]
STOP = 400                     # every chain stops here, so cap 512 is the natural-stop column
TASK = "gsm8k"
N, N_CAL, N_SEL = 300, 100, 70
ONE = E.BUDGET_FRACTIONS.index(1.0)
HALF = E.BUDGET_FRACTIONS.index(0.5)
QUARTER = E.BUDGET_FRACTIONS.index(0.25)

# The plant. On the SELECTION questions (ids 0..69) the cheap shallow cell is right 90% of the
# time and the deep cells are not; from id 70 on -- the verification half and every evaluation
# question -- it is right 10% and the deep cells are right 90/95%. A score fitted on the selection
# half therefore buys (1, 64) at every budget, and it is 80 points behind normal operation on
# questions that took no part in fitting it.
ACC_SELECT = {(1, 64): 0.9, (1, 512): 0.9, (2, 64): 0.3, (2, 512): 0.3, (4, 64): 0.2, (4, 512): 0.3}
ACC_AFTER = {(1, 64): 0.1, (1, 512): 0.1, (2, 64): 0.3, (2, 512): 0.3, (4, 64): 0.9, (4, 512): 0.95}


def plant_rows():
    """Rows whose prompt lengths are short enough that depth 4 at cap 64 fits half the default
    cost on average while depth 4 at natural stop does not."""
    reserve = C.answer_budget(TASK)
    out = []
    for i in range(N):
        ptok = 120 + 20 * (i % 5)
        acc = ACC_SELECT if i < N_SEL else ACC_AFTER
        for k in KS:
            for T in CAPS:
                right = (i % 100) < int(round(100 * acc[(k, T)]))
                out.append({"idx": i, "k": k, "B": T,
                            "split": "cal" if i < N_CAL else "eval", "task": TASK,
                            "correct": right, "correct_v2": right,
                            "pred": ("A%d" % k) if T == CAPS[-1] else ("B%d" % k),
                            "gold": ("A%d" % k) if right else "Z",
                            "trace_answer": None, "trace_correct": False,
                            "n_cut": min(T, STOP), "natural_stop": STOP,
                            "n_generated": min(T, STOP) + reserve,
                            "n_prompt_tokens": ptok, "n_suffix_tokens": 4,
                            "n_answer_tokens": 3})
    return out


_CACHE = {}


def grid():
    if "cells" not in _CACHE:
        _CACHE["cells"] = C.Cells(plant_rows(), TASK, name="planted", ks=KS, caps=CAPS)
    return _CACHE["cells"]


def table(accounting="cap", c_gate=P.DEFAULT_C_GATE):
    key = ("t1", accounting, c_gate)
    if key not in _CACHE:
        _CACHE[key] = E.table1(grid(), accounting=accounting, avg_budget=True,
                               n_labels_grid=(10,), gate_draws=4, n_boot=40, c_gate=c_gate)
    return _CACHE[key]


class TestTheFixtureIsTheDefectsShape(unittest.TestCase):
    def test_the_default_cell_is_unaffordable_on_average_at_half_the_default_cost(self):
        t1 = table()
        self.assertFalse(t1["rows"]["default_cell"]["affordable_on_average"][HALF])
        self.assertFalse(t1["rows"]["default_cell"]["affordable_on_average"][QUARTER])

    def test_normal_operation_at_half_is_the_deepest_depth_with_the_cap_stepped_down(self):
        cs = grid()
        cost = P.cost_of(cs, accounting="cap")
        cal, ev = cs.select("cal"), cs.select("eval")
        X = 0.5 * E.default_cost(cs)["mean"]
        info = E.normal_at_budget(cs, P.price_tensor(cs, cal[:N_SEL], cost), X, E.default_cell(cs))
        self.assertEqual((info["rule"], cs.ks[info["k"]]), ("deepest_depth_capped", 4))
        _a, _b, rec = E.reference_record(cs, info, ev, P.price_tensor(cs, ev, cost))
        self.assertEqual(rec["reference_cells"], {"k4_T64": len(ev)})
        self.assertLessEqual(rec["reference_mean_price"], X * (1 + P.AVG_TOL))


class TestTheGateRunsBelowTheDefaultCell(unittest.TestCase):
    """The fix: at 0.5x the gate has a reference, measures the margin on the verification half,
    and sends the losing deviation back to normal operation at that budget."""

    def test_the_gate_measures_a_margin_where_it_used_to_have_none(self):
        row = table()["rows"][P.AVG_GATED]
        self.assertIsNotNone(row["gate_margin_pts"][HALF])
        self.assertIsNotNone(row["gate_sd_pts"][HALF])
        self.assertLess(row["gate_margin_pts"][HALF], 0.0)

    def test_the_gated_arm_reverts_to_normal_at_budget_and_the_ungated_one_does_not(self):
        t1 = table()
        gated, plain = t1["rows"][P.AVG_GATED], t1["rows"]["avg_lookup"]
        self.assertTrue(gated["gate_reverted"][HALF])
        self.assertEqual(gated["reference_rule"][HALF], "deepest_depth_capped")
        self.assertEqual(gated["reference_k"][HALF], 4)
        self.assertEqual(gated["cells_used"][HALF], {"k4_T64": t1["n_eval"]})
        self.assertEqual(gated["reference_cells"][HALF], {"k4_T64": t1["n_eval"]})
        # the reverted row IS normal operation at that budget, and the ungated pick is far below it
        self.assertAlmostEqual(gated["acc_pts"][HALF], 90.0, places=6)
        self.assertAlmostEqual(plain["acc_pts"][HALF], 10.0, places=6)
        self.assertGreater(gated["acc_pts"][HALF] - plain["acc_pts"][HALF], 50.0)

    def test_the_reverted_row_holds_the_budget_on_average(self):
        t1, row = table(), table()["rows"][P.AVG_GATED]
        self.assertFalse(row["over_budget"][HALF])
        self.assertLessEqual(row["mean_price_layer_passes"][HALF],
                             t1["budgets"][HALF] * (1 + P.AVG_TOL))

    def test_the_reference_steps_down_a_depth_when_the_deepest_one_cannot_be_afforded(self):
        """At 0.25x not even cap 64 at depth 4 fits on average, so the rule steps down to depth 2."""
        row = table()["rows"][P.AVG_GATED]
        self.assertEqual(row["reference_rule"][QUARTER], "shallower_depth")
        self.assertEqual(row["reference_k"][QUARTER], 2)
        self.assertTrue(row["gate_reverted"][QUARTER])
        self.assertEqual(row["cells_used"][QUARTER], {"k2_T64": table()["n_eval"]})

    def test_vs_fallback_is_read_against_the_reference_and_not_the_default_cell(self):
        row = table()["rows"][P.AVG_GATED]
        self.assertEqual(row["fallback"], "normal_at_budget")
        # reverted: the arm IS its fallback, so the paired difference is exactly zero
        self.assertAlmostEqual(row["vs_fallback"][HALF]["mean_pts"], 0.0, places=6)


class TestTheDefaultCellReferenceIsUnchanged(unittest.TestCase):
    """Where the default cell is affordable on average the rule returns it, so a row that gated
    before the fix gates against the same thing after it."""

    def test_at_one_times_under_expected_accounting_the_reference_is_the_default_cell(self):
        t1 = table(accounting="expected")
        row = t1["rows"][P.AVG_GATED]
        self.assertTrue(t1["rows"]["default_cell"]["affordable_on_average"][ONE])
        self.assertEqual(row["reference_rule"][ONE], "default_cell")
        self.assertTrue(row["gate_reverted"][ONE])
        self.assertEqual(row["cells_used"][ONE], {"k4_T512": t1["n_eval"]})
        self.assertAlmostEqual(row["acc_pts"][ONE], t1["rows"]["default"]["acc_pts"][ONE],
                               places=6)

    def test_a_budget_nothing_fits_still_has_a_reference(self):
        """No gated arm may ever return an ungated pick, so a budget below every cell's price
        still has a reference: the cheapest cell of the shallowest depth, flagged as over budget."""
        cs = grid()
        cost = P.cost_of(cs, accounting="cap")
        info = E.normal_at_budget(cs, P.price_tensor(cs, cs.select("cal"), cost), 1.0,
                                  E.default_cell(cs))
        self.assertEqual((info["rule"], cs.ks[info["k"]]), ("cheapest_over_budget", 1))
        self.assertFalse(info["affordable_on_average"])


class TestTheCheaperEvaluationHalf(unittest.TestCase):
    """arc/ouro_2_6b_base at 1.0x: the default cell is over the budget on the CALIBRATION mean price
    and under it on the evaluation mean, because the calibration questions are the dearer ones. The
    affordability test reads the calibration mean, so the gate was skipped and the row stood ungated
    and lost 1.81 points. The reference must exist whatever that test says, and both mean prices
    must be on the row."""

    @staticmethod
    def rows():
        """The same plant with the calibration questions 10 percent dearer than the evaluation
        ones, which is the only difference that produced the arc loss."""
        out = []
        for r in plant_rows():
            r = dict(r)
            if r["split"] == "cal":
                r["n_prompt_tokens"] = int(round(1.10 * r["n_prompt_tokens"]))
            out.append(r)
        return out

    @classmethod
    def setUpClass(cls):
        cs = C.Cells(cls.rows(), TASK, name="planted_arc", ks=KS, caps=CAPS)
        # `expected` accounting prices the natural-stop cap at its realised length, which is what
        # puts the default cell either side of 1.0x on the two halves.
        cls.t1 = E.table1(cs, accounting="expected", avg_budget=True, n_labels_grid=(10,),
                          gate_draws=4, n_boot=40, c_gate=P.DEFAULT_C_GATE)
        cls.row = cls.t1["rows"][P.AVG_GATED]

    def test_the_fixture_has_the_arc_price_gap(self):
        r = self.row
        self.assertGreater(r["default_cell_mean_price_cal"][ONE],
                           r["default_cell_mean_price_eval"][ONE])
        self.assertFalse(r["default_cell_affordable_on_cal"][ONE])
        self.assertTrue(r["default_cell_affordable_on_eval"][ONE])

    def test_the_gate_still_runs_and_the_row_is_not_an_ungated_pick(self):
        r, plain = self.row, self.t1["rows"]["avg_lookup"]
        self.assertIsNotNone(r["gate_margin_pts"][ONE])
        # the default cell does not fit the calibration mean, so the reference is one of the
        # two normal-operation candidates, whichever reads better on the fitting half
        self.assertEqual(r["reference_rule"][ONE], "default_at_budget")
        self.assertEqual(r["reference_k"][ONE], KS[-1])
        self.assertTrue(r["gate_reverted"][ONE])
        self.assertGreater(r["acc_pts"][ONE], plain["acc_pts"][ONE])

    def test_every_budget_has_a_reference_recorded(self):
        for j in range(len(self.t1["fractions"])):
            self.assertIsNotNone(self.row["reference_rule"][j], j)
            self.assertIsNotNone(self.row["gate_margin_pts"][j], j)
            self.assertIsNotNone(self.row["reference_cells"][j], j)


class TestTheRecordSaysWhichRuleApplied(unittest.TestCase):
    def test_the_picks_block_carries_the_rule_and_the_reference_cells(self):
        t1 = E.table1(grid(), accounting="cap", avg_budget=True, n_labels_grid=(10,),
                      gate_draws=4, n_boot=40, c_gate=P.DEFAULT_C_GATE)
        entry = t1["picks"]["arms"][P.AVG_GATED][HALF]
        ref = entry["gate"]["reference"]
        self.assertEqual(ref["rule"], "deepest_depth_capped")
        self.assertEqual(ref["k"], 4)
        self.assertEqual(ref["cells"], {"k4_T64": t1["picks"]["n_eval"]})
        self.assertLessEqual(ref["mean_price"], entry["budget"] * (1 + P.AVG_TOL))

    def test_the_table_note_names_the_reference_and_the_rule(self):
        md = E.table1_markdown(table())
        self.assertIn("normal operation at the budget", md.lower())
        self.assertIn("deepest_depth_capped", md)
        self.assertIn("k4_T64", md)


if __name__ == "__main__":
    unittest.main()
