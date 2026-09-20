"""Regression tests for token masks, task answers, execution depth, and resumable identities."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest
import torch

from test_recipe import (G, FakeTok, backend, cfg, tok, build, make_visits, use_block_lens,
                         Q, SRC, GOLD)


def test_print_one_visit_and_check_every_token(cfg, tok):
    ids, mask, info = build(cfg, tok, "budget_longest", 8)
    prompt_end = info["n_prompt"]
    chain_end = prompt_end + 8
    suffix_end = chain_end + info["n_suffix"]
    for position, (token, supervised) in enumerate(zip(ids, mask)):
        role = ("prompt" if position < prompt_end else "cut" if position < chain_end else
                "suffix" if position < suffix_end else "EOS" if position == len(ids) - 1 else "answer")
        piece = "<EOS>" if token == tok.eos_token_id else tok.decode([token])
        print(f"{position:4d} {role:7s} loss={supervised} {piece!r}")
        assert supervised == int(role in ("answer", "EOS"))
    use_block_lens(cfg, 256, micro=1, blocks=1)
    visits = [{"ids": ids, "mask": mask, "depth": 3, "n_prompt": prompt_end, "block_len": 256}]
    arrays, spans = G.pack_one_visit_per_block(visits, tok.pad_token_id)
    assert not arrays[256]["mask"][0, len(ids):].any()
    assert arrays[256]["length"].tolist() == [len(ids)]
    assert G.v3_context(arrays, spans)["ok"]


class ContextTok(FakeTok):
    """Encode a letter differently after a colon, exposing separately tokenized continuations."""
    def __call__(self, text, add_special_tokens=False):
        ids = super().__call__(text)["input_ids"]
        for i in range(1, len(text)):
            if text[i - 1] == ":" and text[i] == " ":
                ids[i] = 500
        return {"input_ids": ids}

    def decode(self, ids, **kwargs):
        return "".join(" " if i == 500 else chr(i - 10) for i in ids)


def test_readout_is_tokenized_after_prompt_and_suffix(cfg):
    tok = ContextTok()
    ids, mask, info = build(cfg, tok, "budget_longest", 0)
    text = G.eval_prompt(cfg, tok, "gsm8k", Q, 0) + G.task_bits("gsm8k")[2] + G.answer_text(cfg, SRC, GOLD)
    assert ids[:-1] == tok(text)["input_ids"]
    assert 500 in ids[info["n_prompt"]:]
    assert mask[-1] == 1


def test_fallback_keeps_standard_chain_even_when_it_was_incorrect(cfg, tok):
    ids, mask, info = G.build_target(cfg, tok, "budget_longest", SRC, Q, GOLD, 3,
                                    None, "BBBBBB", fallback_chain_A="standard wrong")
    assert info["chain_used"] == "A_cut"
    start = info["n_prompt"]
    assert tok.decode(ids[start:start + 3]) == "sta"
    assert mask[start:start + 3] == [0, 0, 0]
    ids, _, info = G.build_target(cfg, tok, "budget_longest", SRC, Q, GOLD, 3, None, "BBBBBB")
    assert ids is None


def test_no_limit_obeys_variant_rule_and_default_has_no_extra_readout(cfg, tok):
    for variant, expected in (("budget_longest", "B"), ("budget_shortest", "A"), ("nobudget", "B")):
        _, _, info = build(cfg, tok, variant, None, a="AAA", b="BBBBBB")
        assert info["chain_used"] == expected
        assert info["kind"] == "CHAIN"
    # the extra read-out is opt-in per visit; the configured share is what targets.py draws with
    assert float(cfg["fullplus_p"]) == 0.2


def test_context_gate_rejects_unsupervised_splits(cfg, tok):
    visits = make_visits(cfg, tok, n=2)
    for visit in visits:
        visit["mask"] = [0] * len(visit["ids"])
    arrays, spans = G.legacy_pack(visits, seq=16)
    result = G.v3_context(arrays, spans)
    assert not result["ok"]
    assert result["n_supervised_tokens"] == 0
    assert result["failures_by_reason"]["visit_split"] > 0


@pytest.mark.parametrize("task,text,expected", [
    ("gsm8k", "reason #### -1,234.5\nmore", "reason #### -1,234.5"),
    ("svamp", "reason #### 7", "reason #### 7"),
    ("math500", r"reason \boxed{\frac{1}{2}} trailing", r"reason \boxed{\frac{1}{2}}"),
    ("csqa", "reason The answer is (b). trailing", "reason The answer is (b)."),
])
def test_answer_sentence_detection(task, text, expected):
    assert G.trim_answer_sentence(text, task) == expected


def test_incomplete_answer_and_eos_are_not_answers():
    assert G.answer_sentence_end(r"\boxed{\frac{1}{2}", "math500") is None
    assert G.answer_sentence_end("####", "gsm8k") is None
    assert G.answer_sentence_end("thinking<|endoftext|>#### 3", "gsm8k") is None


def test_depth_is_restored_on_exception():
    base = SimpleNamespace(model=SimpleNamespace(total_ut_steps=4), config=SimpleNamespace(total_ut_steps=7))
    with pytest.raises(RuntimeError):
        with G.execution_depth(base, 2):
            assert base.model.total_ut_steps == base.config.total_ut_steps == 2
            raise RuntimeError("forward failed")
    assert (base.model.total_ut_steps, base.config.total_ut_steps) == (4, 7)


def test_loss_uses_selected_depth_once_and_window_token_denominator():
    path = Path(G.__file__).with_name("train.py")
    spec = importlib.util.spec_from_file_location("recipe_training", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    class Inner(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.total_ut_steps = 4
            self.weight = torch.nn.Parameter(torch.arange(12, dtype=torch.float).reshape(4, 3) / 10)
            self.calls = []
        def forward(self, input_ids, use_cache=False):
            self.calls.append(self.total_ut_steps)
            return None, [self.weight[input_ids] * (i + 1) for i in range(self.total_ut_steps)], None
    base = SimpleNamespace(model=Inner(), config=SimpleNamespace(total_ut_steps=4), lm_head=torch.nn.Identity())
    x = torch.tensor([[0, 1, 2, 0], [1, 2, 0, 0]])
    mask = torch.tensor([[0, 1, 1, 0], [0, 1, 0, 0]])
    ce, count = module.block_ce_sum(base, x, mask, 2)
    expected = torch.nn.functional.cross_entropy((base.model.weight[x] * 2)[:, :-1][mask[:, 1:].bool()],
                                                 x[:, 1:][mask[:, 1:].bool()], reduction="sum")
    assert torch.allclose(ce, expected)
    assert count == 3 and base.model.calls == [2]
    assert base.model.total_ut_steps == base.config.total_ut_steps == 4
    (ce / count).backward()
    gradient = base.model.weight.grad.clone()
    base.model.weight.grad = None
    for i in range(2):
        loss, _ = module.block_ce_sum(base, x[i:i + 1], mask[i:i + 1], 2)
        (loss / count).backward()
    assert torch.allclose(gradient, base.model.weight.grad)


def test_resume_budget_keys_are_identical_for_saved_and_live_rows():
    for budget in (None, "None", "none", "null"):
        assert G.budget_key(budget) == "none"
    for budget in (0, 32, 512):
        assert G.budget_key(str(budget)) == G.budget_key(budget)


def test_grid_twice_generates_matching_lines_without_duplicate_rows(cfg, tok, monkeypatch):
    import json
    import sys
    import tempfile
    import types
    import run_grid

    calls = []
    harness = types.ModuleType("s32_common")
    harness.MAXB, harness.MEM_FRACTION, harness.BATCH_CAP = 512, .5, 8
    harness.set_steps = lambda *args: None
    harness.static_cache_factory = lambda *args: None
    harness.batch_for = lambda *args: (8, None)
    harness.split_rows = lambda task: ([{"idx": 42, "input": Q, "target": GOLD}], [])
    harness.make_find_cut = lambda *args: lambda ids: (len(ids), "answer" if tok.decode(ids).endswith("4") else None)
    def decode(model, tokenizer, sequences, limit, *args):
        calls.append((tok.decode(sequences[0]), limit))
        return [tok(" 4" if limit == 12 else "#### 4")["input_ids"][:limit] for _ in sequences], 0
    harness.decode = decode
    harness.strip_tail = lambda ids, eos: ids
    harness.token_pieces = lambda *args: None
    harness.parse_forced = lambda *args: GOLD
    harness.parse_own = lambda text, *args: GOLD if "#### 4" in text else None
    harness.ans_eq = lambda pred, gold, task: pred == gold
    harness.score_v2 = lambda row: row["trace_correct"] if row["trace_answer"] is not None else row["correct"]
    harness.nvsmi = harness.gpu_procs = lambda: "mock CPU decoder"
    harness.load_base = lambda: (tok, SimpleNamespace(config=SimpleNamespace(vocab_size=512)))
    def load_ckpt(path, key):
        if not Path(path).exists():
            return {}
        rows = [json.loads(line) for line in Path(path).read_text().splitlines()]
        return {key(row): row for row in rows}
    harness.load_ckpt = load_ckpt
    class Appender:
        def __init__(self, path):
            self.file = open(path, "a", encoding="utf-8")
        def write(self, row):
            self.file.write(json.dumps(row) + "\n")
            self.file.flush()
        def close(self):
            self.file.close()
    harness.Appender = Appender
    patch_module = types.ModuleType("s3_patch")
    patch_module.patch_universal_cache = lambda model: (0, 0)
    monkeypatch.setitem(sys.modules, "s32_common", harness)
    monkeypatch.setitem(sys.modules, "s3_patch", patch_module)
    monkeypatch.setattr(G, "load_config", lambda *args: cfg)
    monkeypatch.setattr(G, "parse_forced_fixed", harness.parse_forced)
    monkeypatch.setattr(G, "parse_own_fixed", harness.parse_own)
    monkeypatch.setattr(G, "ans_eq_fixed", harness.ans_eq)
    monkeypatch.setattr(torch.cuda, "empty_cache", lambda: None)
    monkeypatch.setattr(torch.cuda, "max_memory_allocated", lambda: 0)
    with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as root:
        # --eval-rows=s32 keeps this pinned to the S32 subset the fake split_rows above returns;
        # the production default reads the harness's own rows and writes the _full files instead
        args = ["A0", "gsm8k", "--budgets=0,3,none", "--eval-rows=s32", "--no-wait",
                f"--root={root}"]
        assert run_grid.main(args) == 0
        path = Path(root) / "artifacts/cells_gsm8k_A0_k4.jsonl"
        first = path.read_bytes()
        count = len(calls)
        assert run_grid.main(args) == 0
        assert path.read_bytes() == first
        assert len(calls) == count
        rows = [json.loads(line) for line in first.splitlines()]
        # the no-limit pass is its own file: one row per standard cap, in the base grids' format
        caps = [int(c) for c in cfg["eval_standard_caps"]]
        assert len(rows) == len(caps)
        assert sorted(r["B"] for r in rows) == caps
        assert {r["budget"] for r in rows} == {"none"}
        assert len({(r["k"], r["B"], r["row_idx"]) for r in rows}) == len(rows)
        for field in ("idx", "row_idx", "k", "B", "split", "n_prompt_tokens", "n_suffix_tokens",
                      "n_answer_tokens", "natural_stop", "n_cut", "layer_passes",
                      "layer_passes_promptfree", "correct_v2", "trace_answer", "answer_text"):
            assert all(field in r for r in rows), field
        budget_path = Path(root) / "artifacts/cells_budget_gsm8k_A0_k4.jsonl"
        brows = [json.loads(line) for line in budget_path.read_text().splitlines()]
        assert sorted(r["budget"] for r in brows) == [0, 3]     # one line per stated budget
        for row in rows + brows:
            budget = None if row["budget"] == "none" else row["budget"]
            assert row["budget_line"] == G.budget_line(cfg, budget)
            assert row["n_cut"] <= row["B"]
            assert row["correct_v2"]
            assert row["stop_reason"] in ("natural", "budget", "horizon")
            assert len(row["chain_tail"]) <= int(cfg["chain_tail_chars"])
        assert {r["horizon"] for r in rows} == {int(cfg["eval_horizon"])}
        # the 3-token line is cut by its own budget; the no-limit pass stops on its answer sentence
        assert [r["stop_reason"] for r in brows if r["budget"] == 3] == ["budget"]
        assert {r["stop_reason"] for r in rows} == {"natural"}
        assert any("Budget: 3 tokens." in prompt and limit == 3 for prompt, limit in calls)
        assert any("Budget: 2048 tokens." not in prompt for prompt, limit in calls)
        assert any("Budget: no limit." in prompt and limit == 128 for prompt, limit in calls)
        assert max(limit for _p, limit in calls) >= 128
        import chains
        pool_path = Path(root) / "pool.jsonl"
        pool = [{"src": SRC, "pool_i": i, "question": Q, "gold": GOLD} for i in (7, 19)]
        pool_path.write_text("".join(json.dumps(row) + "\n" for row in pool))
        cfg["pool_jsonl"] = str(pool_path)
        chains_args = [SRC, "--n=2", "--no-wait", f"--root={root}"]
        assert chains.main(chains_args) == 0
        chains_file = Path(root) / "artifacts/chains_gsm8k_A_k4.jsonl"
        first_chains, count = chains_file.read_bytes(), len(calls)
        pool_path.write_text("".join(json.dumps(row) + "\n" for row in reversed(pool)))
        assert chains.main(chains_args) == 0
        assert chains_file.read_bytes() == first_chains
        assert len(calls) == count
        hrows = [json.loads(line) for line in first_chains.splitlines()]
        assert all(r["horizon"] == cfg.horizon(SRC) for r in hrows)
        assert all(r["kept"] and not r["hit_horizon"] for r in hrows)
        meta = json.loads((Path(root) / "artifacts/chains_meta_gsm8k_A.json").read_text())
        assert meta["horizon"] == cfg.horizon(SRC) == 1024
        assert meta["n_hit_horizon"] == 0 and meta["n_correct_but_unfinished"] == 0


def test_chains_drops_a_chain_that_ran_into_its_horizon(cfg, tok, monkeypatch):
    """A chain that never stopped is not a correct chain: it is dropped from the kept pool and counted,
    so every no-limit target is a chain that finished on its own."""
    import json
    import sys
    import tempfile
    import types
    import chains

    cfg["chains"] = {SRC: dict(cfg["chains"][SRC], horizon=256)}
    harness = types.ModuleType("s32_common")
    harness.MEM_FRACTION = 0.5
    harness.set_steps = lambda *args: None
    harness.static_cache_factory = lambda *args: None
    harness.batch_for = lambda *args: (8, None)
    # the decoder never writes an answer sentence, so find_cut never finds a stop marker
    harness.make_find_cut = lambda *args: (lambda ids: (len(ids), None))
    seen = []

    def decode(model, tokenizer, sequences, limit, *args):
        seen.append(limit)
        return [tok("z" * limit)["input_ids"] for _ in sequences], 0

    harness.decode = decode
    harness.strip_tail = lambda ids, eos: ids
    harness.token_pieces = lambda *args: None
    harness.nvsmi = harness.gpu_procs = lambda: "mock CPU decoder"
    harness.load_base = lambda: (tok, SimpleNamespace(config=SimpleNamespace(vocab_size=512)))

    def load_ckpt(path, key):
        return {}

    harness.load_ckpt = load_ckpt

    class Appender:
        def __init__(self, path):
            self.file = open(path, "a", encoding="utf-8")

        def write(self, row):
            self.file.write(json.dumps(row) + "\n")
            self.file.flush()

        def close(self):
            self.file.close()

    harness.Appender = Appender
    patch_module = types.ModuleType("s3_patch")
    patch_module.patch_universal_cache = lambda model: (0, 0)
    monkeypatch.setitem(sys.modules, "s32_common", harness)
    monkeypatch.setitem(sys.modules, "s3_patch", patch_module)
    monkeypatch.setattr(G, "load_config", lambda *args, **kw: cfg)
    monkeypatch.setattr(G, "parse_own_fixed", lambda *a, **k: GOLD)      # the text "parses" to gold
    monkeypatch.setattr(G, "ans_eq_fixed", lambda pred, gold, task: True)
    monkeypatch.setattr(torch.cuda, "empty_cache", lambda: None)
    monkeypatch.setattr(torch.cuda, "max_memory_allocated", lambda: 0)
    with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as root:
        pool_path = Path(root) / "pool.jsonl"
        pool_path.write_text("".join(json.dumps(
            {"src": SRC, "pool_i": i, "question": Q, "gold": GOLD}) + "\n" for i in (3, 4)))
        cfg["pool_jsonl"] = str(pool_path)
        assert chains.main([SRC, "--n=2", "--no-wait", "--root=%s" % root]) == 0
        rows = [json.loads(line) for line in
                (Path(root) / "artifacts/chains_gsm8k_A_k4.jsonl").read_text().splitlines()]
        assert rows and all(r["hit_horizon"] for r in rows)
        assert all(r["answer_correct"] and not r["kept"] for r in rows)   # correct text, unfinished
        assert all(r["horizon"] == 256 for r in rows)
        meta = json.loads((Path(root) / "artifacts/chains_meta_gsm8k_A.json").read_text())
        assert meta["horizon"] == 256
        assert meta["n_kept"] == 0 and meta["n_hit_horizon"] == len(rows)
        assert meta["n_correct_but_unfinished"] == len(rows)
        assert max(seen) <= 256 and G.generation_waves(256)[-1] == 256
