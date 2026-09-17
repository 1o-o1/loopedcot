"""Expected-cost accounting: the length table, the three prices, and the default cell at 1.0x.

The package's `cap` price charges a cell its whole cap, so the natural-stop cell costs
(L_fixed + k L)(P + T_horizon + R) while the Table 1 `default` row is the MEAN REALISED cost of
that same run. The two never meet and the allocator cannot buy the default's operating point.
`expected` charges (L_fixed + k L)(P + E_cal[min(len_k, T)] + R), a decision-time price built on
the calibration prompts alone, and the two do meet.

Two facts these tests pin down, because they limit what the accounting can deliver:

1. The budget is one scalar and the default cost is a MEAN, so a per-prompt hard cap can only buy
   the default's operating point for the prompts priced below that mean. With prompts of one
   length that is every prompt (the fixture here); with real prompts it is the share whose length
   is below average -- 0.71 on GSM8K and 0.76 on MATH500, recorded in checks_expected.json, not 1.0.
2. The remaining gap at 1.0x is therefore an accounting fact, not a ranking failure: the arms give
   up accuracy exactly on the prompts too dear to run at the mean price.
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
import synth                                          # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
# The column of Table 1 at 1.0 of the default cost, located by value: the default fraction set
# grew a 0.75 point and a fixed index would have silently read the wrong budget.
ONE = E.BUDGET_FRACTIONS.index(1.0)

S33 = os.path.join(ROOT, "s33_anytime", "artifacts")
_CACHE = {}


def homogeneous_rows(n=80, n_cal=30, task="gsm8k"):
    """Return synthetic rows with ONE prompt length and a read-out that spends its whole reserve.

    Both are deliberate. The default cost is a mean over prompts, so any spread in the per-prompt
    price splits feasibility at that mean and hides the accounting being tested; and a read-out
    shorter than the reserve would make the expected price exceed the realised cost by the unused
    allowance. Stripping both leaves the cap-versus-expected difference alone.
    """
    budget = C.answer_budget(task)
    rows = synth.rows(n=n, n_cal=n_cal, task=task)
    for r in rows:
        r["n_prompt_tokens"] = 600
        r["n_answer_tokens"] = budget
        r["n_generated"] = min(r["B"], r["natural_stop"]) + budget
    return rows


def homogeneous_cells(n=80, n_cal=30, task="gsm8k"):
    return C.Cells(homogeneous_rows(n, n_cal, task), task, name="homogeneous",
                   ks=synth.KS, caps=synth.CAPS)


def real(task, ckpt="A0"):
    if (task, ckpt) not in _CACHE:
        _CACHE[(task, ckpt)] = C.load(S33, task, ckpt)
    return _CACHE[(task, ckpt)]


class TestExpectedLengthTable(unittest.TestCase):
    def test_table_is_the_calibration_mean_of_the_cut_length(self):
        """E[k,T] must equal the calibration mean of min(len_k, T), which the rows record as n_cut."""
        cs = synth.cells(n=80, n_cal=30)
        table = C.expected_lengths(cs)
        cal = cs.select("cal")
        np.testing.assert_allclose(table, np.nanmean(cs.ncut[:, :, cal], axis=2))
        for a in range(len(cs.ks)):                       # the plant: natural stop at 40 tokens
            for c, T in enumerate(cs.caps):
                self.assertAlmostEqual(table[a, c], min(T, 40))

    def test_the_evaluation_prompt_never_prices_itself(self):
        """Moving every evaluation prompt's realised length must not move any price."""
        cs = synth.cells(n=80, n_cal=30)
        before = C.expected_lengths(cs)
        ev = cs.select("eval")
        cs.nstop[:, :, ev] = 999.0
        cs.ncut[:, :, ev] = 999.0
        np.testing.assert_allclose(C.expected_lengths(cs), before)

    def test_evaluation_positions_are_refused(self):
        cs = synth.cells(n=80, n_cal=30)
        with self.assertRaises(ValueError):
            C.expected_lengths(cs, pos=cs.select("eval"))
        with self.assertRaises(ValueError):
            C.expected_lengths(cs, pos=[])

    def test_a_no_cap_marker_stands_for_natural_stop(self):
        """A cap recorded as -1 is 'no cap': it truncates nothing and cap accounting refuses it."""
        rows = [dict(r) for r in synth.rows(n=40, n_cal=15)]
        extra = [dict(r, B=-1, n_cut=r["natural_stop"]) for r in rows if r["B"] == 512]
        cs = C.Cells(rows + extra, "gsm8k", ks=synth.KS, caps=[-1] + synth.CAPS)
        self.assertEqual(C.natural_stop_cap_index(cs), 0)
        table = C.expected_lengths(cs)
        np.testing.assert_allclose(table[:, 0], 40.0)
        self.assertAlmostEqual(P.cost_of(cs, accounting="expected")(4, -1, 600, 16), 96 * 656)
        with self.assertRaises(ValueError):
            P.cost_of(cs, accounting="cap")(4, -1, 600, 16)

    def test_a_longer_calibration_chain_raises_every_expected_price(self):
        cs = homogeneous_cells()
        cheap = P.cost_of(cs, accounting="expected")(4, 512, 600, 16)
        cs.nstop[:, :, cs.select("cal")] = 80.0
        dear = P.cost_of(cs, accounting="expected")(4, 512, 600, 16)
        self.assertAlmostEqual(dear - cheap, 96 * 40)


