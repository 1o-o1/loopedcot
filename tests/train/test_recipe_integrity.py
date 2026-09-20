"""Check that stage outputs are keyed by variant, that constants come from the config, and that
checkpoints and analysis pairing survive interruption and missing grids."""
import importlib.util
import json
import re
import sys
import types
from pathlib import Path

import numpy as np
import pytest

from test_recipe import (G, FakeTok, backend, cfg, tok, build, make_visits, use_block_lens,
                         CONFIG, Q, SRC, GOLD)


def load_module(name, filename):
    """Import one stage module by file name and return it; filename is relative to train/."""
    path = Path(G.__file__).with_name(filename)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ================================================================= stage-2 outputs are per variant
def test_stage2_paths_and_fingerprint_separate_the_variants(tmp_path, cfg, tok):
    P = G.paths(str(tmp_path))
    G.ensure_dirs(P)
    one = G.data_dir(P, "budget_longest")
    two = G.data_dir(P, "nocut")
    assert one != two and Path(one).is_dir() and Path(two).is_dir()
    a_arrays, _ = G.pack_one_visit_per_block(make_visits(cfg, tok, n=4), tok.pad_token_id)
    b_arrays, _ = G.pack_one_visit_per_block(make_visits(cfg, tok, n=5), tok.pad_token_id)
    assert G.blocks_fingerprint(a_arrays) == G.blocks_fingerprint(a_arrays)
    assert G.blocks_fingerprint(a_arrays) != G.blocks_fingerprint(b_arrays)


def test_manifest_budget_keys_match_the_grid_cell_keys(cfg, tok):
    """The manifest must spell the no-limit budget the way run_grid and analysis spell it."""
    assert G.budget_key(None) == "none"
    counts = G.count_by_budget([None, None, 32])
    assert counts == {"none": 2, "32": 1}


def test_stage2_writes_one_variant_and_the_trainer_rejects_the_other(tmp_path, cfg, tok, monkeypatch):
    """Run stage 2 for two variants over the same chains and show the blocks cannot be crossed."""
    import sys
    import types

    class GateTok(FakeTok):
        """The character tokenizer with printable names for the pad and end-of-text ids."""
        def decode(self, ids, **kw):
            return "".join("<|endoftext|>" if i == 1 else "<pad>" if i == 0 else chr(i - 10)
                           for i in ids)

    tok = GateTok()
    transformers = types.ModuleType("transformers")
    transformers.AutoTokenizer = types.SimpleNamespace(from_pretrained=lambda *a, **k: tok)
    monkeypatch.setitem(sys.modules, "transformers", transformers)
    monkeypatch.setattr(FakeTok, "pad_token", 0, raising=False)
    monkeypatch.setattr(FakeTok, "eos_token", 1, raising=False)

    pool = tmp_path / "pool.jsonl"
    pool.write_text("".join(json.dumps(
        {"src": SRC, "pool_i": i, "question": "%s #%d" % (Q, i), "gold": GOLD}) + "\n"
        for i in range(40)), encoding="utf-8")
    cfg["pool_jsonl"] = str(pool)
    cfg["pool_sha256"] = G.file_sha256(str(pool))
    cfg["chains"] = {SRC: dict(cfg["chains"][SRC])}
    use_block_lens(cfg, 512, micro=4, blocks=8)
    cfg["supervised_token_budget"] = 3000
    P = G.paths(str(tmp_path))
    G.ensure_dirs(P)
    for tag, chain in (("A", "A" * 40), ("B", "B" * 12)):
        Path(P["artifacts"], "chains_%s_%s_k4.jsonl" % (SRC, tag)).write_text("".join(
            json.dumps({"pool_i": i, "kept": True, "chain": chain + " #### 4",
                        "question": "%s #%d" % (Q, i)}) + "\n" for i in range(40)),
            encoding="utf-8")
    monkeypatch.setattr(G, "load_config", lambda *a, **k: cfg)

    train = load_module("recipe_training_guard", "train.py")
    built = {}
    for variant in ("budget_longest", "budget_shortest"):
        assert G.main(["--variant=%s" % variant, "--root=%s" % tmp_path]) == 0
        manifest = json.loads(Path(P["artifacts"], "target_manifest_%s.json" % variant)
                              .read_text(encoding="utf-8"))
        assert manifest["variant"] == variant
        assert Path(manifest["data_dir"]) == Path(G.data_dir(P, variant))
        arrays = {}
        for npy in Path(manifest["data_dir"]).glob("blocks_*.npy"):
            L = int(npy.stem.split("_")[1])
            arrays[L] = {"blocks": np.load(npy),
                         "mask": np.load(npy.with_name("mask_%d.npy" % L)),
                         "length": np.load(npy.with_name("length_%d.npy" % L))}
            assert int(arrays[L]["length"].sum()) < int(arrays[L]["blocks"].size)
        assert arrays and manifest["n_visits"] > 0
        train.check_data_matches_variant(arrays, manifest, variant)
        built[variant] = (arrays, manifest)
        assert set(manifest["visits_by_T"]) <= {"none", "0", "16", "32", "64", "128", "256",
                                                "512", "1024"}
        assert manifest["budget_grid_by_source"][SRC][-1] == "none"
        assert manifest["chains_horizon_by_source"][SRC] == cfg.horizon(SRC)
        assert manifest["blocks_by_len"] == {"512": sum(manifest["visits_by_block_len"].values())}
        assert 0.0 < manifest["padding_share_by_block_len"]["512"] < 1.0
        assert manifest["pad_id"] == tok.pad_token_id
        assert manifest["exemplar_sha256"] == G.exemplar_fingerprints(tok, cfg)
        scheduled = manifest["supervised_tokens_scheduled"]
        assert 0 <= scheduled <= manifest["supervised_tokens_drawn"]
        assert manifest["blocks_dropped_as_remainder"] >= 0
    assert built["budget_longest"][1]["blocks_sha256"] != built["budget_shortest"][1]["blocks_sha256"]
    with pytest.raises(AssertionError):
        train.check_data_matches_variant(built["budget_longest"][0], built["budget_shortest"][1],
                                     "budget_shortest")
    gates = load_module("recipe_gates", "gates.py")
    for variant, (arrays, _m) in built.items():
        loaded, spans = gates.load_arrays(cfg, P, variant)
        assert sorted(loaded) == sorted(arrays)
        assert G.v3_context(loaded, spans, pad_id=tok.pad_token_id)["ok"]

    # the CPU gates must find and pass a variant's own directory, and V3 must still catch a split
    from test_recipe import AP, PREFIX, QP
    harness = types.ModuleType("s32_common")
    harness.build_prompts = lambda tk, task, rows, harness_mode, k, T=None, tag_override=None: (
        [PREFIX + QP + r["input"] + AP for r in rows], None, None, None, {"tag_line": ""})
    monkeypatch.setitem(sys.modules, "s32_common", harness)
    screen = {"drop_near": True, "V9_overlap": 0, "n_near_duplicates": 3, "n_pool_after": 40}
    real_jload = G.jload
    monkeypatch.setattr(G, "jload", lambda path, default=None:
                        screen if "v9_contamination" in str(path) else real_jload(path, default))
    checks = Path(P["gates"], "checks.json")
    assert gates.run_cpu(cfg, P, "budget_longest", str(checks)) == 0
    recorded = json.loads(checks.read_text(encoding="utf-8"))
    assert recorded["V1"] == 0 and recorded["V2"] and recorded["V3_CONTEXT"]
    assert recorded["V3_CONTEXT_split_detected"] and recorded["V9"] == 0
    assert Path(P["gates"], "v2_loss_mask.txt").read_text(encoding="utf-8").count("BAD:") == 0
    assert recorded["V9_detail"]["pool_sha256"] == cfg["pool_sha256"]

    # an unpinned pool stops both stage 2 and the gates
    cfg["pool_sha256"] = "0" * 64
    with pytest.raises(SystemExit):
        gates.run_cpu(cfg, P, "budget_longest", str(checks))
    with pytest.raises(SystemExit):
        G.main(["--variant=budget_longest", "--root=%s" % tmp_path])


