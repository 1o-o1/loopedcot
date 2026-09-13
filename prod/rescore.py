"""Re-derive `pred`, `correct` and `correct_v2` of stored cells rows from their stored `answer_text`.

  python -m prod.rescore --cells=artifacts [--apply]

Why it exists: rows written before the eos fix carried the eos marker string (e.g. "<|endoftext|>")
inside `pred` for the math and free-form parsers, so "42<|endoftext|>" scored as wrong. Every row
stores the decoded read-out in `answer_text`, so the label can be rebuilt without regenerating.
The own-answer fields (`trace_answer`, `trace_correct`) are untouched: they were parsed from the cut
chain, which never contains the eos.

Dry run by default: prints, per file, how many rows would change. `--apply` rewrites each file
through a temp file and an atomic rename, keeping the `_header` row and every other field.
"""
import argparse
import glob
import json
import os
import re

from .common import read_jsonl
from .tasks import ans_eq, parse_forced, rows as task_rows

RE_SPECIAL = re.compile(r"<\|[^|<>]*\|>")      # <|endoftext|>, <|end_text|>, <|eot_id|>, ...


def clean(text):
    return RE_SPECIAL.sub("", text) if text else text


def rescore_file(path, apply=False):
    lines = open(path, encoding="utf-8").read().split("\n")
    out, changed, total, task, opts = [], 0, 0, None, {}
    for line in lines:
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("_header"):
            out.append(line)
            continue
        if task is None:
            task = r["task"]
            opts = {int(x["idx"]): (x.get("options") or None) for x in task_rows(task)}
        total += 1
        kind = r.get("kind")
        gold = r["gold"]
        pred = parse_forced(clean(r.get("answer_text")), task, opts.get(int(r["row_idx"])), kind)
        correct = bool(ans_eq(pred, gold, task, kind))
        v2 = bool(r["trace_correct"]) if r.get("trace_answer") is not None else correct
        if pred != r.get("pred") or correct != r.get("correct") or v2 != r.get("correct_v2"):
            changed += 1
            r["pred"], r["correct"], r["correct_v2"] = pred, correct, v2
            r["rescored"] = True
        out.append(json.dumps(r, ensure_ascii=False))
    if apply and changed:
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(out) + "\n")
        os.replace(tmp, path)
    return total, changed


def main(argv=None):
    p = argparse.ArgumentParser(prog="prod.rescore")
    p.add_argument("--cells", required=True)
    p.add_argument("--apply", action="store_true")
    a = p.parse_args(argv)
    files = sorted(glob.glob(os.path.join(a.cells, "cells_*.jsonl")))
    grand = [0, 0]
    for f in files:
        total, changed = rescore_file(f, a.apply)
        grand[0] += total
        grand[1] += changed
        if changed:
            print("%-70s %6d rows, %5d %s" % (os.path.basename(f), total, changed,
                                                "rewritten" if a.apply else "would change"))
    print("%d files, %d rows, %d %s" % (len(files), grand[0], grand[1],
                                        "rewritten" if a.apply else "would change"
                                        + (" (dry run; pass --apply)" if grand[1] else "")))


if __name__ == "__main__":
    main()
