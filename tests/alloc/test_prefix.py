"""alloc.prefix: the prefix-cached pricing, a third accounting of the same grid.

A prefix-cached grid is priced prompt-inclusive on prompts that have had the shared exemplar block
taken off them, so the pricing is pinned at both ends of its own range:

  S = 0   nothing is cached and the prices are the prompt-inclusive ones, to the last digit;
  S = P   the whole prompt is cached and the prices are the prompt-free ones, to the last digit.

Between those two the only thing that can vary is S itself, so the third test plants a task whose
questions carry two different exemplar blocks and checks that each block gets its own value: a cache
is keyed on the text it holds, not on the task slot.

  python -m pytest tests/alloc/test_prefix.py -q
"""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np                                    # noqa: E402

from alloc import evaluate as E                       # noqa: E402
from alloc import policy as P                         # noqa: E402
from alloc import prefix as PX                        # noqa: E402

import synth                                          # noqa: E402

BLOCK_A = [7, 7, 7, 7, 7]                             # 5 shared tokens
BLOCK_B = [9, 9]                                      # 2 shared tokens


def grid():
    return synth.cells(n=60, n_cal=20)


def prices(cs, promptfree, accounting):
    """Every cell's price for every question under one pricing, as one flat array."""
    cost = P.cost_of(cs, promptfree, accounting=accounting)
    return P.price_tensor(cs, np.arange(len(cs.idx)), cost).ravel()


class TestTheTwoEndsOfTheRange(unittest.TestCase):
    """S = 0 is prompt-inclusive and S = P is prompt-free, both exactly."""

    def test_no_shared_prefix_is_prompt_inclusive(self):
        cs = grid()
        got = PX.with_prefix_cached(cs, 0)
        for accounting in P.ACCOUNTINGS:
            np.testing.assert_array_equal(prices(got, False, accounting),
                                          prices(cs, False, accounting))
        self.assertEqual(E.default_cost(got, promptfree=False)["mean"],
                         E.default_cost(cs, promptfree=False)["mean"])

    def test_the_whole_prompt_shared_is_prompt_free(self):
        cs = grid()
        got = PX.with_prefix_cached(cs, cs.ptok)
        for accounting in P.ACCOUNTINGS:
            np.testing.assert_allclose(prices(got, False, accounting),
                                       prices(cs, True, accounting), rtol=0, atol=0)
        self.assertEqual(E.default_cost(got, promptfree=False)["mean"],
                         E.default_cost(cs, promptfree=True)["mean"])

    def test_table1_at_the_two_ends_matches_the_pricing_it_reproduces(self):
        cs = grid()
        kw = dict(accounting="expected", avg_budget=True, n_labels_grid=(30,), gate_draws=5,
                  n_boot=20, n_select=10, n_verify=10)
        zero = E.table1(PX.with_prefix_cached(cs, 0), promptfree=False, **kw)
        whole = E.table1(PX.with_prefix_cached(cs, cs.ptok), promptfree=False, **kw)
        pi = E.table1(cs, promptfree=False, **kw)
        pf = E.table1(cs, promptfree=True, **kw)
        for arm in ("default_at_budget", P.AVG_GATED, "equation_resolved"):
            np.testing.assert_allclose(zero["rows"][arm]["acc_pts"], pi["rows"][arm]["acc_pts"])
            np.testing.assert_allclose(whole["rows"][arm]["acc_pts"], pf["rows"][arm]["acc_pts"])

    def test_the_shared_tokens_are_carried_on_the_copy_and_the_original_is_untouched(self):
        cs = grid()
        before = np.array(cs.ptok, float)
        got = PX.with_prefix_cached(cs, 100)
        np.testing.assert_array_equal(cs.ptok, before)
        np.testing.assert_array_equal(got.ptok, before - 100)
        np.testing.assert_array_equal(got.prefix_shared_tokens, np.full(len(cs.idx), 100.0))
        # the prompt-free field is not a prefix-cached price and is left alone
        np.testing.assert_array_equal(got.passes_pf, cs.passes_pf)


class TestOneValuePerExemplarBlock(unittest.TestCase):
    """A pooled task carries two blocks, so it gets two shared-prefix values, one per block."""

    def encoded(self, cells, _tokenizer, **_kw):
        enc, keys = [], []
        for i in range(len(cells.idx)):
            b = "a" if (i % 2) == 0 else "b"
            keys.append(b)
            enc.append((BLOCK_A if b == "a" else BLOCK_B) + [1000 + i])
        return enc, keys

    def test_a_two_block_task_gets_two_shared_prefixes(self):
        cs = grid()
        with mock.patch.object(PX, "prompt_token_ids", self.encoded):
            S = PX.shared_prefix(cs, tokenizer=None)
        self.assertEqual(len(S), len(cs.idx))
        self.assertEqual(sorted(set(S.tolist())), [2.0, 5.0])
        self.assertTrue((S[0::2] == 5.0).all())
        self.assertTrue((S[1::2] == 2.0).all())

    def test_the_two_blocks_are_priced_apart(self):
        cs = grid()
        with mock.patch.object(PX, "prompt_token_ids", self.encoded):
            got = PX.with_prefix_cached(cs, PX.shared_prefix(cs, tokenizer=None))
        np.testing.assert_array_equal(got.ptok, np.asarray(cs.ptok, float)
                                      - np.where(np.arange(len(cs.idx)) % 2 == 0, 5.0, 2.0))

    def test_one_block_gives_one_value(self):
        seqs = [[4, 4, 4, 1], [4, 4, 4, 2], [4, 4, 4, 3]]
        self.assertEqual(PX.common_prefix_len(seqs), 3)
        self.assertEqual(PX.common_prefix_len([[4, 4, 4]] + seqs), 3)
        self.assertEqual(PX.common_prefix_len([]), 0)
        self.assertEqual(PX.common_prefix_len([[1, 2], [3, 4]]), 0)


class TestWhatIsRefused(unittest.TestCase):
    """A shared prefix that is not a prefix is an error, never a silently clipped price."""

    def test_a_negative_shared_prefix_is_refused(self):
        with self.assertRaises(ValueError):
            PX.with_prefix_cached(grid(), -1)

    def test_a_prefix_longer_than_a_prompt_is_refused(self):
        cs = grid()
        with self.assertRaises(ValueError):
            PX.with_prefix_cached(cs, float(np.max(cs.ptok)) + 1)

    def test_one_value_per_question_or_one_for_all_and_nothing_else(self):
        cs = grid()
        with self.assertRaises(ValueError):
            PX.with_prefix_cached(cs, np.zeros(len(cs.idx) - 1))
        with self.assertRaises(ValueError):
            PX.with_prefix_cached(cs, np.zeros((len(cs.idx), 2)))


if __name__ == "__main__":
    unittest.main()