# ================================================================= the fallback context
def test_a_finished_rejected_chain_never_becomes_the_fallback_context(cfg, tok):
    """A wrong chain that already ends inside the budget must not be handed the gold answer."""
    ids, mask, info = G.build_target(cfg, tok, "budget_longest", SRC, Q, GOLD, 12,
                                     None, None, fallback_chain_A="wrong")
    assert info["kind"] == "FALLBACK" and info["n_chain"] == 0
    n_p = info["n_prompt"]
    assert "wrong" not in tok.decode(ids[n_p:-1])
    assert mask[:n_p + info["n_suffix"]] == [0] * (n_p + info["n_suffix"])
    assert sum(mask) == info["n_answer"] + 1


def test_a_long_rejected_chain_is_still_cut_at_the_budget(cfg, tok):
    ids, mask, info = G.build_target(cfg, tok, "budget_longest", SRC, Q, GOLD, 4,
                                     None, None, fallback_chain_A="wrongwrongwrong")
    assert info["kind"] == "FALLBACK" and info["n_chain"] == 4
    n_p = info["n_prompt"]
    assert tok.decode(ids[n_p:n_p + 4]) == "wron"
    assert mask[n_p:n_p + 4] == [0, 0, 0, 0]


def test_the_kept_chain_is_preferred_over_the_raw_one_for_the_cut(cfg, tok):
    ids, _m, info = G.build_target(cfg, tok, "budget_longest", SRC, Q, GOLD, 5,
                                   "KEPTKEPTKEPT", None, fallback_chain_A="RAWRAWRAWRAW")
    assert info["kind"] == "FALLBACK"
    assert tok.decode(ids[info["n_prompt"]:info["n_prompt"] + 5]) == "KEPTK"


# ================================================================= the read-out matches the grid
@pytest.mark.parametrize("T", [0, 8])
def test_readout_suffix_ids_are_the_ones_the_grid_appends(cfg, tok, T):
    """run_grid appends tok(suffix_text) standalone; the DIRECT and FALLBACK targets must use those exact ids."""
    for src in cfg.sources:
        suffix_text = G.task_bits(cfg.eval_task(src))[2]
        grid_ids = tok(suffix_text, add_special_tokens=False)["input_ids"]   # run_grid.py's SUF
        ids, mask, info = G.build_target(cfg, tok, "budget_longest", src, Q, GOLD, T,
                                         "A" * 40, "B" * 12)
        start = info["n_prompt"] + info["n_chain"]
        assert info["n_suffix"] == len(grid_ids)
        assert ids[start:start + len(grid_ids)] == grid_ids
        assert mask[start:start + len(grid_ids)] == [0] * len(grid_ids)


# ================================================================= the context gate reads the ids
def test_context_gate_catches_corrupted_ids_and_padding(cfg, tok):
    visits = make_visits(cfg, tok, n=4, block_len=512)
    arrays, spans = G.pack_one_visit_per_block(visits, tok.pad_token_id)
    assert G.v3_context(arrays, spans, pad_id=tok.pad_token_id)["ok"]
    swapped = {512: dict(arrays[512], blocks=arrays[512]["blocks"].copy())}
    swapped[512]["blocks"][[0, 1]] = swapped[512]["blocks"][[1, 0]]
    bad = G.v3_context(swapped, spans, pad_id=tok.pad_token_id)
    assert not bad["ok"] and bad["failures_by_reason"].get("block_ids_changed")
    dirty = {512: dict(arrays[512], blocks=arrays[512]["blocks"].copy())}
    dirty[512]["blocks"][2, -1] = 999
    bad = G.v3_context(dirty, spans, pad_id=tok.pad_token_id)
    assert not bad["ok"] and bad["failures_by_reason"].get("padding_not_pad_id")


# ================================================================= the exemplar block is pinned
def test_exemplar_block_is_fingerprinted_and_a_change_is_caught(cfg, tok):
    first = G.exemplar_fingerprints(tok, cfg)
    assert set(first) == {cfg.eval_task(s) for s in cfg.sources}
    assert all(len(v) == 64 for v in first.values())
    G.check_exemplars(tok, cfg, first)
    with pytest.raises(AssertionError):
        G.check_exemplars(tok, cfg, dict(first, **{cfg.eval_task(cfg.sources[0]): "0" * 64}))


