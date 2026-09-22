"""Which of the deviation families that CLEAR the bar is run: policy.GATE_FAMILY_RULE.

v5 to v7 walked the families smallest first and stopped at the FIRST that cleared. That makes the
arm's accuracy non-monotone in the budget, because a small family clearing by a hair is run in place
of a large one clearing by forty points: on the 49 production pairs 36 fall somewhere as the budget
RISES, McLeish/GSM8K from 49.4 to 5.4 near 0.25x where F0 clears first, and Ouro-2.6B Think/GSM8K
stops at F2 for 74.0 at 0.5x where F3 gives 89.7.

`GATE_FAMILY_RULE = "best"` measures every family and runs the cleared one with the largest MEAN
verified margin over the folds, ties to the smaller family. Nothing else moves: the same folds, the
same bar, the same reference, the same pricing, and with no family clearing the arm still reverts.

The plant below separates the two rules. Cap 0 is the cheapest cap and the deepest depth the dearest,
so at the two larger budgets:

  F0 = F1 = the deepest depth at cap 0, planted 20 points over the default cell -- a real edge that
       clears the bar on both folds, and the only one the family ORDER ever reaches;
  F2 = one depth shallower at any cap, planted at the default cell's own accuracy;
  F3 = the free set, which alone can reach the k2 cap-0 cell planted at 0.99 -- cheaper than F0's
       cell and 29 points better.

So "first" runs F0 for 72.5 points and "best" runs F3 for 98.5 at the same budget, off one grid.

  python -m pytest tests/alloc/test_gate_family_rule.py -q
"""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alloc import evaluate as E                        # noqa: E402
from alloc import policy as P                          # noqa: E402

from test_split_gate import KS, CAPS, planted          # noqa: E402

ARMS = ("avg_gated_lookup", "avg_gated_equation_resolved")
# the two budget fractions at which the F0 edge clears the bar on both folds
SPLIT_AT = (0.75, 1.0)
_T1 = {}


def surface(free_cell=0.99):
    """Cap 0 is 20 points over the default cell at the deepest depth, and 49 over it at k2, which
    only the free set can buy. `free_cell` at the default's own accuracy removes the F3 edge."""
    s = {(k, T): 0.50 for k in KS for T in CAPS if T != CAPS[-1]}
    s.update({(k, CAPS[-1]): 0.50 for k in KS})
    s[(KS[-1], 0)] = 0.70                              # F0, and F1's best cell
    s[(KS[1], 0)] = free_cell                          # reachable by F3 alone
    return s


def t1(rule, free_cell=0.99):
    """Table 1 on the plant under one family rule; everything else is the setting of record."""
    key = (rule, free_cell)
    if key not in _T1:
        cs = planted(surface(free_cell))
        with mock.patch.object(P, "GATE_FAMILY_RULE", rule):
            _T1[key] = E.table1(cs, accounting="expected", avg_budget=True, n_labels_grid=(30,),
                                gate_draws=5, n_boot=30, c_gate=P.DEFAULT_C_GATE,
                                gate_mode="split", n_select=50, n_verify=50, families=True)
    return _T1[key]


def at(row, f):
    return list(E.BUDGET_FRACTIONS).index(f)


class TestTheRuleIsDeclared(unittest.TestCase):
    def test_the_two_rules_and_the_new_default(self):
        self.assertEqual(P.GATE_FAMILY_RULES, ("first", "best"))
        self.assertEqual(P.GATE_FAMILY_RULE, "best")

    def test_an_unknown_rule_is_refused_rather_than_guessed(self):
        with mock.patch.object(P, "GATE_FAMILY_RULE", "smallest"):
            with self.assertRaises(ValueError):
                E.table1(planted(surface()), accounting="expected", avg_budget=True,
                         n_labels_grid=(30,), gate_draws=2, n_boot=10, gate_mode="split",
                         n_select=50, n_verify=50, families=True)

    def test_the_table_records_which_rule_produced_it(self):
        for rule in ("first", "best"):
            self.assertEqual(t1(rule)["gate_family_rule"], rule)
            for arm in ARMS:
                self.assertEqual(set(t1(rule)["rows"][arm]["gate_family_rule"]), {rule})


