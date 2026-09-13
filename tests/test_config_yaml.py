"""prod/config.py is now a YAML loader (PP3b task 1): this pins the numbers it must keep producing.

`OLD_DEFAULTS` and `OLD_MODEL_SHAPES` are a frozen copy of what `prod/config.py` returned as literal
Python before the move to `prod/config.yaml` (Brief PP3, decision 2 and decision 1). If
`prod/config.yaml` ever drifts from the protocol of record, this fails and says exactly which key.

  python -m pytest tests/test_config_yaml.py -q
  python tests/test_config_yaml.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prod import config as cfgmod                                    # noqa: E402

OLD_DEFAULTS = {
    "caps": [0, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096],
    "caps_extra": [],
    "horizon": 4096,
    "forced_horizon": 4096,
    "forced_budgets": [0, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096],
    "forced_block": {
        "enabled": False,   # the forced block is its own queue (protocol decision Q15)
        "models": ["ouro_1_4b_base", "ouro_1_4b_think", "ouro_2_6b_base", "ouro_2_6b_think"],
        "tasks": ["gsm8k", "math500"],
        "ks": None,
        "n": None,
    },
    "batch_width": 16,
    "batch_cap": 32,
    "split_seed": 20260908,
    "n_cal": 100,
    "datasets": {
        "gsm8k": 1319, "math500": 500, "svamp": 300, "aqua": 254, "csqa": 1221, "arc": 1172,
        "strategyqa": 2290, "bbh": 2437, "mmlu": 2000, "hellaswag": 2000,
    },
    "depths": {
        "ouro_1_4b_base": [1, 2, 3, 4], "ouro_1_4b_think": [1, 2, 3, 4],
        "ouro_2_6b_base": [1, 2, 3, 4], "ouro_2_6b_think": [1, 2, 3, 4],
        "huginn_0125": [1, 2, 4, 8, 16, 32], "mcleish_llama32_r32": [1, 2, 4, 8],
    },
    "depths_extra": {"mcleish_llama32_r32": {"gsm8k": [16, 32]}},
    "bbh_subtasks": [
        "date_understanding", "logical_deduction_five_objects",
        "tracking_shuffled_objects_three_objects", "sports_understanding", "boolean_expressions",
        "multistep_arithmetic_two", "word_sorting", "navigate", "causal_judgement",
        "temporal_sequences",
    ],
    "mem_util": 0.85,
    "prompt_allowance": 1536,
    "workers_per_gpu": 1,
    "cluster_factor": 4.0,
    "version": "PP3",
}

#: PP3's static MODEL_SHAPES table, verbatim (decision 1), before it moved into config.yaml's
#: `models:` block alongside each model's depths and batch-width overrides.
OLD_MODEL_SHAPES = {
    "ouro_1_4b_base": {"repo": "ByteDance/Ouro-1.4B", "params": 1434652673, "kv_heads": 16,
                       "head_dim": 128, "layers": 24, "entries": "ouro", "dtype_bytes": 2},
    "ouro_1_4b_think": {"repo": "ByteDance/Ouro-1.4B-Thinking", "params": 1434652673,
                        "kv_heads": 16, "head_dim": 128, "layers": 24, "entries": "ouro",
                        "dtype_bytes": 2},
    "ouro_2_6b_base": {"repo": "ByteDance/Ouro-2.6B", "params": 2667974657, "kv_heads": 16,
                       "head_dim": 128, "layers": 48, "entries": "ouro", "dtype_bytes": 2},
    "ouro_2_6b_think": {"repo": "ByteDance/Ouro-2.6B-Thinking", "params": 2667974657,
                        "kv_heads": 16, "head_dim": 128, "layers": 48, "entries": "ouro",
                        "dtype_bytes": 2},
    "huginn_0125": {"repo": "tomg-group-umd/huginn-0125", "params": 3911400096, "kv_heads": 55,
                    "head_dim": 96, "prelude": 2, "core": 4, "coda": 2, "entries": "raven",
                    "dtype_bytes": 2},
    "mcleish_llama32_r32": {"repo": "smcleish/Recurrent-Llama-3.2-train-recurrence-32",
                            "params": 1385228288, "kv_heads": 8, "head_dim": 64, "prelude": 4,
                            "core": 6, "coda": 4, "entries": "raven", "dtype_bytes": 2},
}

#: PP3b ruling Q12: per (model, k) width overrides added on top of the pinned width 16.
EXPECTED_OVERRIDES = {
    "ouro_2_6b_base": {3: 8, 4: 8},
    "ouro_2_6b_think": {3: 8, 4: 8},
    "huginn_0125": {16: 8, 32: 4},
}


def test_yaml_defaults_match_the_old_hard_coded_defaults():
    cfg = cfgmod.defaults()
    for key, want in OLD_DEFAULTS.items():
        assert cfg[key] == want, "config.yaml drift on %r: %r != %r" % (key, cfg[key], want)


def test_model_shapes_match_the_old_static_table():
    for model, want in OLD_MODEL_SHAPES.items():
        got = cfgmod.MODEL_SHAPES[model]
        for k, v in want.items():
            assert got[k] == v, "MODEL_SHAPES[%r][%r]: %r != %r" % (model, k, got.get(k), v)


def test_model_order_unchanged():
    assert cfgmod.MODEL_ORDER == ["ouro_1_4b_base", "ouro_1_4b_think", "ouro_2_6b_base",
                                  "ouro_2_6b_think", "huginn_0125", "mcleish_llama32_r32"]


def test_batch_width_overrides_match_ruling_q12():
    cfg = cfgmod.defaults()
    assert cfg["batch_width_overrides"] == EXPECTED_OVERRIDES
    for model, by_k in EXPECTED_OVERRIDES.items():
        for k, w in by_k.items():
            assert cfgmod.batch_width_for(model, k, cfg) == w
    # everything else still gets the pinned width 16 (rulings Q6 iv)
    assert cfgmod.batch_width_for("ouro_1_4b_base", 4, cfg) == 16
    assert cfgmod.batch_width_for("huginn_0125", 8, cfg) == 16
    assert cfgmod.batch_width_for("ouro_2_6b_base", 2, cfg) == 16


def test_config_json_override_still_works():
    """--config-json (an override path predating this task) still merges before the flags."""
    import argparse
    import json
    import tempfile
    p = argparse.ArgumentParser()
    cfgmod.add_args(p)
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump({"horizon": 999}, f)
        path = f.name
    try:
        a = p.parse_args(["--config-json=%s" % path, "--horizon=123"])
        cfg = cfgmod.from_args(a)
        assert cfg["horizon"] == 123          # the explicit flag still wins over --config-json
    finally:
        os.remove(path)


if __name__ == "__main__":
    fs = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for f in fs:
        f()
        print("ok", f.__name__)
    print("%d test functions" % len(fs))
