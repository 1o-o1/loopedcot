"""The identity resolved by settle time, the ranking built on it, and the two-fold gate.

The planted grid here is the shape the class sets have and the pooled identity cannot rank: the
FIRST answer is the good one. Three fifths of the questions settle at cap 0 and are right; the other
two fifths are ALSO right at cap 0 and then talk themselves out of it, moving through two wrong
read-outs and settling on a wrong answer at the last cap. So measured accuracy FALLS with the token
cap, and the best cell of the grid is cap 0 at the cheapest depth.

The pooled identity carries one c_k and one l_k for the whole depth, so its surface is
G_k(T) c_k + (1 - G_k(T)) l_k with c_k > l_k, which rises with T and must rank the last cap first.
The resolved identity carries c_k(j) per settle cap and l_k(T) per cap, so it sees l_k(0) = 1 -- the
late settlers' first answer is right -- and ranks cap 0 first. Those two facts are the test.
"""
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np                                    # noqa: E402

from alloc import cells as C                          # noqa: E402
from alloc import cli as CLI                          # noqa: E402
from alloc import evaluate as E                       # noqa: E402
from alloc import mechanism as M                      # noqa: E402
from alloc import policy as P                         # noqa: E402

KS = [1, 2, 3]
CAPS = [0, 16, 32, 64]
TASK = "csqa"
N = 200
N_CAL = 100
EARLY_SHARE = 0.6                    # questions that settle at cap 0 and stay right
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
ARTIFACTS = os.path.join(REPO, "artifacts")

# compute.py's own numbers for ouro_1_4b_base / hellaswag, from
# work/analysis_2026-09-18/equation/resolved_fit.csv. Read at the raw 100-question calibration split
# that compute.py uses, no promotion, expected-cost geometry 24 layers per loop and no fixed layers.
REPRO_GRID = ("hellaswag", "ouro_1_4b_base")
REPRO_RMSE_EVAL = {30: 11.544194, 100: 5.641460}          # resolved
REPRO_RMSE_EVAL_POOLED = {30: 11.459727, 100: 6.544860}
REPRO_TOL = 0.05


def is_early(i):
    """Return whether question i settles at the first cap; the first EARLY_SHARE of every ten do."""
    return (i % 10) < int(round(10 * EARLY_SHARE))


def rows(n=N, n_cal=N_CAL):
    """Return cell rows for the planted first-answer-is-best grid, the same shape a spike file has."""
    out = []
    for i in range(n):
        early = is_early(i)
        ptok = 400 + (i % 5)
        for k in KS:
            for T in CAPS:
                if early:
                    pred = "A"                                   # never moves, always right
                else:
                    # right at cap 0, then two wrong read-outs, then settled on a wrong answer
                    pred = {0: "A", 16: "B", 32: "C", 64: "D"}[T]
                ok = pred == "A"
                out.append({"idx": i, "k": k, "B": T,
                            "split": "cal" if i < n_cal else "eval",
                            "task": TASK, "correct": ok, "correct_v2": ok,
                            "pred": pred, "gold": "A",
                            "trace_answer": None, "trace_correct": False,
                            "n_cut": min(T, 30), "natural_stop": 30,
                            "n_generated": min(T, 30) + 3,
                            "n_prompt_tokens": ptok, "n_suffix_tokens": 2,
                            "n_answer_tokens": 3})
    return out


def grid():
    return C.Cells(rows(), TASK, name="first_best", ks=KS, caps=CAPS, L=4, L_fixed=0)


def write_cells(d):
    """Write the planted grid to `d` as one cells file per depth, and return alloc.cli's flags."""
    for k in KS:
        path = os.path.join(d, "cells_SYN_%s_natural_k%d.jsonl" % (TASK, k))
        with open(path, "w", encoding="utf-8") as fh:
            for r in rows():
                if r["k"] == k:
                    fh.write(json.dumps(r) + "\n")
    return ["--cells", d, "--task", TASK, "--checkpoint", "SYN",
            "--layers-per-loop", "4", "--fixed-layers", "0",
            "--accounting", "expected", "--avg-budget", "--boot", "5", "--cal-draws", "1"]


def parts(cs):
    cost = P.cost_of(cs, accounting="expected")
    ev, cal = cs.select("eval"), cs.select("cal")
    Pm, Rm = P.median_point(cs, ev)
    return cost, ev, cal, Pm, Rm


