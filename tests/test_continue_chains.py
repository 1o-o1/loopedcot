"""`prod.generate --continue-chains=<think_tag|horizon>`: continue a stored natural-stop chain past
its old stop, recompute the cuts and read-outs at every cap, and copy the rest of the old grid.

Everything here runs on CPU with a STUB tokenizer and no checkpoint: what is exercised is the
production code that decides which rows continue, where the continued trace is allowed to stop, what
is copied instead of regenerated, and the three text-level diagnostic fields every row now carries.
NOT exercised: a real decode (no weights in this environment; `tests/test_chains.py` drives the real
injection loop with a scripted model), and `main()`'s own CLI wiring.

  python -m pytest tests/test_continue_chains.py -q
  python tests/test_continue_chains.py
"""
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prod.common import Appender, sha256_text                          # noqa: E402
from prod import manifest as manifest_mod                              # noqa: E402
from prod.generate import (CHAIN_TAIL_CHARS, CONTINUE_MODES, chain_tail_of,   # noqa: E402
                           check_not_overwriting, cont_seed, copy_old_rows, fill_shared_cuts,
                           find_cut_after,
                           iter_jsonl, job_tag, own_answer_span, select_continuation_rows,
                           stop_reason_of)

THINK = "</think>"


# ------------------------------------------------------------------ stub tokenizer
class _Tok(object):
    """Only what the cut rule needs: decode(ids) -> the concatenated pieces."""

    def __init__(self, pieces):
        self.pieces = pieces

    def decode(self, ids, clean_up_tokenization_spaces=True):
        return "".join(self.pieces[int(i)] for i in ids)


#  0:"a" 1:"b" 2:"</think>" 3:"\n\n" 4:"Q:" 5:"<eos>"
PIECES = ["a", "b", THINK, "\n\n", "Q:", "<eos>"]
TOK = _Tok(PIECES)
EOS, TAG = 5, 2


# ------------------------------------------------------------------ mode names
def test_continue_modes_are_exactly_the_two_of_record():
    assert CONTINUE_MODES == ("think_tag", "horizon")


# ------------------------------------------------------------------ selection
def test_select_think_tag_uses_the_old_cells_stop_marker():
    # the chains file records `natural_stop` but NOT which marker stopped the chain, so think_tag
    # selection reads `stop_marker` out of the old cells rows
    chain_stop = {10: 120, 11: 4096, 12: 300}
    cells_marker = {10: THINK, 11: None, 12: "\n\nQ: next"}
    s = select_continuation_rows("think_tag", chain_stop, cells_marker, 4096, think_text=THINK)
    assert s["selected"] == {10: 120}
    assert "stop_marker" in s["field"]
    assert s["n_candidates"] == 1 and s["no_chain"] == []


def test_select_think_tag_candidate_without_a_stored_chain_is_not_selected():
    s = select_continuation_rows("think_tag", {10: 120}, {10: THINK, 13: THINK}, 4096,
                                 think_text=THINK)
    assert s["selected"] == {10: 120} and s["no_chain"] == [13] and s["n_candidates"] == 2


def test_select_horizon_uses_the_chain_natural_stop():
    # missing (None) or >= the old horizon
    chain_stop = {10: 4096, 11: None, 12: 4095, 13: 8000}
    s = select_continuation_rows("horizon", chain_stop, {}, 4096)
    assert sorted(s["selected"]) == [10, 11, 13]
    assert s["selected"][11] == 4096                 # a missing stop is the old horizon
    assert "natural_stop" in s["field"]


def test_select_rejects_an_unknown_mode():
    try:
        select_continuation_rows("halfway", {}, {}, 4096)
    except ValueError:
        return
    raise AssertionError("an unknown --continue-chains mode must raise")


# ------------------------------------------------------------------ the continued cut rule
def test_find_cut_after_ignores_the_think_tag_at_the_boundary():
    """The whole point of the boundary: the tag that STOPPED the old chain sits at the end of
    the replayed prefix, so a cut rule that scans from 0 would re-cut there and the continuation
    would be thrown away."""
    ids = [0, 0, TAG, 0, 1, EOS]           # chain [a,a] + tag, then a,b,<eos>
    cut, mk = find_cut_after(TOK, ids, boundary=3, stop_strings=["\n\nQ:"],
                             stop_ids=[TAG, EOS])
    assert (cut, mk) == (5, "<eos>")       # not 2, and not (len, None)


