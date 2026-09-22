"""Load checkpoint/task JSONL rows into arrays indexed by loop depth, token cap, and prompt; prices use task answer budgets."""
import glob as _glob
import hashlib
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

# ---------------------------------------------------------------- the calibration size (v5)
# The split of record draws the calibration questions as the FIRST `n_cal` of one seeded
# permutation of the dataset's row indices, so a larger `n_cal` keeps every id a smaller one had
# and takes the extra ids off the front of the evaluation split. That nesting is what lets the size
# be a function of N rather than a constant.
#
# v4 fixed it at 100 whatever the grid held. 100 questions put about 5 to 7 points of sampling
# error on the gate's 30-question verification margin, which is the live constraint on every
# deviation; a fifth of the questions keeps that error falling with N without spending so much of
# the grid that the evaluation half stops being worth reading. The ceiling is there because the
# error is already under 3 points at 300 and the questions are worth more in the evaluation half
# after that.
SPLIT_SEED = 20260908
N_CAL_MIN = 100
N_CAL_MAX = 300
N_CAL_FRAC = 0.2

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

# Which answer the settle event is read off (mechanism.commitment reads `Cells.pred`).
#   "scored"  the answer the label of record scores at that cell: the chain's own answer when it
#             wrote one inside the cut, else the forced read-out. Once this answer stops changing
#             the label stops changing, so "the label is constant after the settle cap" holds by
#             construction and the settle-resolved identity is exact on a fully labelled grid.
#   "forced"  the forced read-out alone. The label of record can then still move after the settle
#             cap wherever the chain's own answer differs from the forced read-out: over the 49
#             measured pairs that is 0.4 percent of settled cells, and an identity error above one
#             point on 9 of them.
# `Cells.pred_forced` always keeps the forced read-out, whatever this says.
SETTLE_ANSWER = "scored"
SETTLE_ANSWERS = ("scored", "forced")

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


# ---------------------------------------------------------------- the parsed-file cache
# Every cells file is parsed once and kept as a compressed numpy archive beside it (or under
# `cache_dir`), so a second CLI pass over the same grids reads arrays instead of JSON. The archive
# is keyed by the file's SIZE, its MTIME and the sha256 of its `_header` line: a regenerated or
# extended shard changes at least one of the three, so a stale cache is never read and nothing has
# to be told to rebuild it. Nothing is pickled -- the columns are typed arrays, and a column that is
# not numeric or boolean travels as one JSON blob -- so an archive is safe to read from a shared
# directory and portable between machines.
#: bumped whenever the layout below changes, so an older archive is ignored rather than misread
CACHE_VERSION = 1
CACHE_EXT = ".alloc-cache.npz"
_MISSING = object()


def cache_key(path):
    """Return the identity of a cells file: version, size, mtime and the sha256 of its header line.

    None of the three needs the file's rows read, so validating a cache costs one stat and one line.
    """
    st = os.stat(path)
    with open(path, "rb") as f:
        first = f.readline()
    head = first if b'"_header"' in first[:200] else b"(no header line)"
    return "v%d|%d|%d|%s" % (CACHE_VERSION, st.st_size, st.st_mtime_ns,
                             hashlib.sha256(head).hexdigest())


def cache_path(path, cache_dir=None):
    """Where the parsed form of `path` is cached: beside the file, or under `cache_dir`."""
    return os.path.join(cache_dir or os.path.dirname(os.path.abspath(path)),
                        os.path.basename(path) + CACHE_EXT)


def _encode_rows(rows, unparsed=0):
    """Return the archive entries of a columnar, pickle-free form of `rows`.

    One column per key ever seen, each with its own present and null masks, so a key a row does not
    carry comes back MISSING and a key it carries as null comes back None -- a distinction the
    loader's `_f` fallbacks rely on. A column of bools or ints keeps its Python type through the
    round trip; anything else (a float, a string, a list, mixed types) travels as one JSON blob for
    the whole column, which is one `json.loads` per column instead of one per row.
    """
    names = list({k: None for r in rows for k in r})
    out = {"names": np.array(json.dumps(names)), "n": np.array(len(rows), np.int64),
           "unparsed": np.array(int(unparsed), np.int64)}
    for i, name in enumerate(names):
        vals = [r.get(name, _MISSING) for r in rows]
        real = [v for v in vals if v is not _MISSING and v is not None]
        is_bool = all(isinstance(v, bool) for v in real)
        is_int = (not is_bool) and all(isinstance(v, int) and not isinstance(v, bool)
                                       for v in real)
        if is_bool and real:
            kind = "b"
            data = np.array([v is True for v in vals], bool)
        elif is_int and real:
            kind = "i"
            data = np.array([int(v) if isinstance(v, int) and not isinstance(v, bool) else 0
                             for v in vals], np.int64)
        else:
            kind = "j"
            data = np.array(json.dumps([None if (v is _MISSING or v is None) else v
                                        for v in vals]))
        out["c%d_kind" % i] = np.array(kind)
        out["c%d_present" % i] = np.array([v is not _MISSING for v in vals], bool)
        out["c%d_null" % i] = np.array([v is None for v in vals], bool)
        out["c%d_data" % i] = data
    return out


