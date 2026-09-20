"""Check the knobs that run the recipe beyond its two scheduled variants: the production-split
evaluation rows and their `_full` files, the variant list and seed the sbatch files take, the seed
keying of stage 2's outputs, and the two plain-SFT baselines."""
import json
import sys
import types
from pathlib import Path

import numpy as np
import pytest
import torch

from test_recipe import (G, FakeTok, backend, cfg, tok, use_block_lens, CONFIG, Q, SRC, GOLD)

REPO = Path(__file__).resolve().parents[2]
ART = REPO / "artifacts"
TASKS_WITH_A_BASE_GRID = ("gsm8k", "csqa")


def run_grid_module():
    """Import train/run_grid.py by path; it pulls in the harness only inside main()."""
    if str(REPO / "train") not in sys.path:
        sys.path.insert(0, str(REPO / "train"))
    import run_grid
    return run_grid


def base_grid_split(task):
    """{row_idx: split} of the base model's own natural grid, first depth only. The file is not in
    dataset order -- it was written in the production run's batching order -- so it is read as a
    mapping and the dataset order is checked separately."""
    p = ART / ("cells_ouro_1_4b_base_%s_natural_k1.jsonl" % task)
    if not p.exists():
        pytest.skip("the base grid for %s is not in this checkout" % task)
    seen = {}
    with open(p, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if r.get("_header"):
                continue
            seen.setdefault(int(r["row_idx"]), r["split"])
    return seen


# ================================================================= E1: the production split
@pytest.mark.parametrize("task", TASKS_WITH_A_BASE_GRID)
def test_production_rows_and_split_are_the_base_grids_own(task):
    """Row for row, the production mode evaluates what the base grids evaluated, labelled the same.

    The labels are not recomputed here or in run_grid: prod.tasks.split_labels is the seed of
    record and is called. This test is what ties the two together.
    """
    run_grid = run_grid_module()
    rows, split = run_grid.production_rows(task)
    assert [int(r["idx"]) for r in rows] == list(range(len(rows)))     # dataset order, no gaps
    assert {int(r["idx"]): s for r, s in zip(rows, split)} == base_grid_split(task)


def test_production_mode_evaluates_the_full_row_set(cfg):
    """Full N per task, and the config's default is the production split."""
    run_grid = run_grid_module()
    assert cfg["eval_rows"] == "production"
    for task, n in (("gsm8k", 1319), ("math500", 500), ("csqa", 1221), ("aqua", 254)):
        rows, split = run_grid.production_rows(task)
        assert len(rows) == len(split) == n, task
        assert split.count("cal") == 100, task


def test_eval_rows_s32_keeps_the_first_300_eval_and_the_next_100_cal():
    """The old selection is still reachable: the first 300 rows as eval, the next 100 as cal."""
    run_grid = run_grid_module()
    s32 = pytest.importorskip("s32_common")
    ev, cal = s32.split_rows("gsm8k")
    assert (len(ev), len(cal)) == (300, 100)
    rows, split = run_grid.production_rows("gsm8k")
    assert [r["idx"] for r in ev + cal] == [r["idx"] for r in rows[:400]]   # same rows, same order
    assert split[:400] != ["eval"] * 300 + ["cal"] * 100                    # different labels


def test_the_production_label_is_full_and_analysis_reads_it_by_name():
    """`<name>_full` keys the cells, budget and meta files, and is the --name analysis takes."""
    run_grid = run_grid_module()
    assert run_grid.grid_label("s36_budget_longest", "s32") == "s36_budget_longest"
    label = run_grid.grid_label("s36_budget_longest", "production")
    assert label == "s36_budget_longest_full"
    # analysis.py builds "cells_%s_%s_k%d.jsonl" % (task, NAME, k) from --name
    assert ("cells_%s_%s_k%d.jsonl" % ("gsm8k", label, 4)
            == "cells_gsm8k_s36_budget_longest_full_k4.jsonl")


def test_an_unknown_eval_rows_value_is_refused(tmp_path):
    """A value no stage implements stops the load, naming the values that exist."""
    text = Path(CONFIG).read_text(encoding="utf-8").replace("eval_rows: production",
                                                            "eval_rows: whatever")
    bad = tmp_path / "config.yaml"
    bad.write_text(text, encoding="utf-8")
    with pytest.raises(ValueError, match="eval_rows"):
        G.load_config(str(bad))


# ---------------------------------------------------------------- E1 end to end, on three rows
def fake_harness(tok, calls):
    """A CPU stand-in for s32_common: three rows, a one-line chain, no model."""
    h = types.ModuleType("s32_common")
    h.MAXB, h.MEM_FRACTION, h.BATCH_CAP = 512, .5, 8
    h.set_steps = lambda *a: None
    h.static_cache_factory = lambda *a: None
    h.batch_for = lambda *a: (8, None)
    h.split_rows = lambda task: ([{"idx": 7, "input": Q, "target": GOLD}], [])
    h.make_find_cut = lambda *a: (lambda ids: (len(ids),
                                               "answer" if tok.decode(ids).endswith("4") else None))

    def decode(model, tokenizer, sequences, limit, *a):
        calls.append(limit)
        return [tok(" 4" if limit == 12 else "#### 4")["input_ids"][:limit] for _ in sequences], 0

    h.decode = decode
    h.strip_tail = lambda ids, eos: ids
    h.token_pieces = lambda *a: None
    h.parse_forced = lambda *a: GOLD
    h.parse_own = lambda text, *a: GOLD if "#### 4" in text else None
    h.ans_eq = lambda pred, gold, task: pred == gold
    h.score_v2 = lambda row: row["correct"]
    h.nvsmi = h.gpu_procs = lambda: "mock CPU decoder"
    h.load_base = lambda: (tok, types.SimpleNamespace(config=types.SimpleNamespace(vocab_size=512)))

    def load_ckpt(path, key):
        if not Path(path).exists():
            return {}
        return {key(json.loads(line)): json.loads(line)
                for line in Path(path).read_text(encoding="utf-8").splitlines()}

    h.load_ckpt = load_ckpt

    class Appender:
        def __init__(self, path):
            self.file = open(path, "a", encoding="utf-8")

        def write(self, row):
            self.file.write(json.dumps(row) + "\n")
            self.file.flush()

        def close(self):
            self.file.close()

    h.Appender = Appender
    return h


def test_a_production_grid_writes_full_files_and_the_harness_split(tmp_path, cfg, tok, monkeypatch):
    """Run stage 5 on three rows in both modes: the names carry `_full` only under production, the
    two modes never write the same file, and every row carries the harness's own split label."""
    run_grid = run_grid_module()
    calls = []
    monkeypatch.setitem(sys.modules, "s32_common", fake_harness(tok, calls))
    patch = types.ModuleType("s3_patch")
    patch.patch_universal_cache = lambda model: (0, 0)
    monkeypatch.setitem(sys.modules, "s3_patch", patch)
    monkeypatch.setattr(G, "load_config", lambda *a, **k: cfg)
    monkeypatch.setattr(G, "parse_forced_fixed", lambda *a: GOLD)
    monkeypatch.setattr(G, "parse_own_fixed", lambda text, *a: GOLD if "#### 4" in text else None)
    monkeypatch.setattr(G, "ans_eq_fixed", lambda pred, gold, task: pred == gold)
    monkeypatch.setattr(torch.cuda, "empty_cache", lambda: None)
    monkeypatch.setattr(torch.cuda, "max_memory_allocated", lambda: 0)

    args = ["A0", "gsm8k", "--budgets=0,none", "--n=3", "--no-wait", "--root=%s" % tmp_path]
    assert run_grid.main(args) == 0                       # the config default: production
    art = Path(tmp_path, "artifacts")
    assert (art / "cells_gsm8k_A0_full_k4.jsonl").exists()
    assert (art / "cells_budget_gsm8k_A0_full_k4.jsonl").exists()
    assert (art / "meta_gsm8k_A0_full_k4.json").exists()
    assert not (art / "cells_gsm8k_A0_k4.jsonl").exists()

    rows = [json.loads(line) for line in
            (art / "cells_gsm8k_A0_full_k4.jsonl").read_text(encoding="utf-8").splitlines()]
    want = base_grid_split("gsm8k")
    assert {r["row_idx"] for r in rows} == {0, 1, 2}        # the first three dataset rows
    assert all(r["split"] == want[r["row_idx"]] for r in rows)
    assert {r["name"] for r in rows} == {"A0_full"}
    meta = json.loads((art / "meta_gsm8k_A0_full_k4.json").read_text(encoding="utf-8"))
    assert meta["eval_rows"] == "production" and meta["checkpoint"] == "A0"
    assert meta["n_eval"] + meta["n_cal"] == 3

    assert run_grid.main(args + ["--eval-rows=s32"]) == 0   # the flag beats the config key
    assert (art / "cells_gsm8k_A0_k4.jsonl").exists()
    s32rows = [json.loads(line) for line in
               (art / "cells_gsm8k_A0_k4.jsonl").read_text(encoding="utf-8").splitlines()]
    assert {r["row_idx"] for r in s32rows} == {7}          # the fake harness's own row
    assert {r["name"] for r in s32rows} == {"A0"}


# ================================================================= E2: the sbatch knobs
@pytest.mark.parametrize("name,knobs", [
    ("variant_s36.sbatch", ['VARIANTS="${VARIANTS:-budget_longest uniform_longest}"',
                            'VARIANT="${VLIST[$I]}"', 'SEED="${SEED:-$DEFAULT_SEED}"',
                            '--array=0-3 --export=ALL,VARIANTS="nobudget nocut plain_sft '
                            'plain_sft_mix"']),
    ("grids_s36.sbatch", ['VARIANTS="${VARIANTS:-budget_longest uniform_longest}"',
                          'VARIANT="${VLIST[$((I / 4))]}"', 'TASK="${TASKS[$((I % 4))]}"',
                          'EVAL_ROWS="${EVAL_ROWS:-production}"', '--eval-rows="$EVAL_ROWS"',
                          '--array=0-7', '--array=0-15'])])
def test_the_sbatch_files_take_the_variant_list_the_seed_and_the_rows(name, knobs):
    """The two launchers run any variant list and any seed without being edited."""
    text = (REPO / "slurm" / name).read_text(encoding="utf-8")
    for knob in knobs:
        assert knob in text, (name, knob)
    for pinned in ("#!/bin/bash", "set -u", "source env.sh", "export CLUSTER=1", "RC=$?", "cd "):
        assert pinned in text, (name, pinned)


# ================================================================= stage 2 on a synthetic pool
def stage2(tmp_path, cfg, monkeypatch, variant, seed=None, n_pool=40):
    """Run stage 2 over a synthetic pool and return (its manifest, its visits)."""
    class GateTok(FakeTok):
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
        for i in range(n_pool)), encoding="utf-8")
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
                        "question": "%s #%d" % (Q, i)}) + "\n" for i in range(n_pool)),
            encoding="utf-8")
    monkeypatch.setattr(G, "load_config", lambda *a, **k: cfg)
    argv = ["--variant=%s" % variant, "--root=%s" % tmp_path]
    if seed is not None:
        argv.append("--seed=%d" % seed)
    assert G.main(argv) == 0
    key = G.variant_key(cfg, variant, seed)
    man = json.loads(Path(G.manifest_path(P, key)).read_text(encoding="utf-8"))
    visits = [json.loads(l) for l in
              Path(man["data_dir"], "visits.jsonl").read_text(encoding="utf-8").splitlines()]
    return man, visits


