"""End to end on a synthetic grid whose optimum is known by construction.

Depth 3 settles at cap 64 and is right 90 percent of the time once settled; every other depth
settles later and is worse. So (k=3, T=64) is the best cell AND the cheapest cell on the accuracy
plateau. Both rankings must put it first, and at any budget that affords it the allocator must
actually run it and beat normal operation (k=4, which needs cap 128 to be worth anything).
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np                                    # noqa: E402

from alloc import evaluate as E                       # noqa: E402
from alloc import policy as P                         # noqa: E402
import synth                                          # noqa: E402


class TestKnownOptimum(unittest.TestCase):
    def setUp(self):
        self.cs = synth.cells(n=120, n_cal=40)
        self.cost = P.cost_of(self.cs)
        self.ev, self.cal = self.cs.select("eval"), self.cs.select("cal")
        self.Pm, self.Rm = P.median_point(self.cs, self.ev)

    def _order(self, ranking):
        return E.make_order(self.cs, self.cal, self.cost, self.Pm, self.Rm, ranking)[0]

    def test_both_rankings_pick_the_planted_cell(self):
        for ranking in ("lookup", "equation"):
            self.assertEqual(self._order(ranking)[0], synth.PLANTED, ranking)

    def test_the_allocator_runs_the_planted_cell_when_it_fits(self):
        k, T = synth.PLANTED
        pmax = float(self.cs.ptok.max())
        # a budget every prompt can spend on the planted cell AND on normal operation, which at
        # this price can only afford k=4 at cap 0 and is therefore worth nothing
        X = self.cost(4, 0, pmax, self.Rm)
        self.assertGreater(X, self.cost(k, T, pmax, self.Rm))
        for ranking in ("lookup", "equation"):
            Pv, _ = P.policy_vectors(self.cs, self.ev, self.cost, [X], self._order(ranking))
            pv, nv = Pv[0]
            self.assertFalse(np.isnan(pv).any(), ranking)
            self.assertFalse(np.isnan(nv).any(), ranking)
            self.assertAlmostEqual(float(pv.mean()), synth.P_RIGHT[k], places=6, msg=ranking)
            self.assertAlmostEqual(float(nv.mean()), 0.0, places=6, msg=ranking)

    def test_gain_over_normal_is_positive_and_agrees_between_rankings(self):
        gl = E.gain_over_normal(self.cs, ranking="lookup", n_boot=100, n_cal_draws=3)
        ge = E.gain_over_normal(self.cs, ranking="equation", n_boot=100, n_cal_draws=3)
        self.assertGreater(gl["gain_mean_pts"], 0.0)
        self.assertAlmostEqual(gl["gain_mean_pts"], ge["gain_mean_pts"], places=6)

    def test_thirty_labels_reach_the_same_ranking_head(self):
        full = E.make_order(self.cs, self.cal, self.cost, self.Pm, self.Rm, "equation")[0]
        few = E.make_order(self.cs, self.cal, self.cost, self.Pm, self.Rm, "equation",
                           n_labels=10)[0]
        self.assertEqual(full[0], few[0])


if __name__ == "__main__":
    unittest.main()
