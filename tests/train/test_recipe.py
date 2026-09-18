"""Check target selection, prompt bytes, token masks, independent blocks, and schedules using synthetic prompts and a character tokenizer."""
import os
import sys

import numpy as np
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
TRAIN = os.path.join(os.path.dirname(os.path.dirname(HERE)), "train")   # repo root / train
if TRAIN not in sys.path:
    sys.path.insert(0, TRAIN)
import targets as G                                     # noqa: E402

CONFIG = os.path.join(TRAIN, "config.yaml")
OFF = 10                    # keeps synthetic ids clear of pad (0) and eos (1)
PREFIX = "EX|" * 10         # 30 "tokens" of exemplar block
QP, AP, SFX = "Q: ", "\nA:", "\nFinal Answer:"


class FakeTok:
    """Character-level tokenizer: exactly stable under concatenation, so one character is one
    token and a chain of n characters is a chain of n tokens."""
    eos_token_id = 1
    pad_token_id = 0

    def __call__(self, text, add_special_tokens=False):
        return {"input_ids": [ord(c) + OFF for c in text]}

    def decode(self, ids, **kw):
        return "".join(chr(i - OFF) for i in ids)


def fake_prefix(tok, eval_task):
    return PREFIX


def fake_bits(eval_task):
    return (QP, AP, SFX, ["\nQ:"], "The answer is", "numeric")


@pytest.fixture(autouse=True)
def backend():
    G.set_prompt_backend(fake_prefix, fake_bits)
    yield
    G.reset_prompt_backend()


@pytest.fixture
def cfg():
    return G.load_config(CONFIG)


@pytest.fixture
def tok():
    return FakeTok()


def use_block_lens(cfg, *lens, micro=4, blocks=None):
    """Point the config's bucket table at synthetic block lengths, so the CPU tests can pack tiny visits."""
    cfg["block_lens"] = [int(L) for L in lens]
    cfg["micro_by_block_len"] = {int(L): int(micro) for L in lens}
    cfg["effective_batch_blocks"] = int(blocks if blocks is not None else micro * 2)
    return cfg


CH_A = "A" * 40             # the standard-prompt chain: 40 tokens
CH_B = "B" * 12             # the short-exemplar chain: 12 tokens
Q, GOLD, SRC = "what is 2+2", "4", "gsm8k"


def build(cfg, tok, arm, T, a=CH_A, b=CH_B, fullplus=False):
    return G.build_target(cfg, tok, arm, SRC, Q, GOLD, T, a, b, fullplus=fullplus)


# ================================================================= 1. the target rule
def test_longest_fitting_prefers_the_long_chain(cfg, tok):
    ids, msk, info = build(cfg, tok, "budget_longest", 64)
    assert info["kind"] == "CHAIN"
    assert info["chain_used"] == "A" and info["n_chain"] == len(CH_A)


def test_longest_fitting_falls_to_the_short_chain_when_the_long_one_does_not_fit(cfg, tok):
    ids, msk, info = build(cfg, tok, "budget_longest", 32)
    assert info["kind"] == "CHAIN"
    assert info["chain_used"] == "B" and info["n_chain"] == len(CH_B)


def test_exact_fit_counts_as_fitting(cfg, tok):
    _i, _m, info = build(cfg, tok, "budget_longest", len(CH_A))
    assert info["chain_used"] == "A"


def test_fallback_when_neither_chain_fits(cfg, tok):
    ids, msk, info = build(cfg, tok, "budget_longest", 8)
    assert info["kind"] == "FALLBACK"
    assert info["chain_used"] == "A_cut" and info["n_chain"] == 8


def test_t0_is_direct_and_t_none_is_the_full_standard_chain(cfg, tok):
    _i, _m, d0 = build(cfg, tok, "budget_longest", 0)
    assert d0["kind"] == "DIRECT" and d0["n_chain"] == 0
    _i, _m, dn = build(cfg, tok, "budget_longest", None)
    assert dn["kind"] == "CHAIN" and dn["chain_used"] == "A" and dn["n_chain"] == len(CH_A)
    _i, _m, dp = build(cfg, tok, "budget_longest", None, fullplus=True)
    assert dp["kind"] == "CHAIN_PLUS"