# ================================================================= E3: seeds
def test_two_seeds_draw_differently_and_never_share_a_data_directory(tmp_path, cfg, monkeypatch):
    """A second seed is a second draw: its own blocks, its own manifest, its own histogram."""
    P = G.paths(str(tmp_path))
    default, _v = stage2(tmp_path, cfg, monkeypatch, "budget_longest")
    other, _v2 = stage2(tmp_path, cfg, monkeypatch, "budget_longest", seed=20260915)
    assert Path(default["data_dir"]) == Path(G.data_dir(P, "budget_longest"))   # today's path
    assert Path(other["data_dir"]) == Path(G.data_dir(P, "budget_longest_seed20260915"))
    assert default["seed"] != other["seed"] == 20260915
    assert default["visits_by_T"] != other["visits_by_T"]          # a different draw
    assert default["variant"] == other["variant"] == "budget_longest"
    assert Path(G.manifest_path(P, "budget_longest_seed20260915")).exists()


def test_the_config_seed_keys_nothing_and_any_other_seed_keys_everything(cfg):
    """variant_key is what every stage after targets uses to find the blocks and the manifest."""
    assert G.variant_key(cfg, "nocut", None) == "nocut"
    assert G.variant_key(cfg, "nocut", int(cfg["seed"])) == "nocut"
    assert G.variant_key(cfg, "nocut", 20260915) == "nocut_seed20260915"