class TestSettleTime(unittest.TestCase):
    """The settle index, its distribution, and the binning rule."""

    def setUp(self):
        self.cs = grid()
        self.all = self.cs.select("all")

    def test_the_planted_settle_caps_are_recovered(self):
        s = M.settle_time(self.cs, self.all)
        self.assertEqual(s.shape, (len(KS), N))
        for a in range(len(KS)):
            for i in range(N):
                self.assertEqual(int(s[a, i]), 0 if is_early(i) else CAPS.index(64),
                                 "depth index %d question %d" % (a, i))

    def test_an_unparsed_final_readout_never_settles(self):
        """A question whose LAST read-out does not parse is encoded beyond the last cap, not at it."""
        rs = rows()
        for r in rs:
            if r["idx"] == 0 and r["B"] == CAPS[-1]:
                r["pred"] = None
        cs = C.Cells(rs, TASK, name="unparsed", ks=KS, caps=CAPS, L=4, L_fixed=0)
        s = M.settle_time(cs, cs.select("all"))
        self.assertTrue(bool((s[:, 0] == len(CAPS)).all()))
        self.assertTrue(bool((s[:, 1:] < len(CAPS)).all()))

    def test_the_distribution_reports_the_planted_shares(self):
        s = M.settle_time(self.cs, self.all)
        for row in M.settle_distribution(self.cs, s):
            self.assertAlmostEqual(row["share_settle_first"], EARLY_SHARE, places=9)
            self.assertAlmostEqual(row["share_never"], 0.0, places=9)
            self.assertAlmostEqual(row["share_by_cap"]["64"], 1 - EARLY_SHARE, places=9)
            self.assertEqual(row["median_settle_label"], "0")
            self.assertEqual(row["n"], N)

    def test_the_production_bins_are_the_table_and_an_unlisted_cap_pools_alone(self):
        self.assertEqual(M.settle_bin(0), M.settle_bin(0))
        self.assertEqual(M.settle_bin(16), M.settle_bin(32))
        self.assertEqual(M.settle_bin(64), M.settle_bin(128))
        self.assertEqual(M.settle_bin(1024), M.settle_bin(4096))
        self.assertNotEqual(M.settle_bin(0), M.settle_bin(16))
        self.assertNotEqual(M.settle_bin(32), M.settle_bin(64))
        # a cap the frozen table does not cover must not join one of its bins
        for cap in (8, 2, 8192, -1):
            for listed in (0, 16, 32, 64, 128, 256, 512, 1024, 4096):
                self.assertNotEqual(M.settle_bin(cap), M.settle_bin(listed), (cap, listed))


