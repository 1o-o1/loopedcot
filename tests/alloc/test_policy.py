"""Rankings on a planted optimum, the cost and budget conventions, and the gate."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np                                    # noqa: E402

from alloc import evaluate as E                       # noqa: E402
from alloc import mechanism as M                      # noqa: E402
from alloc import policy as P                         # noqa: E402
import synth                                          # noqa: E402


def _setup(n=120):
    cs = synth.cells(n=n, n_cal=40)
    cost = P.cost_of(cs)
    Pm, Rm = P.median_point(cs, cs.select("eval"))
    return cs, cost, Pm, Rm


class TestRankings(unittest.TestCase):
    def test_both_rankings_find_the_planted_optimum(self):
        cs, cost, Pm, Rm = _setup()
        lk, _ = P.rank_lookup(cs, cs.select("cal"), cost, Pm, Rm)
        A_hat, _m = E.surface(cs, cs.select("cal"))
        eq, _ = P.rank_equation(cs, A_hat, cost, Pm, Rm)
        self.assertEqual(lk[0], synth.PLANTED)
        self.assertEqual(eq[0], synth.PLANTED)

    def test_equation_reconstructs_the_measured_surface(self):
        cs = synth.cells(n=120, n_cal=40)
        m = M.mechanism(cs, cs.select("cal"))
        np.testing.assert_allclose(np.array(m["A_hat"]), np.array(m["acc_measured"]), atol=1e-9)
        self.assertLess(m["rmse_pts"], 1e-6)

    def test_ties_break_on_the_cheaper_cell(self):
        """Every cap above the arrival has the same accuracy, so the ranking must take the
        cheapest of them."""
        cs, cost, Pm, Rm = _setup()
        lk, acc = P.rank_lookup(cs, cs.select("cal"), cost, Pm, Rm)
        top = [c for c in lk if abs(acc[c] - acc[lk[0]]) < 1e-12]
        self.assertGreater(len(top), 1)
        self.assertEqual(lk[0], min(top, key=lambda c: cost(c[0], c[1], Pm, Rm)))


class TestCostAndBudgets(unittest.TestCase):
    def test_per_prompt_cost_formula(self):
        f = P.per_prompt_cost(24, promptfree=False, L_fixed=0)
        self.assertEqual(f(3, 64, 600, 16), 3 * 24 * (600 + 64 + 16))
        g = P.per_prompt_cost(24, promptfree=True, L_fixed=0)
        self.assertEqual(g(3, 64, 600, 16), 3 * 24 * (64 + 16))
        h = P.per_prompt_cost(6, promptfree=False, L_fixed=8)
        self.assertEqual(h(2, 32, 100, 8), (8 + 2 * 6) * (100 + 32 + 8))

    def test_sixteen_log_spaced_budgets_from_the_median_prompt(self):
        cs, cost, Pm, Rm = _setup()
        cmat = P.cost_matrix(cs, cost, Pm, Rm)
        Xs = P.budget_grid(cmat)
        self.assertEqual(len(Xs), 16)
        self.assertAlmostEqual(Xs[0] / cmat.min(), 1.0, places=6)
        self.assertAlmostEqual(Xs[-1] / cmat.max(), 1.0, places=6)
        ratios = Xs[1:] / Xs[:-1]
        self.assertTrue(np.allclose(ratios, ratios[0]))

    def test_per_prompt_feasibility_and_normal_operation(self):
        cs, cost, Pm, Rm = _setup()
        ev = cs.select("eval")
        lk, _ = P.rank_lookup(cs, cs.select("cal"), cost, Pm, Rm)
        cheap = cost(1, 0, Pm, Rm)                     # only (k=1, T=0) fits at the median prompt
        Pv, _rev = P.policy_vectors(cs, ev, cost, [cheap], lk)
        pv, nv = Pv[0]
        self.assertTrue(np.all(np.isnan(nv)))          # k_max never fits at that budget
        self.assertGreater(np.mean(np.isnan(pv)), 0.0)  # and the long prompts cannot afford it
        big = cost(4, 512, Pm, Rm) * 10
        Pv, _ = P.policy_vectors(cs, ev, cost, [big], lk)
        pv, nv = Pv[0]
        self.assertFalse(np.isnan(pv).any())
        self.assertFalse(np.isnan(nv).any())


class TestGate(unittest.TestCase):
    def test_gate_returns_the_pick_at_zero_and_normal_when_huge(self):
        A = np.zeros((4, 7))
        A[2, 3] = 0.9                                   # the pick
        A[3, 6] = 0.5                                   # normal operation
        sd = np.full((4, 7, 4, 7), 0.05)
        pick, normal = (2, 3), (3, 6)
        self.assertEqual(P.Gate(A, sd, 0.0).choose(pick, normal)[0], pick)
        self.assertEqual(P.Gate(A, sd, 1e6).choose(pick, normal)[0], normal)
        self.assertEqual(P.Gate(A, sd, 1.0).choose(pick, normal)[0], pick)   # 0.40 > 1 * 0.05
        sd_big = np.full((4, 7, 4, 7), 1.0)
        got, reverted = P.Gate(A, sd_big, 1.0).choose(pick, normal)
        self.assertEqual(got, normal)
        self.assertTrue(reverted)

    def test_gate_changes_the_policy_end_to_end(self):
        cs, cost, Pm, Rm = _setup()
        ev, cal = cs.select("eval"), cs.select("cal")
        A_hat, _ = E.surface(cs, cal)
        lk, _ = P.rank_lookup(cs, cal, cost, Pm, Rm)
        Xs = P.budget_grid(P.cost_matrix(cs, cost, Pm, Rm))
        base, _ = P.policy_vectors(cs, ev, cost, Xs, lk)
        sd = np.zeros((len(cs.ks), len(cs.caps), len(cs.ks), len(cs.caps)))
        shut, rev = P.policy_vectors(cs, ev, cost, Xs, lk,
                                     gate=P.Gate(A_hat, sd + 1e9, 1.0))
        self.assertGreater(max(rev), 0.0)
        for j in range(len(Xs)):
            np.testing.assert_array_equal(shut[j][0][~np.isnan(shut[j][1])],
                                          shut[j][1][~np.isnan(shut[j][1])])
        open_, rev0 = P.policy_vectors(cs, ev, cost, Xs, lk, gate=P.Gate(A_hat, sd, 0.0))
        self.assertEqual(max(rev0), 0.0)
        for j in range(len(Xs)):
            np.testing.assert_array_equal(np.nan_to_num(open_[j][0], nan=-1),
                                          np.nan_to_num(base[j][0], nan=-1))

    def test_margin_sd_shape_and_antisymmetry(self):
        draws = np.random.default_rng(0).normal(size=(20, 4, 7))
        sd = P.margin_sd(draws)
        self.assertEqual(sd.shape, (4, 7, 4, 7))
        self.assertAlmostEqual(sd[1, 2, 1, 2], 0.0)
        self.assertAlmostEqual(sd[1, 2, 3, 4], sd[3, 4, 1, 2])


if __name__ == "__main__":
    unittest.main()
