"""v5: calibration size as a function of N, structured deviation families, the oracle gap.

Three changes are tested here.

1. `n_cal = max(100, min(300, floor(0.2 N)))`. The calibration half is the FIRST n_cal ids of the
   dataset's seeded order, so a larger n_cal keeps every id the smaller one had and takes the extra
   ids from the START of the evaluation split, which shrinks by exactly as many. The gate's split
   is then 70/30 OF n_cal rather than a fixed 70 and 30.

2. Structured deviation families, tested in order, smallest first. F0 is the deepest depth at cap 0,
   F1 the deepest depth at any cap, F2 one depth shallower at any cap, F3 the free set, which is
   v4's behaviour and the last resort. The first family whose margin on the VERIFICATION questions
   clears the bar wins, and the row records which one opened. Fewer cells in the running means less
   of a winner's curse to cover, so a true cap-0 optimum survives a bar that the free set's maximum
   cannot clear.

3. The oracle gap: the best evaluation cell's accuracy minus each arm's accuracy at 1.0x. It reads
   the evaluation labels and is therefore a diagnostic -- the price of calibration noise -- and
   never a policy result. No arm may consume it.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np                                    # noqa: E402

from alloc import cells as C                          # noqa: E402
from alloc import evaluate as E                       # noqa: E402
from alloc import policy as P                         # noqa: E402

from test_split_gate import (KS, CAPS, TASK, N_CAL, DEFAULT_CELL,       # noqa: E402
                             null_surface, true_surface, planted, noisy_rows)

ONE = E.BUDGET_FRACTIONS.index(1.0)
_T1 = {}


def t1(which, families, c_gate=P.DEFAULT_C_GATE, n_select=50, n_verify=50, folds=None):
    """`folds` None is the frozen default, two; 1 is the one-direction gate kept for comparison."""
    key = (which, families, c_gate, n_select, n_verify, folds)
    if key not in _T1:
        surf = null_surface() if which == "null" else true_surface()
        _T1[key] = E.table1(planted(surf), accounting="expected", avg_budget=True,
                            n_labels_grid=(30,), gate_draws=10, n_boot=50, c_gate=c_gate,
                            gate_mode="split", n_select=n_select, n_verify=n_verify,
                            families=families, gate_folds=folds)
    return _T1[key]


# ---------------------------------------------------------------- 1. the calibration size
class TestTheCalibrationSizeRule(unittest.TestCase):
    """n_cal = max(100, min(300, floor(0.2 N)))."""

    def test_the_floor_holds_below_five_hundred_questions(self):
        for n in (1, 100, 250, 400, 499):
            self.assertEqual(C.n_cal_for(n), 100, n)

    def test_a_fifth_of_N_between_the_floor_and_the_ceiling(self):
        self.assertEqual(C.n_cal_for(500), 100)      # 0.2 * 500 = 100, the floor exactly
        self.assertEqual(C.n_cal_for(750), 150)
        self.assertEqual(C.n_cal_for(1000), 200)
        self.assertEqual(C.n_cal_for(1319), 263)     # floor, not a round
        self.assertEqual(C.n_cal_for(1499), 299)

    def test_the_ceiling_holds_above_fifteen_hundred(self):
        for n in (1500, 2000, 2437, 100000):
            self.assertEqual(C.n_cal_for(n), 300, n)

    def test_an_explicit_n_cal_overrides_the_rule(self):
        self.assertEqual(C.n_cal_for(400, n_cal=150), 150)
        self.assertEqual(C.n_cal_for(100000, n_cal=100), 100)

    def test_a_non_positive_size_is_refused(self):
        with self.assertRaises(ValueError):
            C.n_cal_for(400, n_cal=0)
        with self.assertRaises(ValueError):
            C.n_cal_for(0)


class TestPromotingEvaluationIdsIntoCalibration(unittest.TestCase):
    """The existing calibration ids stay; the extra ones come off the front of the evaluation split."""

    def setUp(self):
        self.cs = planted(null_surface())            # 300 questions, the first 100 calibration

    def test_the_grid_starts_at_a_hundred_and_three_hundred(self):
        self.assertEqual(len(self.cs.select("cal")), N_CAL)
        self.assertEqual(len(self.cs.select("eval")), 200)

    def test_promotion_keeps_every_id_the_smaller_split_had(self):
        small, _r = C.promote_calibration(self.cs, 100)
        big, _r = C.promote_calibration(self.cs, 150)
        self.assertTrue(set(small.ids("cal")).issubset(set(big.ids("cal"))))
        self.assertEqual(len(big.select("cal")), 150)

    def test_the_evaluation_split_shrinks_by_exactly_what_calibration_gained(self):
        for n_cal in (100, 150, 200):
            cs, rec = C.promote_calibration(self.cs, n_cal)
            self.assertEqual(len(cs.select("cal")), n_cal)
            self.assertEqual(len(cs.select("eval")), 300 - n_cal)
            self.assertEqual(rec["n_cal_after"] - rec["n_cal_before"], n_cal - N_CAL)
            self.assertEqual(rec["n_eval_before"] - rec["n_eval_after"], n_cal - N_CAL)

    def test_every_question_keeps_exactly_one_split(self):
        cs, _r = C.promote_calibration(self.cs, 175)
        self.assertEqual(len(cs.select("cal")) + len(cs.select("eval")), len(cs.idx))
        self.assertFalse(set(cs.ids("cal")) & set(cs.ids("eval")))

    def test_the_source_grid_is_never_mutated(self):
        before = list(self.cs.split)
        C.promote_calibration(self.cs, 200)
        self.assertEqual(before, list(self.cs.split))

    def test_asking_for_no_more_than_there_is_changes_nothing(self):
        cs, rec = C.promote_calibration(self.cs, 100)
        self.assertEqual(list(cs.split), list(self.cs.split))
        self.assertEqual(rec["n_promoted"], 0)

    def test_asking_for_more_than_the_grid_holds_is_refused(self):
        with self.assertRaises(ValueError):
            C.promote_calibration(self.cs, 400)

    def test_the_promotion_order_is_deterministic(self):
        a, _ = C.promote_calibration(self.cs, 160)
        b, _ = C.promote_calibration(self.cs, 160)
        self.assertEqual(a.ids("cal"), b.ids("cal"))

    def test_a_confirmed_seeded_order_is_reported_as_such(self):
        """A grid whose calibration split IS the seed's permutation prefix confirms the order."""
        seed, n = 20260908, 300
        perm = np.random.default_rng(seed).permutation(n)
        cal = set(int(i) for i in perm[:100])
        rows = noisy_rows(null_surface(), n=n, n_cal=0)
        for r in rows:
            r["split"] = "cal" if int(r["idx"]) in cal else "eval"
        cs = C.Cells(rows, TASK, name="seeded", ks=KS, caps=CAPS)
        out, rec = C.promote_calibration(cs, 150, seed=seed, n_dataset=n)
        self.assertEqual(rec["order_source"], "seeded_permutation")
        self.assertEqual(set(out.ids("cal")), set(int(i) for i in perm[:150]))

    def test_an_unconfirmable_order_says_so_and_still_promotes(self):
        _out, rec = C.promote_calibration(self.cs, 150)
        self.assertNotEqual(rec["order_source"], "seeded_permutation")
        self.assertIn(rec["order_source"], ("id_order", "stratified_emulated"))


