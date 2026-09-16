"""Regression checks for costs, calibration isolation, missing values, and paired resampling."""
import io
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from alloc import cells as C, cli, evaluate as E, mechanism as M, policy as P
import synth


class ReviewTests(unittest.TestCase):
    def test_row_idx_only_and_header_match_spike(self):
        rows = synth.rows(n=20, n_cal=10, production=True)
        for row in rows:
            row.pop("idx", None)
        actual = C.Cells(rows, "gsm8k")
        expected = synth.cells(n=20, n_cal=10)
        for field in ("acc", "pred", "ptok", "reserve", "passes", "passes_pf", "split"):
            np.testing.assert_array_equal(getattr(actual, field), getattr(expected, field))
        self.assertEqual(actual.idx, expected.idx)

    def test_commitment_checks_intermediate_and_last_caps(self):
        cs = synth.cells(n=20, n_cal=10)
        cs.pred[0, :, 0] = [("num", 1)] * len(cs.caps)
        cs.pred[0, 2, 0] = ("num", 2)
        result = M.commitment(cs, [0], caps=[0, 64])
        self.assertEqual(result[0, :, 0].tolist(), [False, True])
        cs.pred[0, -1, 0] = None
        self.assertFalse(M.commitment(cs, [0])[0].any())

    def test_rankings_ignore_evaluation_labels_and_unlabelled_calibration_labels(self):
        cs = synth.cells(n=40, n_cal=20)
        cal = cs.select("cal")
        cost = P.cost_of(cs)
        pm, rm = P.median_point(cs, cs.select("eval"))
        orders = [E.make_order(cs, cal, cost, pm, rm, rank)[0] for rank in ("lookup", "equation")]
        surface = E.surface(cs, cal, n_labels=5)[0]
        cs.acc[:, :, cs.select("eval")] = 1 - cs.acc[:, :, cs.select("eval")]
        for rank, expected in zip(("lookup", "equation"), orders):
            self.assertEqual(E.make_order(cs, cal, cost, pm, rm, rank)[0], expected)
        cs.acc[:, :, cal[5:]] = 1 - cs.acc[:, :, cal[5:]]
        np.testing.assert_array_equal(E.surface(cs, cal, n_labels=5)[0], surface)
        for gs, ls in E.calibration_resamples(cal, 5, 20, 9):
            self.assertTrue((ls < 5).all())
            self.assertEqual(len(gs), len(cal))
        with self.assertRaises(ValueError):
            E.surface(cs, cs.select("eval"))

    def test_gate_uses_strict_margin_even_at_zero(self):
        a = np.array([[.5, .5, .4]])
        gate = P.Gate(a, np.zeros((1, 3, 1, 3)), 0)
        self.assertEqual(gate.choose((0, 1), (0, 0)), ((0, 0), True))
        self.assertEqual(gate.choose((0, 2), (0, 0)), ((0, 0), True))

    def test_nan_scores_sort_last_and_ties_are_explicit(self):
        cs = synth.cells(n=20, n_cal=10)
        cost = lambda k, t, p, r: 1
        a = np.zeros((4, 7)); a[0, 0] = np.nan
        order, _ = P.rank_equation(cs, a, cost, 0, 0)
        self.assertEqual(order[-1], (1, 0))
        self.assertEqual(order[:-1], sorted(order[:-1]))

    def test_equal_budget_mean_and_shared_nan_bootstrap(self):
        """gain_mean_pts is the equal-weight mean over budgets (50 here, not 47.4); the mean pooled
        over feasible (prompt, budget) pairs survives only as pooled_gain_mean_pts, and both
        bootstraps resample one shared set of prompt columns."""
        cs = synth.cells(n=30, n_cal=20)
        pv1, nv1 = np.ones(10), np.zeros(10)
        pv1[-1] = nv1[-1] = np.nan
        pv2, nv2 = np.zeros(10), np.zeros(10)
        vectors = [(pv1, nv1), (pv2, nv2)]
        with patch.object(P, "policy_vectors", return_value=(vectors, [0, 0])):
            got = E.gain_over_normal(cs, n_budgets=2, n_boot=20, n_cal_draws=0, seed=4)
        self.assertEqual(got["gain_mean_pts"], 50)
        self.assertAlmostEqual(got["pooled_gain_mean_pts"], 100 * 9 / 19)
        self.assertEqual(got["n_eval_in_gain"], 10)
        rng = np.random.default_rng(4)
        matrix = np.stack([pv1 - nv1, pv2 - nv2])
        draws = [E._budget_mean(matrix[:, rng.integers(0, 10, 10)]) for _ in range(20)]
        np.testing.assert_allclose(got["gain_ci95_pts"], 100 * np.percentile(draws, [2.5, 97.5]))
        self.assertIsNotNone(got["pooled_gain_ci95_pts"])

    def test_gate_and_calibration_reranking_share_draws(self):
        cs = synth.cells(n=40, n_cal=20)
        cal = cs.select("cal")
        plan = E.calibration_resamples(cal, 5, 8, 4)
        gate, _ = E.gate_for(cs, cal, n_labels=5, resamples=plan)
        expected = P.margin_sd(np.stack([E.surface(cs, cal[gs], label_pos=cal[ls])[0]
                                         for gs, ls in plan]))
        np.testing.assert_allclose(gate.sd, expected)
        seen = []
        original = E.make_order
        def record(*args, **kwargs):
            if kwargs.get("boot_sel") is not None:
                seen.append((kwargs["boot_sel"], kwargs["label_sel"]))
            return original(*args, **kwargs)
        with patch.object(E, "make_order", side_effect=record), patch.object(E, "gate_for", wraps=E.gate_for) as fitted:
            E.gain_over_normal(cs, ranking="equation", n_labels=5, c_gate=.5,
                               n_cal_draws=8, gate_draws=2, n_boot=3, seed=4)
        supplied = fitted.call_args.kwargs["resamples"]
        self.assertEqual(len(seen), 8)
        for actual, expected in zip(seen, supplied):
            for a, b in zip(actual, expected):
                np.testing.assert_array_equal(a, b)

    def test_empty_complete_case_contrast(self):
        """The budgets come from the reference, so a first grid nothing is affordable on leaves the
        complete case empty rather than raising on an empty array."""
        cs = synth.cells(n=20, n_cal=10)
        other = synth.cells(n=20, n_cal=10)
        cs.ptok[:] = 1e12
        got = E.contrast(cs, other, n_boot=2)
        self.assertTrue(got["empty"])
        self.assertEqual(got["n_eval"], 0)

    def test_gate_selection_never_reads_evaluation_labels(self):
        cs = synth.cells(n=40, n_cal=20)
        evaluation = cs.select("eval")
        def evaluate_calibration(heldout, **kwargs):
            self.assertTrue(set(heldout.select("eval")).isdisjoint(evaluation))
            self.assertTrue(set(heldout.select("cal")).isdisjoint(evaluation))
            return {"gain_mean_pts": 1, "gain_worst_budget_pts": 0}
        with patch.object(E, "gain_over_normal", side_effect=evaluate_calibration):
            E.gate_selection({"a": cs, "b": cs}, c_grid=(0, .5), n_boot=1)
        np.testing.assert_array_equal(cs.select("eval"), evaluation)