class TestTheResolvedIdentity(unittest.TestCase):
    def setUp(self):
        self.cs = grid()
        self.cal = self.cs.select("cal")
        self.m = M.resolved_mechanism(self.cs, self.cal)

    def test_c_and_l_are_the_planted_conditional_accuracies(self):
        c, l = np.array(self.m["c"], float), np.array(self.m["l"], float)
        last = len(CAPS) - 1
        for a in range(len(KS)):
            self.assertAlmostEqual(c[a, 0], 1.0, places=9)          # early settlers are right
            self.assertAlmostEqual(c[a, last], 0.0, places=9)       # late settlers end wrong
            self.assertAlmostEqual(l[a, 0], 1.0, places=9)          # and were right at cap 0
            self.assertTrue(np.isnan(l[a, last]) or l[a, last] == l[a, last])

    def test_the_identity_reproduces_the_calibration_surface_exactly(self):
        """Both terms partition the same questions, so with every settle cap estimated from its own
        labels there is nothing left over. The two empty settle caps carry no mass, so their bin
        fallback cannot move the surface."""
        A = M.a_res_matrix(self.m)
        measured = np.nanmean(self.cs.acc[:, :, self.cal], axis=2)
        self.assertLess(float(np.abs(A - measured).max()), 1e-12)
        self.assertEqual(self.m["n_caps_pooled_with_mass"], 0)
        self.assertEqual(self.m["n_caps_binned_with_mass"], 0)

    def test_the_pooled_identity_cannot_see_it(self):
        A_hat = M.a_hat_matrix(M.mechanism(self.cs, self.cal))
        measured = np.nanmean(self.cs.acc[:, :, self.cal], axis=2)
        rmse = lambda A: float(100 * np.sqrt(np.nanmean((A - measured) ** 2)))
        self.assertGreater(rmse(A_hat), 10.0)
        self.assertLess(rmse(M.a_res_matrix(self.m)), 1e-9)
        # and it is wrong in one direction: its surface RISES with the cap where the truth falls
        self.assertGreater(A_hat[0, -1], A_hat[0, 0])
        self.assertLess(measured[0, -1], measured[0, 0])

    def test_n_labels_is_the_first_ids_in_id_order_as_the_pooled_version_is(self):
        want = M.resolved_mechanism(self.cs, self.cal, label_pos=self.cal[:30])
        got = M.resolved_mechanism(self.cs, self.cal, n_labels=30)
        self.assertEqual(got["n_labels"], 30)
        self.assertEqual(json.dumps(got, sort_keys=True), json.dumps(want, sort_keys=True))
        ids = [int(self.cs.idx[n]) for n in self.cal[:30]]
        self.assertEqual(ids, sorted(int(self.cs.idx[n]) for n in self.cal)[:30])

    def test_a_sparse_settle_cap_takes_its_bin_and_then_the_pooled_value(self):
        # 12 labels: eight early settlers, which is one more than the bar, and four late ones,
        # which is fewer, so one cap is read from its own labels and the rest fall back
        m = M.resolved_mechanism(self.cs, self.cal, n_labels=12)
        src = np.array(m["c_source"], dtype=object)
        n_at = np.array(m["n_labels_at_cap"], int)
        for a in range(len(KS)):
            for j in range(len(CAPS)):
                if n_at[a, j] >= M.MIN_SETTLE_LABELS:
                    self.assertEqual(src[a, j], "cap", (a, j))
                else:
                    self.assertIn(src[a, j], ("bin", "pooled"), (a, j))
        self.assertGreater(m["n_caps_own"], 0)
        self.assertGreater(m["n_caps_binned"] + m["n_caps_pooled"], 0)

    def test_a_cap_subset_is_refused_rather_than_answered_wrongly(self):
        with self.assertRaises(ValueError):
            M.resolved_mechanism(self.cs, self.cal, caps=CAPS[:2])
        with self.assertRaises(ValueError):
            M.resolved_mechanism(self.cs, self.cal, label_pos=self.cal[:5], n_labels=5)


class TestTheResolvedRanking(unittest.TestCase):
    """`equation_resolved` must put cap 0 first where the pooled equation cannot."""

    def setUp(self):
        self.cs = grid()
        self.cost, self.ev, self.cal, self.Pm, self.Rm = parts(self.cs)

    def _order(self, ranking, **kw):
        return E.make_order(self.cs, self.cal, self.cost, self.Pm, self.Rm, ranking, **kw)[0]

    def test_the_resolved_ranking_leads_with_cap_zero_and_the_pooled_one_does_not(self):
        res, pooled = self._order("equation_resolved"), self._order("equation")
        self.assertEqual(res[0][1], 0, res[:3])
        self.assertNotEqual(pooled[0][1], 0, pooled[:3])
        self.assertEqual(pooled[0][1], CAPS[-1])
        # cap 0 is also the best MEASURED cell, so the resolved head is the right answer
        best = np.unravel_index(np.argmax(np.nanmean(self.cs.acc[:, :, self.ev], axis=2)),
                                (len(KS), len(CAPS)))
        self.assertEqual(CAPS[int(best[1])], 0)

    def test_a_tie_in_the_surface_goes_to_the_cheaper_cell(self):
        """Every depth scores the same here, so the head must be the cheapest depth."""
        self.assertEqual(self._order("equation_resolved")[0], (KS[0], 0))

    def test_the_resolved_ranking_is_usable_everywhere_the_pooled_one_is(self):
        # a hard per-prompt cap
        g = E.gain_over_normal(self.cs, ranking="equation_resolved", accounting="expected",
                               n_boot=20, n_cal_draws=2)
        gp = E.gain_over_normal(self.cs, ranking="equation", accounting="expected",
                                n_boot=20, n_cal_draws=2)
        self.assertGreater(g["gain_mean_pts"], gp["gain_mean_pts"])
        self.assertEqual(g["ranking"], "equation_resolved")
        # an average budget
        S = E.cell_scores(self.cs, self.cal, "avg_equation_resolved", self.cost, self.Pm, self.Rm)
        self.assertEqual(S.shape, (len(KS), len(CAPS)))
        self.assertEqual(int(np.unravel_index(np.argmax(S), S.shape)[1]), 0)
        # and it is not a cell order in the average-budget form
        for name in P.AVG_RANKINGS_RESOLVED:
            with self.assertRaises(ValueError):
                E.make_order(self.cs, self.cal, self.cost, self.Pm, self.Rm, ranking=name)

    def test_n_labels_narrows_the_resolved_ranking_too(self):
        self.assertEqual(self._order("equation_resolved", n_labels=40)[0][1], 0)