def test_math_exemplars_may_not_come_from_the_evaluation_split():
    G.check_exemplar_source({"source": "EleutherAI/hendrycks_math", "excluded_test_idx": []})
    with pytest.raises(AssertionError):
        G.check_exemplar_source({"source": "MATH-500 test tail (no train split reachable)",
                                 "excluded_test_idx": [496, 497, 498, 499]})


# ================================================================= the config is the only source
def test_optimiser_and_lora_settings_come_from_the_config(cfg):
    assert cfg.micro(1024) == 4 and cfg.accum(1024) == 8
    assert cfg.micro(3072) == 1 and cfg.accum(3072) == 32
    lora = G.lora_settings(cfg)
    assert lora["r"] == 16 and lora["alpha"] == 32
    assert lora["targets"] == list(cfg["lora"]["targets"])
    assert cfg["schedule"] == "cosine"
    assert float(cfg["fullplus_p"]) == 0.2


def test_every_config_key_is_read_by_some_stage():
    train_dir = Path(G.__file__).parent
    source = "\n".join(p.read_text(encoding="utf-8") for p in sorted(train_dir.glob("*.py")))
    top = [line.split(":")[0] for line in
           Path(CONFIG).read_text(encoding="utf-8").splitlines()
           if line[:1].isalpha() and ":" in line]
    unread = [k for k in top if ('"%s"' % k) not in source]
    assert unread == [], unread


def test_analysis_reads_the_grid_from_the_config(cfg):
    analysis = load_module("recipe_analysis", "analysis.py")
    assert analysis.caps_from(cfg) == list(cfg["eval_standard_caps"])
    assert analysis.grid_from(cfg) == [G.budget_key(t) for t in cfg["eval_budgets"]]
    assert analysis.tasks_from(cfg) == [cfg.eval_task(s) for s in cfg.sources]


# ================================================================= analysis pairs by row
def test_f1_own_answer_rate_is_paired_per_row():
    analysis = load_module("recipe_analysis", "analysis.py")
    candidate = {(0, "32", 32): {"split": "eval", "trace_answer": "4"},
                 (1, "32", 32): {"split": "eval", "trace_answer": None}}
    reference = {(0, 32): {"split": "eval", "trace_answer": None},
                 (1, 32): {"split": "eval", "trace_answer": "4"}}
    both = analysis.paired_own(candidate, reference, [0, 1], 32, 32)
    assert both == ([1.0, 0.0], [0.0, 1.0])
    # a row present on one side only must drop out of both variants, never shift the pairing
    one = analysis.paired_own(candidate, {(1, 32): reference[(1, 32)]}, [0, 1], 32, 32)
    assert one == ([0.0], [1.0])


# ================================================================= the training loop
def test_training_refuses_another_variants_blocks(tmp_path, cfg, tok, monkeypatch):
    train = load_module("recipe_training_guard", "train.py")
    arrays, spans = G.pack_one_visit_per_block(make_visits(cfg, tok, n=4), tok.pad_token_id)
    manifest = {"variant": "nocut", "blocks_sha256": G.blocks_fingerprint(arrays)}
    with pytest.raises(AssertionError):
        train.check_data_matches_variant(arrays, manifest, "budget_longest")
    manifest = {"variant": "budget_longest", "blocks_sha256": "0" * 64}
    with pytest.raises(AssertionError):
        train.check_data_matches_variant(arrays, manifest, "budget_longest")
    manifest = {"variant": "budget_longest", "blocks_sha256": G.blocks_fingerprint(arrays)}
    train.check_data_matches_variant(arrays, manifest, "budget_longest")


def test_micro_batch_width_must_match_the_schedule_bucket_by_bucket(cfg, tok):
    """The width is per block length now, and a window must still be the configured 32 blocks."""
    train = load_module("recipe_training_guard", "train.py")
    use_block_lens(cfg, 256, 512, micro=4, blocks=8)
    cfg["micro_by_block_len"] = {256: 4, 512: 2}
    sched = [{"depth": 1, "seq_len": 256, "blocks": [0, 1, 2, 3], "supervised": 5, "window": 0},
             {"depth": 1, "seq_len": 256, "blocks": [4, 5, 6, 7], "supervised": 5, "window": 0},
             {"depth": 2, "seq_len": 512, "blocks": [0, 1], "supervised": 5, "window": 1},
             {"depth": 2, "seq_len": 512, "blocks": [2, 3], "supervised": 5, "window": 1},
             {"depth": 2, "seq_len": 512, "blocks": [4, 5], "supervised": 5, "window": 1},
             {"depth": 2, "seq_len": 512, "blocks": [6, 7], "supervised": 5, "window": 1}]
    assert train.micro_from_schedule(sched) == {256: 4, 512: 2}
    train.check_micro(sched, cfg)
    cfg["micro_by_block_len"] = {256: 2, 512: 2}
    with pytest.raises(AssertionError):
        train.check_micro(sched, cfg)
    cfg["micro_by_block_len"] = {256: 4, 512: 2}
    short = sched[:1] + sched[2:]                       # window 0 now holds 4 blocks, not 8
    with pytest.raises(AssertionError):
        train.check_micro(short, cfg)
    mixed = [dict(mb, window=0) for mb in sched]         # one window over two block lengths
    with pytest.raises(AssertionError):
        train.check_micro(mixed, cfg)


def test_a_schedule_window_is_one_optimiser_step(cfg, tok):
    """train.py steps over windows, not over a fixed accum stride, because accum is per bucket."""
    train = load_module("recipe_training_guard", "train.py")
    use_block_lens(cfg, 256, micro=2, blocks=4)
    visits = make_visits(cfg, tok, n=8, block_len=256)
    for v in visits:
        v["depth"] = 3
    arrays, _ = G.pack_one_visit_per_block(visits, tok.pad_token_id)
    sched, n_opt = G.build_schedule(cfg, arrays, np.random.default_rng(0))
    train.check_micro(sched, cfg)
    windows = G.windows_from_schedule(sched)
    assert n_opt == len(windows) == 2
    assert [len(w) for w in windows] == [2, 2]


