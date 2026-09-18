"""Read candidate and reference cell grids and write paired accuracy and adherence checks in percentage points and tokens."""
import json, os, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import targets as G

def caps_from(cfg):
    """Return the token caps applied to the no-limit generation, in tokens, from config.yaml."""
    return [int(c) for c in cfg["eval_standard_caps"]]


def caps_in(d):
    """Return the token caps a loaded grid actually holds, ascending; a grid is read at its own caps, not at the config's."""
    if not d:
        return []
    return sorted({int(k[-1]) for k in d})


def caps_shared(da, db):
    """Return the token caps both grids hold, ascending, so a paired test never compares a cap only one side measured."""
    a, b = set(caps_in(da)), set(caps_in(db))
    return sorted(a & b)


def top_budgets(cfg):
    """Return the two large-budget cells F3 checks for non-inferiority: the largest numeric budget, and the no-limit run cut at it."""
    nums = [int(t) for t in cfg["eval_budgets"] if t is not None]
    return max(nums) if nums else None


def grid_from(cfg):
    """Return the evaluation budgets as canonical cell keys, from config.yaml."""
    return [G.budget_key(t) for t in cfg["eval_budgets"]]


def tasks_from(cfg):
    """Return the evaluation tasks of the configured harvest sources, in config order."""
    seen = []
    for src in cfg.sources:
        task = cfg.eval_task(src)
        if task not in seen:
            seen.append(task)
    return seen


def truthy(v):
    """Return whether a stored flag is true, tolerating the string spelling."""
    return v in (True, "True")


def has_own(r):
    """Return whether the row's own answer sentence parsed inside the cut."""
    return r.get("trace_answer") not in (None, "None", "")


def paired_own(da, db, ids, T, cap):
    """Return (candidate, reference) own-answer indicators for the rows both grids have, in the same order; a row missing on either side is dropped from both."""
    a, b = [], []
    for i in ids:
        ka, kb = (i, G.budget_key(T), int(cap)), (i, int(cap))
        if ka not in da or kb not in db:
            continue
        a.append(float(has_own(da[ka])))
        b.append(float(has_own(db[kb])))
    return a, b


def commitment(dd, ids, caps, budget_key=None):
    """Return Boolean commitment over the caps a grid was read at, checking every one through the largest; caps are tokens."""
    if dd is None or not caps:
        return None
    A = np.zeros((len(caps), len(ids)), bool)
    CO = np.zeros((len(caps), len(ids)), float)
    for ii, i in enumerate(ids):
        def cell(cap):
            """Return one cell of this grid at a token cap, keyed with the budget when the grid has one."""
            return dd.get((i, budget_key, cap)) if budget_key is not None else dd.get((i, cap))
        fin = cell(caps[-1])
        if fin is None:
            return None
        fp = fin.get("pred")
        settled = fp not in (None, "None", "")
        for j in range(len(caps) - 1, -1, -1):
            c_ = cell(caps[j])
            if c_ is None:
                return None
            settled = settled and (c_.get("pred") == fp)
            A[j, ii] = settled
            CO[j, ii] = float(truthy(c_.get("correct_v2")))
    out = {"caps": list(caps), "c": float(CO[A].mean()) if A.any() else None,
           "l": float(CO[~A].mean()) if (~A).any() else None,
           "acc_top": float(CO[-1].mean()), "cap_top": int(caps[-1])}
    if 128 in caps:
        out["G128"] = float(A[caps.index(128)].mean())
    return out


