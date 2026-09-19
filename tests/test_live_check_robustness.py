"""`prod.live_check`: a failed generation must say WHY, and a bad setup must be caught before the GPU.

129 of the 201 live files the cluster wrote came from generations that exited rc=1 inside 2.5
seconds, and the record held nothing but that rc. These tests pin the four repairs, with a stub
command in place of `prod.generate` so nothing here needs a GPU or a checkpoint:

  (a) every subprocess's stdout and stderr tail (40 lines) is in the run record, and the stderr
      tail is printed and written on failure
  (b) `--preflight` runs one throwaway generation first and exits 3 with the stderr if it fails
  (c) the only-rows file and the --out path are checked BEFORE anything is launched
  (d) a failed run writes NO result, only live_<...>.FAILED.json, and exits 2

  python -m pytest tests/test_live_check_robustness.py -q
"""
import io
import json
import os
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prod import live_check as lc                                    # noqa: E402

# Stubs standing in for `prod.generate`. Each is run as `python -c SCRIPT <out_dir>`.
FAIL = ("import sys; sys.stdout.write('loading model\\n'); "
        "sys.stderr.write('Traceback: OSError: ByteDance/Ouro-1.4B is not in the local cache\\n'); "
        "sys.exit(1)")
CHATTY = ("import sys\n"
          "for i in range(100): sys.stdout.write('out line %d\\n' % i)\n"
          "for i in range(100): sys.stderr.write('err line %d\\n' % i)\n")
WRITES_A_ROW = (
    "import json, os, sys\n"
    "p = os.path.join(sys.argv[1], 'cells_stub_gsm8k_natural_k1.jsonl')\n"
    "rows = [{'_header': True, 'version': 'PP3'},\n"
    "        {'row_idx': 0, 'idx': 0, 'k': 1, 'B': 0, 'correct_v2': True, 'layer_passes': 1.0}]\n"
    "open(p, 'w', encoding='utf-8').write(''.join(json.dumps(r) + chr(10) for r in rows))\n")


def stub(script):
    """A `generate_cmd` replacement running `script` with the run's output directory as argv[1]."""
    def make(model, task, k, B, out_dir, row_ids_path=None, **kw):
        return [sys.executable, "-c", script, out_dir]
    return make


class TestTheFailureSaysWhy(unittest.TestCase):
    def test_the_stderr_tail_reaches_the_failure_json_and_the_exit_code_is_two(self):
        with tempfile.TemporaryDirectory() as d:
            fail_path = os.path.join(d, "live_check_stub.FAILED.json")
            with mock.patch.object(lc, "generate_cmd", stub(FAIL)):
                with self.assertRaises(SystemExit) as cm:
                    lc.run_live("ouro_1_4b_base", "gsm8k", {7: (1, 0)}, [7], d,
                                fail_path=fail_path, context={"arm": "avg_gated_lookup"})
            self.assertEqual(cm.exception.code, 2)
            rec = json.load(open(fail_path, encoding="utf-8"))
            self.assertTrue(rec["failed"])
            self.assertEqual(rec["arm"], "avg_gated_lookup")          # the context travels with it
            self.assertEqual(rec["n_failed"], 1)
            run = rec["runs"][0]
            self.assertEqual(run["rc"], 1)
            self.assertIn("is not in the local cache", run["stderr_tail"])
            self.assertIn("loading model", run["stdout_tail"])

    def test_no_result_file_is_written_beside_the_failure_json(self):
        with tempfile.TemporaryDirectory() as d:
            fail_path = os.path.join(d, "live_check_stub.FAILED.json")
            with mock.patch.object(lc, "generate_cmd", stub(FAIL)):
                with self.assertRaises(SystemExit):
                    lc.run_live("m", "gsm8k", {7: (1, 0)}, [7], d, fail_path=fail_path)
            self.assertFalse(os.path.exists(os.path.join(d, "live_check_stub.json")))

    def test_only_the_last_forty_lines_of_each_stream_are_kept(self):
        with tempfile.TemporaryDirectory() as d:
            with mock.patch.object(lc, "generate_cmd", stub(CHATTY)):
                runs = lc.run_live("m", "gsm8k", {7: (1, 0)}, [7], d)
            self.assertEqual(runs[0]["rc"], 0)
            self.assertEqual(len(runs[0]["stdout_tail"].split("\n")), lc.TAIL_LINES)
            self.assertTrue(runs[0]["stdout_tail"].endswith("out line 99"))
            self.assertTrue(runs[0]["stderr_tail"].endswith("err line 99"))


