"""The loader: both file-name shapes, both row shapes, the reserve, and the grid assertions."""
import io
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np                                    # noqa: E402

from alloc import cells as C                          # noqa: E402
from alloc import mechanism as M                      # noqa: E402
import synth                                          # noqa: E402


class TestReserve(unittest.TestCase):
    def test_reserve_is_constant_per_task(self):
        """Check that reserve tokens equal suffix tokens plus the fixed task allowance."""
        for task, budget in (("gsm8k", 12), ("math500", 32), ("svamp", 8), ("aqua", 8),
                             ("csqa", 8), ("logical_deduction_five_objects", 8)):
            cs = synth.cells(n=60, task=task, n_cal=20, suffix=4, realised_answer=3)
            self.assertTrue(cs.reserve_is_constant(), task)
            self.assertTrue(np.all(cs.reserve == 4 + budget), task)
            self.assertEqual(cs.answer_budget_used()["answer_budget"], [float(budget)], task)

    def test_realised_answer_never_enters_the_reserve(self):
        a = synth.cells(n=60, n_cal=20, realised_answer=3)
        b = synth.cells(n=60, n_cal=20, realised_answer=5)
        np.testing.assert_array_equal(a.reserve, b.reserve)
        self.assertEqual(float(a.answer_tokens_realised[0, 0, 0]), 3.0)
        self.assertEqual(float(b.answer_tokens_realised[0, 0, 0]), 5.0)

    def test_answer_budget_kinds(self):
        self.assertEqual(C.answer_budget("gsm8k"), 12)
        self.assertEqual(C.answer_budget("svamp"), 8)
        self.assertEqual(C.answer_budget("math500"), 32)
        self.assertEqual(C.answer_budget("aqua"), 8)
        self.assertEqual(C.answer_budget("sports_understanding"), 8)


class TestProductionFormat(unittest.TestCase):
    def test_production_rows_load_identically(self):
        """A production file (a `_header` line, `row_idx`, `kind`, `subtask`, and the RESERVE in
        `n_answer_tokens`) must give the same table as the spike file (the REALISED read-out length
        in the same field)."""
        spike = C.Cells(synth.rows(n=60, n_cal=20, production=False), "gsm8k", name="spike",
                        ks=synth.KS, caps=synth.CAPS)
        prod = C.Cells(synth.rows(n=60, n_cal=20, production=True), "gsm8k", name="prod",
                       ks=synth.KS, caps=synth.CAPS)
        self.assertEqual(spike.idx, prod.idx)
        np.testing.assert_array_equal(spike.acc, prod.acc)
        np.testing.assert_array_equal(spike.ptok, prod.ptok)
        np.testing.assert_array_equal(spike.reserve, prod.reserve)
        np.testing.assert_array_equal(spike.passes, prod.passes)
        self.assertEqual(list(spike.split), list(prod.split))
        self.assertTrue(np.all(spike.pred == prod.pred))

    def test_header_line_is_not_a_cell(self):
        r = synth.rows(n=10, n_cal=4, production=True)
        self.assertTrue(r[0].get("_header"))
        cs = C.Cells([x for x in r if not x.get("_header")], "gsm8k", ks=synth.KS,
                     caps=synth.CAPS)
        self.assertEqual(len(cs.idx), 10)

    def test_row_kind_overrides_the_task_default(self):
        """The pooled BBH slot carries the answer kind on the ROW; it must win."""
        rows = synth.rows(n=20, n_cal=8, task="gsm8k", production=True, kind="letter")
        cs = C.Cells([r for r in rows if not r.get("_header")], "gsm8k", ks=synth.KS,
                     caps=synth.CAPS)
        self.assertTrue(np.all(cs.reserve == 4 + 8))


class TestCompleteness(unittest.TestCase):
    def test_missing_cell_raises(self):
        rows = [r for r in synth.rows(n=30, n_cal=10)
                if not (r["k"] == 2 and r["B"] == 64 and r["idx"] == 7)]
        with self.assertRaises(AssertionError):
            C.Cells(rows, "gsm8k", ks=synth.KS, caps=synth.CAPS)

    def test_cell_dependent_reserve_raises(self):
        rows = synth.rows(n=20, n_cal=8)
        for r in rows:
            if r["k"] == 4 and r["B"] == 512:
                r["n_suffix_tokens"] = 99
        with self.assertRaises(ValueError):
            C.Cells(rows, "gsm8k", ks=synth.KS, caps=synth.CAPS)


class TestParsing(unittest.TestCase):
    def test_bbh_parse_and_eos_strip(self):
        self.assertEqual(C.bbh_parse(" (D).\n\nQ: If"), "(D)")
        self.assertEqual(C.bbh_parse(" B. something"), "(B)")
        self.assertEqual(C.bbh_parse(" (A).<|endoftext|> (C)"), "(A)")
        self.assertIsNone(C.bbh_parse("no letter here"))

    def test_norm_answer(self):
        self.assertEqual(C.norm_answer("1,024"), ("num", 1024.0))
        self.assertEqual(C.norm_answer("(B)"), ("str", "b"))
        self.assertIsNone(C.norm_answer("None"))
        self.assertIsNone(C.norm_answer(None))


