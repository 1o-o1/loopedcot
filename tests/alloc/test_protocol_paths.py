"""The loader takes one protocol's files: a forced grid beside the natural one is never unioned in."""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from alloc import cells as C                                        # noqa: E402


class TestProtocolPaths(unittest.TestCase):
    def test_natural_only_by_default_and_forced_on_request(self):
        d = tempfile.mkdtemp()
        names = ["cells_ouro_1_4b_base_gsm8k_natural_k1.jsonl", "cells_ouro_1_4b_base_gsm8k_natural_k4.jsonl",
                 "cells_ouro_1_4b_base_gsm8k_forced_k4_s0of2.jsonl", "cells_ouro_1_4b_base_gsm8k_forced_k4_s1of2.jsonl",
                 "cells_ouro_1_4b_base_gsm8k_natural_k4_dryrun.jsonl"]
        for n in names:
            open(os.path.join(d, n), "w").close()
        nat = [os.path.basename(p) for p in C.cell_paths(d, "gsm8k", "ouro_1_4b_base")]
        self.assertEqual(nat, names[:2])
        forced = [os.path.basename(p) for p in C.cell_paths(d, "gsm8k", "ouro_1_4b_base", protocol="forced")]
        self.assertEqual(forced, names[2:4])


if __name__ == "__main__":
    unittest.main()