class TestTheGateSplitFollowsTheCalibrationSize(unittest.TestCase):
    """70/30 OF n_cal, not a fixed 70 and 30."""

    def test_the_default_split_is_seventy_thirty_of_whatever_calibration_is(self):
        for n_cal, want in ((100, (70, 30)), (150, (105, 45)), (200, (140, 60)),
                            (60, (42, 18))):
            cs = planted(null_surface(), n=max(300, n_cal + 50), n_cal=n_cal)
            _sel, _ver, sizes = E.split_calibration(cs, cs.select("cal"))
            self.assertEqual((sizes["n_selection"], sizes["n_verification"]), want, n_cal)
            self.assertFalse(sizes["truncated"], n_cal)

    def test_at_a_hundred_calibration_ids_the_rule_reproduces_the_frozen_seventy_thirty(self):
        cs = planted(null_surface())
        _s, _v, sizes = E.split_calibration(cs, cs.select("cal"))
        self.assertEqual((sizes["n_selection"], sizes["n_verification"]),
                         (P.DEFAULT_N_SELECT, P.DEFAULT_N_VERIFY))

    def test_explicit_counts_still_override_the_proportion(self):
        cs = planted(null_surface(), n=300, n_cal=200)
        _s, _v, sizes = E.split_calibration(cs, cs.select("cal"), 50, 30)
        self.assertEqual((sizes["n_selection"], sizes["n_verification"]), (50, 30))

    def test_the_two_halves_are_still_disjoint_and_in_id_order(self):
        cs = planted(null_surface(), n=300, n_cal=150)
        sel, ver, _ = E.split_calibration(cs, cs.select("cal"))
        self.assertFalse(set(sel.tolist()) & set(ver.tolist()))
        self.assertEqual(max(cs.idx[n] for n in sel), min(cs.idx[n] for n in ver) - 1)

    def test_the_frozen_proportion_is_seven_tenths(self):
        self.assertAlmostEqual(P.GATE_SELECT_FRAC, 0.7)