def _decode_rows(z):
    """Return the rows of an archive written by `_encode_rows`."""
    names = json.loads(str(z["names"]))
    n = int(z["n"])
    rows = [{} for _ in range(n)]
    for i, name in enumerate(names):
        kind = str(z["c%d_kind" % i])
        present = z["c%d_present" % i].tolist()
        null = z["c%d_null" % i].tolist()
        data = z["c%d_data" % i]
        vals = json.loads(str(data)) if kind == "j" else data.tolist()
        if all(present) and not any(null):
            for r, v in zip(rows, vals):                    # the common column: one insert per row
                r[name] = v
        else:
            for r, p, nul, v in zip(rows, present, null, vals):
                if p:
                    r[name] = None if nul else v
    return rows


def write_cache(path, rows, cache_dir=None, unparsed=0):
    """Cache the parsed rows of one cells file; return the archive's path, or None if it could not
    be written (a read-only artifacts directory is not an error, only a slower load)."""
    dest = cache_path(path, cache_dir)
    try:
        os.makedirs(os.path.dirname(os.path.abspath(dest)) or ".", exist_ok=True)
        entries = _encode_rows(rows, unparsed=unparsed)
        entries["key"] = np.array(cache_key(path))
        tmp = dest + ".tmp%d" % os.getpid()
        with open(tmp, "wb") as fh:
            np.savez_compressed(fh, **entries)
        os.replace(tmp, dest)
        return dest
    except OSError:
        return None


def read_cache(path, cache_dir=None, stats=None):
    """Return the cached rows of one cells file, or None when there is no archive for its current
    size, mtime and header. A damaged archive is treated as no archive."""
    dest = cache_path(path, cache_dir)
    if not os.path.exists(dest):
        return None
    try:
        with np.load(dest, allow_pickle=False) as z:
            if str(z["key"]) != cache_key(path):
                return None
            rows = _decode_rows(z)
            if stats is not None:
                n_bad = int(z["unparsed"]) if "unparsed" in z.files else 0
                stats["rows"] = stats.get("rows", 0) + len(rows)
                stats["header"] = stats.get("header", 0) + 1
                stats["unparsed"] = stats.get("unparsed", 0) + n_bad
                stats.setdefault("unparsed_paths", [])
                if n_bad and path not in stats["unparsed_paths"]:
                    stats["unparsed_paths"].append(path)
                stats["cached_files"] = stats.get("cached_files", 0) + 1
            return rows
    except (OSError, ValueError, KeyError, EOFError):
        return None


def cached_rows(path, stats=None, cache_dir=None, cache=True):
    """Return one cells file's rows, from its cache when that is current, parsing it otherwise.

    `cache=False` neither reads nor writes an archive, which is what `--no-cache` is for: the parse
    is the ground truth and the cache must always be able to be taken out of the picture.
    """
    if not cache:
        return read_rows(path, stats=stats)
    got = read_cache(path, cache_dir, stats=stats)
    if got is not None:
        return got
    own = {}
    rows = read_rows(path, stats=own)
    write_cache(path, rows, cache_dir, unparsed=own.get("unparsed", 0))
    if stats is not None:
        for key in ("unparsed", "header", "rows"):
            stats[key] = stats.get(key, 0) + own.get(key, 0)
        stats.setdefault("unparsed_paths", [])
        for p in own.get("unparsed_paths", []):
            if p not in stats["unparsed_paths"]:
                stats["unparsed_paths"].append(p)
        stats.setdefault("cached_files", 0)
    return rows


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
        if SETTLE_ANSWER not in SETTLE_ANSWERS:
            raise ValueError("SETTLE_ANSWER must be one of %s, got %r"
                             % (", ".join(SETTLE_ANSWERS), SETTLE_ANSWER))
        self.settle_answer = SETTLE_ANSWER
        self.pred = np.empty(shape, dtype=object)          # the answer the settle event reads
        self.pred_forced = np.empty(shape, dtype=object)   # the forced read-out, always
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
        # The stratification field of a POOLED grid (BBH's ten subtasks). It never enters a price
        # or a label; it is read only by `seeded_ranks`, to keep the calibration split spread over
        # the subtasks when evaluation ids are promoted into it.
        self.subtask = np.empty(len(self.idx), dtype=object)
        self.header = None
        for r in rows:
            k, b = int(r["k"]), int(r["B"])
            if k not in ki or b not in bi:
                continue
            a, c, n = ki[k], bi[b], ni[int(r["row_idx"] if "row_idx" in r else r["idx"])]
            self.acc[a, c, n] = float(label_v2(r))
            pred = r.get("pred")
            if task in BBH_TASKS and pred is None:
                pred = bbh_parse(r.get("answer_text"))
            own_answer = r.get("trace_answer")
            has_own = own_answer not in (None, "None", "")
            self.pred_forced[a, c, n] = norm_answer(pred)
            self.pred[a, c, n] = (norm_answer(own_answer) if has_own and SETTLE_ANSWER == "scored"
                                  else self.pred_forced[a, c, n])
            self.own[a, c, n] = float(has_own)
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
            self.subtask[n] = r.get("subtask")
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