class TestThreePrices(unittest.TestCase):
    def test_the_natural_stop_cell_costs_its_cap_only_under_cap_accounting(self):
        cs = homogeneous_cells()
        n = int(cs.select("eval")[0])
        p, r = cs.ptok[n], cs.reserve[n]
        prices = {a: P.cost_of(cs, accounting=a)(4, 512, p, r, n) for a in P.ACCOUNTINGS}
        self.assertAlmostEqual(prices["cap"], 96 * (600 + 512 + 16))
        self.assertAlmostEqual(prices["expected"], 96 * (600 + 40 + 16))
        self.assertAlmostEqual(prices["realised"], float(cs.passes[3, -1, n]))
        self.assertLess(prices["expected"], prices["cap"])

    def test_a_named_prompt_only_matters_to_realised_accounting(self):
        cs = homogeneous_cells()
        n = int(cs.select("eval")[0])
        for a in ("cap", "expected"):
            cost = P.cost_of(cs, accounting=a)
            self.assertEqual(cost(2, 64, 600, 16), cost(2, 64, 600, 16, n))
        cost = P.cost_of(cs, accounting="realised")
        self.assertEqual(cost(2, 64, 600, 16), float(np.nanmedian(cs.passes[1, 3, :])))

    def test_an_unknown_accounting_is_refused(self):
        cs = homogeneous_cells()
        with self.assertRaises(ValueError):
            P.cost_of(cs, accounting="oracle")


class TestDefaultCellAtOneTimes(unittest.TestCase):
    """Fraction 1.0 of the default cost: can the allocator buy the default's operating point?"""

    def _table(self, cs, accounting):
        return E.table1(cs, accounting=accounting, n_labels_grid=(10,), gate_draws=3, n_boot=50)

    def test_expected_makes_the_default_cell_affordable_and_cap_does_not(self):
        cs = homogeneous_cells()
        cap = self._table(cs, "cap")["rows"]["default_cell"]
        exp = self._table(cs, "expected")["rows"]["default_cell"]
        self.assertEqual(cap["feasible_frac"][ONE], 0.0)
        self.assertFalse(cap["affordable_on_average"][ONE])
        self.assertGreaterEqual(exp["feasible_frac"][ONE], 0.9)
        self.assertTrue(exp["affordable_on_average"][ONE])
        self.assertEqual(exp["feasible_frac"][:ONE], [0.0] * ONE)   # not bought below its own cost
        self.assertFalse(np.isnan(exp["acc_pts"][ONE]))

    def test_the_arms_are_not_below_the_default_row_at_1x(self):
        """Neither ranking may sit below the unbudgeted default by more than the paired interval."""
        t1 = self._table(homogeneous_cells(), "expected")
        for arm in ("lookup", "equation"):
            vs = t1["rows"][arm]["vs_default"][ONE]
            self.assertGreaterEqual(vs["hi95_pts"], 0.0, arm)

    def test_the_markdown_reports_the_accounting_and_the_default_cell(self):
        md = E.table1_markdown(self._table(homogeneous_cells(), "expected"))
        self.assertIn("expected accounting", md)
        self.assertIn("| default_cell |", md)
        self.assertIn("Affordable ON AVERAGE", md)


class TestAccountingIsAcceptedEverywhere(unittest.TestCase):
    def test_gain_contrast_and_noninferiority_take_all_three(self):
        a, b = homogeneous_cells(), homogeneous_cells()
        for acc in P.ACCOUNTINGS:
            g = E.gain_over_normal(a, n_boot=20, n_cal_draws=1, accounting=acc)
            self.assertEqual(g["accounting"], acc)
            self.assertTrue(np.isfinite(g["gain_mean_pts"]))
            self.assertEqual(E.contrast(a, b, n_boot=5, accounting=acc)["accounting"], acc)
            ni = E.noninferiority(a, b, n_boot=20, accounting=acc)
            self.assertEqual(ni["accounting"], acc)
            self.assertAlmostEqual(ni["mean_pts"], 0.0)
            self.assertEqual(E.table1(a, accounting=acc, n_labels_grid=(10,), gate_draws=3,
                                      n_boot=20)["accounting"], acc)
        with self.assertRaises(ValueError):
            E.gain_over_normal(a, n_boot=5, n_cal_draws=1, accounting="nonsense")

    def test_the_budget_grid_is_priced_in_the_same_accounting(self):
        """Expected pricing must move the budget grid itself, not only the arms."""
        cs = homogeneous_cells()
        g_cap = E.gain_over_normal(cs, n_boot=5, n_cal_draws=1, accounting="cap")
        g_exp = E.gain_over_normal(cs, n_boot=5, n_cal_draws=1, accounting="expected")
        self.assertLess(g_exp["budgets"][-1], g_cap["budgets"][-1])
        cost = P.cost_of(cs, accounting="expected")
        pm, rm = P.median_point(cs, cs.select("eval"))
        self.assertAlmostEqual(g_exp["budgets"][-1], P.cost_matrix(cs, cost, pm, rm).max())