def test_find_cut_after_takes_the_earliest_of_stop_string_and_stop_token():
    ids = [0, 0, TAG, 0, 3, 4, 1]          # "aa</think>a" + "\n\nQ:" + "b"
    cut, mk = find_cut_after(TOK, ids, boundary=3, stop_strings=["\n\nQ:"], stop_ids=[EOS])
    assert cut == 4                        # the tokens before the stop string's first character
    assert mk.startswith("\n\nQ:")
    # the same ids with an eos BEFORE that stop string: the eos wins
    ids2 = [0, 0, TAG, EOS, 3, 4]
    assert find_cut_after(TOK, ids2, 3, ["\n\nQ:"], [EOS]) == (3, "<eos>")


def test_find_cut_after_ignores_a_stop_string_before_the_boundary():
    ids = [3, 4, 0, TAG, 0, 1]             # the prefix itself contains "\n\nQ:"
    assert find_cut_after(TOK, ids, 4, ["\n\nQ:"], [EOS]) == (6, None)


def test_find_cut_after_returns_the_horizon_when_nothing_stops():
    ids = [0, 1, TAG, 0, 1, 0]
    assert find_cut_after(TOK, ids, 3, ["\n\nQ:"], [EOS]) == (6, None)


# ------------------------------------------------------------------ stop_reason
def test_stop_reason_natural():
    assert stop_reason_of(None, 4096, 4096) == "horizon"
    assert stop_reason_of(None, 0, 0) == "none"                       # the tagged B=0 pass
    assert stop_reason_of("eos", 300, 4096) == "eos"
    assert stop_reason_of(THINK, 300, 4096, think_text=THINK) == "think_tag"
    assert stop_reason_of("<|endoftext|>", 300, 4096, think_text=THINK,
                          eos_texts=["<|endoftext|>", THINK]) == "eos"
    assert stop_reason_of("\n\nQ: what is", 300, 4096,
                          stops=["\n\nQ:", "\nQ:"]) == "stop_string:\n\nQ:"


def test_stop_reason_forced():
    assert stop_reason_of("hash_line", 4096, 4096, forced=True) == "stop_string:hash_line"
    assert stop_reason_of("tok_5", 4096, 4096, forced=True, eos_ids=[5]) == "eos"
    assert stop_reason_of("tok_7", 4096, 4096, forced=True, eos_ids=[5, 7],
                          think_id=7) == "think_tag"
    assert stop_reason_of(None, 4096, 4096, forced=True) == "horizon"


# ------------------------------------------------------------------ chain_tail / own_answer_span
def test_chain_tail_is_the_last_200_characters():
    assert CHAIN_TAIL_CHARS == 200
    txt = "x" * 500 + "TAIL"
    t = chain_tail_of(txt)
    assert len(t) == 200 and t.endswith("TAIL")
    assert chain_tail_of("short") == "short"
    assert chain_tail_of("") == ""


def test_own_answer_span_offsets_the_parsed_answer():
    txt = "blah #### 42\nmore"
    sp = own_answer_span(txt, "42", "####")
    assert sp == [10, 12] and txt[sp[0]:sp[1]] == "42"
    # the LAST marker wins, as parse_own does
    txt2 = "#### 1\nand #### 42\n"
    sp2 = own_answer_span(txt2, "42", "####")
    assert txt2[sp2[0]:sp2[1]] == "42" and sp2[0] > 10


def test_own_answer_span_falls_back_to_the_text_the_parser_read():
    # the parser normalised "1,234" to "1234", so the exact string is not in the text: the span is
    # the region after the last marker, which is what the parser actually read
    txt = "sum #### 1,234\nnext"
    sp = own_answer_span(txt, "1234", "####")
    assert sp == [4, 14] and txt[sp[0]:sp[1]] == "#### 1,234"
    assert own_answer_span(txt, None, "####") is None
    assert own_answer_span("no marker here", "7", "####") is None


# ------------------------------------------------------------------ seeding from the stored chains
def _chain(idx, ids, enc, stop=None):
    return {"idx": idx, "natural_stop": stop, "n_prompt_tokens": len(enc),
            "chain_ids": list(ids), "prompt_sha256": sha256_text(json.dumps(enc)),
            "batch_width": 16}


def test_cont_seed_think_tag_appends_the_tag_and_sets_the_boundary():
    rws = [{"idx": 10}, {"idx": 11}]
    enc = [[1, 2], [3, 4]]
    cur = {0: {"ids": [], "done": False}, 1: {"ids": [], "done": False}}
    cont = {"mode": "think_tag", "selected": {10: 3}, "tag_ids": [TAG],
            "chains": {10: _chain(10, [0, 1, 0], enc[0], 3)}}
    st = cont_seed(cont, rws, enc, cur, horizon=4096)
    assert cur[0]["ids"] == [0, 1, 0, TAG]          # the tag the stored ids omit is put back
    assert cont["boundary"][0] == 4                 # continue AFTER the tag
    assert cur[0]["done"] is False
    assert st["continued"] == [10]
    # row 11 was never selected: it is copied, not generated
    assert cur[1]["done"] is True and cur[1]["ids"] == [] and cur[1]["_copy"] is True
    assert 1 not in cont["boundary"]


