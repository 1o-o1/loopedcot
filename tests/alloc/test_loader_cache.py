"""The parsed-file cache: `alloc.cells.load` must reuse a parse, and never a stale one.

Every cells file is cached as a compressed numpy archive (pickle free) keyed by the file's size, its
mtime and the sha256 of its `_header` line, so a regenerated or extended shard invalidates its own
cache without anything being told. The contract these tests hold:

  1. a cached load equals a parsed load FIELD FOR FIELD
  2. a changed source file is reparsed, and the new rows are what comes back
  3. `--cache-dir` puts the archives somewhere else, `--no-cache` uses none and writes none
  4. the odd values survive the round trip: a missing key, a null, a string, a bool, a float
  5. through `alloc.cli` -- the only way a grid is ever read in anger -- the two flags behave the
     same way, and the three routes (cached, relocated, uncached) give byte-identical Table 1s

  python -m unittest test_loader_cache -v
"""
import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np                                    # noqa: E402

import synth                                          # noqa: E402
from alloc import cells as C                          # noqa: E402

TASK = "gsm8k"


def write_grid(d, rows=None, name="cells_SYN_gsm8k_natural_k1.jsonl"):
    """One production-shaped cells file, header line included, in directory `d`."""
    rows = synth.rows(n=12, task=TASK, n_cal=6, production=True) if rows is None else rows
    path = os.path.join(d, name)
    with open(path, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    return path


def fields_equal(case, a, b, skip=("read_stats",)):
    """Assert two Cells hold the same attributes with the same values, arrays included."""
    ka, kb = sorted(k for k in vars(a) if k not in skip), sorted(k for k in vars(b) if k not in skip)
    case.assertEqual(ka, kb)
    for k in ka:
        va, vb = getattr(a, k), getattr(b, k)
        if isinstance(va, np.ndarray):
            case.assertEqual(va.dtype.kind, vb.dtype.kind, k)
            np.testing.assert_array_equal(va, vb, err_msg=k)
        else:
            case.assertEqual(va, vb, k)


class TestTheCachedLoadIsTheParsedLoad(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.path = write_grid(self.d)
        self.addCleanup(shutil.rmtree, self.d, True)

    def test_a_cached_load_equals_a_parsed_load_field_for_field(self):
        cold = C.load(self.d, TASK, "SYN", L=24, L_fixed=0)
        self.assertTrue(os.path.exists(C.cache_path(self.path)))
        self.assertEqual(cold.read_stats.get("cached_files"), 0)
        warm = C.load(self.d, TASK, "SYN", L=24, L_fixed=0)
        self.assertEqual(warm.read_stats.get("cached_files"), 1)
        fields_equal(self, cold, warm)
        for key in ("rows", "header", "unparsed"):
            self.assertEqual(cold.read_stats[key], warm.read_stats[key], key)

    def test_the_rows_themselves_round_trip(self):
        rows = C.read_rows(self.path)
        C.write_cache(self.path, rows)
        back = C.read_cache(self.path)
        self.assertEqual(len(back), len(rows))
        self.assertEqual(back, rows)

    def test_the_odd_values_round_trip(self):
        rows = [{"idx": 0, "row_idx": 0, "k": 1, "B": 0, "split": "cal", "task": TASK,
                 "correct": True, "correct_v2": False, "pred": "7", "gold": None,
                 "trace_answer": None, "n_cut": 0, "natural_stop": 40.5, "n_generated": 12,
                 "n_prompt_tokens": 600, "n_suffix_tokens": 4, "n_answer_tokens": 12,
                 "kind": "numeric", "subtask": TASK, "options": ["A", "B"]},
                # the second row is MISSING two of those keys and carries a null where the first
                # carries a number, which is the pair a columnar cache can confuse
                {"idx": 1, "row_idx": 1, "k": 1, "B": 0, "split": "eval", "task": TASK,
                 "correct": False, "correct_v2": False, "pred": None, "gold": "3",
                 "n_cut": None, "natural_stop": None, "n_generated": 12,
                 "n_prompt_tokens": 600, "n_suffix_tokens": 4, "n_answer_tokens": 12,
                 "kind": "numeric", "subtask": TASK, "options": None}]
        path = write_grid(self.d, rows, name="cells_ODD_gsm8k_natural_k1.jsonl")
        C.write_cache(path, rows)
        back = C.read_cache(path)
        self.assertEqual(back, rows)
        for r, want in zip(back, rows):
            self.assertEqual(sorted(r), sorted(want))              # absence is not a null
            self.assertIsInstance(r["k"], int)
            self.assertIsInstance(r["correct"], bool)

    def test_a_changed_file_is_reparsed(self):
        cold = C.load(self.d, TASK, "SYN", L=24, L_fixed=0)
        more = synth.rows(n=12, task=TASK, n_cal=6, production=True)
        more = [r for r in more if not r.get("_header")]
        for r in more:
            r["idx"] = r["row_idx"] = int(r["row_idx"]) + 100
        with open(self.path, "a", encoding="utf-8") as fh:
            for r in more:
                fh.write(json.dumps(r) + "\n")
        warm = C.load(self.d, TASK, "SYN", L=24, L_fixed=0)
        self.assertEqual(warm.read_stats.get("cached_files"), 0)    # the key changed with the size
        self.assertGreater(len(warm.idx), len(cold.idx))
        again = C.load(self.d, TASK, "SYN", L=24, L_fixed=0)
        self.assertEqual(again.read_stats.get("cached_files"), 1)
        fields_equal(self, warm, again)

    def test_a_stale_archive_is_ignored_rather_than_read(self):
        rows = C.read_rows(self.path)
        C.write_cache(self.path, rows[:1])                         # pretend an older, shorter parse
        dest = C.cache_path(self.path)
        with np.load(dest, allow_pickle=False) as z:
            entries = {k: z[k] for k in z.files}
        entries["key"] = np.array("v0|1|1|deadbeef")
        np.savez_compressed(dest, **entries)
        self.assertIsNone(C.read_cache(self.path))
        cs = C.load(self.d, TASK, "SYN", L=24, L_fixed=0)
        self.assertEqual(cs.read_stats.get("cached_files"), 0)
        self.assertEqual(len(cs.idx), 12)

    def test_the_cache_dir_holds_the_archives_instead(self):
        cdir = os.path.join(self.d, "cache")
        cs = C.load(self.d, TASK, "SYN", L=24, L_fixed=0, cache_dir=cdir)
        self.assertFalse(os.path.exists(C.cache_path(self.path)))
        self.assertTrue(os.path.exists(C.cache_path(self.path, cdir)))
        warm = C.load(self.d, TASK, "SYN", L=24, L_fixed=0, cache_dir=cdir)
        self.assertEqual(warm.read_stats.get("cached_files"), 1)
        fields_equal(self, cs, warm)

    def test_no_cache_writes_nothing_and_reads_nothing(self):
        cs = C.load(self.d, TASK, "SYN", L=24, L_fixed=0, cache=False)
        self.assertFalse(os.path.exists(C.cache_path(self.path)))
        self.assertIsNone(cs.read_stats.get("cached_files"))
        C.write_cache(self.path, C.read_rows(self.path))
        off = C.load(self.d, TASK, "SYN", L=24, L_fixed=0, cache=False)
        self.assertIsNone(off.read_stats.get("cached_files"))
        fields_equal(self, cs, off)

    def test_an_unparseable_line_is_still_counted_from_the_cache(self):
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write("{not json\n")
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cold = C.load(self.d, TASK, "SYN", L=24, L_fixed=0)
            warm = C.load(self.d, TASK, "SYN", L=24, L_fixed=0)
        self.assertEqual(cold.read_stats["unparsed"], 1)
        self.assertEqual(warm.read_stats["unparsed"], 1)
        self.assertEqual(warm.read_stats["unparsed_paths"], cold.read_stats["unparsed_paths"])


class TestTheCliFlags(unittest.TestCase):
    """`--cache-dir` and `--no-cache` on `alloc.cli`. The CLI is how every grid is actually read,
    so the two flags are tested through it: the cache must be relocatable and removable, and the
    numbers it produces must not depend on which of the three it used."""

    BOOT = ["--boot", "20", "--cal-draws", "2", "--layers-per-loop", "24"]

    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.d, True)
        self.cells_dir = os.path.join(self.d, "cells")
        os.makedirs(self.cells_dir)
        self.path = write_grid(self.cells_dir,
                               synth.rows(n=150, task=TASK, n_cal=100, production=True))

    def run_cli(self, out, *extra):
        """Run `alloc.cli` into a fresh output directory; return (its return value, results.json)."""
        import contextlib
        import io as _io
        from alloc import cli
        dest = os.path.join(self.d, out)
        argv = ["--cells", self.cells_dir, "--task", TASK, "--checkpoint", "SYN",
                "--out", dest] + self.BOOT + list(extra)
        with contextlib.redirect_stdout(_io.StringIO()):
            res = cli.main(argv)
        with open(os.path.join(dest, "results.json"), encoding="utf-8") as fh:
            return res, json.load(fh)

    def test_the_cli_caches_beside_the_cells_by_default_and_reuses_it(self):
        _r, cold = self.run_cli("cold")
        self.assertTrue(os.path.exists(C.cache_path(self.path)))
        self.assertEqual(cold["read"]["cached_files"], 0)
        self.assertEqual(cold["read"]["cache"], True)
        self.assertIsNone(cold["read"]["cache_dir"])
        _r, warm = self.run_cli("warm")
        self.assertEqual(warm["read"]["cached_files"], 1)
        self.assertEqual(warm["read"]["files"], cold["read"]["files"])
        # the cache changes the wall time and nothing else
        self.assertEqual(warm["table1"], cold["table1"])
        self.assertEqual(warm["gain"], cold["gain"])

    def test_the_cache_dir_flag_moves_the_archives_and_leaves_the_cells_tree_clean(self):
        cdir = os.path.join(self.d, "elsewhere", ".alloc_cache")
        _r, cold = self.run_cli("cd_cold", "--cache-dir", cdir)
        self.assertFalse(os.path.exists(C.cache_path(self.path)))
        self.assertTrue(os.path.exists(C.cache_path(self.path, cdir)))
        self.assertEqual(cold["read"]["cached_files"], 0)
        self.assertEqual(cold["read"]["cache_dir"], cdir)
        _r, warm = self.run_cli("cd_warm", "--cache-dir", cdir)
        self.assertEqual(warm["read"]["cached_files"], 1)
        self.assertEqual(warm["table1"], cold["table1"])

    def test_no_cache_reads_none_writes_none_and_gives_the_same_numbers(self):
        _r, cached = self.run_cli("with")                       # writes the archive
        self.assertTrue(os.path.exists(C.cache_path(self.path)))
        _r, plain = self.run_cli("without", "--no-cache")
        self.assertEqual(plain["read"]["cache"], False)
        self.assertNotIn("cached_files", plain["read"])          # nothing was read from a cache
        self.assertEqual(plain["table1"], cached["table1"])
        self.assertEqual(plain["gain"], cached["gain"])
        # and a run with --no-cache on a clean tree writes no archive at all
        os.remove(C.cache_path(self.path))
        self.run_cli("without2", "--no-cache")
        self.assertFalse(os.path.exists(C.cache_path(self.path)))

    def test_a_changed_grid_invalidates_the_cli_cache(self):
        _r, cold = self.run_cli("v1")
        self.assertEqual(cold["read"]["cached_files"], 0)
        _r, warm = self.run_cli("v1b")
        self.assertEqual(warm["read"]["cached_files"], 1)
        more = [r for r in synth.rows(n=40, task=TASK, n_cal=0, production=True,
                                      idx_offset=1000) if not r.get("_header")]
        with open(self.path, "a", encoding="utf-8") as fh:
            for r in more:
                fh.write(json.dumps(r) + "\n")
        _r, after = self.run_cli("v2")
        self.assertEqual(after["read"]["cached_files"], 0)        # the key moved with the file
        self.assertGreater(after["n_cal_rule"]["n_questions"],
                           cold["n_cal_rule"]["n_questions"])
        _r, again = self.run_cli("v2b")
        self.assertEqual(again["read"]["cached_files"], 1)
        self.assertEqual(again["table1"], after["table1"])        # the new parse, not the old one


if __name__ == "__main__":
    unittest.main()