def test_checkpoint_is_written_whole_or_not_at_all(tmp_path):
    train = load_module("recipe_training_guard", "train.py")
    target = tmp_path / "ckpt"
    with pytest.raises(RuntimeError):
        with train.atomic_checkpoint(str(target)) as staging:
            Path(staging, "half.json").write_text("{}")
            raise RuntimeError("interrupted before the state file")
    assert not target.exists()
    with train.atomic_checkpoint(str(target)) as staging:
        Path(staging, "state.json").write_text('{"opt_step": 3}')
    assert json.loads((target / "state.json").read_text())["opt_step"] == 3


def test_oom_split_resets_between_windows():
    train = load_module("recipe_training_guard", "train.py")
    assert train.INITIAL_SPLIT == 1


# ================================================================= packaged short prompts
def test_short_exemplar_prompts_ship_with_the_package(cfg):
    for src in cfg.sources:
        path = G.short_prompt_path(G.paths("~/nowhere-at-all"), cfg, src)
        assert Path(path).exists(), path
        assert Path(path).read_text(encoding="utf-8").strip()


# ================================================================= the mask, token by token
KINDS = [(0, False, "DIRECT"), (8, False, "FALLBACK"), (64, False, "CHAIN"),
         (None, False, "CHAIN"), (None, True, "CHAIN_PLUS")]


@pytest.mark.parametrize("T,fullplus,kind", KINDS)
def test_every_position_of_every_target_kind_has_the_spec_mask(cfg, tok, T, fullplus, kind):
    """Build one visit of each kind and assert the supervision flag of every single position."""
    ids, mask, info = build(cfg, tok, "budget_longest", T, fullplus=fullplus)
    assert info["kind"] == kind
    n_p, n_c, n_s, n_a = (info["n_prompt"], info["n_chain"], info["n_suffix"], info["n_answer"])
    supervises_chain = kind in ("CHAIN", "CHAIN_PLUS")
    has_readout = kind in ("DIRECT", "FALLBACK", "CHAIN_PLUS")
    expected = [0] * n_p + [int(supervises_chain)] * n_c
    if has_readout:
        expected += [0] * n_s + [1] * n_a
    expected += [1]
    assert len(ids) == len(expected), (kind, len(ids), len(expected))
    for position, (flag, want) in enumerate(zip(mask, expected)):
        assert flag == want, (kind, position, tok.decode([ids[position]]))
    assert ids[-1] == tok.eos_token_id
    assert sum(mask) == info["n_supervised"] == (n_c if supervises_chain else 0) + \
           (n_a if has_readout else 0) + 1
    prompt = G.eval_prompt(cfg, tok, cfg.eval_task(SRC), Q, T)
    assert ids[:n_p] == tok(prompt)["input_ids"]
    assert not any(mask[:n_p])


def test_padding_is_outside_every_count(cfg, tok):
    use_block_lens(cfg, 512, micro=1, blocks=1)
    visits = make_visits(cfg, tok, n=4, block_len=512)
    arrays, spans = G.pack_one_visit_per_block(visits, tok.pad_token_id)
    content = sum(len(v["ids"]) for v in visits)
    padded = sum(int(a["blocks"].size) for a in arrays.values())
    assert padded > content
    assert int(arrays[512]["length"].sum()) == content
    assert int(arrays[512]["mask"].sum()) == sum(sum(v["mask"]) for v in visits)
    for span, visit in zip(spans, visits):
        assert arrays[512]["mask"][span["block"], span["end"]:].sum() == 0
    sched, _ = G.build_schedule(cfg, arrays, np.random.default_rng(0))
    assert all(m["supervised"] <= content for m in sched)


# ================================================================= F1: the GPU wait policy
WAIT_CASES = [([], {}, False),                                  # unknown box: do not block
              (["--wait"], {}, True),                           # asked for explicitly
              ([], {"CLUSTER": "0"}, True),                     # the shared unmanaged box
              ([], {"CLUSTER": "1"}, False),                    # any other marker is not a wait
              (["--no-wait"], {"CLUSTER": "0"}, False),         # the flag beats the marker
              (["--wait"], {"SLURM_JOB_ID": "918"}, False),     # the scheduler owns the GPU
              ([], {"CLUSTER": "0", "SLURM_JOBID": "918"}, False)]


@pytest.mark.parametrize("argv,env,expected", WAIT_CASES)
def test_gpu_wait_policy(argv, env, expected):
    """A Slurm job never waits, --no-wait never waits, and an unmarked box does not wait either."""
    assert G.should_wait_for_gpu(argv, env) is expected


def test_v4_preflight_takes_its_wait_from_the_flags(tmp_path, monkeypatch):
    """gates.py --v4 must not call wait_for_gpu unconditionally: it blocks for hours on a shared GPU."""
    gates = load_module("recipe_gates_wait", "gates.py")
    seen = {}

    def fake_v4(cfg, P, variant, CK, wait, key=None):
        seen["wait"] = wait
        return 0

    monkeypatch.setattr(gates, "run_v4", fake_v4)
    assert gates.main(["--v4", "--root=%s" % tmp_path, "--no-wait"]) == 0
    assert seen["wait"] is False
    assert gates.main(["--v4", "--root=%s" % tmp_path, "--wait"]) == 0
    assert seen["wait"] is True


# ================================================================= F2: the share caps
def test_share_caps_are_inactive_only_when_no_mixture_could_satisfy_them(cfg):
    """One source can never hold a third of the tokens, so that cap is reported, not enforced."""
    one = G.share_caps(cfg, ["gsm8k"])
    assert one["source"]["active"] is False and one["source"]["n_sources"] == 1
    four = G.share_caps(cfg, ["gsm8k", "math", "csqa", "aqua"])
    assert four["source"]["active"] is True and four["format"]["active"] is True
    assert four["source"]["cap"] == float(cfg["source_max_share"])
    assert four["format"]["cap"] == float(cfg["format_max_share"])


