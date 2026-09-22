"""cells.SETTLE_ANSWER: which answer the settle event is read off.

Planted grid: every question's FORCED read-out is "B" at every cap, so under the "forced" rule every
question settles at cap 0. Half the questions also write their OWN answer "A" (the gold) inside the
cut from cap 32 on, and the label of record scores that own answer. So for those questions the label
is wrong at caps 0 and 16 and right from cap 32: it MOVES after the forced settle cap. Under the
"scored" rule the same questions settle at cap 32, the label is constant from the settle cap on, and
the settle-resolved identity reproduces the measured surface exactly on a fully labelled grid.

  python -m pytest tests/alloc/test_settle_answer.py -q
"""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np                                    # noqa: E402

from alloc import cells as C                          # noqa: E402
from alloc import mechanism as M                      # noqa: E402

KS = [1, 2]
CAPS = [0, 16, 32, 64]
TASK = "csqa"
N = 40


def rows():
    out = []
    for i in range(N):
        writes_own = (i % 2) == 0
        for k in KS:
            for T in CAPS:
                own = "A" if (writes_own and T >= 32) else None
                ok = own == "A"
                out.append({"idx": i, "k": k, "B": T, "split": "cal" if i < 20 else "eval",
                            "task": TASK, "correct": False, "correct_v2": ok,
                            "pred": "B", "gold": "A",
                            "trace_answer": own, "trace_correct": ok,
                            "n_cut": min(T, 40), "natural_stop": 40,
                            "n_generated": min(T, 40) + 3,
                            "n_prompt_tokens": 300, "n_suffix_tokens": 2,
                            "n_answer_tokens": 3})
    return out


def grid(rule):
    with mock.patch.object(C, "SETTLE_ANSWER", rule):
        return C.Cells(rows(), TASK, name="settle_answer", ks=KS, caps=CAPS, L=4, L_fixed=0)


def max_identity_error(cs):
    pos = np.arange(len(cs.idx))
    m = M.resolved_mechanism(cs, pos, label_pos=pos, min_labels=1)
    return float(np.nanmax(np.abs(np.array(m["A_res"]) - np.array(m["acc_measured"]))))


class SettleAnswer(unittest.TestCase):
    def test_default_is_scored(self):
        self.assertEqual(C.SETTLE_ANSWER, "scored")
        self.assertEqual(grid("scored").settle_answer, "scored")

    def test_unknown_rule_is_an_error(self):
        with self.assertRaises(ValueError):
            grid("own")

    def test_forced_readout_is_kept_under_either_rule(self):
        for rule in C.SETTLE_ANSWERS:
            cs = grid(rule)
            self.assertTrue(all(p == ("str", "b") for p in cs.pred_forced.ravel()))

    def test_forced_rule_settles_everything_at_the_first_cap(self):
        cs = grid("forced")
        s = M.settle_time(cs, np.arange(N))
        self.assertTrue((s == 0).all())

    def test_scored_rule_settles_where_the_scored_answer_stops_moving(self):
        cs = grid("scored")
        s = M.settle_time(cs, np.arange(N))
        own = np.array([(i % 2) == 0 for i in range(N)])
        self.assertTrue((s[:, own] == CAPS.index(32)).all())
        self.assertTrue((s[:, ~own] == 0).all())

    def test_label_is_constant_after_the_scored_settle_cap(self):
        cs = grid("scored")
        s = M.settle_time(cs, np.arange(N))
        for a in range(len(KS)):
            for n in range(N):
                seg = cs.acc[a, s[a, n]:, n]
                self.assertTrue((seg == seg[-1]).all())

    def test_resolved_identity_is_exact_only_under_the_scored_rule(self):
        self.assertLess(max_identity_error(grid("scored")), 1e-12)
        # forced rule: c(0) is read at the last cap (0.5) and applied at caps 0 and 16, where the
        # measured accuracy is 0 -- an error of half the grid.
        self.assertAlmostEqual(max_identity_error(grid("forced")), 0.5, places=12)


if __name__ == "__main__":
    unittest.main()
