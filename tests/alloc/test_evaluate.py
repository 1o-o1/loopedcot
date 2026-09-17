"""The pairing assertion, the default cost, the non-inferiority test, and Table 1's shape."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np                                    # noqa: E402

from alloc import cells as C                          # noqa: E402
from alloc import evaluate as E                       # noqa: E402
import synth                                          # noqa: E402


class TestPairingAssertion(unittest.TestCase):
    """Check that checkpoint contrasts reject mismatched evaluation prompt IDs."""

    def test_identical_ids_pass(self):
        a = synth.cells(n=60, n_cal=20)
        b = synth.cells(n=60, n_cal=20)
        self.assertTrue(E.assert_paired(a, b))

    def test_mismatched_ids_raise(self):
        a = synth.cells(n=60, n_cal=20)
        b = C.Cells(synth.rows(n=60, n_cal=20, idx_offset=5), "gsm8k", name="shifted",
                    ks=synth.KS, caps=synth.CAPS)
        with self.assertRaises(AssertionError):
            E.assert_paired(a, b)
        with self.assertRaises(AssertionError):
            E.contrast(a, b, which="Bstar", n_boot=10)

    def test_different_eval_counts_raise(self):
        a = synth.cells(n=60, n_cal=20)
        b = synth.cells(n=50, n_cal=20)
        with self.assertRaises(AssertionError):
            E.assert_paired(a, b)


class TestDefaultCost(unittest.TestCase):
    def test_horizon_rows_are_counted_not_skipped(self):
        """Check that horizon-capped prompts contribute to mean realised layer-token cost."""
        rows = synth.rows(n=40, n_cal=10)
        for r in rows:                                  # question 0 never stops inside any cap
            if r["idx"] == 10:
                r["natural_stop"] = 10000
        cs = C.Cells(rows, "gsm8k", ks=synth.KS, caps=synth.CAPS)
        dc = E.default_cost(cs)
        self.assertEqual(dc["n_at_horizon"], 1)
        self.assertGreater(dc["horizon_share"], 0.0)
        self.assertEqual(dc["n"], len(cs.select("eval")))   # nothing dropped
        self.assertEqual(dc["k"], 4)

    def test_default_cost_is_a_realised_cost(self):
        cs = synth.cells(n=40, n_cal=10)
        dc = E.default_cost(cs)
        self.assertIsNotNone(dc["mean"])
        self.assertEqual(dc["n_at_horizon"], 0)


class TestTable1(unittest.TestCase):
    def test_rows_and_budgets(self):
        cs = synth.cells(n=80, n_cal=30)
        t1 = E.table1(cs, n_labels_grid=(10,), gate_draws=5)
        for name in ("default", "default_at_budget", "lookup", "equation", "equation_n10",
                     "gated_equation"):
            self.assertIn(name, t1["rows"], name)
            self.assertEqual(len(t1["rows"][name]["acc_pts"]), 4)
        self.assertEqual(t1["fractions"], [0.25, 0.5, 0.75, 1.0])
        t1m = E.table1(cs, n_labels_grid=(10,), gate_draws=5, basis="mean")
        self.assertAlmostEqual(t1m["budgets"][3] / t1m["default_cost"]["mean"], 1.0)
        md = E.table1_markdown(t1)
        self.assertIn("| lookup |", md)
        self.assertIn("| gated_equation |", md)

    def test_prompt_basis_anchors_at_one_and_prices_every_arm(self):
        """basis="prompt": at 1.00 normal operation IS the default (same accuracy, same realised
        price), and every arm carries a realised price wherever it is feasible."""
        cs = synth.cells(n=80, n_cal=30)
        t1 = E.table1(cs, n_labels_grid=(10,), gate_draws=3)
        d, nb = t1["rows"]["default"], t1["rows"]["default_at_budget"]
        self.assertAlmostEqual(nb["acc_pts"][3], d["acc_pts"][3], places=9)
        self.assertAlmostEqual(nb["price_layer_passes"][3], d["price_layer_passes"][3], places=6)
        self.assertEqual(nb["feasible_frac"][3], 1.0)
        for name in ("lookup", "equation", "gated_equation"):
            r = t1["rows"][name]
            for j in range(4):
                if r["feasible_frac"][j] > 0:
                    self.assertFalse(np.isnan(r["price_layer_passes"][j]), (name, j))


class TestNonInferiority(unittest.TestCase):
    def test_identical_grids_are_non_inferior(self):
        a = synth.cells(n=80, n_cal=30)
        b = synth.cells(n=80, n_cal=30)
        ni = E.noninferiority(a, b, n_boot=200)
        self.assertEqual(ni["verdict"], "non-inferior")
        self.assertAlmostEqual(ni["mean_pts"], 0.0)
        self.assertEqual(ni["margin_pts"], -2.0)
        self.assertEqual(ni["n_budgets"], 3)


class TestGainOverNormal(unittest.TestCase):
    def test_nan_columns_stay_in_place(self):
        cs = synth.cells(n=80, n_cal=30)
        g = E.gain_over_normal(cs, n_boot=50, n_cal_draws=2)
        self.assertIsNotNone(g["gain_mean_pts"])
        self.assertEqual(len(g["budgets"]), 16)
        self.assertEqual(len(g["gain_per_budget_pts"]), g["n_budgets_with_normal"])
        self.assertLessEqual(g["gain_worst_budget_pts"], g["gain_mean_pts"] + 1e-9)
        for rec in g["per_budget"]:
            self.assertTrue(0.0 <= rec["normal_feasible_frac"] <= 1.0)

    def test_equation_with_fewer_labels_still_runs(self):
        cs = synth.cells(n=80, n_cal=30)
        g = E.gain_over_normal(cs, ranking="equation", n_labels=10, n_boot=20, n_cal_draws=1)
        self.assertEqual(g["mechanism"]["n_labels"], 10)
        self.assertEqual(g["mechanism"]["n_g"], 30)
        self.assertTrue(np.isfinite(g["gain_mean_pts"]))


if __name__ == "__main__":
    unittest.main()