class TestProductionFileNames(unittest.TestCase):
    """Production files put the MODEL first and may split one depth over shards."""

    def _write(self, d, name, rows):
        with io.open(os.path.join(d, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps({"_header": True, "version": "PP3"}) + "\n")
            for r in rows:
                f.write(json.dumps(r) + "\n")

    def test_model_first_names_with_shards_are_found_and_unioned(self):
        rows = [r for r in synth.rows(n=20, n_cal=8, production=True) if not r.get("_header")]
        with tempfile.TemporaryDirectory() as d:
            for k in synth.KS:
                kr = [r for r in rows if r["k"] == k]
                half = len(kr) // 2
                self._write(d, "cells_ouro_1_4b_base_gsm8k_natural_k%d_s1of2.jsonl" % k, kr[:half])
                self._write(d, "cells_ouro_1_4b_base_gsm8k_natural_k%d_s2of2.jsonl" % k, kr[half:])
            paths = C.cell_paths(d, "gsm8k", "ouro_1_4b_base")
            self.assertEqual(len(paths), 2 * len(synth.KS))
            cs = C.load(d, "gsm8k", "ouro_1_4b_base")
            self.assertEqual(cs.ks, synth.KS)
            self.assertEqual(cs.caps, synth.CAPS)
            self.assertEqual(len(cs.idx), 20)

    def test_model_first_names_without_a_protocol_segment_are_found(self):
        rows = [r for r in synth.rows(n=10, n_cal=4, production=True) if not r.get("_header")]
        with tempfile.TemporaryDirectory() as d:
            for k in synth.KS:
                self._write(d, "cells_m1_gsm8k_k%d.jsonl" % k, [r for r in rows if r["k"] == k])
            self.assertEqual(len(C.cell_paths(d, "gsm8k", "m1")), len(synth.KS))
            self.assertEqual(len(C.load(d, "gsm8k", "m1").idx), 10)

    def test_task_first_spike_names_still_load(self):
        rows = synth.rows(n=10, n_cal=4)
        with tempfile.TemporaryDirectory() as d:
            for k in synth.KS:
                self._write(d, "cells_gsm8k_A0_fixed_k%d.jsonl" % k,
                            [r for r in rows if r["k"] == k])
            self.assertEqual(len(C.cell_paths(d, "gsm8k", "A0")), len(synth.KS))
            self.assertEqual(len(C.load(d, "gsm8k", "A0").idx), 10)

    def test_unparseable_lines_are_counted_not_swallowed(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "cells_m1_gsm8k_k1.jsonl")
            with io.open(p, "w", encoding="utf-8", newline="\n") as f:
                f.write(json.dumps({"_header": True}) + "\n")
                f.write('{"k": 1, "B": 0, "idx": 0}\n')
                f.write("{not json\n")
                f.write("also not json\n")
            stats = {}
            rows = C.read_rows(p, stats=stats)
            self.assertEqual(len(rows), 1)
            self.assertEqual(stats["unparsed"], 2)
            self.assertEqual(stats["header"], 1)


class TestGridFromRows(unittest.TestCase):
    """The depth set and the cap set come from the rows, not from a fixed protocol table."""

    def test_a_4096_cap_grid_loads_whole(self):
        caps = [0, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
        ks = [1, 2, 4, 8, 16, 32]
        rows = []
        for i in range(12):
            for k in ks:
                for T in caps:
                    rows.append({"row_idx": i, "k": k, "B": T, "split": "cal" if i < 5 else "eval",
                                 "task": "gsm8k", "kind": "numeric", "subtask": "gsm8k",
                                 "correct_v2": T >= 1024, "pred": "7" if T >= 1024 else "%d" % T,
                                 "gold": "7", "trace_answer": None, "n_cut": min(T, 900),
                                 "natural_stop": 900, "n_generated": min(T, 900) + 12,
                                 "n_prompt_tokens": 600, "n_suffix_tokens": 4,
                                 "n_answer_tokens": 12})
        cs = C.Cells(rows, "gsm8k", name="big")
        self.assertEqual(cs.ks, ks)
        self.assertEqual(cs.caps, caps)
        self.assertFalse(cs.missing())
        # commitment is anchored on the LARGEST loaded cap, so the settled tail is committed
        A = M.commitment(cs, cs.select("cal"))
        self.assertTrue(A[0, caps.index(4096), :].all())
        self.assertTrue(A[0, caps.index(1024), :].all())
        self.assertFalse(A[0, caps.index(512), :].any())

    def test_an_override_may_only_subset_the_rows(self):
        rows = synth.rows(n=10, n_cal=4)
        C.Cells(rows, "gsm8k", caps=[0, 64, 512])              # a subset is fine
        with self.assertRaises(ValueError):
            C.Cells(rows, "gsm8k", caps=[0, 64, 4096])
        with self.assertRaises(ValueError):
            C.Cells(rows, "gsm8k", ks=[1, 2, 99])


class TestFreeformKind(unittest.TestCase):
    def test_freeform_answer_budget(self):
        self.assertEqual(C.answer_budget("word_sorting"), 48)
        self.assertEqual(C.answer_budget("anything", kind="freeform"), 48)


if __name__ == "__main__":
    unittest.main()