class TestTheArmsInTheTable(unittest.TestCase):
    def setUp(self):
        self.cs = grid()
        self.t1 = E.table1(self.cs, accounting="expected", avg_budget=True, n_labels_grid=(30,),
                           gate_draws=3, n_boot=30)
        self.one = list(E.BUDGET_FRACTIONS).index(1.0)

    def test_every_new_arm_is_a_row(self):
        for name in ("equation_resolved", "gated_equation_resolved",
                     "avg_equation_resolved", "avg_gated_equation_resolved"):
            self.assertIn(name, self.t1["rows"], name)
            self.assertEqual(len(self.t1["rows"][name]["acc_pts"]), len(E.BUDGET_FRACTIONS))

    def test_every_new_arm_is_in_the_markdown_and_in_the_price_table(self):
        md = E.table1_markdown(self.t1)
        for name in ("equation_resolved", "gated_equation_resolved",
                     "avg_equation_resolved", "avg_gated_equation_resolved"):
            self.assertIn("| %s |" % name, md, name)
        # the second table, the realised mean price of the average-budget arms
        tail = md.split("Realised mean price")[1]
        for name in P.AVG_RANKINGS_RESOLVED:
            self.assertIn("| %s |" % name, tail, name)

    def test_every_new_arm_records_its_picks(self):
        arms = self.t1["picks"]["arms"]
        for name in ("equation_resolved", "gated_equation_resolved",
                     "avg_equation_resolved", "avg_gated_equation_resolved"):
            recs = arms[name][self.one]["picks"]
            self.assertEqual(len(recs), self.t1["picks"]["n_eval"], name)
            self.assertTrue(all(r["cap"] == 0 for r in recs), name)

    def test_the_resolved_arms_beat_the_pooled_ones_on_this_grid(self):
        for res, pooled in (("equation_resolved", "equation"),
                            ("avg_equation_resolved", "avg_equation")):
            self.assertGreater(self.t1["rows"][res]["acc_pts"][self.one],
                               self.t1["rows"][pooled]["acc_pts"][self.one], res)

    def test_the_gate_consumes_the_resolved_ranking(self):
        """With the structured families off the gate rules on the cell the RANKING named, so the
        cell it was asked about is the resolved head and not the pooled one."""
        t = E.table1(self.cs, accounting="expected", avg_budget=True, n_labels_grid=(30,),
                     gate_draws=3, n_boot=30, families=False)
        row = t["rows"]["gated_equation_resolved"]
        cap0 = list(CAPS).index(0)
        picks = t["picks"]["arms"]["gated_equation_resolved"][self.one]["picks"]
        self.assertTrue(all(r["cap"] == 0 for r in picks))
        decided = [d for d in (row.get("gate_decisions") or []) if d["pick"][1] == cap0]
        self.assertTrue(decided, "the gate never ruled on a cap-0 pick")
        self.assertTrue(any(d["opened"] for d in decided))
        # the pooled arm's gate was never offered cap 0 by its own ranking
        self.assertTrue(all(r["cap"] != 0
                            for r in t["picks"]["arms"]["equation"][self.one]["picks"]))
        # the gated average-budget arm ran the resolved cells too
        used = t["rows"]["avg_gated_equation_resolved"]["cells_used"][self.one]
        self.assertTrue(all(k.endswith("_T0") for k in used), used)