def synthetic_run(tmp_path, cfg, tok, monkeypatch, chains, budget):
    """Write a pool and a chains file per source, pin the pool, and return the run paths."""
    transformers = types.ModuleType("transformers")
    transformers.AutoTokenizer = types.SimpleNamespace(from_pretrained=lambda *a, **k: tok)
    monkeypatch.setitem(sys.modules, "transformers", transformers)
    monkeypatch.setattr(FakeTok, "pad_token", 0, raising=False)
    monkeypatch.setattr(FakeTok, "eos_token", 1, raising=False)
    pool = tmp_path / "pool.jsonl"
    pool.write_text("".join(json.dumps(
        {"src": src, "pool_i": i, "question": "%s %s #%d" % (Q, src, i), "gold": GOLD}) + "\n"
        for src in chains for i in range(40)), encoding="utf-8")
    cfg["pool_jsonl"] = str(pool)
    cfg["pool_sha256"] = G.file_sha256(str(pool))
    cfg["chains"] = {s: dict(cfg["chains"][s]) for s in chains}
    use_block_lens(cfg, 512, micro=4, blocks=8)
    cfg["supervised_token_budget"] = budget
    P = G.paths(str(tmp_path))
    G.ensure_dirs(P)
    for src, chain in chains.items():
        for tag in ("A", "B"):
            Path(P["artifacts"], "chains_%s_%s_k4.jsonl" % (src, tag)).write_text("".join(
                json.dumps({"pool_i": i, "kept": True, "chain": chain,
                            "question": "%s %s #%d" % (Q, src, i)}) + "\n" for i in range(40)),
                encoding="utf-8")
    monkeypatch.setattr(G, "load_config", lambda *a, **k: cfg)
    return P


def test_share_caps_bind_below_fifty_thousand_supervised_tokens(tmp_path, cfg, tok, monkeypatch):
    """A long-chain source takes most of a small budget unless the caps apply from token one."""
    P = synthetic_run(tmp_path, cfg, tok, monkeypatch,
                      {"gsm8k": "A" * 60, "csqa": "A" * 4}, budget=4000)
    cfg["source_max_share"] = 0.6       # feasible for two sources
    cfg["format_max_share"] = 0.9       # feasible for two formats
    assert G.main(["--variant=budget_longest", "--root=%s" % tmp_path]) == 0
    man = json.loads(Path(P["artifacts"], "target_manifest_budget_longest.json")
                     .read_text(encoding="utf-8"))
    caps = man["share_caps"]
    assert caps["applied_from_supervised_token"] == 0
    assert caps["source"]["active"] is True and caps["format"]["active"] is True
    assert caps["source"]["realised"] == man["supervised_share_by_source"]
    assert caps["format"]["realised"] == man["supervised_share_by_format"]
    assert caps["source"]["draws_refused"] > 0
    assert man["supervised_share_by_source"]["gsm8k"] <= 0.63, man["supervised_share_by_source"]


def test_a_single_source_run_is_not_starved_by_an_unsatisfiable_cap(tmp_path, cfg, tok,
                                                                   monkeypatch):
    """The cap is recorded inactive and the run still draws its whole budget."""
    P = synthetic_run(tmp_path, cfg, tok, monkeypatch, {"gsm8k": "A" * 40}, budget=3000)
    assert G.main(["--variant=budget_longest", "--root=%s" % tmp_path]) == 0
    man = json.loads(Path(P["artifacts"], "target_manifest_budget_longest.json")
                     .read_text(encoding="utf-8"))
    assert man["share_caps"]["source"]["active"] is False
    assert man["share_caps"]["source"]["draws_refused"] == 0
    assert man["supervised_tokens_drawn"] >= 3000


# ================================================================= F3: the pool is pinned
def test_the_pool_file_is_pinned_by_sha256(tmp_path, cfg):
    """An edited pool must stop stage 2 and the gates, not silently retrain on other questions."""
    pool = tmp_path / "pool.jsonl"
    pool.write_text('{"src": "gsm8k", "pool_i": 0, "question": "q", "gold": "1"}\n',
                    encoding="utf-8")
    cfg["pool_jsonl"] = str(pool)
    cfg["pool_sha256"] = G.file_sha256(str(pool))
    assert G.check_pool(cfg) == cfg["pool_sha256"]
    pool.write_text('{"src": "gsm8k", "pool_i": 0, "question": "q", "gold": "2"}\n',
                    encoding="utf-8")
    with pytest.raises(SystemExit) as raised:
        G.check_pool(cfg)
    assert "pool_sha256" in str(raised.value)


def test_the_config_pins_the_shipped_pool(cfg):
    """config.yaml carries the hash of the screened pool the recipe was built against."""
    assert re.fullmatch(r"[0-9a-f]{64}", str(cfg["pool_sha256"]))
    pool = Path(__file__).resolve().parents[2] / "train" / "data" / "pool.jsonl"
    if not pool.exists():
        pytest.skip("the s33 pool copy is not in this checkout")
    assert G.file_sha256(str(pool)) == cfg["pool_sha256"]


# ================================================================= F4: --root is required
ROOT_STAGES = [("chains", "chains.py", ["gsm8k"]),
               ("targets", "targets.py", []),
               ("gates", "gates.py", []),
               ("train", "train.py", ["s36_budget_longest"]),
               ("run_grid", "run_grid.py", ["s36_budget_longest", "gsm8k"]),
               ("analysis", "analysis.py", [])]


@pytest.mark.parametrize("name,filename,argv", ROOT_STAGES)
def test_every_stage_refuses_to_guess_the_run_root(name, filename, argv):
    """No stage may default to a fixed home directory: two runs would share one directory."""
    module = load_module("recipe_root_%s" % name, filename)
    with pytest.raises(SystemExit) as raised:
        module.main(list(argv))
    assert "--root" in str(raised.value)
    source = Path(G.__file__).with_name(filename).read_text(encoding="utf-8")
    assert '"~/' not in source and "'~/" not in source, filename     # no home-directory default


