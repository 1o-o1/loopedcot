"""Load checkpoint/task JSONL rows into arrays indexed by loop depth, token cap, and prompt; prices use task answer budgets."""
import glob as _glob
import json
import os
import re
import warnings

import numpy as np

# The depth set and the cap set are read off the rows; these two are only the fallback geometry of
# a model whose whole stack is inside the recurrence with 24 layers, and every other family must
# pin its own (see model_geometry).
L_LOOP_DEFAULT = 24
L_FIXED_DEFAULT = 0

# Reserve the task's answer allowance independently of the generated read-out length.
ANSWER_BUDGET = {"numeric": 8, "math": 32, "letter": 8, "yesno": 8, "boolean": 8, "freeform": 48}
ANSWER_BUDGET_TASK = {"gsm8k": 12}          # numeric, but 12 on GSM8K

# Fallback only: a production row carries its own `kind`, and this table answers for a row that
# does not. A task absent from it must arrive with a `kind` or the load fails loudly.
TASK_KIND = {
    "gsm8k": "numeric", "svamp": "numeric", "math500": "math", "math": "math",
    "aqua": "letter", "csqa": "letter",
    "date_understanding": "letter", "logical_deduction_five_objects": "letter",
    "tracking_shuffled_objects_three_objects": "letter", "sports_understanding": "yesno",
    "causal_judgement": "yesno", "word_sorting": "freeform",
}

BBH_TASKS = ("date_understanding", "logical_deduction_five_objects",
             "tracking_shuffled_objects_three_objects")

EOS_STR = "<|endoftext|>"
RE_PAREN = re.compile(r"\(([A-F])\)")
RE_BARE = re.compile(r"^[^A-Za-z0-9]*([A-F])\b")


def answer_budget(task, kind=None):
    """Return the task/kind answer allowance in tokens, independent of the realised read-out length."""
    if kind is None:
        kind = TASK_KIND.get(task)
    if kind is None:
        raise KeyError("no answer kind for task %r" % task)
    if kind == "numeric" and task in ANSWER_BUDGET_TASK:
        return ANSWER_BUDGET_TASK[task]
    if kind not in ANSWER_BUDGET:
        raise KeyError("unknown answer kind %r" % kind)
    return ANSWER_BUDGET[kind]


# parsing
def strip_eos(t):
    """Return text preceding the first EOS marker, or None for missing input."""
    if t is None:
        return None
    i = t.find(EOS_STR)
    return t if i < 0 else t[:i]


def bbh_parse(text):
    """Return the first parenthesized or leading answer letter from text, or None when no letter parses."""
    t = strip_eos(text)
    if t is None:
        return None
    m = RE_PAREN.search(t)
    if m:
        return "(%s)" % m.group(1)
    m = RE_BARE.match(t)
    if m:
        return "(%s)" % m.group(1)
    return None


def norm_answer(p):
    """Return a normalized numeric/string key from an answer, or None for missing answers; numbers round to six decimals."""
    if p is None or p in ("None", ""):
        return None
    s = str(p).strip().strip("()").strip().lower().replace(",", "")
    try:
        return ("num", round(float(s), 6))
    except ValueError:
        return ("str", s)


def label_v2(r):
    """Return a Boolean correctness label from stored row fields, preferring a parsed own answer inside the token cut."""
    if r.get("correct_v2") is not None:
        return bool(r["correct_v2"] in (True, "True"))
    if r.get("trace_answer") not in (None, "None", ""):
        return bool(r.get("trace_correct") in (True, "True"))
    return bool(r.get("correct") in (True, "True"))


def _f(x, default=np.nan):
    """Return a numeric field as a float, or the supplied default for missing or invalid input; units follow the field."""
    if x is None:
        return default
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


# ---------------------------------------------------------------- reading
def read_rows(path, stats=None):
    """Return cell dictionaries from a JSONL path.

    A leading configuration line (`_header`) is not a cell and is skipped. A line that is not JSON
    is skipped too, but it is COUNTED rather than swallowed: pass a dict as `stats` and it comes
    back with "unparsed", "header" and "rows" totals and an "unparsed_paths" list, so a truncated
    shard shows up instead of quietly shrinking the grid.
    """
    out = []
    if stats is None:
        stats = {}
    for key in ("unparsed", "header", "rows"):
        stats.setdefault(key, 0)
    stats.setdefault("unparsed_paths", [])
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except ValueError:
                stats["unparsed"] += 1
                if path not in stats["unparsed_paths"]:
                    stats["unparsed_paths"].append(path)
                continue
            if isinstance(r, dict) and r.get("_header"):
                stats["header"] += 1
                continue
            stats["rows"] += 1
            out.append(r)
    return out


