"""Scoring: both parses, protocol v2, the commitment arrival event, and the cell tables.

  python -m prod.score --cells=artifacts --model=ouro_1_4b_base --task=gsm8k [--protocol=natural]
                       [--label=v2|forced|own] [--split=eval|cal|all] [--out=FILE]

Definitions:
  * protocol v2: the model's own answer if it parses inside the cut, else the forced read-out.
    Computed from stored fields only, never by re-parsing text.
  * the answer-arrival event is COMMITMENT: a question has arrived at cap T_j if the forced
    read-out at every cap >= T_j equals the read-out at the largest cap, after the task's own
    normalisation; no gold label, no answer-string search in the chain.
  * the allocator never uses the arrival event.
"""
import argparse
import glob
import os
import re

import numpy as np

from .common import CAPS_STANDARD, read_jsonl, save_json


# ------------------------------------------------------------------ labels
def label_v2(r):
    """s32_common.score_v2 / generate.score_v2, from stored fields."""
    if "correct_v2" in r:
        return bool(r["correct_v2"] in (True, "True"))
    if r.get("trace_answer") not in (None, "None", ""):
        return bool(r.get("trace_correct") in (True, "True"))
    return bool(r.get("correct") in (True, "True"))


def label_of(r, which):
    if which == "v2":
        return label_v2(r)
    if which == "forced":
        return bool(r.get("correct") in (True, "True"))
    if which == "own":
        return bool(r.get("trace_correct") in (True, "True"))
    raise ValueError(which)


def _f(x, default=np.nan):
    """float() that tolerates a missing or null field: older spike rows omit some of them."""
    if x is None:
        return default
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


def norm_answer(p):
    """v4_commitment.norm, verbatim: a number if it parses as one, else a lowercased string with
    brackets and commas stripped. A parse failure (None) never equals anything."""
    if p is None or p in ("None", ""):
        return None
    s = str(p).strip().strip("()").strip().lower().replace(",", "")
    try:
        return ("num", round(float(s), 6))
    except ValueError:
        return ("str", s)


# ------------------------------------------------------------------ loading
# `generate.py` builds a cells filename as cells_<model>_<task>_<protocol>_k<k><tag><shard>.jsonl
# with tag in {"", "_tagK", "_tagT"} (an arm whose prompt carries a control line) and shard in
# {"", "_s<i>of<n>", "_sub<N>", "_s<i>of<n>_sub<N>"} ("_sub<N>" is an --only-rows subset). Only the
# shards of one tag are a UNION of the same grid; a _tagK arm is a DIFFERENT arm and a _sub file
# holds only some rows, so mixing either into one grid makes load_cells' last-write-wins override
# real rows with rows from another arm or another subset.
CELL_NAME_RE = re.compile(r"^cells_(?P<body>.+)_k(?P<k>\d+)(?P<rest>.*)\.jsonl$")
SHARD_RE = re.compile(r"^_s\d+of\d+")
SUB_RE = re.compile(r"^_sub\d+$")


def cell_suffix_ok(rest, tag="", include_sub=False):
    """Is `rest` (what follows k<k> in a cells filename) part of the grid the caller asked for?

    tag=""  the untagged arm: "" or "_s<i>of<n>" only
    tag=X   that arm's files only ("_tagK" / "_tagT", with or without a shard suffix)
    include_sub  also accept an --only-rows subset file ("_sub<N>")
    """
    if tag:
        want = "_" + str(tag).lstrip("_")
        if not rest.startswith(want):
            return False
        rest = rest[len(want):]
    elif rest.startswith("_tag"):
        return False
    m = SHARD_RE.match(rest)
    if m:
        rest = rest[m.end():]
    if rest.startswith("_sub"):
        return bool(include_sub) and bool(SUB_RE.match(rest))
    return rest == ""