# ---------------------------------------------------------------- the calibration size (v5)
def n_cal_for(n_questions, n_cal=None):
    """Return how many questions calibrate a grid of `n_questions`, or the explicit override.

        n_cal = max(N_CAL_MIN, min(N_CAL_MAX, floor(N_CAL_FRAC * N)))

    A fifth of the questions, never fewer than 100 and never more than 300. At N = 400, the size of
    the production grids here, the floor binds and the rule returns the 100 that v4 used, so
    nothing about those grids changes by the rule alone; the size only starts to move at N = 500.
    """
    if n_cal is not None:
        if int(n_cal) < 1:
            raise ValueError("n_cal must be at least 1, got %r" % (n_cal,))
        return int(n_cal)
    n = int(n_questions)
    if n < 1:
        raise ValueError("a grid of %d questions has no calibration split" % n)
    return int(max(N_CAL_MIN, min(N_CAL_MAX, int(N_CAL_FRAC * n))))


def resolve_n_cal(cells, n_cal=None):
    """Return (the calibration size this grid will use, why).

    An EXPLICIT `n_cal` is honoured as asked; `promote_calibration` refuses one the grid cannot
    hold. The RULE is clipped instead: a grid too small to carry it -- one where the 100 floor would
    take more than half the questions -- keeps the split its rows arrived with, because sizing
    calibration is not a licence to eat the evaluation half. That never binds on a production grid,
    where a fifth of the questions is by construction at most half of them.
    """
    n = int(len(cells.idx))
    cal_now = int(len(cells.select("cal")))
    if n_cal is not None:
        return n_cal_for(n, n_cal), "explicit"
    target = n_cal_for(n)
    if target > n // 2:
        return cal_now, "grid too small for the rule; the split the rows carry is kept"
    return max(target, cal_now), "rule"


def dataset_size(cells, task=None):
    """Return the size of the DATASET the grid was sub-sampled from, or the grid's own size.

    A production grid carries its config on a `_header` line whose `datasets` map holds the row
    count of every task, and that count is what the split permutation was drawn over. A grid
    without one answers with the number of questions it holds.
    """
    hdr = getattr(cells, "header", None) or {}
    cfg = hdr.get("config") or {}
    sizes = cfg.get("datasets") or {}
    n = sizes.get(task or cells.task)
    return int(n) if n else int(len(cells.idx))


def seeded_ranks(cells, seed=SPLIT_SEED, n_dataset=None):
    """Return ({question id: rank in the dataset's seeded order}, how that order was obtained).

    The split of record is one permutation of the dataset's row indices under
    `numpy.random.default_rng(seed)`, the first `n_cal` of which calibrate. Rebuilding that
    permutation from the seed and the dataset size reproduces the order exactly, and the rebuild is
    CHECKED against the split the rows already carry: if the first `len(cal)` entries of the
    permutation are the grid's own calibration ids, the order is confirmed and `order_source` reads
    `seeded_permutation`.

    Two shapes cannot confirm. A task whose calibration rows are drawn STRATIFIED over a field (the
    pooled BBH grid, ten rows per subtask) has an order this module cannot rebuild, because the
    per-group draws come from a dataset it never sees; what is used there is a round-robin over the
    subtasks in sorted order, which keeps the stratification the production draw has, and
    `order_source` reads `stratified_emulated`. A grid with neither a confirmed permutation nor a
    subtask field falls back to ascending id order, `id_order`.

    Only the order in which EVALUATION ids are promoted depends on this, never which ids already
    calibrate: promotion adds and never removes (see promote_calibration).
    """
    ids = [int(i) for i in cells.idx]
    n = int(n_dataset) if n_dataset is not None else dataset_size(cells)
    cal_now = set(int(cells.idx[int(p)]) for p in cells.select("cal"))
    perm = np.random.default_rng(int(seed)).permutation(max(n, (max(ids) + 1) if ids else 1))
    flat = {int(v): r for r, v in enumerate(perm)}
    if cal_now and set(int(v) for v in perm[:len(cal_now)]) == cal_now:
        return {i: flat[i] for i in ids}, "seeded_permutation"

    groups = {}
    for pos, i in enumerate(ids):
        groups.setdefault(cells.subtask[pos], []).append(i)
    if len(groups) > 1:
        keys = sorted(groups, key=lambda x: (x is None, str(x)))
        ranks = {}
        for gi, gk in enumerate(keys):
            for within, i in enumerate(sorted(groups[gk], key=lambda v: flat[v])):
                ranks[i] = within * len(keys) + gi
        return ranks, "stratified_emulated"
    return {i: r for r, i in enumerate(sorted(ids))}, "id_order"