class TestTheSetupIsCheckedBeforeTheGpu(unittest.TestCase):
    def test_the_preflight_exits_three_with_the_stderr(self):
        with tempfile.TemporaryDirectory() as d:
            with mock.patch.object(lc, "generate_cmd", stub(FAIL)):
                with self.assertRaises(SystemExit) as cm:
                    lc.preflight("ouro_1_4b_base", "gsm8k", out_dir=d)
            self.assertEqual(cm.exception.code, 3)

    def test_the_preflight_reports_the_resolved_path_the_python_and_the_env(self):
        with tempfile.TemporaryDirectory() as d:
            with mock.patch.object(lc, "generate_cmd", stub(WRITES_A_ROW)):
                info = lc.preflight("ouro_1_4b_base", "gsm8k", out_dir=d)
        self.assertEqual((info["rc"], info["n_rows"]), (0, 1))
        self.assertEqual(info["python"], sys.executable)
        self.assertEqual(info["model_path"]["repo"], "ByteDance/Ouro-1.4B")
        self.assertIn("hf_hub_offline", info)
        self.assertTrue(os.path.isdir(info["cwd"]))

    def test_an_unwritable_out_path_is_refused_and_leaves_no_file(self):
        with tempfile.TemporaryDirectory() as d:
            blocker = os.path.join(d, "afile")
            with open(blocker, "w", encoding="utf-8") as fh:
                fh.write("x")
            with self.assertRaises(SystemExit):
                lc.check_writable(os.path.join(blocker, "live.json"))
            ok = os.path.join(d, "sub", "live.json")
            self.assertTrue(lc.check_writable(ok))
            self.assertFalse(os.path.exists(ok))          # the probe leaves nothing behind

    def test_an_empty_only_rows_file_stops_the_run(self):
        """An empty --only-rows list would generate the WHOLE shard instead of the picks."""
        with tempfile.TemporaryDirectory() as d:
            with mock.patch.object(lc, "generate_cmd", stub(WRITES_A_ROW)):
                with mock.patch.object(lc, "save_json", lambda path, obj: path):
                    with self.assertRaises(SystemExit) as cm:
                        lc.run_live("m", "gsm8k", {7: (1, 0)}, [7], d)
        self.assertIn("row_ids", str(cm.exception))


if __name__ == "__main__":
    unittest.main()


class TestArms(unittest.TestCase):
    def test_every_recorded_arm_is_accepted_and_an_unknown_one_is_refused(self):
        """The four arms alloc records are all runnable; each gets past argparse and stops only at
        the (absent) alloc output directory, and a name alloc never records is refused by argparse
        (exit code 2) before anything else is looked at."""
        self.assertEqual(lc.ARMS, ("lookup", "avg_gated_lookup", "equation_resolved",
                                   "avg_gated_equation_resolved"))
        d = tempfile.mkdtemp()
        for arm in lc.ARMS:
            with self.assertRaises(SystemExit) as cm:
                lc.main(["--model", "m", "--task", "gsm8k", "--alloc-dir", d, "--arm", arm,
                         "--budget-fraction", "0.5"])
            self.assertIn("results.json", str(cm.exception), arm)
        with mock.patch("sys.stderr", new=io.StringIO()):
            with self.assertRaises(SystemExit) as cm:
                lc.main(["--model", "m", "--task", "gsm8k", "--alloc-dir", d, "--arm", "avg_gated_equation",
                         "--budget-fraction", "0.5"])
        self.assertEqual(cm.exception.code, 2)


class TestPriceAccounting(unittest.TestCase):
    def test_the_live_price_is_read_under_the_accounting_alloc_priced_the_budget_in(self):
        """An alloc run with --promptfree charges generated tokens only; the live price must then come
        from layer_passes_promptfree, else every check reports hundreds of percent over budget."""
        d = tempfile.mkdtemp()
        with open(os.path.join(d, "cells_x.jsonl"), "w") as f:
            f.write(json.dumps({"row_idx": 7, "idx": 7, "k": 4, "B": 512, "correct_v2": True,
                                "layer_passes": 60000, "layer_passes_promptfree": 4000}) + "\n")
        runs = [{"dir": d}]
        chosen = {7: (4, 512)}
        self.assertEqual(lc.collect_live(runs, chosen, promptfree=True)[1][7], 4000.0)
        self.assertEqual(lc.collect_live(runs, chosen, promptfree=False)[1][7], 60000.0)
        self.assertEqual(lc.price_field(True), "layer_passes_promptfree")