def dedup(rows):
    """Return the last row for each (loop depth, token cap, prompt ID), excluding non-cell headers."""
    seen = {}
    for r in rows:
        if not isinstance(r, dict) or r.get("_header"):
            continue                 # the production header line is a config, not a cell
        seen[(int(r["k"]), int(r["B"]), int(r["row_idx"] if "row_idx" in r else r["idx"]))] = r
    return list(seen.values())


def bbh_base_rows(rows, task, n_problems=250, n_cal=100, seed=20260908):
    """Return copied letter-task rows with parsed answers, correctness, and seeded calibration/evaluation splits."""
    perm = np.random.RandomState(seed).permutation(n_problems)
    cal = set(int(i) for i in perm[:n_cal])
    out = []
    for r in rows:
        pred = bbh_parse(r.get("answer_text"))
        gold = r.get("gold")
        ok = pred is not None and pred.strip().upper() == str(gold).strip().upper()
        r = dict(r)
        r["split"] = "cal" if int(r["idx"]) in cal else "eval"
        r["pred"], r["correct"] = pred, ok
        r["correct_v2"] = (r.get("trace_correct")
                           if r.get("trace_answer") not in (None, "None", "") else ok)
        r.setdefault("n_answer_tokens", answer_budget(task))
        out.append(r)
    return out


# ---------------------------------------------------------------- the table
def _subset(asked, seen, what, name, task):
    """Return the requested depths or caps sorted, or raise if the rows do not contain them all."""
    asked = sorted(int(x) for x in asked)
    missing = [x for x in asked if x not in seen]
    if missing:
        raise ValueError("%s/%s: no rows at %s %s; the rows hold %s"
                         % (name, task, what, missing, seen))
    return asked


