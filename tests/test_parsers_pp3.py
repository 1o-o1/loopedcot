"""Parser unit cases for the four PP3 evaluation sets.

Twenty cases each for StrategyQA, pooled BBH, MMLU and HellaSwag, over the forced read-out parse
(`parse_forced`), the own-answer parse inside a cut trace (`parse_own`) and the equality rule
(`ans_eq`). Every string here is the shape a checkpoint actually emits after the task's forced
suffix ("So the answer is"), including the failure shapes: an empty read-out, a read-out that starts
a new question, a letter with no parentheses, a yes/no inside a sentence.

  python -m pytest tests/test_parsers_pp3.py -q
  python tests/test_parsers_pp3.py                 # no pytest needed
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prod.tasks import ans_eq, parse_forced, parse_own, row_kind, rows, task_cfg   # noqa: E402

Y = "strategyqa"
B = "bbh"
M = "mmlu"
H = "hellaswag"


# ------------------------------------------------------------------ StrategyQA (yes/no)
STRATEGYQA = [
    (" yes.", "yes", True), (" no.", "no", True), (" Yes.", "yes", True), (" No.", "no", True),
    (" yes", "yes", True), (" no", "no", True),
    (" yes.\nQ: Is the sky blue?", "yes", True),
    (" The answer is no.", "no", True),
    (" no, because the Colosseum predates it.", "no", True),
    (" YES.", "yes", True),
    (" yes.", "no", False), (" no.", "yes", False),
    ("", None, False), ("   ", None, False),
    (" maybe.", None, False),
    (" 42", None, False),
    (" (A)", None, False),
    (" Yes", "Yes", True),                    # gold casing is irrelevant: ans_eq lowercases
    (" no.\n\nQ: next question", "no", True),
    (" It is yes and no.", "yes", True),      # first match wins, the S26 rule
]


def test_strategyqa():
    assert len(STRATEGYQA) == 20
    for text, gold, want in STRATEGYQA:
        p = parse_forced(text, Y)
        assert bool(ans_eq(p, gold, Y)) is want, (text, gold, p)
    # the own-answer parse reads AFTER the last own marker inside the cut
    assert parse_own("...so it is old. So the answer is no.", Y) == "no"
    assert parse_own("no marker here", Y) is None


# ------------------------------------------------------------------ pooled BBH (five kinds)
BBH = [
    # letter (date_understanding, logical_deduction, tracking, temporal_sequences)
    (" (B).", "(B)", "letter", True),
    (" (B)", "B", "letter", True),
    (" B.", "(B)", "letter", True),
    (" (F).", "(B)", "letter", False),
    (" (b).", "(B)", "letter", True),
    ("", "(B)", "letter", False),
    (" the answer is (D), because", "(D)", "letter", True),
    # yesno (sports_understanding, navigate, causal_judgement). BBH writes Yes/No capitalised on
    # navigate and causal_judgement and lowercase on sports_understanding; ans_eq lowercases both.
    (" yes.", "Yes", "yesno", True),
    (" No.", "no", "yesno", True),
    (" yes.", "No", "yesno", False),
    (" Probably not.", None, "yesno", False),
    # boolean (boolean_expressions)
    (" False.", "False", "boolean", True),
    (" True.", "True", "boolean", True),
    (" true", "True", "boolean", True),
    (" False.", "True", "boolean", False),
    (" (A)", "True", "boolean", False),
    # numeric (multistep_arithmetic_two)
    (" -70.", "-70", "numeric", True),
    (" 1,024", "1024", "numeric", True),
    # freeform (word_sorting)
    (" arrest burglar cadaver.", "arrest burglar cadaver", "freeform", True),
    (" arrest  burglar   cadaver", "arrest burglar cadaver", "freeform", True),
]


def test_bbh():
    assert len(BBH) == 20
    for text, gold, kind, want in BBH:
        p = parse_forced(text, B, None, kind)
        assert bool(ans_eq(p, gold, B, kind)) is want, (text, gold, kind, p)


def test_bbh_rows_carry_their_kind():
    """Every pooled row names its own kind and its own exemplar file."""
    ks = {row_kind(B, r) for r in rows(B)}
    assert ks == {"letter", "yesno", "boolean", "numeric", "freeform"}
    assert task_cfg(B)["per_row_kind"] and task_cfg(B)["per_row_prefix"]
    assert all(r.get("prefix_key", "").startswith("bbh_") for r in rows(B))
    assert all(r.get("subtask") for r in rows(B))


# ------------------------------------------------------------------ MMLU (letter A-D)
MMLU = [
    (" (C).", "C", True), (" (c).", "C", True), (" C.", "C", True), (" (C)", "C", True),
    (" (A).", "C", False), (" (D).", "D", True), (" (B).", "B", True),
    (" the answer is (A).", "A", True),
    (" (C).\n\nQ: next", "C", True),
    ("", "C", False), ("   ", "C", False),
    (" I do not know.", "C", False),
    (" 3", "C", False),
    (" (E).", "C", False),                    # E is not an MMLU option, and it is not C
    (" (A)", "A", True),
    (" A", "A", True),
    (" (D) 42", "D", True),
    (" answer: (B)", "B", True),
    (" (b)", "B", True),
    (" yes", "C", False),
]


def test_mmlu():
    assert len(MMLU) == 20
    for text, gold, want in MMLU:
        p = parse_forced(text, M, ["A", "B", "C", "D"])
        assert bool(ans_eq(p, gold, M)) is want, (text, gold, p)
    assert parse_own("... So the answer is (C).", M, ["A", "B", "C", "D"]) == "(C)"


# ------------------------------------------------------------------ HellaSwag (letter A-D)
HELLASWAG = [
    (" (D).", "D", True), (" (d).", "D", True), (" D.", "D", True), (" (D)", "D", True),
    (" (A).", "D", False), (" (B).", "B", True), (" (C).", "C", True),
    (" ending (A) is most plausible.", "A", True),
    (" (D).\nQ: ", "D", True),
    ("", "D", False), ("  ", "D", False),
    (" none of them", "D", False),
    (" the man", "D", False),
    (" (A)", "A", True), (" (B)", "B", True), (" (C)", "C", True),
    (" B", "B", True),
    (" answer (C)", "C", True),
    (" (a)", "A", True),
    (" 2", "D", False),
]


def test_hellaswag():
    assert len(HELLASWAG) == 20
    for text, gold, want in HELLASWAG:
        p = parse_forced(text, H, ["A", "B", "C", "D"])
        assert bool(ans_eq(p, gold, H)) is want, (text, gold, p)


# ------------------------------------------------------------------ the data files themselves
def test_row_counts():
    from prod import config as cfgmod
    for t in (Y, B, M, H):
        assert len(rows(t)) == cfgmod.DATASETS[t], t
        for i, r in enumerate(rows(t)):
            assert int(r["idx"]) == i, (t, i, r["idx"])
            assert str(r["input"]).strip() and str(r["target"]).strip(), (t, i)


if __name__ == "__main__":
    fs = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for f in fs:
        f()
        print("ok", f.__name__)
    print("%d test functions, %d parser cases"
          % (len(fs), len(STRATEGYQA) + len(BBH) + len(MMLU) + len(HELLASWAG)))