def promote_calibration(cells, n_cal, seed=SPLIT_SEED, n_dataset=None):
    """Return (a copy of `cells` whose calibration split holds `n_cal` questions, a record).

    Promotion only ever ADDS: every id already calibrating stays calibrating, and the shortfall is
    taken from the front of the evaluation split in the dataset's seeded order, so the evaluation
    split shrinks by exactly as many questions as calibration gains. Asking for no more than the
    grid already has is a no-op, and asking for more than the grid holds is an error rather than a
    silently smaller split.

    The source grid is left untouched: the copy carries its own `split` array and shares everything
    else, which is read-only once loaded.
    """
    from copy import copy as _copy
    want = int(n_cal)
    cal, ev = cells.select("cal"), cells.select("eval")
    if want > len(cal) + len(ev):
        raise ValueError("%s/%s: cannot calibrate on %d of %d questions"
                         % (cells.name, cells.task, want, len(cal) + len(ev)))
    ranks, source = seeded_ranks(cells, seed=seed, n_dataset=n_dataset)
    need = max(0, want - len(cal))
    order = sorted((int(p) for p in ev),
                   key=lambda p: (ranks[int(cells.idx[p])], int(cells.idx[p])))
    promoted = order[:need]
    out = _copy(cells)
    out.split = np.array(cells.split, dtype=object)
    for p in promoted:
        out.split[p] = "cal"
    return out, {"n_cal_before": int(len(cal)), "n_cal_after": int(len(cal) + need),
                 "n_eval_before": int(len(ev)), "n_eval_after": int(len(ev) - need),
                 "n_promoted": int(need), "requested": want, "order_source": source,
                 "seed": int(seed),
                 "n_dataset": int(n_dataset if n_dataset is not None else dataset_size(cells)),
                 "promoted_ids": [int(cells.idx[p]) for p in promoted]}


