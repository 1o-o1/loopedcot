"""Memory-aware multi-worker placement, without a GPU (Brief PP3, decision 1).

The claim path, the admission rule and the re-queue semantics are pure file and arithmetic work, so
they are testable on the laptop; the Spark gate G5 then exercises the same code with real jobs.

  python -m pytest tests/test_launcher_placement.py -q
  python tests/test_launcher_placement.py
"""
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prod import config as cfgmod                                    # noqa: E402
from prod import launcher                                            # noqa: E402


def test_estimate_matches_the_formula():
    """weights + width x (horizon + allowance) x KV/token, with KV/token from the shapes."""
    m, k, w, h = "ouro_1_4b_base", 4, 16, 4096
    kv = cfgmod.kv_bytes_per_token(m, k)
    assert kv == 2 * 16 * 128 * 2 * (24 * k)          # 2(K,V) x kv_heads x head_dim x bf16 x 24k
    assert cfgmod.cache_entries("huginn_0125", 4) == 2 + 4 * 4 + 2
    assert cfgmod.cache_entries("mcleish_llama32_r32", 4) == 4 + 6 * 4 + 4
    assert cfgmod.cache_entries("ouro_2_6b_base", 4) == 48 * 4
    want = cfgmod.weight_bytes(m) + w * (h + cfgmod.PROMPT_ALLOWANCE) * kv
    assert cfgmod.job_bytes(m, k, w, h) == want


def _queue(tmp, jobs):
    q = launcher.queue_dir(tmp)
    for i, j in enumerate(jobs):
        with open(os.path.join(q, "todo", "%05d_%s.json" % (i, j["tag"])), "w",
                  encoding="utf-8") as f:
            json.dump(j, f)
    return q


GB = 1024 ** 3


def test_admission_respects_the_ceiling():
    tmp = tempfile.mkdtemp()
    try:
        jobs = [{"tag": "big", "est_bytes": 60 * GB, "cmd": []},
                {"tag": "small_a", "est_bytes": 30 * GB, "cmd": []},
                {"tag": "small_b", "est_bytes": 30 * GB, "cmd": []}]
        q = _queue(tmp, jobs)
        budget = launcher.GpuBudget({0: int(0.85 * 100 * GB)})       # 85 GB
        p1, r1 = launcher.claim(q, "gpu0.w0", 0, budget)             # takes big (60)
        assert r1["tag"] == "big"
        # 85 - 60 = 25 GB left: neither 30 GB job fits, and the gpu is NOT idle -> WAIT, not None,
        # so the second slot blocks instead of dropping the queue on the floor.
        p2, r2 = launcher.claim(q, "gpu0.w1", 0, budget)
        assert (p2, r2) == ("WAIT", None)
        budget.release(0, 60 * GB)
        p3, r3 = launcher.claim(q, "gpu0.w1", 0, budget)
        assert r3["tag"] == "small_a"
        p4, r4 = launcher.claim(q, "gpu0.w0", 0, budget)             # 30 + 30 = 60 <= 85
        assert r4["tag"] == "small_b"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_a_job_that_never_fits_is_reported_not_run():
    tmp = tempfile.mkdtemp()
    try:
        q = _queue(tmp, [{"tag": "too_big", "est_bytes": 200 * GB, "cmd": []}])
        budget = launcher.GpuBudget({0: int(0.85 * 141 * GB)})
        path, rec = launcher.claim(q, "gpu0.w0", 0, budget)
        assert rec is None and path is None
        assert budget.blocked and budget.blocked[0]["job"] == "too_big"
        # and it is STILL in todo: nothing is silently dropped
        assert os.listdir(os.path.join(q, "todo")) == ["00000_too_big.json"]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_no_budget_is_pp2_behaviour():
    """With one worker per GPU and no measurable device, claim() is the old lowest-numbered take."""
    tmp = tempfile.mkdtemp()
    try:
        q = _queue(tmp, [{"tag": "a", "est_bytes": 999 * GB, "cmd": []},
                         {"tag": "b", "est_bytes": 1 * GB, "cmd": []}])
        path, rec = launcher.claim(q, "gpu0", 0, None)
        assert rec["tag"] == "a" and rec["worker"] == "gpu0"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_requeue_still_works_under_slots():
    tmp = tempfile.mkdtemp()
    try:
        q = _queue(tmp, [{"tag": "a", "est_bytes": 1 * GB, "cmd": []}])
        budget = launcher.GpuBudget({0: 10 * GB})
        path, rec = launcher.claim(q, "gpu0.w0", 0, budget)
        assert os.path.dirname(path).endswith("claimed")
        moved = launcher.requeue_claimed(q)
        assert len(moved) == 1
        assert os.listdir(os.path.join(q, "todo")) == ["00000_a.json"]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    fs = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for f in fs:
        f()
        print("ok", f.__name__)
    print("%d test functions" % len(fs))