def cell_files(cells_dir, model=None, task=None, protocol=None, k=None, tag="",
               include_sub=False):
    """The cells files of ONE grid: the exact tag, its shards, and nothing else.

    The trailing wildcard this replaces ("..._k<k>*.jsonl") also matched a sibling _tagK arm, a
    _sub20 only-rows file and anything else appended to the tag, which `load_cells` then merged into
    one grid with the last file's rows winning.
    """
    pat = "cells_%s_%s_%s_k%s*.jsonl" % (model.replace("+", "-") if model else "*",
                                         task or "*", protocol or "*",
                                         k if k is not None else "*")
    out = []
    for fp in sorted(glob.glob(os.path.join(cells_dir, pat))):
        m = CELL_NAME_RE.match(os.path.basename(fp))
        if m is None:
            continue
        if k is not None and int(m.group("k")) != int(k):
            continue
        if not cell_suffix_ok(m.group("rest"), tag, include_sub):
            continue
        out.append(fp)
    return out


def load_cells(paths, split="all"):
    """Rows from one or more cells jsonl files, de-duplicated on (k, B, row_idx).

    Shards write disjoint problems, so concatenating a run's shards is a plain union; a resumed run
    can repeat a row, and the LAST occurrence wins (append-only files, the later write is the one
    that completed).
    """
    if isinstance(paths, str):
        paths = [paths]
    seen = {}
    for p in paths:
        for r in read_jsonl(p):
            if split != "all" and r.get("split", "eval") != split:
                continue
            seen[(int(r["k"]), int(r["B"]), int(r.get("row_idx", r["idx"])))] = r
    return list(seen.values())