def test_the_readme_commands_pass_the_root():
    """Every documented RUN stage carries --root, so the README can be pasted as it stands.

    Stage 0 is the one exception and is pinned as such: `theory_weights.py` reads the base grids and
    writes into the package, so it has no run root to take and must not invent one.
    """
    text = Path(G.__file__).resolve().parent.joinpath("README.md").read_text(encoding="utf-8")
    lines = [line for line in text.splitlines()
             if "train/" in line and line.strip().startswith("$PY")]
    stage0 = [line for line in lines if "theory_weights.py" in line]
    runs = [line for line in lines if "theory_weights.py" not in line]
    assert len(runs) >= 7
    assert all("--root=" in line for line in runs), runs
    assert stage0 and all("--root=" not in line for line in stage0), stage0


# ================================================================= F5: the measured memory claim
def readme_text():
    """Return the package README, the only place the cost estimates are written down."""
    return Path(G.__file__).resolve().parent.joinpath("README.md").read_text(encoding="utf-8")


def test_the_readme_states_the_measured_micro4_memory():
    """The micro-4 configuration has been timed; the README must not still say it has not."""
    text = readme_text()
    assert "has not been timed yet" not in text
    for claim in ("58.4 GB", "15 of 20", "70 GB", "uncontended", "101.3 GB"):
        assert claim in text, claim


def test_the_readme_costs_are_the_ones_the_new_buckets_imply(cfg):
    """The estimates are recomputed for the bucket set, and the superseded per-variant figure is named."""
    text = readme_text()
    assert "7.4 h per variant** figure was 590 steps" in text      # superseded, and said to be
    for claim in ("9.1 h", "about 800 steps", "14.8 h", "5.9 h", "about 26 h",
                  "s/step idle", "1.12 h each"):
        assert claim in text, claim
    for L in cfg.block_lens:                                   # every bucket has a priced step
        assert "| %d | %d x %d |" % (L, cfg.micro(L), cfg.accum(L)) in text, L
    assert "micro_by_block_len: {1536: 2}" in text              # the memory escape hatch
    assert "6,144" in text and "5,120" in text                  # the resident-positions argument


def test_the_readme_states_the_variant_order_of_record():
    """Item 6: the four variants stay, but the plan of record runs two of them."""
    text = readme_text()
    head = text[text.index("## Ablations"):text.index("## Files")]
    assert "plan of record" in head
    assert head.index("budget_longest") < head.index("nobudget")
    for variant in ("budget_longest", "budget_shortest", "nobudget", "nocut"):
        assert variant in head, variant
    assert "only if time remains" in head


# ================================================================= the horizon and the grid of record
def test_config_pins_the_production_caps_horizon_and_budgets(cfg):
    """The no-limit grid has to be placeable beside the base grids, so its caps and horizon are theirs."""
    assert [int(c) for c in cfg["eval_standard_caps"]] == [0, 16, 32, 64, 128, 256, 512, 1024,
                                                           2048, 4096]
    assert int(cfg["eval_horizon"]) == 4096
    assert [("none" if t is None else int(t)) for t in cfg["eval_budgets"]] == [0, 32, 128, 512,
                                                                               2048, "none"]
    assert int(cfg["chain_tail_chars"]) == 200
    prod = Path(__file__).resolve().parents[2] / "prod" / "config.yaml"
    if not prod.exists():
        pytest.skip("the production config is not in this checkout")
    import yaml
    pc = yaml.safe_load(prod.read_text(encoding="utf-8"))
    assert [int(c) for c in pc["caps"]] == [int(c) for c in cfg["eval_standard_caps"]]
    assert int(pc["horizon"]) == int(cfg["eval_horizon"])


def test_the_chains_horizon_is_per_source_and_covers_that_source_grid(cfg):
    assert {s: cfg.horizon(s) for s in cfg.sources} == {"gsm8k": 1024, "math": 2048,
                                                        "csqa": 1024, "aqua": 1024}
    assert cfg.budget_grid_for("math")[-2] == 2048
    assert cfg.budget_grid_for("gsm8k")[-2] == 1024
    assert cfg.budget_grid_for("csqa") == cfg.budget_grid_for("aqua") == cfg.budget_grid
    for src in cfg.sources:
        grid = cfg.budget_grid_for(src)
        assert grid[-1] is None                              # the no-limit draw is always there
        assert max(t for t in grid if t is not None) <= cfg.horizon(src)


def test_load_config_refuses_a_bucket_table_or_a_grid_that_cannot_be_run(tmp_path):
    """A micro that does not divide the window, a bucket with no micro, and a budget above the
    source's horizon are all config errors, not silent reweightings."""
    text = Path(CONFIG).read_text(encoding="utf-8")
    bad = tmp_path / "micro.yaml"
    bad.write_text(text.replace("micro_by_block_len: {1024: 4, 1536: 2, 2048: 2, 2560: 2, 3072: 1}",
                                "micro_by_block_len: {1024: 5, 1536: 2, 2048: 2, 2560: 2, 3072: 1}"),
                   encoding="utf-8")
    with pytest.raises(AssertionError):
        G.load_config(str(bad))
    bad2 = tmp_path / "bucket.yaml"
    bad2.write_text(text.replace("block_lens: [1024, 1536, 2048, 2560, 3072]",
                                 "block_lens: [1024, 1536, 2048, 2560, 3072, 4096]"),
                    encoding="utf-8")
    with pytest.raises(AssertionError):
        G.load_config(str(bad2))
    bad3 = tmp_path / "grid.yaml"
    bad3.write_text(text.replace("gsm8k: {eval_task: gsm8k,   n: 3000, format: numeric_hash, horizon: 1024}",
                                 "gsm8k: {eval_task: gsm8k,   n: 3000, format: numeric_hash, horizon: 512}"),
                    encoding="utf-8")
    with pytest.raises(AssertionError):
        G.load_config(str(bad3))