def main(argv):
    """Compare one run's cell grids with a reference arm's and write F1-F5 with paired bootstrap intervals in percentage points; returns a process exit code."""
    NAME, REF, BOOT = "s36", "s33", 2000
    cfg_path, root = G.DEFAULT_CONFIG, None
    cells_dir = ref_dir = out_dir = None
    for a in argv:
        k, _, v = a.lstrip("-").partition("=")
        if k == "name":
            NAME = v
        elif k == "ref":
            REF = v
        elif k == "config":
            cfg_path = v
        elif k == "root":
            root = v
        elif k == "cells-dir":
            cells_dir = v
        elif k == "ref-dir":
            ref_dir = v
        elif k == "out":
            out_dir = v
        elif k == "boot":
            BOOT = int(v)
    G.require_root(root, "analysis.py")
    cfg = G.load_config(cfg_path)
    CAPS, GRID_T, TASKS4 = caps_from(cfg), grid_from(cfg), tasks_from(cfg)
    TOP_T = top_budgets(cfg)          # the largest generated budget: F3's non-inferiority cell
    P = G.paths(root)
    ART = os.path.expanduser(cells_dir or P["artifacts"])
    REFART = os.path.expanduser(ref_dir or "~/latent-loop/s33/artifacts")
    OUT = os.path.expanduser(out_dir or ART)
    os.makedirs(OUT, exist_ok=True)
    rng = np.random.default_rng(int(cfg["seed"]))

    def load_s36(task, k):
        """Return this run's cells for one (task, k) keyed by (row, budget key, cap), reading the no-limit and the budgeted files, or None when that grid was never generated."""
        paths = [os.path.join(ART, "cells_%s_%s_k%d.jsonl" % (task, NAME, k)),
                 os.path.join(ART, "cells_budget_%s_%s_k%d.jsonl" % (task, NAME, k))]
        if not any(os.path.exists(p) for p in paths):
            return None
        d = {}
        for p in paths:
            if not os.path.exists(p):
                continue
            for line in open(p, encoding="utf-8"):
                r = json.loads(line)
                d[(int(r["idx"]), G.budget_key(r["budget"]), int(r["B"]))] = r
        return d or None

    def load_ref(task, k):
        """Return the reference arm's cells for one (task, k) keyed by (row, cap), or None when absent."""
        for name in ("cells_%s_%s_k%d.jsonl" % (task, REF, k),
                     "cells_%s_%s_fixed_k%d.jsonl" % (task, REF, k),
                     # the production grid's spelling: model first, then the natural-stop protocol
                     "cells_%s_%s_natural_k%d.jsonl" % (REF, task, k)):
            p = os.path.join(REFART, name)
            if os.path.exists(p):
                d = {}
                for line in open(p, encoding="utf-8"):
                    r = json.loads(line)
                    if r.get("_header"):
                        continue
                    d[(int(r.get("row_idx", r["idx"])), int(r["B"]))] = r
                return d
        return None

    def eval_ids(da, db):
        """Return the sorted evaluation rows both grids contain."""
        a = {i for (i, _t, _b) in da if da[(i, _t, _b)].get("split") == "eval"}
        b = {i for (i, _b) in db if db[(i, _b)].get("split", "eval") == "eval"}
        return sorted(a & b)

    def boot_ci(v, n_boot=BOOT):
        """Return the mean of v and its two-sided 95 percent bootstrap interval, in the units of v."""
        n = len(v)
        if n == 0:
            return None, None, None
        bs = np.array([v[rng.integers(0, n, n)].mean() for _ in range(n_boot)])
        return float(v.mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))

    def one_sided_lo(v, n_boot=BOOT):
        """Return the mean of v and its one-sided 95 percent lower bootstrap bound, in the units of v."""
        n = len(v)
        if n == 0:
            return None, None
        bs = np.array([v[rng.integers(0, n, n)].mean() for _ in range(n_boot)])
        return float(v.mean()), float(np.percentile(bs, 5))

    def paired(da, db, ids, T, cap, field="correct_v2"):
        """Return the paired accuracy difference at one budget and cap in percentage points, or None when no row is shared."""
        a, b = [], []
        for i in ids:
            ka, kb = (i, G.budget_key(T), int(cap)), (i, int(cap))
            if ka not in da or kb not in db:
                continue
            a.append(float(truthy(da[ka].get(field))))
            b.append(float(truthy(db[kb].get(field))))
        if not a:
            return None
        v = np.array(a) - np.array(b)
        m, lo, hi = boot_ci(v)
        _ml, lo5 = one_sided_lo(v)
        return {"n": len(a), "s36": round(float(np.mean(a)), 4),
                "ref": round(float(np.mean(b)), 4), "delta_pts": round(100 * m, 2),
                "ci95_pts": [round(100 * lo, 2), round(100 * hi, 2)],
                "lo95_one_sided_pts": round(100 * lo5, 2),
                "not_below_beyond_interval": bool(hi >= 0.0),
                "non_inferior_2pts": bool(100 * lo5 > -2.0)}

    cells, ref = {}, {}
    for t in TASKS4:
        for k in (1, 2, 4):
            cells[(t, k)] = load_s36(t, k)
            ref[(t, k)] = load_ref(t, k)
    grids_done = sorted("%s_k%d" % (t, k) for (t, k), v in cells.items() if v)
    print("[load] candidate grids present: %s (reference %s)" % (grids_done, REF), flush=True)
    res = {"name": NAME, "reference": REF, "grids_done": grids_done, "boot": BOOT}

    # ------------------------------------------------------------ F1
    f1 = {"rule": ("own answer sentence complete within the cap, at budgets 32 and 128, k=4, at "
                   "least 10 points above the reference on GSM8K and MATH500"), "per_task": {}}
    for t in [x for x in ("gsm8k", "math500") if x in TASKS4]:
        da, db = cells.get((t, 4)), ref.get((t, 4))
        if not da or not db:
            f1["per_task"][t] = "not run"
            continue
        ids = eval_ids(da, db)
        e = {"n": len(ids)}
        for T in (32, 128):
            a, b = paired_own(da, db, ids, T, T)     # one row contributes to both arms or neither
            if not a:
                e[str(T)] = "not run"
                continue
            v = np.array(a) - np.array(b)
            m, lo, hi = boot_ci(v)
            e[str(T)] = {"n": len(a),
                         "s36": round(float(np.mean(a)), 4), "ref": round(float(np.mean(b)), 4),
                         "delta_pts": round(100 * m, 2),
                         "ci95_pts": [round(100 * lo, 2), round(100 * hi, 2)],
                         "meets_10pt": bool(100 * m >= 10.0)}
        e["holds"] = bool(all(isinstance(e.get(str(T)), dict) and e[str(T)]["meets_10pt"]
                              for T in (32, 128)))
        f1["per_task"][t] = e
    ran1 = [t for t in TASKS4 if isinstance(f1["per_task"].get(t), dict)]
    f1["holds"] = (None if not ran1 else bool(all(f1["per_task"][t]["holds"] for t in ran1)))
    f1["tasks_run"] = ran1
    f1["tasks_failing"] = [t for t in ran1 if not f1["per_task"][t]["holds"]]
    res["F1"] = f1

    # ------------------------------------------------------------ F2
    f2 = {"rule": ("median chain length non-decreasing in T; at most 1.5 T at T in {32,128}; under "
                   "no limit at least 0.8 x the reference's median natural stop"), "per_grid": {}}
    for (t, k), da in sorted(cells.items()):
        name = "%s_k%d" % (t, k)
        if not da:
            continue                       # that grid was never generated; nothing to report
        db = ref.get((t, k))
        ids = (eval_ids(da, db) if db
               else sorted({i for (i, _a, _b), r in da.items() if r.get("split") == "eval"}))
        med = {}
        own_caps = caps_in(da) or CAPS
        for T in GRID_T:
            cap = own_caps[-1] if T == "none" else int(T)
            vals = [da[(i, T, cap)]["n_cut"] for i in ids if (i, T, cap) in da]
            if vals:
                med[T] = float(np.median(vals))
        if not med:
            f2["per_grid"][name] = "not run"
            continue
        order = [med[T] for T in GRID_T if T in med]
        e = {"median_by_T": med,
             "non_decreasing": bool(all(order[j] <= order[j + 1] + 1e-9
                                        for j in range(len(order) - 1)))}
        for T in (32, 128):
            if str(T) in med:
                e["within_1.5T_%d" % T] = bool(med[str(T)] <= 1.5 * T)
        if db and "none" in med:
            ref_cap = (caps_in(db) or CAPS)[-1]
            rm = float(np.median([db[(i, ref_cap)]["natural_stop"]
                                  for i in ids if (i, ref_cap) in db]))
            e["ref_cap_for_natural_stop"] = int(ref_cap)
            e["ref_median_natural_stop"] = rm
            e["none_ratio_to_ref"] = round(med["none"] / max(1e-9, rm), 4)
            e["none_at_least_0.8x"] = bool(med["none"] >= 0.8 * rm)
        e["holds"] = bool(e["non_decreasing"]
                          and all(e.get("within_1.5T_%d" % T, True) for T in (32, 128))
                          and e.get("none_at_least_0.8x", True))
        f2["per_grid"][name] = e
    ran2 = {g: v for g, v in f2["per_grid"].items() if isinstance(v, dict)}
    f2["holds"] = None if not ran2 else bool(all(v["holds"] for v in ran2.values()))
    f2["grids_failing"] = [g for g, v in ran2.items() if not v["holds"]]
    res["F2"] = f2

    # ------------------------------------------------------------ F3
    f3 = {"rule": ("v2 accuracy at budgets 32 and 128 not below the reference beyond the paired "
                   "interval on at least 3 of 4 tasks; at %d/none non-inferior (one-sided 95 "
                   "percent, margin 2 points) on every task" % TOP_T), "per_task": {},
          "top_budget": TOP_T}
    for t in TASKS4:
        ks = [k for k in (4, 2, 1) if cells.get((t, k)) and ref.get((t, k))]
        if not ks:
            f3["per_task"][t] = "not run"
            continue
        k = ks[0]
        da, db = cells[(t, k)], ref[(t, k)]
        ids = eval_ids(da, db)
        e = {"k": k, "n": len(ids)}
        for T in (32, 128):
            e["at_%d" % T] = paired(da, db, ids, T, T)
        # the top cell is the largest budget THIS grid ran that the reference also measured as a
        # cap, and the no-limit run cut at that same cap; a cap only one side has is not compared
        shared = caps_shared(da, db)
        ran = sorted({int(t) for (_i, t, _b) in da if t != "none"})
        choices = [b for b in ran if b in shared]
        top_cap = max(choices) if choices else TOP_T
        e["top_cap"] = int(top_cap)
        e["at_top"] = paired(da, db, ids, top_cap, top_cap)
        e["at_none_top"] = paired(da, db, ids, "none", top_cap)
        tight = [e["at_%d" % T] for T in (32, 128) if isinstance(e.get("at_%d" % T), dict)]
        e["tight_ok"] = bool(tight and all(x["not_below_beyond_interval"] for x in tight))
        top = [x for x in (e["at_top"], e["at_none_top"]) if isinstance(x, dict)]
        e["top_non_inferior"] = bool(top and all(x["non_inferior_2pts"] for x in top))
        f3["per_task"][t] = e
    ran3 = [t for t in TASKS4 if isinstance(f3["per_task"].get(t), dict)]
    f3["tasks_run"] = ran3
    f3["tight_ok_tasks"] = [t for t in ran3 if f3["per_task"][t]["tight_ok"]]
    f3["top_failing"] = [t for t in ran3 if not f3["per_task"][t]["top_non_inferior"]]
    f3["holds"] = (None if not ran3
                   else bool(len(f3["tight_ok_tasks"]) >= min(3, len(ran3))
                             and not f3["top_failing"]))
    res["F3"] = f3

    # ------------------------------------------------------------ F4
    f4 = {"rule": ("committed accuracy c at k=2 and k=4 on MATH500 not below the reference's by "
                   "more than 3 points"), "per_k": {}}
    for k in (2, 4):
        da, db = cells.get(("math500", k)), ref.get(("math500", k))
        if not da or not db:
            f4["per_k"][str(k)] = "not run"
            continue
        ids = eval_ids(da, db)
        shared = caps_shared(da, db)
        ma = commitment(da, ids, shared, budget_key="none")
        mb = commitment(db, ids, shared)
        if not ma or not mb:
            f4["per_k"][str(k)] = "not run"
            continue
        if ma["c"] is None or mb["c"] is None:
            f4["per_k"][str(k)] = "not run"
            continue
        dc = 100 * (ma["c"] - mb["c"])
        f4["per_k"][str(k)] = {"c_s36": round(ma["c"], 4), "c_ref": round(mb["c"], 4),
                               "c_delta_pts": round(dc, 2), "caps": ma["caps"],
                               "G128_s36": (round(ma["G128"], 4) if "G128" in ma else None),
                               "G128_ref": (round(mb["G128"], 4) if "G128" in mb else None),
                               "holds": bool(dc >= -3.0)}
    ran4 = [v for v in f4["per_k"].values() if isinstance(v, dict)]
    f4["holds"] = (None if not ran4 else bool(all(v["holds"] for v in ran4)))
    res["F4"] = f4

    # ------------------------------------------------------------ F5
    f5 = {"rule": ("CSQA and AQuA at k=1 and k=4, accuracy at budgets 0 and 32 not below the "
                   "reference's beyond the paired interval"), "per_grid": {}}
    for t in [x for x in ("csqa", "aqua") if x in TASKS4]:
        for k in (1, 4):
            da, db = cells.get((t, k)), ref.get((t, k))
            if not da or not db:
                f5["per_grid"]["%s_k%d" % (t, k)] = "not run"
                continue
            ids = eval_ids(da, db)
            e = {"n": len(ids)}
            for T in (0, 32):
                e["at_%d" % T] = paired(da, db, ids, T, T)
            got = [e["at_%d" % T] for T in (0, 32) if isinstance(e.get("at_%d" % T), dict)]
            e["holds"] = bool(got and all(x["not_below_beyond_interval"] for x in got))
            f5["per_grid"]["%s_k%d" % (t, k)] = e
    ran5 = [v for v in f5["per_grid"].values() if isinstance(v, dict)]
    f5["holds"] = (None if not ran5 else bool(all(v["holds"] for v in ran5)))
    res["F5"] = f5

    # ------------------------------------------------------------ verdict
    F = {n: res[n]["holds"] for n in ("F1", "F2", "F3", "F4", "F5")}
    math_run = [t for t in ("gsm8k", "math500") if isinstance(f1["per_task"].get(t), dict)]
    f1_fails_both = bool(len(math_run) == 2 and all(not f1["per_task"][t]["holds"]
                                                    for t in math_run))
    f3_fails_three = bool(len(ran3) >= 3 and len(ran3) - len(f3["tight_ok_tasks"]) >= 3)
    core = [F["F1"], F["F2"], F["F3"], F["F4"]]
    if any(v is None for v in core):
        verdict, why = "indeterminate", ("a core test could not be evaluated: %s"
                                         % {n: F[n] for n in ("F1", "F2", "F3", "F4")})
    elif all(core):
        verdict, why = "feasible", "F1, F2, F3 and F4 all hold"
    elif f1_fails_both or f3_fails_three:
        verdict = "not feasible"
        why = "F1 fails on both math tasks" if f1_fails_both else "F3 fails on three tasks"
    else:
        verdict, why = "indeterminate", ("core tests are mixed: %s"
                                         % {n: F[n] for n in ("F1", "F2", "F3", "F4")})
    res["verdict"], res["verdict_reason"], res["holds"] = verdict, why, F
    outp = os.path.join(OUT, "%s_tests_vs_%s.json" % (NAME, REF))
    json.dump(res, open(outp, "w"), indent=1)
    print(json.dumps({"grids_done": grids_done, "holds": F, "verdict": verdict, "why": why},
                     indent=2), flush=True)
    print("ANALYSIS DONE -> %s" % outp, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
