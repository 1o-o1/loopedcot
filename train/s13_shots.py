"""Verbatim copy of s13_common.math_shots and its last_boxed dependency (S13 is read-only).
Used only by the MATH500 stage, to keep the S13 few-shot prefix byte-identical."""
import re

RE_BOXED = re.compile(r"\\boxed\s*{")


def last_boxed(s):
    if s is None:
        return None
    ms = list(RE_BOXED.finditer(s))
    if not ms:
        return None
    i = ms[-1].end()
    depth, out = 1, []
    while i < len(s) and depth:
        c = s[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                break
        out.append(c)
        i += 1
    return "".join(out).strip() or None


def math500(lo=0, hi=None):
    from datasets import load_dataset
    d = load_dataset("HuggingFaceH4/MATH-500", split="test")
    hi = len(d) if hi is None else min(hi, len(d))
    return [{"pid": i, "q": d[i]["problem"], "gold": d[i]["answer"],
             "solution": d[i]["solution"]} for i in range(lo, hi)]


def math_shots(n=4):
    """S13 verbatim: four fixed shots from a MATH TRAIN split, in the S3 layout."""
    from datasets import load_dataset
    for cand, cfg in [("EleutherAI/hendrycks_math", "algebra"),
                      ("nlile/hendrycks-MATH-benchmark", None)]:
        try:
            d = load_dataset(cand, cfg, split="train") if cfg else load_dataset(cand, split="train")
            cols = d.column_names
            pk = "problem" if "problem" in cols else cols[0]
            sk = "solution" if "solution" in cols else cols[1]
            rows = [{"p": d[i][pk], "s": d[i][sk], "a": last_boxed(d[i][sk])} for i in range(64)]
            rows = [r for r in rows if r["a"] and len(r["s"]) < 900][:n]
            if len(rows) == n:
                return rows, {"source": cand, "config": cfg, "excluded_test_idx": []}
        except Exception:
            continue
    d = math500()
    rows = [{"p": d[i]["q"], "s": d[i]["solution"], "a": d[i]["gold"]}
            for i in range(len(d) - n, len(d))]
    return rows, {"source": "MATH-500 test tail (no train split reachable)", "config": None,
                  "excluded_test_idx": list(range(len(d) - n, len(d)))}