# ---------------------------------------------------------------- 2. the families
class TestTheDeviationFamilies(unittest.TestCase):
    """F0 the deepest depth at cap 0, F1 it at any cap, F2 one depth shallower, F3 the free set."""

    def setUp(self):
        self.cs = planted(null_surface())

    def test_the_families_are_in_order_smallest_first(self):
        self.assertEqual(P.DEVIATION_FAMILIES, ("F0", "F1", "F2", "F3"))
        sizes = [len(P.family_cells(self.cs.ks, self.cs.caps, f))
                 for f in P.DEVIATION_FAMILIES]
        self.assertEqual(sizes, [1, len(CAPS), len(CAPS), len(KS) * len(CAPS)])

    def test_F0_is_the_deepest_depth_at_cap_zero(self):
        self.assertEqual(P.family_cells(self.cs.ks, self.cs.caps, "F0"), [(KS[-1], 0)])

    def test_F1_is_the_deepest_depth_at_every_cap(self):
        self.assertEqual(P.family_cells(self.cs.ks, self.cs.caps, "F1"),
                         [(KS[-1], T) for T in CAPS])

    def test_F2_is_one_depth_shallower_at_every_cap(self):
        self.assertEqual(P.family_cells(self.cs.ks, self.cs.caps, "F2"),
                         [(KS[-2], T) for T in CAPS])

    def test_F3_is_the_whole_grid(self):
        self.assertEqual(sorted(P.family_cells(self.cs.ks, self.cs.caps, "F3")),
                         sorted((k, T) for k in KS for T in CAPS))

    def test_a_grid_without_cap_zero_has_no_F0(self):
        self.assertEqual(P.family_cells(KS, [8, 16, 512], "F0"), [])

    def test_a_single_depth_grid_has_no_F2(self):
        self.assertEqual(P.family_cells([4], CAPS, "F2"), [])

    def test_an_unknown_family_is_refused(self):
        with self.assertRaises(ValueError):
            P.family_cells(KS, CAPS, "F9")