# ================================================================= E4: the two plain-SFT baselines
def test_plain_sft_is_the_full_chain_at_depth_four_with_no_line_and_no_cut(tmp_path, cfg,
                                                                          monkeypatch):
    """The control for the whole objective: no budget draw, no budget line, no cut, one depth."""
    man, visits = stage2(tmp_path, cfg, monkeypatch, "plain_sft")
    assert visits and all(v["T"] is None for v in visits)
    assert all(v["depth"] == 4 for v in visits)
    assert all(v["budget_line_tokens"] == 0 for v in visits)
    assert all(v["kind"] in ("CHAIN", "CHAIN_PLUS") for v in visits)
    assert all(v["chain_used"] == "A" for v in visits)          # the full standard chain
    assert man["fallback_share_overall"] == 0.0
    assert "FALLBACK" not in man["visits_by_kind"]
    assert man["visits_by_T"] == {"none": len(visits)}
    assert man["depth_fraction_realised"] == {"1": 0.0, "2": 0.0, "3": 0.0, "4": 1.0}
    assert man["draw_rule"] == "none_only" and man["depth_rule"] == "fixed:4"
    assert man["variant_config"]["budget_line"] is False
    blocks = np.load(Path(man["data_dir"], "bdepth_512.npy"))
    assert blocks.size and set(blocks.tolist()) == {4}
    assert man["v10_draw_weights"]["ok"] is True                # V10 accepts the baseline
    v10 = man["v10_draw_weights"]["by_source"]
    assert v10["budget_%s" % SRC]["intended"] == {"none": 1.0}
    assert v10["depth_%s" % SRC]["intended"] == {"4": 1.0}