# ---------------------------------------------------------------- directory loading
def cell_paths(cells_dir, task, checkpoint, protocol="natural"):
    """Return every existing JSONL path holding cells for one task and one checkpoint, sorted.

    Only the `protocol` grid (natural stop by default): a forced-continuation grid of the same
    checkpoint and task shares every (depth, cap, question) key and must never be unioned with it.

    Production files are named `cells_<model>_<task>_<protocol>_k<K>[_s<I>of<N>].jsonl`: the model
    comes first and one depth may be split over shards, so EVERY shard of EVERY depth is returned
    and the caller unions their rows. Files whose name marks them a dry run or a smoke test are
    never returned. The older task-first names are kept as a fallback, and the first family of
    names that matches anything wins, so a directory holding one shape is never mixed with another.
    """
    pats = ["cells_%s_%s_%s_k*.jsonl" % (checkpoint, task, protocol),   # model, task, protocol, depth, shards
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


def load(cells_dir, task, checkpoint, name=None, ks=None, caps=None, bbh_base=False,
         protocol="natural", cache=True, cache_dir=None, **kw):
    """Return Cells built from every cell file of one task and checkpoint in `cells_dir`.

    The depth set and the cap set come from the rows themselves; `ks` and `caps` are optional
    SUBSETS of what the rows hold, never a way to introduce a depth or a cap the rows lack.
    `bbh_base` re-parses the answer letter and re-derives the calibration split for a reference file
    of raw multiple-choice rows. Unparseable lines are counted and reported as a warning, and the
    totals are left on the result as `read_stats`, with `cached_files` saying how many of the files
    were read from their cache.

    `cache` (on) reads and writes the per-file archives described above; `cache_dir` puts them
    somewhere other than beside the cells files. `cache=False` parses every time, which is the
    ground truth the cache is tested against.
    """
    paths = cell_paths(cells_dir, task, checkpoint, protocol)
    if not paths:
        raise FileNotFoundError("no cell files for %s/%s in %s" % (task, checkpoint, cells_dir))
    rows, stats = [], {}
    for p in paths:
        rows.extend(cached_rows(p, stats=stats, cache_dir=cache_dir, cache=cache))
    header = read_header(paths[0])
    if stats.get("unparsed"):
        warnings.warn("%s/%s: %d unparseable line(s) skipped in %s"
                      % (task, checkpoint, stats["unparsed"],
                         ", ".join(os.path.basename(x) for x in stats["unparsed_paths"])))
    if bbh_base:
        rows = bbh_base_rows(rows, task)
    cs = Cells(rows, task, name=name or checkpoint, ks=ks, caps=caps, **kw)
    cs.read_stats = dict(stats, files=len(paths))
    cs.header = header
    return cs


def read_header(path):
    """Return the `_header` configuration line of a cell file, or None when it has none.

    Only the first line is read. The header is not a cell and never enters a price or a label; it
    is kept so `dataset_size` can say how many rows the grid was sub-sampled FROM, which is the
    number the split permutation was drawn over.
    """
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except ValueError:
                return None
            return r if isinstance(r, dict) and r.get("_header") else None
    return None


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


# ---------------------------------------------------------------- realised chain lengths
def natural_stop_cap_index(cells):
    """Return the index of the cap that stands for natural stop.

    A grid may mark "no cap at all" with a negative cap; that marker is natural stop outright.
    Otherwise the largest measured cap stands for it: a chain is either finished by then or is at
    the horizon, which is exactly how `evaluate.default_cost` counts the same prompts.
    """
    nocap = [i for i, T in enumerate(cells.caps) if T < 0]
    return nocap[0] if nocap else len(cells.caps) - 1


def cap_limits(cells):
    """Return each cap as a token limit; a negative cap marks "no cap" and limits nothing."""
    return np.array([np.inf if T < 0 else float(T) for T in cells.caps])


def natural_lengths(cells, pos=None):
    """Return the (depth, prompt) generated chain length in tokens when the chain is not cut.

    Read from `natural_stop` at the cap that stands for natural stop, falling back to that cap's
    `n_cut` and then to the largest `n_cut` measured at that depth. A chain that never stops inside
    the grid is counted at the horizon rather than dropped, so the table below and the default cost
    treat those prompts alike.
    """
    pos = np.arange(len(cells.idx)) if pos is None else np.asarray(pos, dtype=int)
    j = natural_stop_cap_index(cells)
    horizon = cap_limits(cells)[j]
    out = np.full((len(cells.ks), len(pos)), np.nan)
    for a in range(len(cells.ks)):
        for ii, n in enumerate(pos):
            v = cells.nstop[a, j, n]
            if np.isnan(v):
                v = cells.ncut[a, j, n]
            if np.isnan(v):
                row = cells.ncut[a, :, n]
                v = np.nanmax(row) if np.isfinite(row).any() else np.nan
            out[a, ii] = min(v, horizon) if not np.isnan(v) else np.nan
    return out


def expected_lengths(cells, pos=None):
    """Return the (depth, cap) table E_cal[min(len_k, T)] in tokens.

    `len_k` is the prompt's own generated length at depth k run to its natural stop, and the mean
    is over the CALIBRATION prompts only, so the number is known before any evaluation prompt is
    generated. The evaluation prompt's own realised length never enters its price: that length is
    not known at decision time, and using it would price a cell with the answer it is buying.
    The largest cap (or an explicit no-cap marker) stands for natural stop, so the table's last
    column is the mean natural length itself.
    """
    if pos is None:
        pos = cells.select("cal")
    pos = np.asarray(pos, dtype=int)
    if not len(pos):
        raise ValueError("%s/%s: the expected-length table needs calibration prompts"
                         % (cells.name, cells.task))
    if any(cells.split[n] != "cal" for n in pos):
        raise ValueError("the expected-length table is a calibration statistic: "
                         "evaluation prompts must not enter it")
    lens = natural_lengths(cells, pos)
    lim = cap_limits(cells)
    out = np.full((len(cells.ks), len(cells.caps)), np.nan)
    for a in range(len(cells.ks)):
        row = lens[a][np.isfinite(lens[a])]
        if not len(row):
            continue
        for c, T in enumerate(lim):
            out[a, c] = float(np.minimum(row, T).mean())
    return out