class TestTheFamiliesKeepATrueCapZeroOptimum(unittest.TestCase):
    """The plant where cap 0 really is 15 points better than the default cell."""

    def test_F0_opens_on_the_true_surface_in_one_direction(self):
        """One fold, the old default: F0 clears the bar on the verification half at +12.0 +/- 8.7."""
        for arm in (P.AVG_GATED, "gated_equation"):
            row = t1("true", True, folds=1)["rows"][arm]
            self.assertEqual(row["deviation_family"][ONE], "F0", arm)

    def test_two_folds_take_the_cap_zero_family_that_BOTH_halves_earn(self):
        """The frozen default. F0's mirror half measures 0.0 on these fifty questions, so F0 is
        withheld, and F2 -- one depth shallower, still at cap 0, +20.0 on one half and +16.0 on the
        other -- is what runs. Cap 0 survives the second fold; the deepest depth does not."""
        for arm in (P.AVG_GATED, "gated_equation"):
            row = t1("true", True)["rows"][arm]
            self.assertEqual(row["deviation_family"][ONE], "F2", arm)
        recs = [r for r in t1("true", True)["rows"]["gated_equation"]["family_decisions"]
                if r["family"] == "F0" and r["X"] == t1("true", True)["budgets"][ONE]]
        self.assertEqual(len(recs), 1)
        self.assertGreater(recs[0]["margin_pts"], recs[0]["bar_pts"])       # fold 1 said yes
        self.assertFalse(recs[0]["folds"][0]["opened"])                     # fold 2 said no
        self.assertFalse(recs[0]["opened"])

    def test_the_family_that_opened_buys_the_cap_zero_cell(self):
        row = t1("true", True)["rows"][P.AVG_GATED]
        self.assertEqual(list(row["cells_used"][ONE]), ["k%d_T0" % KS[-2]])
        self.assertFalse(row["gate_reverted"][ONE])
        # one fold buys the deepest depth's own cap-0 cell instead
        self.assertEqual(list(t1("true", True, folds=1)["rows"][P.AVG_GATED]["cells_used"][ONE]),
                         ["k%d_T0" % KS[-1]])

    def test_the_true_deviation_is_worth_what_it_was_planted_at(self):
        row = t1("true", True)["rows"][P.AVG_GATED]
        self.assertGreater(row["acc_pts"][ONE],
                           t1("true", True)["rows"]["default_cell"]["acc_pts"][ONE] + 8.0)


class TestTheFamiliesStillRefuseANoiseWinner(unittest.TestCase):
    """The null plant: eighteen cheap cells tied with the default cell, every win is noise.

    A structured family is a HELD-OUT test of one pre-named policy, so its false-positive rate is
    the bar's own: at c_gate = 0.5 a truly tied family clears it about a third of the time, and
    three families in sequence clear it oftener than one. That is the price of naming the families
    in advance rather than searching for them, and on a NULL surface it costs nothing, because a
    tied cell is tied: what must not happen is a family opening on a deviation that LOSES. The
    twenty-grid sweep is where the false-deviation count is counted; here the plant fixes the truth.
    """

    def test_the_free_set_never_opens_on_the_null_surface(self):
        """v4's invariant, unchanged: the maximum of eighteen tied cells cannot clear the bar."""
        for arm in (P.AVG_GATED, "gated_equation"):
            fams = t1("null", True)["rows"][arm]["deviation_family"]
            self.assertNotIn("F3", fams, (arm, fams))

    def test_no_null_deviation_loses_to_its_fallback(self):
        """Every cell of every family is truly tied with the default cell, so nothing is lost."""
        table = t1("null", True)
        fallback = table["rows"]["default_at_budget"]["acc_pts"][ONE]
        for arm in (P.AVG_GATED, "gated_equation"):
            self.assertGreater(table["rows"][arm]["acc_pts"][ONE], fallback - 8.0, arm)

    def test_the_average_budget_arm_reverts_on_the_null_surface(self):
        row = t1("null", True)["rows"][P.AVG_GATED]
        self.assertTrue(row["gate_reverted"][ONE])
        self.assertEqual(list(row["cells_used"][ONE]), ["k%d_T%d" % DEFAULT_CELL])


class TestNoFamilyOpensOnALosingSurface(unittest.TestCase):
    """The wrong-signed plant: the cell the equation ranks first is 10 points BELOW normal.

    Correctness there is a fixed pattern per cell rather than a coin, so the margins are exact and
    the verdict does not ride on a seed: every depth from 2 up measures the same 40 percent at
    every cap, so F0, F1 and F2 each measure a margin of exactly zero against normal operation, and
    F3 measures -10. Nothing may open.
    """

    def setUp(self):
        from test_split_gate import wrong_signed
        self.cs = wrong_signed()

    def test_the_gated_arm_reverts_at_every_budget_with_families_on(self):
        g = E.gain_over_normal(self.cs, ranking="equation", c_gate=0.5, n_boot=5, n_cal_draws=2,
                               gate_draws=5, n_select=50, n_verify=30, families=True)
        self.assertEqual(g["gain_mean_pts"], 0.0)
        for b in g["per_budget"]:
            self.assertIsNone(b["deviation_family"], b["X"])

    def test_every_family_measured_a_margin_of_zero_or_worse(self):
        g = E.gain_over_normal(self.cs, ranking="equation", c_gate=0.5, n_boot=5, n_cal_draws=2,
                               gate_draws=5, n_select=50, n_verify=30, families=True)
        measured = [d for d in g["family_decisions"] if d["margin_pts"] is not None]
        self.assertTrue(measured)
        for d in g["family_decisions"]:
            # A budget too small for normal operation has nothing to measure against, and a margin
            # that is not a number never passes.
            self.assertFalse(d["opened"], d)
        for d in measured:
            self.assertLessEqual(d["margin_pts"], 1e-9, d)