def test_cont_seed_does_not_double_append_a_tag_already_in_the_chain():
    rws = [{"idx": 10}]
    enc = [[1, 2]]
    cur = {0: {"ids": [], "done": False}}
    cont = {"mode": "think_tag", "selected": {10: 3}, "tag_ids": [TAG],
            "chains": {10: _chain(10, [0, 1, TAG], enc[0], 3)}}
    cont_seed(cont, rws, enc, cur, horizon=4096)
    assert cur[0]["ids"] == [0, 1, TAG] and cont["boundary"][0] == 3


def test_cont_seed_horizon_mode_replays_the_chain_unchanged():
    rws = [{"idx": 10}]
    enc = [[1, 2]]
    cur = {0: {"ids": [], "done": False}}
    cont = {"mode": "horizon", "selected": {10: 6}, "tag_ids": [],
            "chains": {10: _chain(10, [0, 1, 0, 1, 0, 1], enc[0], 6)}}
    cont_seed(cont, rws, enc, cur, horizon=12)
    assert cur[0]["ids"] == [0, 1, 0, 1, 0, 1] and cont["boundary"][0] == 6
    assert cur[0]["done"] is False


def test_cont_seed_prompt_mismatch_and_missing_chain_fall_back_to_copy():
    rws = [{"idx": 10}, {"idx": 11}]
    enc = [[1, 2], [3, 4]]
    cur = {0: {"ids": [], "done": False}, 1: {"ids": [], "done": False}}
    bad = _chain(10, [0, 1], [9, 9, 9], 2)               # a different prompt
    cont = {"mode": "horizon", "selected": {10: 2, 11: 4}, "tag_ids": [], "chains": {10: bad}}
    st = cont_seed(cont, rws, enc, cur, horizon=4096)
    assert st["prompt_mismatch"] == [10] and st["no_chain"] == [11]
    assert st["continued"] == []
    assert cur[0]["_copy"] is True and cur[1]["_copy"] is True
    assert cont["boundary"] == {}


def test_cont_seed_leaves_a_resumed_trace_alone_but_still_sets_the_boundary():
    rws = [{"idx": 10}]
    enc = [[1, 2]]
    cur = {0: {"ids": [0, 1, 0, TAG, 1, 1], "done": False}}     # a killed continuation job's ids
    cont = {"mode": "think_tag", "selected": {10: 3}, "tag_ids": [TAG],
            "chains": {10: _chain(10, [0, 1, 0], enc[0], 3)}}
    cont_seed(cont, rws, enc, cur, horizon=4096)
    assert cur[0]["ids"] == [0, 1, 0, TAG, 1, 1]      # untouched
    assert cont["boundary"][0] == 4                   # from the chain, not the checkpoint


# ------------------------------------------------------------------ copying the old grid
def _old_cells(path, caps=(0, 16, 64)):
    ap = Appender(path)
    ap.write({"_header": True, "tag": "old", "horizon": 4096})
    for ridx in (10, 11):
        for B in caps:
            ap.write({"idx": ridx - 10, "row_idx": ridx, "B": B, "n_cut": min(16, B),
                      "protocol": "natural", "correct_v2": True, "trace_answer": "42",
                      "answer_text": "x", "natural_stop": 16, "stop_marker": THINK})
    ap.close()
    return path


