"""The forced-continuation stopper on every task family, with fake token pieces (no tokenizer)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from prod.models.ouro import make_stopper                              # noqa: E402

EOS = 0


def run(stopper, pieces_seq):
    """Feed one piece per token; return (index, reason) of the first firing, or None."""
    pieces = {i + 1: p for i, p in enumerate(pieces_seq)}
    pieces[EOS] = "<eos>"
    tail = ""
    for i, p in enumerate(pieces_seq):
        x = i + 1
        r = stopper(x, tail)
        if r:
            return i, r
        tail = (tail + pieces[x])[-64:]
    return None


def mk(task, seq):
    pieces = {i + 1: p for i, p in enumerate(seq)}
    pieces[EOS] = "<eos>"
    return make_stopper(False, pieces, [EOS], task), seq


def test_letter_answer_fires_on_the_period():
    st, seq = mk("csqa", ["So", " the", " answer", " is", " (", "b", ")", ".", "\n", "\n", "Q", ":"])
    assert run(st, seq) == (7, "answer_sentence")


def test_letter_without_period_fires_on_the_newline():
    st, seq = mk("arc", ["So the answer is", " (C)", "\n", "\n", "Q:"])
    assert run(st, seq) == (2, "answer_sentence")


def test_article_is_not_an_answer():
    st, seq = mk("csqa", ["So the answer is", " a", " rock", ".", "\n\nQ:"])
    assert run(st, seq) == (4, "new_question")


def test_yes_no_and_boolean():
    st, seq = mk("strategyqa", ["So the answer is", " yes", "."])
    assert run(st, seq) == (2, "answer_sentence")
    st, seq = mk("bbh", ["So the answer is", " False", "."])
    assert run(st, seq) == (2, "answer_sentence")


def test_numeric_answer_bbh_arithmetic():
    st, seq = mk("bbh", ["So the answer is", " -", "12", ".", "\n"])
    assert run(st, seq) == (3, "answer_sentence")


def test_aqua_marker():
    st, seq = mk("aqua", ["The answer is", " (", "d", ")", "."])
    assert run(st, seq) == (4, "answer_sentence")


def test_eos_and_new_question_still_stop():
    st, seq = mk("csqa", ["some", " chain"])
    assert st(EOS, "some chain") == "eos"
    st, seq = mk("mmlu", ["no answer here", "\n\nQ:"])
    assert run(st, seq) == (1, "new_question")


def test_svamp_uses_the_gsm8k_rule():
    st, seq = mk("svamp", ["####", " 42", "\n"])
    assert run(st, seq) == (2, "hash_line")


def test_gsm8k_and_math500_unchanged():
    st, seq = mk("gsm8k", ["####", " 18", "\n"])
    assert run(st, seq) == (2, "hash_line")
    st, seq = mk("math500", ["Final", " Answer:", " 3"])
    assert run(st, seq) == (1, "final_answer")


if __name__ == "__main__":
    fs = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for f in fs:
        f()
        print("ok", f.__name__)
    print("%d test functions" % len(fs))