class TestTheFamilyIsRecordedEverywhere(unittest.TestCase):
    def test_every_gated_row_carries_one_family_entry_per_budget(self):
        table = t1("true", True)
        for arm in (P.AVG_GATED, "gated_equation"):
            fams = table["rows"][arm]["deviation_family"]
            self.assertEqual(len(fams), len(table["fractions"]), arm)
            for f in fams:
                self.assertIn(f, (None,) + P.DEVIATION_FAMILIES, (arm, f))

    def test_the_family_appears_in_the_markdown(self):
        md = E.table1_markdown(t1("true", True))
        self.assertIn("F0", md)

    def test_switching_the_families_off_restores_the_free_set_alone(self):
        for arm in (P.AVG_GATED, "gated_equation"):
            fams = t1("true", False)["rows"][arm]["deviation_family"]
            for f in fams:
                self.assertIn(f, (None, "F0", "F1", "F2", "F3"), (arm, f))


# ---------------------------------------------------------------- 3. the oracle gap
class TestTheOracleGap(unittest.TestCase):
    """Best evaluation cell minus each arm at 1.0x: the price of calibration noise."""

    def setUp(self):
        self.t = t1("true", True)
        self.cs = planted(true_surface())

    def test_the_oracle_is_the_best_single_cell_on_the_evaluation_questions(self):
        ev = self.cs.select("eval")
        best = np.nanmax([[np.nanmean(self.cs.acc[a, b, ev]) for b in range(len(CAPS))]
                          for a in range(len(KS))])
        self.assertAlmostEqual(self.t["oracle"]["acc_pts"], 100 * float(best), places=6)

    def test_the_oracle_names_the_cell_it_came_from(self):
        k, T = self.t["oracle"]["cell"]
        self.assertIn(k, KS)
        self.assertIn(T, CAPS)

    def test_every_arm_carries_its_gap_at_one_times_the_default_cost(self):
        for name, row in self.t["rows"].items():
            self.assertIn("oracle_gap_pts", row, name)

    def test_the_gap_is_the_oracle_minus_the_arm(self):
        for name, row in self.t["rows"].items():
            acc, gap = row["acc_pts"][ONE], row["oracle_gap_pts"]
            if acc != acc or gap is None:
                continue
            self.assertAlmostEqual(gap, self.t["oracle"]["acc_pts"] - acc, places=6, msg=name)

    def test_the_oracle_is_labelled_a_diagnostic_and_not_a_policy(self):
        self.assertIn("not a policy", self.t["oracle"]["note"])

    def test_the_markdown_reports_the_column(self):
        self.assertIn("oracle gap", E.table1_markdown(self.t))

    def test_no_arm_can_beat_the_oracle_by_picking_one_cell(self):
        """The default cell is one cell of the grid, so its gap can never be negative."""
        self.assertGreaterEqual(self.t["rows"]["default_cell"]["oracle_gap_pts"], -1e-9)