def test_no_limit_uses_the_short_chain_only_when_the_standard_one_is_not_correct(cfg, tok):
    _i, _m, info = build(cfg, tok, "budget_longest", None, a=None)
    assert info["chain_used"] == "B"
    ids, msk, info = build(cfg, tok, "budget_longest", None, a=None, b=None)
    assert ids is None and info["dropped"] == "no_correct_chain"


# ================================================================= 6. the arm flags
def test_shortest_fitting_arm_reproduces_the_s34_p1_rule(cfg, tok):
    """Check that the shortest-fitting ablation selects the short correct chain when both candidates fit."""
    _i, _m, info = build(cfg, tok, "budget_shortest", 64)
    assert info["chain_used"] == "B" and info["n_chain"] == len(CH_B)
    _i, _m, longest = build(cfg, tok, "budget_longest", 64)
    assert longest["chain_used"] == "A"


def test_nocut_arm_drops_instead_of_falling_back(cfg, tok):
    ids, msk, info = build(cfg, tok, "nocut", 8)
    assert ids is None and info["dropped"] == "no_fitting_chain_and_no_fallback"
    ids, _m, info = build(cfg, tok, "nocut", 64)
    assert ids is not None and info["kind"] == "CHAIN"


def test_nobudget_arm_carries_no_line_but_the_same_target(cfg, tok):
    _i, _m, nb = build(cfg, tok, "nobudget", 64)
    _i, _m, bl = build(cfg, tok, "budget_longest", 64)
    assert nb["budget_line"] == "" and nb["budget_line_tokens"] == 0
    assert bl["budget_line"] != "" and bl["budget_line_tokens"] > 0
    assert nb["chain_used"] == bl["chain_used"] == "A"
    assert nb["n_prompt"] == bl["n_prompt"] - bl["budget_line_tokens"]


def test_every_arm_in_the_config_builds(cfg, tok):
    for arm in cfg["arms"]:
        ids, _m, info = build(cfg, tok, arm, 64)
        assert ids is not None, (arm, info)


# ================================================================= 5. the budget line
def test_budget_line_text_and_placement(cfg, tok):
    for T in (0, 16, 512):
        line = G.budget_line(cfg, T)
        assert line == "\nBudget: %d tokens." % T
        p = G.eval_prompt(cfg, tok, "gsm8k", Q, T)
        assert p.count(line) == 1
        assert p.endswith(line + AP)                     # immediately before the answer prefix
        assert p.replace(line, "", 1) == PREFIX + QP + Q + AP
        assert PREFIX in p.split(QP)[0]                  # exemplars unchanged, line not inside them
        assert line not in PREFIX


def test_no_limit_line_and_suppressed_line(cfg, tok):
    assert G.budget_line(cfg, None) == "\nBudget: no limit."
    assert G.budget_line(cfg, 32, with_line=False) == ""
    assert G.eval_prompt(cfg, tok, "gsm8k", Q, 32, False) == PREFIX + QP + Q + AP


# ================================================================= 2. the loss masks
def test_prompt_line_and_suffix_are_never_supervised(cfg, tok):
    for T in (0, 8, 32, 64, None):
        ids, msk, info = build(cfg, tok, "budget_longest", T)
        n_p = info["n_prompt"]
        assert not any(msk[:n_p]), (T, "prompt or budget line supervised")
        n_s = len(tok(SFX)["input_ids"])
        if info["kind"] in ("DIRECT", "FALLBACK"):
            st = n_p + info["n_chain"]
            assert not any(msk[st:st + n_s]), (T, "suffix supervised")
            assert sum(msk) == info["n_answer"] + 1      # answer + EOS only
        if info["kind"] == "CHAIN":
            assert all(msk[n_p:n_p + info["n_chain"]])
            assert sum(msk) == info["n_chain"] + 1       # chain + EOS
        assert msk[-1] == 1 and ids[-1] == tok.eos_token_id
        assert len(ids) == len(msk)