def test_copy_old_rows_copies_unselected_whole_and_continued_only_below_the_old_stop():
    tmp = tempfile.mkdtemp()
    try:
        old = _old_cells(os.path.join(tmp, "cells_old.jsonl"))
        new = os.path.join(tmp, "cells_new.jsonl")
        ap = Appender(new)
        done = {}
        n_copy, n_skip = copy_old_rows(
            old, ap, idx_of={10: 0, 11: 1}, done=done,
            copy_all={11}, copy_upto={10: 16},
            extra_of=lambda i, ridx, B, row: {"protocol_tag": "natural2",
                                              "continued": ridx in (10,)})
        ap.close()
        assert (n_copy, n_skip) == (5, 1)              # 10: B=0,16 ; 11: all three ; skip 10@64
        rows = [json.loads(ln) for ln in open(new, encoding="utf-8")]
        assert {(r["row_idx"], r["B"]) for r in rows} == {(10, 0), (10, 16), (11, 0), (11, 16),
                                                          (11, 64)}
        assert all(r["protocol_tag"] == "natural2" for r in rows)
        assert all(r["answer_text"] == "x" and r["correct_v2"] is True for r in rows)  # verbatim
        assert {(int(r["idx"]), int(r["B"])) for r in rows} == set(done)
        # the header of the OLD file is never copied into the new one
        assert not any(r.get("_header") for r in rows)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_copy_old_rows_skips_rows_already_written_and_rows_outside_this_job():
    tmp = tempfile.mkdtemp()
    try:
        old = _old_cells(os.path.join(tmp, "cells_old.jsonl"))
        new = os.path.join(tmp, "cells_new.jsonl")
        ap = Appender(new)
        done = {(1, 0): {"already": True}}
        n_copy, _ = copy_old_rows(old, ap, idx_of={11: 1}, done=done, copy_all={11}, copy_upto={},
                                  extra_of=lambda *_a: {})
        ap.close()
        assert n_copy == 2                              # row 10 is not in this job; 11@0 was done
        rows = [json.loads(ln) for ln in open(new, encoding="utf-8")]
        assert {r["B"] for r in rows} == {16, 64} and all(r["idx"] == 1 for r in rows)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_fill_shared_cuts_serves_a_new_cap_from_an_identical_cut():
    tmp = tempfile.mkdtemp()
    try:
        p = os.path.join(tmp, "out.jsonl")
        ap = Appender(p)
        # a copied problem that stopped at 20: its cut is 20 at every cap of 20 or more
        have = {0: {"B": 0, "n_cut": 0, "natural_stop": 20, "pred": "a"},
                16: {"B": 16, "n_cut": 16, "natural_stop": 20, "pred": "b"},
                64: {"B": 64, "n_cut": 20, "natural_stop": 20, "pred": "c"}}
        got = fill_shared_cuts(ap, [0, 16, 64, 128], have, lambda B: False)
        ap.close()
        assert [r["B"] for r in got] == [128]
        assert got[0]["pred"] == "c" and got[0]["n_cut"] == 20 and got[0]["shared_cut_from_B"] == 64
        assert len([x for x in open(p, encoding="utf-8") if x.strip()]) == 1
        # nothing to share when no copied row has that cut
        ap2 = Appender(os.path.join(tmp, "o2.jsonl"))
        assert fill_shared_cuts(ap2, [8], {0: {"B": 0, "n_cut": 0, "natural_stop": 4096}},
                                lambda B: False) == []
        ap2.close()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_iter_jsonl_streams_and_skips_the_header():
    tmp = tempfile.mkdtemp()
    try:
        p = os.path.join(tmp, "x.jsonl")
        with open(p, "w", encoding="utf-8") as f:
            f.write(json.dumps({"_header": True}) + "\n")
            f.write(json.dumps({"a": 1}) + "\n\n")
            f.write('{"truncated": ')                    # a killed writer's last line
        got = list(iter_jsonl(p))
        assert got == [{"a": 1}]
        assert list(iter_jsonl(os.path.join(tmp, "nope.jsonl"))) == []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ------------------------------------------------------------------ the new file is never the old
def test_job_tag_and_the_overwrite_guard():
    t1 = job_tag("ouro_1_4b_think", "gsm8k", "natural", 4)
    t2 = job_tag("ouro_1_4b_think", "gsm8k", "natural2", 4)
    assert t1 == "ouro_1_4b_think_gsm8k_natural_k4" and t2.endswith("natural2_k4")
    assert job_tag("a+b", "t", "natural", 1, "_tagK", "_s0of8") == "a-b_t_natural_k1_tagK_s0of8"
    check_not_overwriting("/art/cells_%s.jsonl" % t2, "/art/cells_%s.jsonl" % t1)
    try:
        check_not_overwriting("/art/cells_%s.jsonl" % t1, "/art/cells_%s.jsonl" % t1)
    except SystemExit:
        return
    raise AssertionError("writing the continuation over its own source must be refused")