class TestTheWholeModeGateReadsItsOwnSurface(unittest.TestCase):
    """`--gate-mode whole` reads a PREDICTED margin off a surface, so it must read the resolved one
    for a resolved arm and the pooled one for a pooled arm. Reading the pooled surface for a resolved
    arm would gate the deviation on a prediction the arm never made."""

    def setUp(self):
        self.cs = grid()
        self.cal = self.cs.select("cal")

    def test_the_gate_surface_follows_the_ranking(self):
        pooled, _ = E.gate_for(self.cs, self.cal, c_gate=0.5, n_draws=3, ranking="equation")
        res, _ = E.gate_for(self.cs, self.cal, c_gate=0.5, n_draws=3,
                            ranking="equation_resolved")
        cap0, last = 0, len(CAPS) - 1
        # the pooled surface prefers the last cap and the resolved one prefers cap 0
        self.assertLess(pooled.A_hat[0, cap0], pooled.A_hat[0, last])
        self.assertGreater(res.A_hat[0, cap0], res.A_hat[0, last])
        self.assertEqual(E._gate_ranking("equation_resolved"), "equation_resolved")
        self.assertEqual(E._gate_ranking("lookup"), "equation")
        with self.assertRaises(ValueError):
            E.surface_of(self.cs, self.cal, "lookup")

    def test_both_gate_modes_run_the_resolved_arm_end_to_end(self):
        for mode in P.GATE_MODES:
            t = E.table1(self.cs, accounting="expected", avg_budget=True, n_labels_grid=(30,),
                         gate_draws=3, n_boot=30, gate_mode=mode)
            for name in ("gated_equation_resolved", "avg_gated_equation_resolved"):
                self.assertIn(name, t["rows"], (mode, name))
                self.assertEqual(t["rows"][name]["gate_mode"], mode)
            g = E.gain_over_normal(self.cs, ranking="equation_resolved", c_gate=0.5,
                                   accounting="expected", gate_mode=mode, n_boot=20,
                                   n_cal_draws=2, gate_draws=3)
            self.assertEqual(g["gate_mode"], mode)
            # two folds are the frozen default under `split`; `whole` has one set and one fold
            self.assertEqual(g["gate_folds"], P.resolve_gate_folds(mode))
            self.assertEqual(t["gate_folds"], P.resolve_gate_folds(mode))


class TestTheCardRmseFields(unittest.TestCase):
    def setUp(self):
        self.card = CLI.card(grid())

    def test_both_rmses_are_reported_on_both_splits(self):
        r = self.card["rmse_pts"]
        for key in ("pooled_cal", "resolved_cal", "pooled_eval", "resolved_eval",
                    "noise_floor_cal", "noise_floor_eval"):
            self.assertIn(key, r)
            self.assertTrue(np.isfinite(r[key]), key)

    def test_the_resolved_rmse_is_the_smaller_one_on_this_grid(self):
        r = self.card["rmse_pts"]
        self.assertLess(r["resolved_cal"], 1e-9)
        self.assertGreater(r["pooled_cal"], 10.0)
        self.assertLess(r["resolved_eval"], r["pooled_eval"])

    def test_the_card_carries_the_settle_time_distribution_and_c_and_l(self):
        st = self.card["settle_time"]
        self.assertAlmostEqual(st["share_settle_first_cap"], EARLY_SHARE, places=9)
        self.assertEqual(len(st["distribution"]), len(KS))
        self.assertEqual(np.array(st["c_by_settle_cap"]).shape, (len(KS), len(CAPS)))
        self.assertEqual(np.array(st["l_by_cap"]).shape, (len(KS), len(CAPS)))
        self.assertEqual(np.array(st["P"]).shape, (len(KS), len(CAPS)))
        self.assertAlmostEqual(st["c_by_settle_cap"][0][0], 1.0, places=9)
        self.assertAlmostEqual(st["l_by_cap"][0][0], 1.0, places=9)
        self.assertEqual(self.card["ranking_equation_resolved"][0], "k%d_T0" % KS[0])


