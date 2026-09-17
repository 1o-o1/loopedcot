"""Every answer kind a production row can carry has a reserve (pooled BBH mixes six of them)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from alloc import cells as C                                        # noqa: E402


class TestAnswerBudget(unittest.TestCase):
    def test_every_production_kind_is_priced(self):
        for kind, expect in (("numeric", 8), ("math", 32), ("letter", 8), ("yesno", 8),
                             ("boolean", 8), ("freeform", 48)):
            self.assertEqual(C.answer_budget("bbh", kind), expect, kind)
        self.assertEqual(C.answer_budget("gsm8k", "numeric"), 12)


if __name__ == "__main__":
    unittest.main()