class Cells(object):
    """A (model, task, protocol) grid: per-problem labels at every (k, B), with costs."""

    def __init__(self, rows, label="v2", caps=None, drop_extra=True):
        if drop_extra:
            rows = [r for r in rows if not r.get("extra", False)]
        self.rows = rows
        self.label = label
        self.ks = sorted({int(r["k"]) for r in rows})
        self.Bs = sorted({int(r["B"]) for r in rows}) if caps is None else sorted(caps)
        self.idx = sorted({int(r.get("row_idx", r["idx"])) for r in rows})
        ki = {k: i for i, k in enumerate(self.ks)}
        bi = {b: i for i, b in enumerate(self.Bs)}
        ni = {n: i for i, n in enumerate(self.idx)}
        shape = (len(self.ks), len(self.Bs), len(self.idx))
        self.acc = np.full(shape, np.nan)
        self.pred = np.empty(shape, dtype=object)
        self.own = np.full(shape, np.nan)
        self.nstop = np.full(shape, np.nan)
        self.ncut = np.full(shape, np.nan)
        self.ptok = np.full(len(self.idx), np.nan)
        self.reserve = np.full(len(self.idx), np.nan)
        self.split = np.empty(len(self.idx), dtype=object)
        self.passes = np.full(shape, np.nan)
        self.passes_pf = np.full(shape, np.nan)
        for r in rows:
            b = int(r["B"])
            if b not in bi:
                continue
            a, c, n = ki[int(r["k"])], bi[b], ni[int(r.get("row_idx", r["idx"]))]
            self.acc[a, c, n] = float(label_of(r, label))
            self.pred[a, c, n] = norm_answer(r.get("pred"))
            self.own[a, c, n] = float(r.get("trace_answer") not in (None, "None", ""))
            self.nstop[a, c, n] = _f(r.get("natural_stop"))
            self.ncut[a, c, n] = _f(r.get("n_cut"))
            self.passes[a, c, n] = _f(r.get("layer_passes"))
            self.passes_pf[a, c, n] = _f(r.get("layer_passes_promptfree"))
            self.ptok[n] = float(r["n_prompt_tokens"])
            self.reserve[n] = float(r.get("n_suffix_tokens", 0)) + float(r.get("n_answer_tokens", 0))
            self.split[n] = r.get("split", "eval")
        self.model = rows[0].get("model") if rows else None
        self.task = rows[0].get("task") if rows else None
        self.protocol = rows[0].get("protocol") if rows else None

    # ---------------------------------------------------------------- completeness
    def missing(self):
        w = np.argwhere(np.isnan(self.acc))
        return [(self.ks[int(a)], self.Bs[int(b)], self.idx[int(n)]) for a, b, n in w]

    def complete(self):
        return not np.isnan(self.acc).any()

    def select(self, split):
        if split == "all":
            return np.arange(len(self.idx))
        return np.array([i for i, s in enumerate(self.split) if s == split], dtype=int)

    # ---------------------------------------------------------------- tables
    def mean_acc(self, sel=None):
        a = self.acc if sel is None else self.acc[:, :, sel]
        return np.nanmean(a, 2)

    def parse_rate(self, sel=None):
        """Forced parse rate per (k, B): the share of cells whose read-out parsed.

        `sel` is a question selection (`select(split)`); None is every question, which is what the
        whole-grid checks want. `table(split)` passes the split's own questions, because an all-split
        parse rate printed beside a split accuracy is two different populations in one row.

        An empty grid or an empty split has nothing to average: the rate is NaN, not a crash
        (np.vectorize raises on an empty object array) and not a silent 0.
        """
        pr = self.pred if sel is None else self.pred[:, :, sel]
        if pr.size == 0:
            return np.full(pr.shape[:2], np.nan)
        got = np.vectorize(lambda x: x is not None, otypes=[bool])(pr)
        return got.mean(2)

    def own_rate(self, sel=None):
        """Share of cells whose OWN answer parsed, over `sel` (None: every question)."""
        ow = self.own if sel is None else self.own[:, :, sel]
        if ow.size == 0:
            return np.full(ow.shape[:2], np.nan)
        return np.nanmean(ow, 2)

    def table(self, split="eval"):
        sel = self.select(split)
        A = self.mean_acc(sel)
        out = {"model": self.model, "task": self.task, "protocol": self.protocol,
               "label": self.label, "split": split, "n": int(len(sel)),
               "ks": self.ks, "Bs": self.Bs,
               "acc": np.round(A, 6).tolist(),
               "parse_rate_forced": np.round(self.parse_rate(sel), 6).tolist(),
               "own_rate": np.round(self.own_rate(sel), 6).tolist(),
               "natural_stop_mean": np.round(np.nanmean(self.nstop[:, :, sel], 2), 3).tolist(),
               "mean_layer_passes": np.round(np.nanmean(self.passes[:, :, sel], 2), 1).tolist(),
               "mean_layer_passes_promptfree":
                   np.round(np.nanmean(self.passes_pf[:, :, sel], 2), 1).tolist(),
               "median_prompt_tokens": float(np.median(self.ptok[sel])) if len(sel) else None,
               "median_reserve_tokens": float(np.median(self.reserve[sel])) if len(sel) else None}
        return out

    # ---------------------------------------------------------------- commitment arrival
    def commitment(self, split="eval", strict=False, caps=None):
        """v4_commitment.arrival, verbatim.

        arrived[k, j, i] is True when the read-out at caps j..last all equal the read-out at the
        last cap and that read-out parsed. `strict` additionally rules out a question whose B=0
        read-out already equals the final answer (nothing was written, so nothing arrived).
        """
        caps = [c for c in (caps or CAPS_STANDARD) if c in self.Bs]
        bi = {b: i for i, b in enumerate(self.Bs)}
        sel = self.select(split)
        J = len(caps)
        A = np.zeros((len(self.ks), J, len(sel)), bool)
        for a in range(len(self.ks)):
            for ii, n in enumerate(sel):
                final = self.pred[a, bi[caps[-1]], n]
                if final is None:
                    continue
                ok = True
                for j in range(J - 1, -1, -1):
                    ok = ok and (self.pred[a, bi[caps[j]], n] == final)
                    A[a, j, ii] = ok
                if strict and self.pred[a, bi[caps[0]], n] == final:
                    A[a, :, ii] = False
        return A, caps, sel

    def mechanism(self, split="eval", strict=False, caps=None):
        """G (share arrived), c (accuracy given arrived), l (accuracy given not), and the RMSE of
        the reconstruction A ~= G c + (1 - G) l. v4_commitment.analyse, verbatim."""
        AR, caps, sel = self.commitment(split, strict, caps)
        bi = {b: i for i, b in enumerate(self.Bs)}
        CO = np.array([[[self.acc[a, bi[b], n] for n in sel] for b in caps]
                       for a in range(len(self.ks))], float)
        A = CO.mean(2)
        G = AR.mean(2)
        c = np.array([CO[i][AR[i]].mean() if AR[i].any() else np.nan
                      for i in range(len(self.ks))])
        l = np.array([CO[i][~AR[i]].mean() if (~AR[i]).any() else np.nan
                      for i in range(len(self.ks))])
        R = G * c[:, None] + (1 - G) * l[:, None]
        rmse = float(100 * np.sqrt(np.nanmean((R - A) ** 2)))
        N = max(1, len(sel))
        noise = float(100 * np.sqrt(np.mean(A * (1 - A)) / N))
        # earliest arrival cap per (k, question), None when it never stabilises
        first = np.full((len(self.ks), len(sel)), np.nan)
        for a in range(len(self.ks)):
            for ii in range(len(sel)):
                w = np.where(AR[a, :, ii])[0]
                if len(w):
                    first[a, ii] = caps[int(w[0])]
        # kept at full precision, for comparison against a fixed reference table
        return {"caps": caps, "ks": self.ks, "n": int(len(sel)),
                "G": G.tolist(), "c": c.tolist(), "l": l.tolist(), "acc": A.tolist(),
                "rmse_commitment": rmse, "noise_floor": noise,
                "arrival_cap_median": [None if np.all(np.isnan(first[a]))
                                       else float(np.nanmedian(first[a]))
                                       for a in range(len(self.ks))],
                "arrival_cap_never_frac": [float(np.mean(np.isnan(first[a])))
                                           for a in range(len(self.ks))],
                "strict": bool(strict)}