class TestTheTwoFoldGate(unittest.TestCase):
    """Both directions of the split must clear the bar, and one fold's behaviour must not move."""

    def test_a_fold_that_says_no_withholds_the_deviation(self):
        # two cells, two questions: the first half's labels say +1, the second half's say 0
        yes = np.array([[[1.0, 1.0, 1.0, 1.0], [0.0, 0.0, 0.0, 0.0]]])       # (1 depth, 2 caps, 4 q)
        no = np.array([[[1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0]]])
        one = P.MeasuredGate(yes, c_gate=0.5, n_boot=200, seed=7)
        two = P.MeasuredGate(yes, c_gate=0.5, n_boot=200, seed=7, folds=[(no, None)])
        pick, normal = (0, 0), (0, 1)
        self.assertEqual(one.choose(pick, normal), (pick, False))
        self.assertEqual(two.choose(pick, normal), (normal, True))
        self.assertEqual(two.n_folds, 2)
        self.assertEqual(one.n_folds, 1)

    def test_the_decision_record_carries_every_fold(self):
        yes = np.array([[[1.0, 1.0, 1.0, 1.0], [0.0, 0.0, 0.0, 0.0]]])
        no = np.array([[[1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0]]])
        two = P.MeasuredGate(yes, c_gate=0.5, n_boot=200, seed=7, folds=[(no, None)])
        two.choose((0, 0), (0, 1))
        d, = two.decisions()
        self.assertEqual(d["n_folds"], 2)
        self.assertEqual(len(d["folds"]), 1)
        self.assertTrue(d["folds"][0]["margin_pts"] == 0.0)
        self.assertFalse(d["opened"])

    def test_the_split_is_mirrored_and_the_fit_positions_do_not_move(self):
        cs = grid()
        one = E.gate_and_fit(cs, cs.select("cal"), None, 0.5, 3, 7, gate_mode="split", folds=1)
        two = E.gate_and_fit(cs, cs.select("cal"), None, 0.5, 3, 7, gate_mode="split", folds=2)
        self.assertEqual(list(one[1]), list(two[1]))            # same half fits the ranking
        self.assertEqual(one[2]["n_folds"], 1)
        self.assertEqual(two[2]["n_folds"], 2)
        self.assertEqual(E.fold_fits(one[0]), [])
        (fit, ver), = E.fold_fits(two[0])
        self.assertEqual(list(fit), list(two[0].pos))            # fold 2 fits where fold 1 verifies
        self.assertEqual(list(ver), list(two[1]))                # and verifies where fold 1 fits
        self.assertEqual(len(set(list(fit)) & set(list(ver))), 0)

    def test_the_whole_gate_refuses_a_second_fold(self):
        cs = grid()
        with self.assertRaises(ValueError):
            E.gate_and_fit(cs, cs.select("cal"), None, 0.5, 3, 7, gate_mode="whole", folds=2)
        with self.assertRaises(ValueError):
            E.gate_and_fit(cs, cs.select("cal"), None, 0.5, 3, 7, gate_mode="split", folds=3)

    def test_two_folds_can_only_withhold_a_deviation(self):
        cs = grid()
        kw = dict(accounting="expected", avg_budget=True, n_labels_grid=(30,), gate_draws=3,
                  n_boot=30)
        one = E.table1(cs, gate_folds=1, **kw)
        two = E.table1(cs, gate_folds=2, **kw)
        self.assertEqual(one["gate_folds"], 1)
        self.assertEqual(two["gate_folds"], 2)
        for name in ("gated_equation", "gated_equation_resolved",
                     "avg_gated_lookup", "avg_gated_equation_resolved"):
            f1 = one["rows"][name]["deviation_family"]
            f2 = two["rows"][name]["deviation_family"]
            for j in range(len(E.BUDGET_FRACTIONS)):
                if f2[j] is not None:
                    self.assertIsNotNone(f1[j], (name, j))
            self.assertEqual(two["rows"][name]["gate_folds"], 2)

    def test_the_cli_takes_the_flag_and_records_it(self):
        d = tempfile.mkdtemp()
        try:
            base = write_cells(d)
            with contextlib.redirect_stdout(io.StringIO()):
                res = CLI.main(base + ["--out", os.path.join(d, "two"), "--gate-folds", "2"])
            self.assertEqual(res["gate_folds"], 2)
            self.assertEqual(res["table1"]["gate_folds"], 2)
            for name in ("equation_resolved", "gated_equation_resolved"):
                self.assertIn(name, res["gain"])
            for name in ("avg_equation_resolved", "avg_gated_equation_resolved"):
                self.assertIn(name, res["table1"]["rows"])
                self.assertIn(name, res["picks"]["by_accounting"]["expected"]["arms"])
            with open(os.path.join(d, "two", "cards.json"), encoding="utf-8") as fh:
                card = json.load(fh)["SYN"]
            self.assertIn("resolved_eval", card["rmse_pts"])
            self.assertIn("distribution", card["settle_time"])
        finally:
            shutil.rmtree(d, ignore_errors=True)