class TestFirstTakesTheSmallFamilyAndBestTakesTheLargeOne(unittest.TestCase):
    """The one plant, the two rules: F0 clears by 20 points, F3 by 49, both on both folds."""

    def test_first_stops_at_F0_and_best_runs_F3(self):
        for arm in ARMS:
            for f in SPLIT_AT:
                j = at(arm, f)
                self.assertEqual(t1("first")["rows"][arm]["deviation_family"][j], "F0", (arm, f))
                self.assertEqual(t1("best")["rows"][arm]["deviation_family"][j], "F3", (arm, f))

    def test_best_buys_the_cell_the_family_order_never_tested(self):
        for arm in ARMS:
            for f in SPLIT_AT:
                j = at(arm, f)
                self.assertEqual(list(t1("first")["rows"][arm]["cells_used"][j]),
                                 ["k%d_T0" % KS[-1]], (arm, f))
                self.assertEqual(list(t1("best")["rows"][arm]["cells_used"][j]),
                                 ["k%d_T0" % KS[1]], (arm, f))

    def test_best_is_worth_twenty_points_here_at_no_more_compute(self):
        for arm in ARMS:
            for f in SPLIT_AT:
                j = at(arm, f)
                a0 = t1("first")["rows"][arm]["acc_pts"][j]
                a1 = t1("best")["rows"][arm]["acc_pts"][j]
                self.assertGreater(a1 - a0, 20.0, (arm, f))
                self.assertLessEqual(t1("best")["rows"][arm]["mean_price_layer_passes"][j],
                                     t1("first")["rows"][arm]["mean_price_layer_passes"][j] + 1e-9)

    def test_first_measures_only_the_families_the_order_reached(self):
        """"first" stops at F0, so nothing larger is measured; "best" measures them all."""
        for arm in ARMS:
            for f in SPLIT_AT:
                j = at(arm, f)
                self.assertEqual(t1("first")["rows"][arm]["gate_family_cleared"][j], ["F0"])
                self.assertIn("F3", t1("best")["rows"][arm]["gate_family_cleared"][j])
                mm = t1("best")["rows"][arm]["gate_family_mean_margin_pts"][j]
                self.assertGreater(mm["F3"], mm["F0"], (arm, f))

    def test_the_folds_the_bar_and_the_reference_are_the_same_test_either_way(self):
        """Only the choice among the cleared families differs, so what a family MEASURED at a budget
        is identical under the two rules wherever both rules measured it."""
        for arm in ARMS:
            for f in SPLIT_AT:
                j = at(arm, f)
                a = t1("first")["rows"][arm]["gate_family_mean_margin_pts"][j]
                b = t1("best")["rows"][arm]["gate_family_mean_margin_pts"][j]
                self.assertTrue(set(a) <= set(b), (arm, f))
                for fam in a:
                    self.assertEqual(a[fam], b[fam], (arm, f, fam))
                self.assertEqual(t1("first")["budgets"][j], t1("best")["budgets"][j])
        for rule in ("first", "best"):
            self.assertEqual(t1(rule)["gate_folds"], 2)
            self.assertEqual(t1(rule)["gate_c"], P.DEFAULT_C_GATE)
            self.assertEqual(t1(rule)["gate_mode"], "split")


class TestATieGoesToTheSmallerFamily(unittest.TestCase):
    """With the free cell planted at the default's own accuracy, every family that clears is
    clearing on the SAME cap-0 cell, so their mean margins tie and the smaller family runs."""

    def test_the_smallest_cleared_family_wins_a_tie(self):
        for arm in ARMS:
            for f in SPLIT_AT:
                j = at(arm, f)
                row = t1("best", free_cell=0.50)["rows"][arm]
                cleared = row["gate_family_cleared"][j]
                mm = row["gate_family_mean_margin_pts"][j]
                self.assertIn("F0", cleared, (arm, f))
                self.assertEqual(row["deviation_family"][j], "F0", (arm, f))
                # F1 can only reach F0's own cell here, so it measured the same margin and lost
                # the tie to the smaller family rather than to a smaller number
                self.assertIn("F1", cleared, (arm, f))
                self.assertEqual(mm["F1"], mm["F0"], (arm, f))

    def test_first_and_best_agree_when_the_smallest_cleared_family_is_the_best_one(self):
        for arm in ARMS:
            a = t1("first", free_cell=0.50)["rows"][arm]
            b = t1("best", free_cell=0.50)["rows"][arm]
            for f in SPLIT_AT:
                j = at(arm, f)
                self.assertEqual(a["deviation_family"][j], b["deviation_family"][j], (arm, f))
                self.assertAlmostEqual(a["acc_pts"][j], b["acc_pts"][j], places=9)


class TestNothingClearingStillReverts(unittest.TestCase):
    """Neither rule can open a deviation no family earned: with nothing cleared the arm reverts to
    normal operation at the budget, which is what the family order did before."""

    def test_no_cleared_family_means_no_deviation_under_either_rule(self):
        for rule in ("first", "best"):
            for free_cell in (0.99, 0.50):
                for arm in ARMS:
                    row = t1(rule, free_cell)["rows"][arm]
                    for j, f in enumerate(E.BUDGET_FRACTIONS):
                        if row["gate_family_cleared"][j]:
                            continue
                        self.assertIsNone(row["deviation_family"][j], (rule, free_cell, arm, f))
                        self.assertTrue(row["gate_reverted"][j], (rule, free_cell, arm, f))

    def test_the_family_that_runs_is_always_one_that_cleared(self):
        for rule in ("first", "best"):
            for free_cell in (0.99, 0.50):
                for arm in ARMS:
                    row = t1(rule, free_cell)["rows"][arm]
                    for j, f in enumerate(E.BUDGET_FRACTIONS):
                        fam = row["deviation_family"][j]
                        if fam is None:
                            continue
                        self.assertIn(fam, row["gate_family_cleared"][j],
                                      (rule, free_cell, arm, f))


if __name__ == "__main__":
    unittest.main()
