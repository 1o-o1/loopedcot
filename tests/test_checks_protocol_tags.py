"""`prod.checks.parse_cells_name` reads every protocol tag the package has, not two of them.

The defect: the function knew only "natural" and "forced", so a continuation grid
(`cells_<model>_<task>_natural2_k<k>.jsonl`, and `natural2h` for the horizon mode) parsed as
nothing at all. `run_checks` skips a name it cannot parse, so those grids were dropped from the run
silently -- never completeness-checked, never parse-rate-checked, and absent from the checks JSON
rather than failing in it. The tags now come from `manifest.protocol_of_tag`, the one list in the
package, so a continuation grid is checked by its natural-stop parent's rules under its own key.

  python -m pytest tests/test_checks_protocol_tags.py -q
  python tests/test_checks_protocol_tags.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prod import manifest as manifest_mod                              # noqa: E402
from prod.checks import parse_cells_name                               # noqa: E402


def test_every_protocol_tag_parses_and_keeps_the_model_task_boundary():
    """One synthetic name per tag, on the two names that break a non-greedy split: the model and
    the task both carry underscores, and `natural2` is a prefix-sharing tag."""
    for tag in manifest_mod.PROTOCOL_TAGS:
        got = parse_cells_name("cells_ouro_1_4b_think_gsm8k_%s_k4.jsonl" % tag)
        assert got == ("ouro_1_4b_think", "gsm8k", tag, 4, ""), (tag, got)
        got = parse_cells_name("cells_mcleish_llama32_r32_bbh_%s_k32_part1.jsonl" % tag)
        assert got == ("mcleish_llama32_r32", "bbh", tag, 32, "part1"), (tag, got)
    # the two continuation tags stay APART from each other and from the natural grid they replay
    protos = {parse_cells_name("cells_ouro_2_6b_think_math500_%s_k3.jsonl" % t)[2]
              for t in ("natural", "natural2", "natural2h")}
    assert protos == {"natural", "natural2", "natural2h"}
    # and a name with no tag, or an unknown one, is still not a cells file
    for bad in ("cells_ouro_1_4b_think_gsm8k_k4.jsonl", "cells_junk.jsonl",
                "cells_ouro_1_4b_think_gsm8k_natural3_k4.jsonl",
                "meta_ouro_1_4b_think_gsm8k_natural2_k4.json"):
        assert parse_cells_name(bad) is None, bad


if __name__ == "__main__":
    fs = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for f in fs:
        f()
        print("ok", f.__name__)
    print("%d test functions" % len(fs))
