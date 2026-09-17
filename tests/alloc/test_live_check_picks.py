"""The live check's avg_gated_lookup picks are alloc's own picks for the same cells and budget."""
import json
import os
import sys
import tempfile
import unittest

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import synth                                                          # noqa: E402
from alloc import cells as C, evaluate as E, policy as P              # noqa: E402


class TestLiveCheckPicks(unittest.TestCase):
    def test_avg_gated_picks_equal_alloc_picks(self):
        rows = [r for r in synth.rows(n=60, n_cal=20, production=True) if not r.get("_header")]
        d = tempfile.mkdtemp()
        for k in synth.KS:
            with open(os.path.join(d, "cells_ouro_1_4b_base_gsm8k_natural_k%d.jsonl" % k), "w") as f:
                f.write(json.dumps({"_header": True}) + "\n")
                for r in rows:
                    if r["k"] == k:
                        f.write(json.dumps(r) + "\n")
        from prod.live_check import avg_gated_picks
        cs, X, rec, chosen, ev, dc = avg_gated_picks(d, "ouro_1_4b_base", "gsm8k", 0.5, c_gate=0.5,
                                                     gate_draws=8)
        # alloc's own computation, independently
        cs2 = C.load(d, "gsm8k", "ouro_1_4b_base", L=24, L_fixed=0)
        cost = P.cost_of(cs2, promptfree=False, accounting="expected")
        ev2, cal2 = cs2.select("eval"), cs2.select("cal")
        Pm, Rm = P.median_point(cs2, ev2)
        X2 = 0.5 * E.default_cost(cs2, promptfree=False)["mean"]
        score = E.cell_scores(cs2, cal2, P.AVG_GATED, cost, Pm, Rm)
        rec2 = E.avg_gated_vectors(cs2, ev2, cal2, cost, [X2], score, E.default_cell(cs2),
                                   c_gate=0.5, n_draws=8, seed=7)[0]
        self.assertAlmostEqual(X, X2)
        self.assertEqual(bool(rec.get("gate_reverted")), bool(rec2.get("gate_reverted")))
        if rec2.get("gate_reverted"):
            dk, dT = E.default_cell(cs2)
            expect = {int(cs2.idx[n]): (int(dk), int(dT)) for n in ev2}
        else:
            a, b = P.avg_picks(np.asarray(score, float), P.price_tensor(cs2, ev2, cost), rec2["lambda"])
            expect = {int(cs2.idx[n]): (int(cs2.ks[i]), int(cs2.caps[j])) for n, i, j in zip(ev2, a, b)}
        self.assertEqual(chosen, expect)
        self.assertEqual(len(chosen), len(ev2))


if __name__ == "__main__":
    unittest.main()