def test_chain_ids_match_the_ids_the_harness_would_generate(cfg, tok):
    prompt = G.eval_prompt(cfg, tok, "gsm8k", Q, 64)
    p_ids, c_ids = G.chain_ids(tok, prompt, CH_A)
    assert tok(prompt + CH_A)["input_ids"] == p_ids + c_ids


# ================================================================= 3. one visit per block
def make_visits(cfg, tok, arm="budget_longest", n=12, block_len=256):
    visits = []
    for j in range(n):
        T = [0, 8, 32, 64, None][j % 5]
        ids, msk, info = G.build_target(cfg, tok, arm, SRC, Q + " #%d" % j, GOLD, T, CH_A, CH_B)
        assert ids is not None
        visits.append({"ids": ids, "mask": msk, "depth": 1 + (j % 4),
                       "n_prompt": info["n_prompt"], "block_len": block_len,
                       "n_tokens": len(ids)})
    return visits


def test_one_visit_per_block_with_right_padding(cfg, tok):
    visits = make_visits(cfg, tok)
    arrays, spans = G.pack_one_visit_per_block(visits, pad_id=tok.pad_token_id)
    (L, A), = arrays.items()
    assert A["blocks"].shape == (len(visits), L)
    assert len(spans) == len(visits)
    for b, v in enumerate(visits):
        m = len(v["ids"])
        assert A["blocks"][b, :m].tolist() == v["ids"]
        assert A["mask"][b, :m].tolist() == v["mask"]
        assert (A["blocks"][b, m:] == tok.pad_token_id).all()     # right padding
        assert (A["mask"][b, m:] == 0).all()                      # padding never supervised
        assert spans[b]["v_start"] == 0 and spans[b]["start"] == 0


def test_v3_context_passes_on_one_visit_per_block(cfg, tok):
    visits = make_visits(cfg, tok)
    arrays, spans = G.pack_one_visit_per_block(visits, pad_id=tok.pad_token_id)
    v3 = G.v3_context(arrays, spans)
    assert v3["ok"] is True
    assert v3["n_failing_spans"] == 0 and v3["failures_by_reason"] == {}
    assert v3["n_supervised_tokens"] == sum(sum(v["mask"]) for v in visits)


def test_a_visit_longer_than_its_block_is_refused_not_split(cfg, tok):
    visits = make_visits(cfg, tok, block_len=64)
    with pytest.raises(AssertionError):
        G.pack_one_visit_per_block(visits, pad_id=tok.pad_token_id)


# ================================================================= 4. V3-CONTEXT on a split stream
def test_v3_context_fails_on_a_deliberately_split_stream(cfg, tok):
    """Check that concatenating visits into fixed-length blocks fails the context gate."""
    visits = make_visits(cfg, tok, n=16)
    arrays, spans = G.legacy_pack(visits, seq=128)
    v3 = G.v3_context(arrays, spans)
    assert v3["ok"] is False
    assert v3["n_failing_spans"] > 0
    assert "prompt_split_or_absent" in v3["failures_by_reason"]
    assert "cross_visit_context" in v3["failures_by_reason"]
    assert v3["detail"], "the gate must name the offending blocks"


def test_the_two_packers_disagree_only_about_context(cfg, tok):
    """Same visits, same supervised tokens; the legacy packing is what breaks V3-CONTEXT."""
    visits = make_visits(cfg, tok, n=16)
    good = G.v3_context(*G.pack_one_visit_per_block(visits, pad_id=tok.pad_token_id))
    bad = G.v3_context(*G.legacy_pack(visits, seq=128))
    assert good["ok"] and not bad["ok"]
    assert bad["n_supervised_tokens"] > 0