class SecondPassTests(unittest.TestCase):
    """Table 1 feasibility, the headline gain statistic, reference pricing, and budget tolerance."""

    def test_table1_default_row_is_not_feasible_below_its_own_cost(self):
        """The deepest depth at natural stop costs the full default cost, so it cannot run at
        0.25x or 0.50x of it and must not report its uncapped accuracy there."""
        cs = synth.cells(n=80, n_cal=30)
        t1 = E.table1(cs, n_labels_grid=(10,), gate_draws=3)
        row = t1["rows"]["default"]
        self.assertEqual(row["feasible"], [False, False, True])
        self.assertTrue(np.isnan(row["acc_pts"][0]) and np.isnan(row["acc_pts"][1]))
        self.assertFalse(np.isnan(row["acc_pts"][2]))
        line = [l for l in E.table1_markdown(t1).split("\n") if l.startswith("| default |")][0]
        self.assertEqual(line.count("not feasible"), 2)

    def test_contrast_prices_the_budget_grid_from_the_reference(self):
        """The second grid is the reference: it supplies the median prompt, the cost function and
        the budget range, so a cheaper first grid cannot shrink the budgets it is read at."""
        rows = synth.rows(n=40, n_cal=15)
        a = C.Cells(rows, "gsm8k", name="a", ks=synth.KS, caps=synth.CAPS, L=6)
        b = C.Cells(rows, "gsm8k", name="b", ks=synth.KS, caps=synth.CAPS, L=24)
        got = E.contrast(a, b, which="Bstar", n_boot=5)
        cost_b = P.cost_of(b)
        pm, rm = P.median_point(b, b.select("eval"))
        grid = P.budget_grid(P.cost_matrix(b, cost_b, pm, rm))
        bstar, _blow, _meta = P.budget_ranges(b, cost_b, grid, pm, rm)
        self.assertEqual(got["reference"], "b")
        np.testing.assert_allclose(got["budgets"], [grid[i] for i in bstar])

    def test_budget_grid_is_not_inflated_and_affordability_carries_the_tolerance(self):
        """The grid spans exactly the cheapest and dearest cell; the float slack lives in the
        affordability test instead."""
        cs = synth.cells(n=40, n_cal=15)
        cost = P.cost_of(cs)
        pm, rm = P.median_point(cs, cs.select("eval"))
        cmat = P.cost_matrix(cs, cost, pm, rm)
        Xs = P.budget_grid(cmat)
        self.assertLess(abs(Xs[0] / cmat.min() - 1.0), 1e-12)
        self.assertLess(abs(Xs[-1] / cmat.max() - 1.0), 1e-12)
        self.assertTrue(P.affordable(cmat.min(), Xs[0]))
        self.assertTrue(P.affordable(cmat.max(), Xs[-1]))
        self.assertFalse(P.affordable(cmat.max() * 1.001, Xs[-1]))