# ================================================================= the per-source budget grid
def test_each_source_draws_only_its_own_budget_grid(tmp_path, cfg, tok, monkeypatch):
    """MATH draws 2048 because its chains run to 2048; GSM8K must never see a budget it cannot fill."""
    P = synthetic_run(tmp_path, cfg, tok, monkeypatch,
                      {"gsm8k": "A" * 40, "math": "M" * 60}, budget=8000)
    assert G.main(["--variant=budget_longest", "--root=%s" % tmp_path]) == 0
    man = json.loads(Path(P["artifacts"], "target_manifest_budget_longest.json")
                     .read_text(encoding="utf-8"))
    assert man["budget_grid_by_source"]["math"][-2] == "2048"
    assert "2048" not in man["budget_grid_by_source"]["gsm8k"]
    drawn = man["visits_by_src_T"]
    assert "2048" not in drawn["gsm8k"], drawn["gsm8k"]
    assert "1024" in drawn["gsm8k"]
    assert "2048" in drawn["math"], drawn["math"]
    # the no-limit target is the FULL chain, and a chain that fits every cap is the same target
    assert set(man["visits_by_T"]) <= set(man["budget_grid_by_source"]["math"])


# ================================================================= the buckets, end to end
def test_a_visit_longer_than_the_longest_bucket_is_dropped_and_counted(tmp_path, cfg, tok,
                                                                      monkeypatch):
    """Truncating would delete the answer supervision at exactly the budgets this recipe repairs."""
    P = synthetic_run(tmp_path, cfg, tok, monkeypatch, {"gsm8k": "A" * 200}, budget=1500)
    cfg["block_lens"] = [128]                  # a 78-token prompt: the long chains cannot fit
    cfg["micro_by_block_len"] = {128: 4}
    cfg["effective_batch_blocks"] = 8
    cfg["fallback_ceiling"] = 1.0              # a 200-token chain fits almost no budget here
    assert G.main(["--variant=budget_longest", "--root=%s" % tmp_path]) == 0
    man = json.loads(Path(P["artifacts"], "target_manifest_budget_longest.json")
                     .read_text(encoding="utf-8"))
    assert man["dropped_draws"].get("longer_than_longest_block", 0) > 0
    assert all(int(L) <= 128 for L in man["blocks_by_len"])
    assert man["drop_share_of_draws"] > 0
    # a bucket that could not fill one window is named, never silently untrained
    assert set(man["blocks_dropped_as_remainder_by_len"]) == set(man["blocks_by_len"])
    assert isinstance(man["buckets_with_no_window"], list)


def test_the_manifest_reports_padding_per_bucket(cfg, tok):
    """Padding share per bucket is what says whether the bucket set is the right one."""
    use_block_lens(cfg, 256, 512, micro=2, blocks=4)
    visits = make_visits(cfg, tok, n=4, block_len=256) + make_visits(cfg, tok, n=4, block_len=512)
    arrays, _ = G.pack_one_visit_per_block(visits, tok.pad_token_id)
    per_bucket = {str(L): round(1.0 - float(a["length"].sum()) / int(a["blocks"].size), 5)
                  for L, a in arrays.items()}
    assert set(per_bucket) == {"256", "512"}
    assert per_bucket["512"] > per_bucket["256"]          # the same visits, twice the padding


# ================================================================= analysis reads the rows
def test_analysis_reads_the_cap_set_from_the_rows():
    analysis = load_module("recipe_analysis", "analysis.py")
    cand = {(0, "none", 0): {}, (0, "none", 128): {}, (0, "none", 4096): {}}
    ref = {(0, 0): {}, (0, 128): {}, (0, 512): {}}
    assert analysis.caps_in(cand) == [0, 128, 4096]
    assert analysis.caps_in(ref) == [0, 128, 512]
    assert analysis.caps_shared(cand, ref) == [0, 128]
    assert analysis.caps_in(None) == [] and analysis.caps_shared({}, ref) == []


def test_analysis_top_budget_is_the_largest_budget_the_grid_runs(cfg):
    analysis = load_module("recipe_analysis", "analysis.py")
    assert analysis.top_budgets(cfg) == 2048
    assert analysis.grid_from(cfg)[-1] == "none"
    assert analysis.caps_from(cfg)[-1] == 4096


def test_commitment_uses_only_the_caps_both_grids_measured():
    """A cap the reference never ran must not decide commitment, and 128 stays the reported gate."""
    analysis = load_module("recipe_analysis", "analysis.py")
    caps = [0, 128, 512]
    cand = {}
    for cap in caps + [4096]:
        cand[(7, "none", cap)] = {"pred": "4", "correct_v2": True}
    cand[(7, "none", 0)] = {"pred": "3", "correct_v2": False}
    out = analysis.commitment(cand, [7], caps, budget_key="none")
    assert out["caps"] == caps and out["cap_top"] == 512
    assert out["G128"] == 1.0 and out["acc_top"] == 1.0
    assert analysis.commitment(cand, [7], [0, 128, 512, 4096], budget_key="none")["cap_top"] == 4096
    assert analysis.commitment(cand, [7], [], budget_key="none") is None