class TestTheFrozenDefaults(unittest.TestCase):
    """The 2026-09-18 freeze: two-fold verification, and the resolved arm at the head of the list.

    Both rulings came off the 60-pair run under work/analysis_2026-09-18 (see alloc/README.md).
    """

    def test_two_folds_are_the_default(self):
        self.assertEqual(P.GATE_FOLDS, 2)
        self.assertEqual(P.resolve_gate_folds("split"), 2)
        self.assertEqual(P.resolve_gate_folds("split", 1), 1)

    def test_the_whole_gate_keeps_its_one_fold_and_still_refuses_two(self):
        """`whole` has one set that both fits and measures, so the DEFAULT there is one fold; asking
        for two is still refused rather than silently ignored."""
        self.assertEqual(P.resolve_gate_folds("whole"), 1)
        self.assertEqual(P.resolve_gate_folds("whole", 2), 2)
        cs = grid()
        cost, ev, cal, Pm, Rm = parts(cs)
        with self.assertRaises(ValueError):
            E.gate_and_fit(cs, cal, None, 0.5, 3, 7, gate_mode="whole", folds=2)
        with self.assertRaises(ValueError):
            E.avg_gated_vectors(cs, ev, cal, cost, [1e9],
                                E.cell_scores(cs, cal, P.AVG_GATED, cost, Pm, Rm),
                                E.default_cell(cs), c_gate=0.5, gate_mode="whole", folds=2)

    def test_the_default_table_and_gain_carry_two_folds(self):
        cs = grid()
        t = E.table1(cs, accounting="expected", avg_budget=True, n_labels_grid=(30,),
                     gate_draws=3, n_boot=30)
        self.assertEqual(t["gate_folds"], 2)
        self.assertEqual(t["gate_sizes"]["n_folds"], 2)
        for name in ("gated_equation", "gated_equation_resolved",
                     "avg_gated_lookup", "avg_gated_equation_resolved"):
            self.assertEqual(t["rows"][name]["gate_folds"], 2, name)
        g = E.gain_over_normal(cs, ranking="equation_resolved", c_gate=0.5, accounting="expected",
                               n_boot=20, n_cal_draws=2, gate_draws=3)
        self.assertEqual(g["gate_folds"], 2)

    def test_the_help_quotes_the_frozen_fold_default_and_still_formats(self):
        """argparse expands `help % params` when it prints, so a help string that carries a literal
        per-cent sign crashes --help. The fold default is quoted in that help, so it is read here."""
        with contextlib.redirect_stdout(io.StringIO()) as out:
            with self.assertRaises(SystemExit):
                CLI._args(["--help"])
        text = " ".join(out.getvalue().split())
        self.assertIn("%d, the frozen default" % P.GATE_FOLDS, text)
        self.assertIn("70% of the calibration split", text)

    def test_the_ranking_of_record_leads_the_arm_list(self):
        self.assertEqual(P.RANKING_OF_RECORD, "equation_resolved")
        self.assertEqual(P.AVG_ARMS[:2], ("avg_gated_equation_resolved", "avg_gated_lookup"))
        # every other arm is still there, and the v5 sets did not move
        self.assertEqual(set(P.AVG_ARMS), set(P.AVG_RANKINGS + P.AVG_RANKINGS_RESOLVED))
        self.assertEqual(P.AVG_RANKINGS, ("avg_lookup", "avg_equation", "avg_gated_lookup"))

    def test_the_markdown_puts_the_resolved_gated_arm_above_the_lookup_one(self):
        md = E.table1_markdown(E.table1(grid(), accounting="expected", avg_budget=True,
                                        n_labels_grid=(30,), gate_draws=3, n_boot=30))
        for block in (md, md.split("Realised mean price")[1]):
            self.assertLess(block.index("| avg_gated_equation_resolved |"),
                            block.index("| avg_gated_lookup |"))

    def test_a_default_run_records_the_freeze_and_every_fold_decision(self):
        """A run with no fold flag: results.json says two folds, and every deviation the gate ruled
        on at 1.0x carries the second fold's own margin and SD beside the first's."""
        d = tempfile.mkdtemp()
        try:
            base = write_cells(d)
            out = os.path.join(d, "frozen")
            with contextlib.redirect_stdout(io.StringIO()):
                CLI.main(base + ["--out", out])
            with open(os.path.join(out, "results.json"), encoding="utf-8") as fh:
                res = json.load(fh)
            self.assertEqual(res["gate_folds"], 2)
            self.assertEqual(res["ranking_of_record"], "equation_resolved")
            t1 = res["table1"]
            self.assertEqual(t1["gate_folds"], 2)
            one = list(t1["fractions"]).index(1.0)
            X1 = t1["budgets"][one]

            def both(rec, where):
                self.assertEqual(rec["n_folds"], 2, where)
                self.assertEqual(len(rec["folds"]), 1, where)
                for f in rec["folds"]:
                    self.assertIsNotNone(f["margin_pts"], where)
                    self.assertIsNotNone(f["sd_pts"], where)
                    self.assertIsNotNone(f["bar_pts"], where)

            seen = 0
            for name in ("gated_equation", "gated_equation_resolved"):
                row = t1["rows"][name]
                self.assertEqual(row["gate_folds"], 2, name)
                # the free set: one record per cell pair the gate ruled on
                for dec in row.get("gate_decisions") or []:
                    both(dec, (name, dec["pick"]))
                    seen += 1
                # the structured families, at the 1.0x budget
                for rec in row.get("family_decisions") or []:
                    if rec["X"] == X1 and rec["folds"] is not None:
                        both(rec, (name, rec["family"]))
                        seen += 1
            for name in P.AVG_GATED_ARMS:
                row = t1["rows"][name]
                self.assertEqual(row["gate_folds_per_budget"][one], 2, name)
                if row["deviation_family"][one] is not None:
                    detail = row["gate_fold_detail"][one]
                    self.assertIsNotNone(detail, name)
                    self.assertEqual(len(detail), 1, name)
                    for f in detail:
                        self.assertIsNotNone(f["margin_pts"], name)
                        self.assertIsNotNone(f["sd_pts"], name)
                    seen += 1
                for rec in row.get("family_decisions") or []:
                    if rec["folds"] is not None:
                        both(rec, name)
                        seen += 1
            self.assertGreater(seen, 0, "no gate decision on this grid carried a second fold")
        finally:
            shutil.rmtree(d, ignore_errors=True)


