"""Fix 1 (PP3b): prod.cleanup must never touch a chains_<model>_<task>_k<k>.jsonl sidecar -- it has
no tag in its name, so it can never be a job's `trace_<tag>_*.jsonl` checkpoint, and it is never a
`cells_<tag>.jsonl` file either. This is a regression test for that guarantee, not a unit test of
the (already tag-scoped) globs alone.

  python -m pytest tests/test_cleanup_preserves_chains.py -q
  python tests/test_cleanup_preserves_chains.py
"""
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prod import cleanup                                             # noqa: E402


def test_cleanup_apply_never_deletes_or_modifies_a_chains_file():
    tmp = tempfile.mkdtemp()
    try:
        tag = "ouro_1_4b_base_gsm8k_natural_k4"
        cells_p = os.path.join(tmp, "cells_%s.jsonl" % tag)
        meta_p = os.path.join(tmp, "meta_%s.json" % tag)
        trace_p = os.path.join(tmp, "trace_%s_single.jsonl" % tag)
        chain_p = os.path.join(tmp, "chains_ouro_1_4b_base_gsm8k_k4.jsonl")

        with open(cells_p, "w", encoding="utf-8") as f:
            f.write(json.dumps({"idx": 0, "row_idx": 0, "k": 4, "B": 16, "correct_v2": True,
                                "answer_text": "long text that would be slimmed"}) + "\n")
        with open(meta_p, "w", encoding="utf-8") as f:
            json.dump({"cells_written": 1, "cells_expected": 1}, f)
        with open(trace_p, "w", encoding="utf-8") as f:
            f.write(json.dumps({"idx": 0, "ids": [1, 2, 3], "done": True}) + "\n")
        chain_bytes = (json.dumps({"idx": 0, "natural_stop": 3, "n_prompt_tokens": 50,
                                  "chain_ids": [1, 2, 3], "prompt_sha256": "x",
                                  "batch_width": 16}) + "\n").encode("utf-8")
        with open(chain_p, "wb") as f:
            f.write(chain_bytes)

        rep = cleanup.run(tmp, manifest_path=None, logs_dir=tmp, apply=True)

        assert rep["n_complete_jobs"] == 1
        assert not os.path.exists(trace_p)               # the job's own checkpoint IS deleted
        assert os.path.exists(chain_p)                    # the chains sidecar survives
        with open(chain_p, "rb") as f:
            assert f.read() == chain_bytes                # byte for byte, untouched
        # and it is never named anywhere in the report as freed, deleted, or even seen
        blob = json.dumps(rep)
        assert "chains_ouro_1_4b_base_gsm8k_k4" not in blob
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_trace_files_for_excludes_chains_defensively():
    tmp = tempfile.mkdtemp()
    try:
        tag = "m_t_natural_k1"
        open(os.path.join(tmp, "trace_%s_single.jsonl" % tag), "w").close()
        open(os.path.join(tmp, "chains_m_t_k1.jsonl"), "w").close()
        found = cleanup.trace_files_for(tmp, tag)
        assert len(found) == 1
        assert "chains_" not in os.path.basename(found[0])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    fs = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for f in fs:
        f()
        print("ok", f.__name__)
    print("%d test functions" % len(fs))