def load_grid(cells_dir, model, task, protocol="natural", label="v2", split="all", caps=None,
              tag="", include_sub=False):
    """One grid's Cells and the files it came from: the exact tag and its shards (see cell_files)."""
    paths = cell_files(cells_dir, model, task, protocol, tag=tag, include_sub=include_sub)
    if not paths:
        raise FileNotFoundError("no cells for %s/%s/%s%s under %s"
                                % (model, task, protocol,
                                   (" tag=%s" % tag) if tag else "", cells_dir))
    return Cells(load_cells(paths, split="all"), label=label, caps=caps), paths


# ------------------------------------------------------------------ CLI
def main(argv=None):
    p = argparse.ArgumentParser(prog="prod.score")
    p.add_argument("--cells", required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--protocol", default="natural")
    p.add_argument("--label", default="v2", choices=("v2", "forced", "own"))
    p.add_argument("--split", default="eval", choices=("eval", "cal", "all"))
    p.add_argument("--strict-commitment", dest="strict", action="store_true")
    p.add_argument("--out", default=None)
    a = p.parse_args(argv)
    g, paths = load_grid(a.cells, a.model, a.task, a.protocol, a.label)
    out = {"files": paths, "complete": g.complete(), "n_missing": len(g.missing()),
           "table": g.table(a.split),
           "mechanism": g.mechanism(a.split, strict=a.strict)}
    dest = a.out or os.path.join(a.cells, "score_%s_%s_%s.json"
                                 % (a.model.replace("+", "-"), a.task, a.protocol))
    save_json(dest, out)
    t = out["table"]
    print("%s %s %s label=%s split=%s n=%d complete=%s" % (a.model, a.task, a.protocol, a.label,
                                                           a.split, t["n"], out["complete"]))
    print("  Bs " + " ".join("%6d" % b for b in t["Bs"]))
    for i, k in enumerate(t["ks"]):
        print("  k%-2d" % k + " ".join("%6.1f" % (100 * v) for v in t["acc"][i]))
    print("  min forced parse rate %.3f" % min(min(r) for r in t["parse_rate_forced"]))
    print("wrote", dest)
    return out


if __name__ == "__main__":
    main()