def repro_available():
    return all(os.path.isfile(os.path.join(
        ARTIFACTS, "cells_%s_%s_natural_k%d.jsonl" % (REPRO_GRID[1], REPRO_GRID[0], k)))
        for k in (1, 2, 3, 4))


@unittest.skipUnless(repro_available(), "the production cell files are not on this machine")
class TestReproducesComputeDotPy(unittest.TestCase):
    """The resolved surface on a production grid must be compute.py's, to 0.05 of a point.

    The reference is work/analysis_2026-09-18/equation/resolved_fit.csv, which loads the grid with no
    calibration promotion, so this test loads it the same way: the first 100 questions calibrate and
    `c` and `l` come from the first `n_labels` of them in id order.
    """

    @classmethod
    def setUpClass(cls):
        import warnings
        task, model = REPRO_GRID
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cls.cs = C.load(ARTIFACTS, task, model, L=24, L_fixed=0)
        cls.cal, cls.ev = cls.cs.select("cal"), cls.cs.select("eval")
        cls.ev_mean = np.nanmean(cls.cs.acc[:, :, cls.ev], axis=2)

    def _rmse(self, A):
        return float(100 * np.sqrt(np.nanmean((A - self.ev_mean) ** 2)))

    def test_the_grid_is_the_one_compute_py_read(self):
        self.assertEqual(len(self.cal), 100)
        self.assertEqual(len(self.ev), 1900)
        self.assertEqual(list(self.cs.ks), [1, 2, 3, 4])
        self.assertEqual(len(self.cs.caps), 10)

    def test_the_resolved_evaluation_rmse_matches(self):
        for n_labels, want in REPRO_RMSE_EVAL.items():
            got = self._rmse(E.resolved_surface(self.cs, self.cal, n_labels=n_labels)[0])
            self.assertAlmostEqual(got, want, delta=REPRO_TOL,
                                   msg="n_labels=%d: got %.4f, compute.py %.4f"
                                       % (n_labels, got, want))

    def test_the_pooled_evaluation_rmse_matches_too(self):
        """The pooled column is unchanged by this work, so it pins that nothing moved under it."""
        import warnings
        for n_labels, want in REPRO_RMSE_EVAL_POOLED.items():
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                got = self._rmse(E.surface(self.cs, self.cal, n_labels=n_labels)[0])
            self.assertAlmostEqual(got, want, delta=REPRO_TOL,
                                   msg="n_labels=%d: got %.4f, compute.py %.4f"
                                       % (n_labels, got, want))

    def test_the_resolved_surface_finds_the_cap_zero_optimum_the_pooled_one_misses(self):
        """compute.py's argmax columns for this grid: evaluation k4_T0, pooled k4_T4096,
        resolved k4_T0 at 100 labels."""
        import warnings
        A_res = E.resolved_surface(self.cs, self.cal, n_labels=100)[0]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            A_hat = E.surface(self.cs, self.cal, n_labels=100)[0]
        cell = lambda A: (self.cs.ks[int(np.unravel_index(np.argmax(A), A.shape)[0])],
                          self.cs.caps[int(np.unravel_index(np.argmax(A), A.shape)[1])])
        self.assertEqual(cell(self.ev_mean), (4, 0))
        self.assertEqual(cell(A_res), (4, 0))
        self.assertEqual(cell(A_hat), (4, 4096))


if __name__ == "__main__":
    unittest.main()
