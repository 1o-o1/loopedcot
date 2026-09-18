"""The closing think tag as a natural stop, and the switch that stops treating it as one.

For a chat-template Thinking checkpoint `build_prompts` puts `</think>` in `eos_ids`, so the
natural-stop cut lands ON that tag: the chain is cut at the end of the reasoning block and the
answer the model writes AFTER it is discarded. Measured cost: ouro_2_6b_think on GSM8K, natural
k=4, 21.7 against 56.8 forced, with 98 percent of rows cut at the tag.

`think_tag_is_stop` (config, default True) keeps that behaviour, so every grid already generated
stays reproducible. With it False the tag is not a stop: generation runs on to the task's stop
strings or the eos token, the cut rule is the base one, and the own-answer parser reads THROUGH the
tag -- the answer after the reasoning block is the model's own answer.

  python -m pytest tests/test_think_tag_stop.py -q
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prod import config as cfgmod                                    # noqa: E402
from prod import tasks as T                                          # noqa: E402

EOS, END_THINK = 0, 99
# One token per string, so a decoded id list is the concatenation of its pieces.
PIECES = {EOS: "<|eos|>", END_THINK: "</think>", 1: "Half of 8 is 4. ", 2: "So 4 apples.\n",
          3: "The answer is 4. ", 4: "Final Answer: 4", 5: "\n\nQuestion: next one"}
CHAIN = [1, 2, END_THINK, 3, 4, 5]
TAG_AT = CHAIN.index(END_THINK)


class FakeTok(object):
    """Enough tokenizer for `build_prompts` and `make_find_cut`: one piece per id, no vocabulary."""

    eos_token_id = EOS

    def convert_tokens_to_ids(self, s):
        return END_THINK if s == "</think>" else None

    def decode(self, ids, clean_up_tokenization_spaces=True, **kw):
        return "".join(PIECES[int(i)] for i in ids)

    def __call__(self, text, add_special_tokens=False):
        return {"input_ids": [7] * max(1, len(str(text).split()))}

    def apply_chat_template(self, msgs, tokenize=False, add_generation_prompt=True,
                            enable_thinking=True):
        return "<user>%s<assistant>" % msgs[0]["content"]


def cut_at(think_tag_is_stop):
    tok = FakeTok()
    prompts, suf, stops, eos_ids, extra = T.build_prompts(
        tok, "gsm8k", [{"input": "q", "subtask": "gsm8k"}], chat_template=True,
        think_tag_is_stop=think_tag_is_stop)
    find_cut = T.make_find_cut(tok, stops or [], eos_ids, chat_template=True,
                              think_tag_is_stop=think_tag_is_stop)
    return find_cut(CHAIN), stops, eos_ids, extra, suf


def test_the_tag_is_a_stop_by_default_and_the_cut_lands_on_it():
    (cut, marker), stops, eos_ids, extra, suf = cut_at(True)
    assert cut == TAG_AT                       # the reasoning block, and nothing after it
    assert marker == "</think>"
    assert eos_ids == [EOS, END_THINK]
    assert stops is None                       # no stop strings: the tag ends the chain
    assert extra["think_tag_is_stop"] is True
    assert suf[0] == END_THINK                 # the forced read-out still opens with the tag


def test_with_the_switch_off_the_chain_runs_past_the_tag_to_the_task_stop_string():
    (cut, marker), stops, eos_ids, extra, _suf = cut_at(False)
    assert eos_ids == [EOS]                    # the tag is no longer an end of generation
    assert stops == list(T.task_cfg("gsm8k")["stops"])
    assert extra["think_tag_is_stop"] is False
    assert cut > TAG_AT                        # the answer after the block is INSIDE the cut
    assert marker is not None
    text = FakeTok().decode(CHAIN[:cut])
    assert "</think>" in text and "The answer is 4" in text


def test_the_two_settings_disagree_by_the_answer_the_model_wrote_after_the_block():
    (with_stop, _m1), _s, _e, _x, _f = cut_at(True)
    (without, _m2), _s2, _e2, _x2, _f2 = cut_at(False)
    kept = FakeTok().decode(CHAIN[with_stop:without])
    assert "The answer is 4" in kept           # exactly what the default rule throws away


def test_the_own_answer_parser_reads_through_the_tag():
    """The own answer is what the model writes AFTER the reasoning block, so the parser reads there
    first; where nothing after the tag parses, the block is still read, so the switch can never turn
    an answer into no answer."""
    trace = "half of 8 is #### 4 in the block</think>The final line is #### 7"
    assert T.parse_own(trace, "gsm8k", think_tag_is_stop=False) == "7"
    assert T.parse_own(trace, "gsm8k") == "7"                       # the LAST marker either way
    block_only = "half of 8 is #### 4 in the block</think>"
    assert T.parse_own(block_only, "gsm8k", think_tag_is_stop=False) == "4"
    boxed = "we get \\boxed{3} while thinking</think>so \\boxed{5}"
    assert T.parse_own(boxed, "math500", kind="math", think_tag_is_stop=False) == "5"
    # the answer after the tag carries no marker of its own: the block is read rather than nothing
    letters = "So the answer is (A) I think</think>(B)"
    assert T.parse_own(letters, "csqa", ["A", "B"], think_tag_is_stop=False) == "(A)"


def test_the_config_default_keeps_every_generated_grid_reproducible():
    cfg = cfgmod.defaults()
    assert cfg["think_tag_is_stop"] is True
    import argparse
    p = argparse.ArgumentParser()
    cfgmod.add_args(p)
    assert cfgmod.from_args(p.parse_args([]))["think_tag_is_stop"] is True
    assert cfgmod.from_args(p.parse_args(["--no-think-tag-is-stop"]))["think_tag_is_stop"] is False