class Cells(object):
    """Store one task/checkpoint as (depth, token cap, prompt) arrays; accuracy is fractional and costs are layer-token passes.

    The depth set and the cap set are whatever the rows contain, so a grid that runs its caps out to
    4096 or its depths out to 32 loads whole. `ks` and `caps` may narrow that to a subset for a
    smaller run; a value the rows do not contain is an error, never an empty row of the table.
    `L` is the layers inside one loop pass and `L_fixed` the layers paid once per token; both must
    match the checkpoint's own shape (see model_geometry) and the defaults suit only a model whose
    whole 24-layer stack is recurrent.
    """

    def __init__(self, rows, task, name="", ks=None, caps=None, L=L_LOOP_DEFAULT,
                 L_fixed=L_FIXED_DEFAULT, require_complete=True):
        rows = [r for r in dedup(rows) if not r.get("extra", False)]
        if not rows:
            raise ValueError("%s/%s: no rows" % (name, task))
        self.task, self.name, self.L, self.L_fixed = task, name, L, L_fixed
        self.read_stats = None
        ks_seen = sorted({int(r["k"]) for r in rows})
        caps_seen = sorted({int(r["B"]) for r in rows})
        self.ks = ks_seen if ks is None else _subset(ks, ks_seen, "depth", name, task)
        self.caps = caps_seen if caps is None else _subset(caps, caps_seen, "token cap", name, task)
        self.idx = sorted({int(r["row_idx"] if "row_idx" in r else r["idx"]) for r in rows})
        ki = {k: i for i, k in enumerate(self.ks)}
        bi = {b: i for i, b in enumerate(self.caps)}
        ni = {n: i for i, n in enumerate(self.idx)}
        self._ki, self._bi, self._ni = ki, bi, ni
        shape = (len(self.ks), len(self.caps), len(self.idx))
        self.acc = np.full(shape, np.nan)
        self.pred = np.empty(shape, dtype=object)
        self.own = np.full(shape, np.nan)
        self.nstop = np.full(shape, np.nan)
        self.ncut = np.full(shape, np.nan)
        self.passes = np.full(shape, np.nan)
        self.passes_pf = np.full(shape, np.nan)
        self.answer_tokens_realised = np.full(shape, np.nan)   # NEVER enters a cost
        self.ptok = np.full(len(self.idx), np.nan)
        self.suffix = np.full(len(self.idx), np.nan)
        self.reserve = np.full(len(self.idx), np.nan)
        self.kind = np.empty(len(self.idx), dtype=object)
        self.split = np.empty(len(self.idx), dtype=object)
        for r in rows:
            k, b = int(r["k"]), int(r["B"])
            if k not in ki or b not in bi:
                continue
            a, c, n = ki[k], bi[b], ni[int(r["row_idx"] if "row_idx" in r else r["idx"])]
            self.acc[a, c, n] = float(label_v2(r))
            pred = r.get("pred")
            if task in BBH_TASKS and pred is None:
                pred = bbh_parse(r.get("answer_text"))
            self.pred[a, c, n] = norm_answer(pred)
            self.own[a, c, n] = float(r.get("trace_answer") not in (None, "None", ""))
            self.nstop[a, c, n] = _f(r.get("natural_stop"))
            self.ncut[a, c, n] = _f(r.get("n_cut"))
            self.answer_tokens_realised[a, c, n] = _f(r.get("n_answer_tokens"))
            p = float(r["n_prompt_tokens"])
            suf = float(r.get("n_suffix_tokens", 0))
            kind = r.get("kind") or TASK_KIND.get(r.get("subtask") or task)
            res = suf + answer_budget(r.get("subtask") or task, kind)
            ngen = _f(r.get("n_generated"), _f(r.get("n_cut"), 0.0)
                      + _f(r.get("n_answer_tokens"), 0.0))
            self.passes[a, c, n] = _f(r.get("layer_passes"),
                                      (L_fixed + k * L) * (p + ngen + suf))
            self.passes_pf[a, c, n] = _f(r.get("layer_passes_promptfree"),
                                         (L_fixed + k * L) * (ngen + suf))
            if not np.isnan(self.reserve[n]) and self.reserve[n] != res:
                raise ValueError("%s/%s: question %d has two reserves (%g and %g): the reserve "
                                 "must not depend on the cell" % (name, task, self.idx[n],
                                                                  self.reserve[n], res))
            if not np.isnan(self.ptok[n]) and (self.ptok[n] != p or self.split[n] != r.get("split", "eval")):
                raise ValueError("prompt tokens and split must not depend on the cell")
            self.ptok[n], self.suffix[n], self.reserve[n] = p, suf, res
            self.kind[n] = kind
            self.split[n] = r.get("split", "eval")
        if require_complete:
            self.assert_complete()

    # ------------------------------------------------------------ completeness
    def missing(self):
        w = np.argwhere(np.isnan(self.acc))
        return [(self.ks[int(a)], self.caps[int(b)], self.idx[int(n)]) for a, b, n in w]

    def assert_complete(self):
        """Raise if any expected (loop depth, token cap, prompt ID) cell lacks an accuracy label."""
        m = self.missing()
        if m:
            raise AssertionError("%s/%s: %d missing cells, first (k=%d, T=%d, id=%d)"
                                 % (self.name, self.task, len(m), m[0][0], m[0][1], m[0][2]))

    # ------------------------------------------------------------ selections
    def select(self, split="eval"):
        """Return zero-based prompt positions belonging to the requested split; all returns every position."""
        if split == "all":
            return np.arange(len(self.idx))
        return np.array([i for i, s in enumerate(self.split) if s == split], dtype=int)

    def ids(self, split="eval"):
        return [self.idx[i] for i in self.select(split)]

    def pos_of(self, ids):
        return np.array([self._ni[int(i)] for i in ids], dtype=int)

    # ------------------------------------------------------------ the reserve
    def answer_budget_used(self):
        """Return answer kinds and their observed task answer allowances, measured in tokens."""
        vals = {}
        for n in range(len(self.idx)):
            vals.setdefault(self.kind[n], set()).add(self.reserve[n] - self.suffix[n])
        if len(vals) == 1:
            (k, v), = vals.items()
            return {"kind": k, "answer_budget": sorted(v)}
        return {kk: sorted(v) for kk, v in vals.items()}

    def reserve_is_constant(self):
        """Return whether every prompt has a defined reserve and the task uses one answer allowance in tokens."""
        ab = self.answer_budget_used()
        one_budget = ("answer_budget" in ab and len(ab["answer_budget"]) == 1)
        return bool(one_budget and not np.isnan(self.reserve).any())


