"""Check frozen real-data policy gains and checkpoint differences within 0.1 percentage point.

Two gain statistics are pinned separately because they answer different questions: GAIN_* is the
headline, the equal-weight mean over the qualifying budgets; POOLED_* is the mean over every
feasible (prompt, budget) pair, which weights a budget by how many prompts can afford it.

Both sets, and the checkpoint contrasts, are pinned regression values."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alloc import cells as C                          # noqa: E402
from alloc import evaluate as E                       # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S33 = os.path.join(ROOT, "s33_anytime", "artifacts")
S26 = os.path.join(ROOT, "s26_bbh", "artifacts")
TOL = 0.1

GAIN_LOOKUP_A0 = {"gsm8k": 14.0, "math500": 17.4, "svamp": 5.2, "aqua": 4.1, "csqa": 3.3,
                  "logical_deduction_five_objects": 6.8}
POOLED_LOOKUP_A0 = {"gsm8k": 13.4, "math500": 17.3, "svamp": 5.2, "aqua": 4.0, "csqa": 3.3,
                    "logical_deduction_five_objects": 6.8}
GAIN_EQ30_A0 = {"gsm8k": 14.1, "math500": 17.4, "svamp": 5.8, "aqua": 3.8,
                "logical_deduction_five_objects": 7.2}
POOLED_EQ30_A0 = {"gsm8k": 13.6, "math500": 17.3, "svamp": 5.8, "aqua": 3.8,
                  "logical_deduction_five_objects": 7.2}
CONTRAST_S33_MINUS_A0 = {("gsm8k", "Blow"): 11.7, ("math500", "Blow"): -0.4,
                         ("gsm8k", "Bstar"): 2.8, ("math500", "Bstar"): -4.1}

_CACHE = {}


def grid(task, ckpt):
    key = (task, ckpt)
    if key not in _CACHE:
        if task in C.BBH_TASKS and ckpt == "A0":
            _CACHE[key] = C.load(S26, task, "base", name="A0", bbh_base=True)
        else:
            _CACHE[key] = C.load(S33, task, ckpt)
    return _CACHE[key]


def available():
    return os.path.isdir(S33) and os.path.isdir(S26)


@unittest.skipUnless(available(), "the cell files are not on this machine")
class TestReproduction(unittest.TestCase):
    """Deviations are accumulated so the report can quote one maximum."""

    devs = []

    def _check(self, label, got, want):
        dev = abs(got - want)
        TestReproduction.devs.append((label, got, want, dev))
        self.assertLessEqual(dev, TOL, "%s: got %+.2f, frozen %+.1f" % (label, got, want))

    def test_gain_over_normal_lookup(self):
        for task, want in GAIN_LOOKUP_A0.items():
            g = E.gain_over_normal(grid(task, "A0"), ranking="lookup", n_boot=1, n_cal_draws=1)
            self._check("gain lookup %s" % task, g["gain_mean_pts"], want)
            self._check("pooled lookup %s" % task, g["pooled_gain_mean_pts"],
                        POOLED_LOOKUP_A0[task])

    def test_gain_over_normal_equation_30_labels(self):
        for task, want in GAIN_EQ30_A0.items():
            g = E.gain_over_normal(grid(task, "A0"), ranking="equation", n_labels=30,
                                   n_boot=1, n_cal_draws=1)
            self._check("gain equation30 %s" % task, g["gain_mean_pts"], want)
            self._check("pooled equation30 %s" % task, g["pooled_gain_mean_pts"],
                        POOLED_EQ30_A0[task])
            self.assertEqual(g["mechanism"]["n_labels"], 30)
            self.assertEqual(g["mechanism"]["n_g"], 100)

    def test_checkpoint_contrasts(self):
        for (task, which), want in CONTRAST_S33_MINUS_A0.items():
            r = E.contrast(grid(task, "s33"), grid(task, "A0"), which=which, n_boot=1)
            self._check("contrast %s %s" % (task, which), r["mean_pts"], want)
            self.assertEqual(r["reference"], "A0")

    def test_math500_blow_drops_the_same_questions(self):
        """Check that the paired lower-budget range retains exactly 274 complete evaluation prompts."""
        r = E.contrast(grid("math500", "s33"), grid("math500", "A0"), which="Blow", n_boot=1)
        self.assertEqual(r["n_eval"], 274)

    def test_the_reserve_is_the_same_on_both_checkpoints(self):
        """Check checkpoint reserve parity despite differing realised read-out token lengths."""
        for task, budget in (("gsm8k", 12), ("math500", 32), ("svamp", 8), ("csqa", 8)):
            a, b = grid(task, "s33"), grid(task, "A0")
            self.assertTrue(a.reserve_is_constant(), task)
            self.assertTrue(b.reserve_is_constant(), task)
            self.assertEqual(a.answer_budget_used()["answer_budget"], [float(budget)], task)
            self.assertEqual(list(a.reserve), list(b.reserve), task)
        # and the realised counts really do differ between the two checkpoints, which is the cause
        a, b = grid("gsm8k", "s33"), grid("gsm8k", "A0")
        self.assertNotEqual(float(a.answer_tokens_realised[0, 0, 0]),
                            float(b.answer_tokens_realised[0, 0, 0]))


if __name__ == "__main__":
    unittest.main()