def test_plain_sft_mix_keeps_the_depth_mix_and_drops_only_the_budget(tmp_path, cfg, monkeypatch):
    """The second baseline isolates the depth sampling: same targets, the theory depth mix back."""
    man, visits = stage2(tmp_path, cfg, monkeypatch, "plain_sft_mix")
    assert visits and all(v["T"] is None for v in visits)
    assert all(v["budget_line_tokens"] == 0 for v in visits)
    assert man["visits_by_T"] == {"none": len(visits)}
    assert man["draw_rule"] == "none_only" and man["depth_rule"] == "theory"
    realised = man["draw_histogram_realised"]["depth"][SRC]
    assert len(realised) >= 2, realised                          # not degenerate
    assert man["v10_draw_weights"]["ok"] is True
    intended = man["v10_draw_weights"]["by_source"]["depth_%s" % SRC]["intended"]
    assert intended == G.jload(G.THEORY_WEIGHTS)["sources"][SRC]["depth_weights"]


@pytest.mark.parametrize("variant", ["plain_sft", "plain_sft_mix"])
def test_v1_parity_runs_on_a_baseline_with_no_budget_line(cfg, tok, variant):
    """V1's check with the line switched off: the prompt is the harness's, at every T the grid can
    draw, and it still ends on the answer prefix."""
    assert cfg.variant(variant)["budget_line"] is False
    bare = G.eval_prompt(cfg, tok, "gsm8k", Q, None, False)
    for T in cfg.budget_grid_for(SRC):
        assert G.budget_line(cfg, T, False) == ""
        mine = G.eval_prompt(cfg, tok, "gsm8k", Q, T, False)
        assert mine == bare and mine.endswith(G.task_bits("gsm8k")[1])


@pytest.mark.parametrize("field,value", [("draw", "whatever"), ("depth", "fixed:9"),
                                         ("depth", "sometimes"), ("rule", "middle_fitting")])
def test_an_unknown_variant_field_is_refused_at_load(cfg, field, value):
    """A variant field no stage implements stops the load, naming the variant and the values."""
    bad = dict(cfg)
    bad["variants"] = dict(cfg["variants"])
    bad["variants"]["mystery"] = dict(cfg["variants"]["budget_longest"])
    bad["variants"]["mystery"][field] = value
    with pytest.raises(ValueError, match="mystery"):
        G.check_variants(G.Config(bad))