# ------------------------------------------------------------------ manifest accepts the new tag
def test_manifest_knows_the_continuation_protocol_tag():
    assert "natural2" in manifest_mod.PROTOCOL_TAGS
    assert manifest_mod.protocol_of_tag("ouro_1_4b_think_gsm8k_natural2_k4") == "natural2"
    assert manifest_mod.protocol_of_tag("ouro_1_4b_think_gsm8k_natural_k4") == "natural"
    assert manifest_mod.protocol_of_tag("ouro_1_4b_base_gsm8k_forced_k2_s0of8") == "forced"
    assert manifest_mod.protocol_of_tag("nonsense") is None
    # the horizon mode's own tag, so both continuations of one (model, task, k) can coexist
    assert manifest_mod.protocol_of_tag("mcleish_llama32_r32_math500_natural2h_k8") == "natural2h"
    assert set(manifest_mod.CONTINUATION_TAGS) == {"natural2", "natural2h"}
    # a continuation job sorts after every natural-stop job and after the forced block
    assert manifest_mod.priority_of("ouro_1_4b_think", "gsm8k", "natural2") > \
        manifest_mod.priority_of("ouro_1_4b_think", "gsm8k", "forced")


def test_manifest_check_lists_a_continuation_file_apart_from_unknown_files():
    tmp = tempfile.mkdtemp()
    try:
        man = {"shard_jobs": [{"tag": "m_gsm8k_natural_k1", "expected_cells": 1}]}
        for name in ("cells_m_gsm8k_natural_k1.jsonl", "cells_m_gsm8k_natural2_k1.jsonl",
                     "cells_junk.jsonl"):
            with open(os.path.join(tmp, name), "w", encoding="utf-8") as f:
                f.write(json.dumps({"idx": 0, "B": 0}) + "\n")
        ck = manifest_mod.check(tmp, man)
        assert [c["tag"] for c in ck["continuation_files"]] == ["m_gsm8k_natural2_k1"]
        assert ck["files_not_in_manifest"] == ["junk"]
        assert ck["counts"]["complete"] == 1 and ck["complete"] is True
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    fs = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for f in fs:
        f()
        print("ok", f.__name__)
    print("%d test functions" % len(fs))


def test_fill_shared_cuts_reads_the_stop_off_the_highest_cap():
    """A source row continued once already: caps copied below the old boundary carry the old stop
    (900), caps regenerated above it carry the final stop (2300). The new horizon cap must be
    shared from the top cap, not looked up by the old stop (which no row's cut equals)."""
    from prod.generate import fill_shared_cuts
    caps_old = [0, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
    rows = {}
    for B in caps_old:
        if B <= 900:
            rows[B] = {"B": B, "n_cut": min(900, B), "natural_stop": 900, "pred": "old"}
        else:
            rows[B] = {"B": B, "n_cut": min(2300, B), "natural_stop": 2300, "pred": "new"}

    class AP:
        def __init__(self):
            self.w = []

        def write(self, r):
            self.w.append(r)

    ap = AP()
    out = fill_shared_cuts(ap, caps_old + [8192], dict(rows), lambda B: False)
    assert [r["B"] for r in out] == [8192]
    assert out[0]["pred"] == "new" and out[0]["shared_cut_from_B"] == 4096
    # a plain row (one stop everywhere) still shares by its identical cut
    plain = {B: {"B": B, "n_cut": min(278, B), "natural_stop": 278, "pred": "p"} for B in caps_old}
    out = fill_shared_cuts(AP(), caps_old + [8192], plain, lambda B: False)
    assert [r["B"] for r in out] == [8192] and out[0]["shared_cut_from_B"] == 512
    # a row that never stopped is not shared: it has to be regenerated
    none = {B: {"B": B, "n_cut": B, "natural_stop": None, "pred": "n"} for B in caps_old}
    assert fill_shared_cuts(AP(), caps_old + [8192], none, lambda B: False) == []


import unittest  # noqa: E402


class TestExtendForcedHorizon(unittest.TestCase):
    """--extend-forced-horizon re-opens a finished forced row only when the horizon grew."""

    def test_reopen_rule(self):
        from prod.generate import reopen_for_longer_horizon as R, build_parser
        fin = {"ids": [1] * 4096, "done": True}
        self.assertFalse(R(fin, 8192, forced=True, extend=True))      # horizon grew: carry on
        self.assertTrue(R(fin, 4096, forced=True, extend=True))       # same horizon: stays done
        self.assertTrue(R(fin, 8192, forced=True, extend=False))      # flag off: untouched
        self.assertTrue(R(fin, 8192, forced=False, extend=True))      # natural rows: untouched
        self.assertFalse(R({"ids": [1] * 10, "done": False}, 8192, forced=True, extend=True))
        a = build_parser().parse_args(["--model", "m", "--task", "gsm8k", "--k", "4",
                                       "--protocol", "forced", "--extend-forced-horizon"])
        self.assertTrue(a.extend_forced_horizon)
        self.assertFalse(build_parser().parse_args(["--model", "m", "--task", "gsm8k", "--k", "4"])
                         .extend_forced_horizon)