# ---------------------------------------------------------------- directory loading
def cell_paths(cells_dir, task, checkpoint):
    """Return every existing JSONL path holding cells for one task and one checkpoint, sorted.

    Production files are named `cells_<model>_<task>_<protocol>_k<K>[_s<I>of<N>].jsonl`: the model
    comes first and one depth may be split over shards, so EVERY shard of EVERY depth is returned
    and the caller unions their rows. Files whose name marks them a dry run or a smoke test are
    never returned. The older task-first names are kept as a fallback, and the first family of
    names that matches anything wins, so a directory holding one shape is never mixed with another.
    """
    pats = ["cells_%s_%s_*_k*.jsonl" % (checkpoint, task),   # model, task, protocol, depth, shards
            "cells_%s_%s_k*.jsonl" % (checkpoint, task),     # model first, no protocol segment
            "cells_%s_%s_k*.jsonl" % (task, checkpoint),     # task first
            "cells_%s_%s_fixed_k*.jsonl" % (task, checkpoint),
            "cells_%s_%s_*.jsonl" % (task, checkpoint),
            "%s__%s*.jsonl" % (checkpoint, task)]
    for p in pats:
        got = sorted(_glob.glob(os.path.join(cells_dir, p)))
        got = [g for g in got if "dryrun" not in os.path.basename(g)
               and "smoke" not in os.path.basename(g)]
        if got:
            return got
    return []


def load(cells_dir, task, checkpoint, name=None, ks=None, caps=None, bbh_base=False, **kw):
    """Return Cells built from every cell file of one task and checkpoint in `cells_dir`.

    The depth set and the cap set come from the rows themselves; `ks` and `caps` are optional
    SUBSETS of what the rows hold, never a way to introduce a depth or a cap the rows lack.
    `bbh_base` re-parses the answer letter and re-derives the calibration split for a reference file
    of raw multiple-choice rows. Unparseable lines are counted and reported as a warning, and the
    totals are left on the result as `read_stats`.
    """
    paths = cell_paths(cells_dir, task, checkpoint)
    if not paths:
        raise FileNotFoundError("no cell files for %s/%s in %s" % (task, checkpoint, cells_dir))
    rows, stats = [], {}
    for p in paths:
        rows.extend(read_rows(p, stats=stats))
    if stats.get("unparsed"):
        warnings.warn("%s/%s: %d unparseable line(s) skipped in %s"
                      % (task, checkpoint, stats["unparsed"],
                         ", ".join(os.path.basename(x) for x in stats["unparsed_paths"])))
    if bbh_base:
        rows = bbh_base_rows(rows, task)
    cs = Cells(rows, task, name=name or checkpoint, ks=ks, caps=caps, **kw)
    cs.read_stats = dict(stats, files=len(paths))
    return cs


# ---------------------------------------------------------------- model geometry
def read_model_shapes(config_path):
    """Return {model name: {key: int}} for the per-model shape keys of a production config file.

    Reads only the `models:` block and only the four integer keys that fix the cost of a token
    (`layers`, `prelude`, `core`, `coda`), so it needs no YAML library. Two-space indent marks a
    model name, four-space indent marks one of its keys.
    """
    wanted = ("layers", "prelude", "core", "coda")
    out, model, in_models = {}, None, False
    with open(config_path, encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            indent = len(line) - len(line.lstrip(" "))
            if indent == 0:
                in_models = line.split(":")[0].strip() == "models"
                model = None
                continue
            if not in_models:
                continue
            if indent == 2 and line.rstrip().endswith(":"):
                model = line.strip()[:-1]
                out.setdefault(model, {})
            elif indent >= 4 and model is not None and ":" in line:
                key, _, value = line.strip().partition(":")
                if key in wanted:
                    try:
                        out[model][key] = int(value.strip())
                    except ValueError:
                        pass
    return out


def model_geometry(model, config_path):
    """Return (layers_per_loop, fixed_layers) for `model`, both counts of transformer layers.

    A model whose whole stack is recurrent states `layers`, and every layer is inside the loop. A
    model with a fixed prelude and coda around a recurrent core states those three, and then one
    loop pass costs `core` layers while `prelude + coda` layers are paid once per token whatever
    the depth. Raises KeyError when the model is not in the file or states neither shape.
    """
    shapes = read_model_shapes(config_path)
    if model not in shapes:
        raise KeyError("%r is not in %s" % (model, config_path))
    s = shapes[model]
    if "core" in s:
        return int(s["core"]), int(s.get("prelude", 0)) + int(s.get("coda", 0))
    if "layers" in s:
        return int(s["layers"]), 0
    raise KeyError("%r states neither `layers` nor `core` in %s" % (model, config_path))