CONFIG_FIXTURE = """version: PP3
caps: [0, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]

models:
  ouro_1_4b_base:
    repo: ByteDance/Ouro-1.4B
    layers: 24
    entries: ouro
    depths: [1, 2, 3, 4]

  ouro_2_6b_base:
    repo: ByteDance/Ouro-2.6B
    layers: 48
    entries: ouro
    depths: [1, 2, 3, 4]

  huginn_0125:
    repo: tomg-group-umd/huginn-0125
    prelude: 2
    core: 4
    coda: 2
    entries: raven
    depths: [1, 2, 4, 8, 16, 32]

  mcleish_llama32_r32:
    repo: smcleish/Recurrent-Llama-3.2-train-recurrence-32
    prelude: 4
    core: 6
    coda: 4
    entries: raven
    depths: [1, 2, 4, 8]

mem_util: 0.85
"""


class GeometryTests(unittest.TestCase):
    """Layers per loop and fixed layers come from a flag or a model config, never a hard default."""

    def _config(self, d):
        p = os.path.join(d, "config.yaml")
        with io.open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(CONFIG_FIXTURE)
        return p

    def test_geometry_of_each_family(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._config(d)
            self.assertEqual(C.model_geometry("ouro_1_4b_base", p), (24, 0))
            self.assertEqual(C.model_geometry("ouro_2_6b_base", p), (48, 0))
            self.assertEqual(C.model_geometry("huginn_0125", p), (4, 4))
            self.assertEqual(C.model_geometry("mcleish_llama32_r32", p), (6, 8))
            with self.assertRaises(KeyError):
                C.model_geometry("not_a_model", p)

    def test_huginn_price_of_a_deep_long_cell(self):
        with tempfile.TemporaryDirectory() as d:
            L, L_fixed = C.model_geometry("huginn_0125", self._config(d))
        price = P.per_prompt_cost(L, promptfree=False, L_fixed=L_fixed)
        self.assertEqual(price(32, 4096, 600, 12), 621456)

    def test_cli_refuses_an_unpinned_non_ouro_checkpoint(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(SystemExit):
                cli.resolve_geometry(cli._args(["--cells", d, "--task", "gsm8k",
                                                "--checkpoint", "huginn_0125", "--out", d]))
            pinned = cli.resolve_geometry(cli._args(
                ["--cells", d, "--task", "gsm8k", "--checkpoint", "huginn_0125", "--out", d,
                 "--layers-per-loop", "4", "--fixed-layers", "4"]))
            self.assertEqual(pinned, (4, 4))
            viaconf = cli.resolve_geometry(cli._args(
                ["--cells", d, "--task", "gsm8k", "--checkpoint", "huginn_0125", "--out", d,
                 "--model-config", self._config(d)]))
            self.assertEqual(viaconf, (4, 4))
            ouro = cli.resolve_geometry(cli._args(
                ["--cells", d, "--task", "gsm8k", "--checkpoint", "ouro_1_4b_base", "--out", d]))
            self.assertEqual(ouro, (24, 0))
