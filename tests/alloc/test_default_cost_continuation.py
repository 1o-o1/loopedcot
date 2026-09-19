"""The default row of a continuation grid: a problem whose chain ran into the old horizon carries
that horizon as its natural stop on the cells copied from below it, and its real stop on the cell the
continuation regenerated. The default cost and accuracy must read the real stop, not the copied one."""
import json
import os
import sys
import tempfile
import unittest

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
import synth                                                          # noqa: E402
from alloc import cells as C, evaluate as E                           # noqa: E402

MODEL, TASK = "ouro_1_4b_base", "gsm8k"
OLD, NEW = max(synth.CAPS), 1024                                      # the old horizon and the extension


class TestDefaultCostOnAContinuationGrid(unittest.TestCase):
    def _grid(self):
        rows = [r for r in synth.rows(n=12, n_cal=4, production=True) if not r.get("_header")]
        out = []
        for r in rows:
            out.append(r)
            if int(r["B"]) != OLD:
                continue
            ext = dict(r, B=NEW)
            if int(r["row_idx"]) == 0:
                # problem 0 ran into the old horizon: its copied cells say the stop is the horizon
                # itself, the regenerated cell knows the chain stopped 200 tokens later and reads
                # out differently
                r["natural_stop"], r["n_cut"], r["n_generated"] = OLD, OLD, OLD
                ext["natural_stop"], ext["n_cut"], ext["n_generated"] = OLD + 200, OLD + 200, OLD + 200
                ext["correct_v2"] = not bool(r["correct_v2"])
            out.append(ext)
        d = tempfile.mkdtemp()
        for k in synth.KS:
            with open(os.path.join(d, "cells_%s_%s_natural2h_k%d.jsonl" % (MODEL, TASK, k)), "w") as f:
                f.write(json.dumps({"_header": True}) + "\n")
                for r in out:
                    if r["k"] == k:
                        f.write(json.dumps(r) + "\n")
        return C.load(d, TASK, MODEL, L=24, L_fixed=0, protocol="natural2h", cache=False)

    def test_the_default_reads_the_regenerated_cell_of_a_continued_problem(self):
        cs = self._grid()
        self.assertEqual(cs.caps[-1], NEW)
        ki, j_old, j_new = cs.ks.index(cs.ks[-1]), cs.caps.index(OLD), cs.caps.index(NEW)
        n0 = list(cs.idx).index(0)
        pos = cs.select("all") if hasattr(cs, "select") else np.arange(len(cs.idx))
        dc = E.default_cost(cs, promptfree=False, split="all")
        acc = E.default_accuracy(cs, split="all")
        # every other problem stops inside the old caps, so only problem 0 can move the mean
        cost_new = float(cs.passes[ki, j_new, n0]); cost_old = float(cs.passes[ki, j_old, n0])
        self.assertGreater(cost_new, cost_old)
        others = [float(cs.passes[ki, min(j for j in range(len(cs.caps)) if cs.ncut[ki, j, n] >= cs.nstop[ki, j, n] - 1e-9), n])
                  for n in pos if n != n0]
        self.assertAlmostEqual(dc["mean"], (sum(others) + cost_new) / (len(others) + 1), places=3)
        self.assertEqual(float(acc[list(pos).index(n0)]), float(cs.acc[ki, j_new, n0]))
        self.assertNotEqual(float(cs.acc[ki, j_new, n0]), float(cs.acc[ki, j_old, n0]))


if __name__ == "__main__":
    unittest.main()