class TestCli(unittest.TestCase):
    """The CLI writes the tables; its own progress print is swallowed so the suite stays readable."""

    @staticmethod
    def _run(argv):
        with contextlib.redirect_stdout(io.StringIO()):
            return cli.main(argv)

    def test_all_writes_one_table_per_accounting(self):
        with tempfile.TemporaryDirectory() as d:
            for k in synth.KS:
                with open(os.path.join(d, "cells_gsm8k_SYN_k%d.jsonl" % k), "w",
                          encoding="utf-8") as f:
                    for r in homogeneous_rows(n=60, n_cal=25):
                        if r["k"] == k:
                            f.write(json.dumps(r) + "\n")
            out = os.path.join(d, "out")
            res = self._run(["--cells", d, "--task", "gsm8k", "--checkpoint", "SYN",
                             "--layers-per-loop", "24", "--out", out, "--accounting", "all",
                             "--boot", "5", "--cal-draws", "1"])
            for acc in P.ACCOUNTINGS:
                self.assertTrue(os.path.exists(os.path.join(out, "table1_%s.md" % acc)), acc)
                self.assertEqual(res["table1_by_accounting"][acc]["accounting"], acc)
            self.assertEqual(res["accounting_priced"], "cap")
            self.assertEqual(res["gain"]["lookup"]["accounting"], "cap")
            with open(os.path.join(out, "cards.json"), encoding="utf-8") as fh:
                card = json.load(fh)["SYN"]
            self.assertAlmostEqual(card["expected_length_tokens"]["k4_T512"], 40.0)

    def test_one_accounting_prices_the_gains_too(self):
        with tempfile.TemporaryDirectory() as d:
            for k in synth.KS:
                with open(os.path.join(d, "cells_gsm8k_SYN_k%d.jsonl" % k), "w",
                          encoding="utf-8") as f:
                    for r in homogeneous_rows(n=60, n_cal=25):
                        if r["k"] == k:
                            f.write(json.dumps(r) + "\n")
            out = os.path.join(d, "out")
            res = self._run(["--cells", d, "--task", "gsm8k", "--checkpoint", "SYN",
                             "--layers-per-loop", "24", "--out", out,
                             "--accounting", "expected", "--boot", "5", "--cal-draws", "1"])
            self.assertEqual(res["accounting_priced"], "expected")
            self.assertEqual(res["gain"]["lookup"]["accounting"], "expected")
            self.assertEqual(list(res["table1_by_accounting"]), ["expected"])


@unittest.skipUnless(os.path.isdir(S33), "the cell files are not on this machine")
class TestRealGrids(unittest.TestCase):
    """The same claims on the S33 grids, where prompt lengths are not uniform."""

    FRACTIONS = {"gsm8k": 0.71, "math500": 0.76}

    def _table(self, task, accounting):
        return E.table1(real(task), accounting=accounting, n_labels_grid=(30,), gate_draws=5,
                        n_boot=50)

    def test_expected_buys_the_default_cell_that_cap_never_can(self):
        for task, want in self.FRACTIONS.items():
            cap = self._table(task, "cap")["rows"]["default_cell"]
            exp = self._table(task, "expected")["rows"]["default_cell"]
            self.assertEqual(cap["feasible_frac"][ONE], 0.0, task)
            self.assertFalse(cap["affordable_on_average"][ONE], task)
            self.assertAlmostEqual(exp["feasible_frac"][ONE], want, delta=0.02)
            # Below 1.0 and below 0.9: the budget is the MEAN cost, so the prompts priced above
            # that mean cannot buy the operating point whose mean it is. On average they can.
            self.assertTrue(exp["affordable_on_average"][ONE], task)

    def test_expected_never_prices_the_arms_worse_than_cap_at_1x(self):
        for task in self.FRACTIONS:
            cap, exp = self._table(task, "cap"), self._table(task, "expected")
            for arm in ("lookup", "equation", "default_at_budget"):
                self.assertGreaterEqual(exp["rows"][arm]["acc_pts"][ONE],
                                        cap["rows"][arm]["acc_pts"][ONE] - 1e-9,
                                        "%s/%s" % (task, arm))
                self.assertGreaterEqual(exp["rows"][arm]["vs_default"][ONE]["mean_pts"],
                                        cap["rows"][arm]["vs_default"][ONE]["mean_pts"] - 1e-9,
                                        "%s/%s" % (task, arm))

    def test_the_expected_table_is_the_calibration_mean_of_n_cut(self):
        for task in self.FRACTIONS:
            cs = real(task)
            cal = cs.select("cal")
            np.testing.assert_allclose(C.expected_lengths(cs),
                                       np.nanmean(cs.ncut[:, :, cal], axis=2))


if __name__ == "__main__":
    unittest.main()