# ================================================================= alloc can load the no-limit grid
def test_alloc_loads_the_no_limit_grid_and_ignores_the_budgeted_one(tmp_path, cfg):
    """The point of the no-limit pass is that it sits beside the base grids, so load it with alloc."""
    prod = Path(__file__).resolve().parents[2]
    if not (prod / "alloc" / "cells.py").exists():
        pytest.skip("the production alloc package is not in this checkout")
    sys.path.insert(0, str(prod))
    try:
        from alloc import cells as AC
    finally:
        sys.path.remove(str(prod))
    caps = [int(c) for c in cfg["eval_standard_caps"]]
    rows = []
    for i in range(12):
        nat = 100 + 9 * i
        for B in caps:
            cut = min(nat, B)
            rows.append({"idx": i, "row_idx": i, "split": "eval", "task": "gsm8k", "k": 4,
                         "budget": "none", "B": B, "pred": "4", "gold": "4",
                         "correct": cut >= nat, "correct_v2": cut >= nat,
                         "trace_answer": ("4" if cut >= nat else None),
                         "trace_correct": cut >= nat, "n_cut": cut, "natural_stop": nat,
                         "stop_reason": "natural", "chain_tail": "#### 4", "horizon": 4096,
                         "n_generated": cut + 9, "n_prompt_tokens": 640, "n_answer_tokens": 9,
                         "n_suffix_tokens": 5, "layer_passes": 96 * (640 + cut + 14),
                         "layer_passes_promptfree": 96 * (cut + 14), "answer_text": " 4"})
    Path(tmp_path, "cells_gsm8k_s36bl_k4.jsonl").write_text(
        "".join(json.dumps(r) + chr(10) for r in rows), encoding="utf-8")
    Path(tmp_path, "cells_budget_gsm8k_s36bl_k4.jsonl").write_text(
        json.dumps(dict(rows[0], budget=512, B=512, n_cut=512)) + chr(10), encoding="utf-8")
    found = [Path(x).name for x in AC.cell_paths(str(tmp_path), "gsm8k", "s36bl")]
    assert found == ["cells_gsm8k_s36bl_k4.jsonl"], found     # the budgeted file must not leak in
    loaded = AC.load(str(tmp_path), "gsm8k", "s36bl")
    assert loaded.ks == [4] and loaded.caps == caps
    assert len(loaded.idx) == 12
    loaded.assert_complete()                                   # every (depth, cap, question) present


# ================================================================= F3 runs at the new budgets
def write_grid(path, rows):
    """Write one cells file from dicts, one JSON row per line."""
    path.write_text("".join(json.dumps(r) + chr(10) for r in rows), encoding="utf-8")


def s36_rows(caps, budgets, n=12, correct=True):
    """Return the no-limit rows (every cap) and the budgeted rows (one cap each) of a fake s36 grid."""
    nat, nolimit, budgeted = 200, [], []
    for i in range(n):
        for B in caps:
            nolimit.append({"idx": i, "row_idx": i, "split": "eval", "task": "gsm8k", "k": 4,
                            "budget": "none", "B": B, "pred": "4", "correct_v2": correct,
                            "trace_answer": "4", "trace_correct": correct,
                            "n_cut": min(nat, B), "natural_stop": nat})
        for T in budgets:
            budgeted.append({"idx": i, "row_idx": i, "split": "eval", "task": "gsm8k", "k": 4,
                             "budget": T, "B": T, "pred": "4", "correct_v2": correct,
                             "trace_answer": "4", "trace_correct": correct,
                             "n_cut": min(nat, T), "natural_stop": min(nat, T)})
    return nolimit, budgeted


def run_analysis(tmp_path, cfg, monkeypatch, ref_caps):
    """Run stage 6 over a fake s36 grid and a fake reference whose caps stop where ref_caps stop."""
    analysis = load_module("recipe_analysis_run", "analysis.py")
    monkeypatch.setattr(analysis.G, "load_config", lambda *a, **k: cfg)
    art, ref = tmp_path / "artifacts", tmp_path / "ref"
    art.mkdir(parents=True), ref.mkdir(parents=True)
    caps = [int(c) for c in cfg["eval_standard_caps"]]
    budgets = [int(t) for t in cfg["eval_budgets"] if t is not None]
    nolimit, budgeted = s36_rows(caps, budgets)
    write_grid(art / "cells_gsm8k_s36bl_k4.jsonl", nolimit)
    write_grid(art / "cells_budget_gsm8k_s36bl_k4.jsonl", budgeted)
    write_grid(ref / "cells_gsm8k_s33_k4.jsonl",
               [{"idx": i, "split": "eval", "B": B, "pred": "4", "correct_v2": False,
                 "trace_answer": None, "trace_correct": False, "n_cut": min(150, B),
                 "natural_stop": 150} for i in range(12) for B in ref_caps])
    assert analysis.main(["--root=%s" % tmp_path, "--name=s36bl", "--ref=s33", "--boot=40",
                          "--cells-dir=%s" % art, "--ref-dir=%s" % ref,
                          "--out=%s" % (tmp_path / "out")]) == 0
    return json.loads((tmp_path / "out" / "s36bl_tests_vs_s33.json").read_text(encoding="utf-8"))


def test_f3_tests_non_inferiority_at_2048_and_at_no_limit_cut_there(tmp_path, cfg, monkeypatch):
    """Item 5: the top cell of F3 is the grid's largest budget, 2048, and the no-limit run cut at it."""
    res = run_analysis(tmp_path, cfg, monkeypatch,
                       ref_caps=[int(c) for c in cfg["eval_standard_caps"]])
    f3 = res["F3"]
    assert f3["top_budget"] == 2048 and "2048/none" in f3["rule"]
    e = f3["per_task"]["gsm8k"]
    assert e["top_cap"] == 2048
    assert e["at_top"]["n"] == 12 and e["at_none_top"]["n"] == 12
    assert e["at_top"]["delta_pts"] == 100.0 and e["top_non_inferior"] is True
    assert e["at_32"]["n"] == 12 and e["at_128"]["n"] == 12
    # F1 and F2 still read: the own-answer rate at 32 and 128, and the medians in budget order
    assert res["F1"]["per_task"]["gsm8k"]["32"]["n"] == 12
    med = res["F2"]["per_grid"]["gsm8k_k4"]["median_by_T"]
    assert list(med) == ["0", "32", "128", "512", "2048", "none"]
    assert med["none"] == 200.0 and med["2048"] == 200.0 and med["32"] == 32.0


def test_f3_falls_back_to_the_top_cap_a_512_reference_also_measured(tmp_path, cfg, monkeypatch):
    """A reference that only ran to 512 is still comparable, at 512, and never at a cap it lacks."""
    res = run_analysis(tmp_path, cfg, monkeypatch, ref_caps=[0, 16, 32, 64, 128, 256, 512])
    e = res["F3"]["per_task"]["gsm8k"]
    assert e["top_cap"] == 512                       # 2048 is not a cap the reference measured
    assert e["at_top"]["n"] == 12 and e["at_none_top"]["n"] == 12
    assert res["F2"]["per_grid"]["gsm8k_k4"]["ref_cap_for_natural_stop"] == 512