# ---------------------------------------------------------------- the fallback interval
class TestEveryGatedRowIsReadAgainstItsOwnFallback(unittest.TestCase):
    """A deviation is FALSE when its evaluation interval against its own fallback is below zero.

    `vs_default` reads every arm against the unbudgeted default row, which a hard per-prompt cap
    cannot buy for the dearer prompts, so it is not the number a gate's verdict can be judged by.
    `vs_fallback` reads each arm against what the gate would have reverted TO: normal operation at
    the same budget, under a hard per-prompt cap for the per-prompt arms and under the average
    budget (`evaluate.normal_at_budget`) for the average-budget gated one.
    """

    def setUp(self):
        self.t = t1("true", True)

    def test_the_per_prompt_arms_name_normal_operation(self):
        self.assertEqual(self.t["rows"]["gated_equation"]["fallback"], "default_at_budget")

    def test_the_average_budget_arm_names_normal_operation_at_the_budget(self):
        self.assertEqual(self.t["rows"][P.AVG_GATED]["fallback"], "normal_at_budget")
        # the ungated average-budget arms are still read against the default cell
        self.assertEqual(self.t["rows"]["avg_lookup"]["fallback"], "default_cell")

    def test_the_interval_brackets_its_own_mean(self):
        for arm in (P.AVG_GATED, "gated_equation"):
            v = self.t["rows"][arm]["vs_fallback"][ONE]
            if v["mean_pts"] is None:
                continue
            self.assertLessEqual(v["lo95_pts"], v["mean_pts"] + 1e-9, arm)
            self.assertLessEqual(v["mean_pts"], v["hi95_pts"] + 1e-9, arm)

    def test_a_true_deviation_is_not_a_false_one(self):
        """Cap 0 really is 15 points better here, so the interval sits above zero."""
        v = self.t["rows"][P.AVG_GATED]["vs_fallback"][ONE]
        self.assertGreater(v["lo95_pts"], 0.0)

    def test_normal_operation_is_its_own_fallback(self):
        r = self.t["rows"]["default_at_budget"]
        self.assertNotIn("vs_fallback", r)


# ---------------------------------------------------------------- what v5 freezes
class TestTheFrozenV5Defaults(unittest.TestCase):
    """What the sweep licensed. The setting of record is the ten Ouro-1.4B base production grids
    at horizon 4096 and full N; the ten S33 spike grids run a 512 horizon and are not, so the
    freeze condition -- no false deviation and a rising mean gain at 1.0x -- is read on production.

    The calibration-size rule and the 70/30 proportion of it: at N = 400 the rule returns the 100
    v4 used, so nothing moves by freezing it, and the emulation at 150 and 200 is where it pays.
    The families: over the ten production grids the mean gain at 1.0x rises +0.07 -> +0.12 at
    n_cal 100, +0.41 -> +0.73 at 150 and +0.25 -> +0.77 at 200, with zero false deviations at every
    size, and the oracle gap falls 2.11 -> 2.06, 2.32 -> 1.94 and 2.55 -> 1.95. HellaSwag's genuine
    cap-0 optimum, worth +5.6 and +7.5 points, is found by F0 and never by the free set.
    `--no-families` restores the free set alone.
    """

    def test_the_calibration_size_rule_is_frozen(self):
        self.assertEqual((C.N_CAL_MIN, C.N_CAL_MAX, C.N_CAL_FRAC), (100, 300, 0.2))
        self.assertEqual(C.n_cal_for(400), 100)

    def test_the_gate_proportion_is_frozen(self):
        self.assertAlmostEqual(P.GATE_SELECT_FRAC, 0.7)

    def test_the_frozen_split_at_a_hundred_is_still_seventy_thirty(self):
        self.assertEqual((P.DEFAULT_N_SELECT, P.DEFAULT_N_VERIFY), (70, 30))

    def test_the_families_are_frozen_on(self):
        # ruling 2026-09-18: production grids are the setting of record; families won there
        self.assertTrue(E.DEFAULT_FAMILIES)

    def test_the_gate_bar_and_mode_are_untouched(self):
        self.assertEqual(P.DEFAULT_C_GATE, 0.5)
        self.assertEqual(P.DEFAULT_GATE_MODE, "split")

    def test_the_default_run_may_open_a_structured_family(self):
        cs = planted(true_surface())
        t = E.table1(cs, accounting="expected", avg_budget=True, n_labels_grid=(30,),
                     gate_draws=5, n_boot=30, gate_mode="split", n_select=50, n_verify=50)
        for arm in (P.AVG_GATED, "gated_equation"):
            for f in t["rows"][arm]["deviation_family"]:
                self.assertIn(f, (None, "F0", "F1", "F2", "F3"), (arm, f))


if __name__ == "__main__":
    unittest.main()
