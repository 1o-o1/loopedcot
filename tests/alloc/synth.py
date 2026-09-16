"""Synthetic cell rows with a planted optimum. No model, no real data, CPU, numpy only."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alloc import cells as C          # noqa: E402

KS = [1, 2, 3, 4]
CAPS = [0, 16, 32, 64, 128, 256, 512]

# The plant: depth 3 settles at cap 64 and is right 90% of the time once settled; the other depths
# settle later and are worse. The best cell is therefore (k=3, T=64) -- the cheapest cell on the
# accuracy plateau, which is what both rankings must return first.
ARRIVE = {1: 512, 2: 256, 3: 64, 4: 128}
P_RIGHT = {1: 0.2, 2: 0.5, 3: 0.9, 4: 0.6}
PLANTED = (3, 64)


def rows(n=120, task="gsm8k", n_cal=40, production=False, suffix=4, realised_answer=3,
         idx_offset=0, kind=None):
    """`production=True` writes the production shape: a `_header` line, `row_idx`, `kind`,
    `subtask`, and a `n_answer_tokens` that holds the RESERVE; the spike shape holds the REALISED
    read-out length there instead. The loader must ignore both."""
    out = []
    if production:
        out.append({"_header": True, "version": "PP3", "task": task, "n_answer_tokens": 99})
    for i in range(n):
        qid = i + idx_offset
        ptok = 600 + (i % 7)
        for k in KS:
            right = (i % 10) < int(round(10 * P_RIGHT[k]))
            for T in CAPS:
                settled = T >= ARRIVE[k]
                pred = ("%d" % (100 + k) if (settled and right)
                        else ("%d" % (200 + k) if settled else "%d" % (300 + k + T)))
                gold = "%d" % (100 + k) if right else "%d" % (900 + k)
                ok = settled and right
                r = {"idx": qid, "k": k, "B": T, "split": "cal" if i < n_cal else "eval",
                     "task": task, "correct": ok, "correct_v2": ok, "pred": pred, "gold": gold,
                     "trace_answer": None, "trace_correct": False,
                     "n_cut": min(T, 40), "natural_stop": 40, "n_generated": min(T, 40) + 3,
                     "n_prompt_tokens": ptok, "n_suffix_tokens": suffix}
                if production:
                    r["row_idx"] = qid
                    r["kind"] = kind or C.TASK_KIND[task]
                    r["subtask"] = task
                    r["n_answer_tokens"] = C.answer_budget(task)          # the reserve
                else:
                    r["n_answer_tokens"] = realised_answer                # the realised read-out
                out.append(r)
    return out


def cells(n=120, task="gsm8k", **kw):
    return C.Cells(rows(n=n, task=task, **kw), task, name="synthetic",
                   ks=KS, caps=CAPS)
