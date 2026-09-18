"""`alloc.cli --protocol`: a directory holding the natural grid and a natural2 continuation of the
same pair loads only the grid asked for (the loader keys its files on the protocol segment)."""
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
import synth                                                          # noqa: E402
from alloc import cells as C, cli                                     # noqa: E402

MODEL, TASK = "ouro_1_4b_base", "gsm8k"


def write_grid(d, protocol, n):
    rows = [r for r in synth.rows(n=n, n_cal=20, production=True) if not r.get("_header")]
    for k in synth.KS:
        with open(os.path.join(d, "cells_%s_%s_%s_k%d.jsonl" % (MODEL, TASK, protocol, k)), "w") as f:
            f.write(json.dumps({"_header": True}) + "\n")
            for r in rows:
                if r["k"] == k:
                    f.write(json.dumps(r) + "\n")


class TestCliProtocol(unittest.TestCase):
    def test_natural_and_natural2_side_by_side_load_only_the_requested_grid(self):
        d = tempfile.mkdtemp()
        write_grid(d, "natural", 60)
        write_grid(d, "natural2", 40)
        # the loader itself
        self.assertEqual(len(C.load(d, TASK, MODEL, L=24, L_fixed=0, cache=False).idx), 60)
        self.assertEqual(len(C.load(d, TASK, MODEL, L=24, L_fixed=0, cache=False, protocol="natural2").idx), 40)
        self.assertEqual([os.path.basename(x) for x in C.cell_paths(d, TASK, MODEL, protocol="natural2")],
                         ["cells_%s_%s_natural2_k%d.jsonl" % (MODEL, TASK, k) for k in synth.KS])
        # the CLI end to end: results.json records the protocol and the grid it read
        for protocol, n in (("natural2", 40), ("natural", 60)):
            out = tempfile.mkdtemp()
            with contextlib.redirect_stdout(io.StringIO()):
                cli.main(["--cells", d, "--task", TASK, "--checkpoint", MODEL, "--protocol", protocol,
                          "--layers-per-loop", "24", "--fixed-layers", "0", "--accounting", "expected",
                          "--boot", "10", "--cal-draws", "2", "--no-cache", "--out", out])
            res = json.load(open(os.path.join(out, "results.json")))
            self.assertEqual(res["protocol"], protocol)
            self.assertEqual(res["n_cal_rule"]["n_questions"], n, protocol)
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stderr(io.StringIO()):
                cli.main(["--cells", d, "--task", TASK, "--checkpoint", MODEL, "--protocol", "forced",
                          "--layers-per-loop", "24", "--out", tempfile.mkdtemp()])


if __name__ == "__main__":
    unittest.main()