# ================================================================= the block-length buckets
def test_a_visit_goes_in_the_smallest_bucket_that_fits_it(cfg):
    assert cfg.block_lens == [1024, 1536, 2048, 2560, 3072]
    assert cfg.block_len_for(1) == 1024
    assert cfg.block_len_for(1024) == 1024                 # an exact fit does not spill upwards
    assert cfg.block_len_for(1025) == 1536
    assert cfg.block_len_for(2049) == 2560
    assert cfg.block_len_for(3072) == 3072
    assert cfg.block_len_for(3073) is None                 # longer than every bucket: dropped


def test_every_bucket_has_a_micro_and_a_whole_number_of_them_per_step(cfg):
    """The window is the same 32 blocks in every bucket, so a long bucket only changes the split."""
    assert int(cfg["effective_batch_blocks"]) == 32
    assert {L: cfg.micro(L) for L in cfg.block_lens} == {1024: 4, 1536: 2, 2048: 2, 2560: 2,
                                                         3072: 1}
    for L in cfg.block_lens:
        assert cfg.micro(L) * cfg.accum(L) == 32


def test_generation_waves_cover_every_horizon_in_the_config(cfg):
    """Harvest and the grid step through the same doubling waves, or a 4096 horizon is one blind pass."""
    assert G.generation_waves(512) == [128, 256, 512]
    assert G.generation_waves(1024) == [128, 256, 512, 1024]
    assert G.generation_waves(2048) == [128, 256, 512, 1024, 2048]
    assert G.generation_waves(4096) == [128, 256, 512, 1024, 2048, 4096]
    assert G.generation_waves(32) == [32] and G.generation_waves(0) == []
    for src in cfg.sources:
        assert G.generation_waves(cfg.horizon(src))[-1] == cfg.horizon(src)
    assert G.generation_waves(int(cfg["eval_horizon"]))[-1] == 4096


# ================================================================= the schedule
def test_micro_batches_are_homogeneous_in_depth_and_block_length(cfg, tok):
    use_block_lens(cfg, 256, 320, micro=4, blocks=8)
    visits = []
    for L in (256, 320):
        vs = make_visits(cfg, tok, n=16, block_len=L)
        for v in vs:
            v["depth"] = 1
        visits += vs
    arrays, _spans = G.pack_one_visit_per_block(visits, pad_id=tok.pad_token_id)
    sched, n_opt = G.build_schedule(cfg, arrays, np.random.default_rng(0))
    assert sched and n_opt == 4                             # 2 buckets x 16 blocks / 8 per window
    for mb in sched:
        L = mb["seq_len"]
        assert len(mb["blocks"]) == cfg.micro(L)
        assert len({int(arrays[L]["depth"][b]) for b in mb["blocks"]}) == 1
        assert mb["supervised"] > 0
    windows = G.windows_from_schedule(sched)
    assert len(windows) == n_opt
    for w in windows:
        assert len({int(mb["seq_len"]) for mb in w}) == 1   # a window never mixes block lengths
        assert len({int(mb["depth"]) for mb in w}) == 1
        assert sum(len(mb["blocks"]) for mb in w) == cfg["effective_batch_blocks"]


def test_a_long_bucket_takes_a_smaller_micro_and_a_longer_accumulation(cfg, tok):
    """Same window in blocks, half resident per forward: that is the whole point of micro_by_block_len."""
    cfg["block_lens"] = [256, 512]
    cfg["micro_by_block_len"] = {256: 4, 512: 2}
    cfg["effective_batch_blocks"] = 8
    visits = []
    for L in (256, 512):
        vs = make_visits(cfg, tok, n=8, block_len=L)
        for v in vs:
            v["depth"] = 2
        visits += vs
    arrays, _ = G.pack_one_visit_per_block(visits, pad_id=tok.pad_token_id)
    sched, n_opt = G.build_schedule(cfg, arrays, np.random.default_rng(0))
    assert n_opt == 2                                       # one window of 8 blocks per bucket
    by_len = {}
    for w in G.windows_from_schedule(sched):
        L = int(w[0]["seq_len"])
        by_len[L] = (len(w), len(w[0]["blocks"]))
    assert by_len == {256: (2, 4), 512: (4, 2)}
