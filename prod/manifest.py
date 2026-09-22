"""The run list and its manifest: every (model, task, depth) job with its expected files and rows.

  python -m prod.manifest --write [--out=FILE] [--priority=1,2,3] [--forced-n=300]
  python -m prod.manifest --check --cells=DIR [--manifest=FILE]

The run list of record:
  models   Ouro-1.4B base and Thinking, Ouro-2.6B base and Thinking, Huginn-0125,
           McLeish Recurrent-Llama-3.2
  tasks    GSM8K 1319, MATH500 500, SVAMP 1000, AQuA 254, CSQA 1221, four BBH tasks 250 each,
           ARC-Challenge 1172
  depths   Ouro {1,2,3,4}; Huginn {1,2,4,8,16,32}; McLeish {1,2,4,8} everywhere and {16,32} on GSM8K
  protocol natural stop everywhere, plus forced continuation to 4096 for GSM8K and MATH500 on the
           four Ouro checkpoints (at the spike's N by default, full N optional)

Priority order if the window shrinks: 1 = Ouro-1.4B base and Thinking on all ten datasets,
2 = Ouro-2.6B, 3 = McLeish, 4 = Huginn and any model not listed (a LoRA arm), 5 = forced
continuation, 6 = chain continuation.
"""
import argparse
import glob
import os
import re

from . import config as cfgmod
from .common import (CAPS_EXTRA, CAPS_STANDARD, FORCED_BUDGETS, FORCED_N,
                     count_cells, save_json, load_json)
from .models import MODEL_ORDER, depths_for
from .tasks import FORCED_TASKS, TASK_ORDER, task_cfg

FORCED_N_DEFAULT = dict(FORCED_N)     # empty = full N

#: Priority order of the queue: Ouro-1.4B base and Thinking on all ten datasets first, then
#: Ouro-2.6B, then McLeish, then Huginn.
PRIORITY_MODELS = {"ouro_1_4b_base": 1, "ouro_1_4b_think": 1,
                   "ouro_2_6b_base": 2, "ouro_2_6b_think": 2,
                   "mcleish_llama32_r32": 3, "huginn_0125": 4}


#: the protocol tags a cells filename may carry. "natural2" is the default tag of a CONTINUATION job
#: (`prod.generate --continue-chains`), which replays a finished natural-stop grid's stored chains
#: and continues them: its own grid in its own files, never a shard of the natural grid it reads, so
#: it is listed apart and never merged into a natural-protocol job's rows.
#: "natural2h" is the same thing for the horizon mode: a (model, task, k) can have BOTH a think-tag
#: and a horizon continuation, and one tag per mode keeps them in separate files.
PROTOCOL_TAGS = ("natural2h", "natural2", "natural", "forced")
CONTINUATION_TAGS = ("natural2", "natural2h")
_PROTO_RE = re.compile(r"_(%s)_k\d+" % "|".join(PROTOCOL_TAGS))


def protocol_of_tag(tag):
    """The protocol tag inside an artifact tag (`<model>_<task>_<protocol>_k<k>...`), or None."""
    m = _PROTO_RE.search(str(tag))
    return m.group(1) if m else None


def priority_of(model, task, protocol):
    """Queue priority. Forced continuation (its own queue, priced separately) sorts after every
    natural-stop job regardless of model, and a chain-continuation job after that: it can only run
    once the natural-stop grid whose chains it reads is finished."""
    if protocol in CONTINUATION_TAGS:
        return 6
    if protocol == "forced":
        return 5
    return PRIORITY_MODELS.get(model, 4)


def run_list(forced_n=None, models=None, tasks=None, cfg=None):
    """Every (model, task, depth, protocol) job of record.

    The natural-stop grids run at horizon `cfg["horizon"]` over `cfg["caps"]`, and the
    forced-continuation block is a SEPARATE, configurable block -- `cfg["forced_block"]` names its
    models, tasks, depths and N, and `enabled: false` removes it entirely.
    """
    cfg = cfg or cfgmod.defaults()
    fb = cfg["forced_block"]
    forced_n = dict(FORCED_N_DEFAULT) if forced_n is None else dict(forced_n)
    if isinstance(fb.get("n"), dict):
        forced_n = dict(fb["n"])
    models = models or [m for m in MODEL_ORDER if m in cfg["depths"]] or MODEL_ORDER
    tasks = tasks or list(cfg["datasets"].keys()) or TASK_ORDER
    caps = list(cfg["caps"])
    jobs = []
    for model in models:
        for task in tasks:
            n_full = cfg["datasets"].get(task) or task_cfg(task)["n_full"]
            for k in depths_for(model, task, cfg):
                jobs.append({"model": model, "task": task, "k": k, "protocol": "natural",
                             "n": n_full, "caps": list(caps),
                             "extra_caps": list(CAPS_EXTRA), "horizon": int(cfg["horizon"]),
                             "block": "R1",
                             "priority": priority_of(model, task, "natural")})
    if fb.get("enabled", True):
        for model in fb["models"]:
            for task in fb["tasks"]:
                ks = fb.get("ks") or depths_for(model, task, cfg)
                for k in ks:
                    n = forced_n.get(task) or (fb["n"] if isinstance(fb.get("n"), int) else None) \
                        or cfg["datasets"].get(task) or task_cfg(task)["n_full"]
                    jobs.append({"model": model, "task": task, "k": k, "protocol": "forced",
                                 "n": n, "caps": list(cfg["forced_budgets"]), "extra_caps": [],
                                 "horizon": int(cfg["forced_horizon"]), "block": "R2",
                                 "priority": priority_of(model, task, "forced")})
    for j in jobs:
        j["tag"] = "%s_%s_%s_k%d" % (j["model"].replace("+", "-"), j["task"], j["protocol"], j["k"])
        j["expected_cells"] = j["n"] * len(set(j["caps"]) | set(j["extra_caps"]))
        j["cells_file"] = "cells_%s.jsonl" % j["tag"]
        j["meta_file"] = "meta_%s.json" % j["tag"]
        # the per-job width, overridden for (model, k) pairs config.yaml names; stored per row
        # already, and the launcher's memory estimate reads this same field.
        bw = cfgmod.batch_width_for(j["model"], j["k"], cfg)
        j["batch_width"] = bw
        j["command"] = ("python -m prod.generate --model=%s --task=%s --k=%d --protocol=%s"
                        " --batch-width=%d"
                        % (j["model"], j["task"], j["k"], j["protocol"], bw))
        if j["protocol"] == "forced" or j["n"] != task_cfg(j["task"])["n_full"]:
            j["command"] += " --n=%d" % j["n"]
        if j["protocol"] == "forced":
            j["command"] += " --resume-from-chains"
    return jobs


def shard_jobs(jobs, shards):
    """One job per (model, task, depth, shard). Shards write disjoint problems, so a run's shards
    are a plain union and any shard can be resumed on its own."""
    out = []
    for j in jobs:
        for s in range(shards):
            k = dict(j)
            k["shard"] = s
            k["shards"] = shards
            k["tag"] = "%s_s%dof%d" % (j["tag"], s, shards)
            k["cells_file"] = "cells_%s.jsonl" % k["tag"]
            k["meta_file"] = "meta_%s.json" % k["tag"]
            k["expected_cells"] = (len(range(s, j["n"], shards))
                                   * len(set(j["caps"]) | set(j["extra_caps"])))
            k["command"] = j["command"] + " --shard=%d --shards=%d" % (s, shards)
            out.append(k)
    return out


GPU_HOUR_BLOCKS = {"R1": "natural-stop grids", "R2": "forced-continuation block",
                   "R3": "S33 seeds", "R4": "live allocator check"}

# R3: per seed on the GB10, from the measured stage times -- training 1.0 h, the check on 100
# problems per task 0.4 h, the seven grids 10.0 h, the forced tail 2.0 h. Seed 20260912 is trained
# and its grids are running, so two seeds remain.
R3_SPARK_HOURS_PER_SEED = 13.4
R3_SEEDS_REMAINING = 2
# R4: one live-allocator pass over the GSM8K evaluation split at one budget is one generation per
# prompt at the chosen cell, i.e. about one natural-stop job's worth on the Spark.
R4_SPARK_HOURS = 2.0


def gpu_hours(jobs, cfg, throughput=None):
    """Estimated GPU-hours per block.

    Rate basis: the Spark tokens/s already measured per (model, task, depth) and stored in
    `checks.json.throughput_tokens_per_s`; the tokens a job emits are the trace (its natural stop,
    capped at the horizon) plus one forced read-out per DISTINCT cut length. The cluster factor is an
    ASSUMPTION (`cfg["cluster_factor"]`, 4.0) until the first timed job on the cluster.
    """
    tp = throughput or {}
    import re as _re

    def _passes(model, k):
        """Layer passes per generated token: k L for Ouro, prelude + k core + coda for the ravens."""
        sh = cfgmod.shapes_for(model)
        if sh.get("entries") == "ouro":
            return int(k) * int(sh["layers"])
        return int(sh["prelude"]) + int(k) * int(sh["core"]) + int(sh["coda"])

    def _scaled(keys, model, k):
        """Throughput scales inversely with layer passes per token; that is the basis used for
        every unmeasured (model, depth) and it is what makes a 2.6B estimate a projection rather
        than a guess."""
        vals = []
        for x in keys:
            m = _re.search(r"^([^/]+)/[^/]+/k(\d+)/", x)
            if not m:
                continue
            vals.append(tp[x] * _passes(m.group(1), int(m.group(2))) / float(_passes(model, k)))
        return (sum(vals) / len(vals)) if vals else None

    FAMILY_OF = {m: ("ouro" if m.startswith("ouro") else
                     ("huginn" if m.startswith("huginn") else "mcleish"))
                 for m in cfgmod.MODEL_ORDER}

    def rate(model, k):
        keys = [x for x in tp if x.startswith(model + "/") and ("/k%d/" % k) in x]
        if keys:                                   # measured at this model AND this depth
            return sum(tp[x] for x in keys) / len(keys)
        keys = [x for x in tp if x.startswith(model + "/")]
        if keys:                                   # same model, another depth
            return _scaled(keys, model, k)
        fam = FAMILY_OF.get(model)
        keys = [x for x in tp if FAMILY_OF.get(x.split("/")[0]) == fam]
        return _scaled(keys, model, k) if keys else None

    # Tokens per problem. NAT_TOKENS is the measured mean natural-stop length over the Spark
    # smokes; READOUTS is the mean number of DISTINCT cut lengths a problem has (a trace that stops
    # at 150 tokens shares one cut with every cap above it), and N_ANS the read-out length.
    #
    # CAVEAT, and it is the largest uncertainty in these hours: the rate used for a FORCED job is
    # the measured NATURAL-STOP rate, and those are not the same regime. Under natural stop the
    # batch drains as rows hit their stop marker, so the measured aggregate tokens/s is well below
    # the peak; a forced trace never stops, so all 16 rows stay alive for all 4,096 tokens and the
    # real rate is higher. R2 is therefore an UPPER bound; the corresponding lower bound is 33 h,
    # from a seconds-per-problem fit rather than a token rate. The first timed job on the cluster
    # must include ONE FORCED job, and the estimate is refreshed from it before the queue is
    # released.
    NAT_TOKENS, READOUTS, N_ANS = 220.0, 5.0, 12.0
    out = {}
    detail = []
    for j in jobs:
        r = rate(j["model"], j["k"])
        if j["protocol"] == "forced":
            toks = float(j["horizon"]) + READOUTS * N_ANS
        else:
            toks = min(NAT_TOKENS, float(j["horizon"])) + READOUTS * N_ANS
        secs = (j["n"] * toks / r) if r else None
        h_spark = (secs / 3600.0) if secs else None
        h = (h_spark / float(cfg["cluster_factor"])) if h_spark else None
        b = j.get("block", "R1")
        out.setdefault(b, 0.0)
        if h:
            out[b] += h
        detail.append({"tag": j["tag"], "block": b, "rate_tokens_per_s": r,
                       "spark_hours": h_spark, "cluster_hours": h,
                       "priced": h is not None,
                       "basis": ("measured (model, depth)"
                                 if any(x.startswith(j["model"] + "/") and
                                        ("/k%d/" % j["k"]) in x for x in tp)
                                 else ("same model, scaled by layer passes"
                                       if any(x.startswith(j["model"] + "/") for x in tp)
                                       else ("same family, scaled by layer passes" if r
                                             else "NOT PRICED")))})
    # R3 and R4 are not (model, task, depth) jobs, so they are priced from their own measured
    # stage times on the Spark, divided by the same assumed cluster factor. Stated as an assumption.
    f = float(cfg["cluster_factor"])
    out["R3"] = round(R3_SPARK_HOURS_PER_SEED * R3_SEEDS_REMAINING / f, 2)
    out["R4"] = round(R4_SPARK_HOURS / f, 2)
    return {k: round(v, 2) for k, v in out.items()}, detail


def manifest(forced_n=None, shards=1, priorities=None, cfg=None, throughput=None):
    cfg = cfg or cfgmod.defaults()
    jobs = run_list(forced_n, cfg=cfg)
    if priorities:
        jobs = [j for j in jobs if j["priority"] in priorities]
    sh = shard_jobs(jobs, shards) if shards > 1 else jobs
    by_pr = {}
    for j in jobs:
        by_pr.setdefault(j["priority"], {"jobs": 0, "problems": 0, "cells": 0})
        by_pr[j["priority"]]["jobs"] += 1
        by_pr[j["priority"]]["problems"] += j["n"]
        by_pr[j["priority"]]["cells"] += j["expected_cells"]
    by_block = {}
    for j in jobs:
        b = by_block.setdefault(j.get("block", "R1"),
                                {"jobs": 0, "problems": 0, "cells": 0})
        b["jobs"] += 1
        b["problems"] += j["n"]
        b["cells"] += j["expected_cells"]
    hours, hours_detail = gpu_hours(jobs, cfg, throughput)
    return {"n_jobs": len(jobs), "n_shard_jobs": len(sh), "shards": shards,
            "total_problems": sum(j["n"] for j in jobs),
            "total_cells": sum(j["expected_cells"] for j in jobs),
            "by_priority": by_pr, "by_block": by_block, "jobs": jobs, "shard_jobs": sh,
            "caps": list(cfg["caps"]), "extra_caps": list(CAPS_EXTRA),
            "forced_budgets": list(cfg["forced_budgets"]),
            "estimated_gpu_hours_by_block": hours,
            "estimated_gpu_hours_detail": hours_detail,
            "block_names": dict(GPU_HOUR_BLOCKS),
            "cluster_factor_assumed": cfg["cluster_factor"],
            "config": cfg, "config_sha256": cfgmod.digest(cfg)}


NAME_RE = re.compile(r"^cells_(?P<tag>.+)\.jsonl$")


def check(cells_dir, man):
    """Which manifest entries are complete, partial or absent."""
    have = {}
    for fp in sorted(glob.glob(os.path.join(cells_dir, "cells_*.jsonl"))):
        m = NAME_RE.match(os.path.basename(fp))
        if m:
            have[m.group("tag")] = count_cells(fp)     # the header row is not a cell
    rows = []
    for j in man["shard_jobs"]:
        got = have.get(j["tag"], 0)
        rows.append({"tag": j["tag"], "expected_cells": j["expected_cells"], "rows_found": got,
                     "state": ("complete" if got >= j["expected_cells"]
                               else ("partial" if got else "absent"))})
    counts = {"complete": 0, "partial": 0, "absent": 0}
    for r in rows:
        counts[r["state"]] += 1
    extra = sorted(set(have) - {j["tag"] for j in man["shard_jobs"]})
    # a continuation grid (--continue-chains, protocol tag natural2) is not a manifest job: it is
    # listed on its own rather than reported as an unknown file
    cont = [{"tag": t, "rows_found": have[t], "protocol_tag": protocol_of_tag(t)}
            for t in extra if protocol_of_tag(t) in CONTINUATION_TAGS]
    seen = {c["tag"] for c in cont}
    return {"counts": counts, "rows": rows,
            "files_not_in_manifest": [t for t in extra if t not in seen],
            "continuation_files": cont,
            "complete": counts["partial"] == 0 and counts["absent"] == 0}


def main(argv=None):
    p = argparse.ArgumentParser(prog="prod.manifest")
    p.add_argument("--write", action="store_true")
    p.add_argument("--check", action="store_true")
    p.add_argument("--cells", default=None)
    p.add_argument("--manifest", default=None)
    p.add_argument("--shards", type=int, default=1)
    p.add_argument("--priority", default=None)
    p.add_argument("--out", default=None)
    p.add_argument("--throughput", default=None,
                   help="checks.json (or any JSON with throughput_tokens_per_s) for the hours")
    cfgmod.add_args(p)
    a = p.parse_args(argv)
    cfg = cfgmod.from_args(a)
    tp = None
    if a.throughput:
        d = load_json(a.throughput, {})
        tp = d.get("throughput_tokens_per_s", d)
    fn = cfg["forced_block"].get("n")
    fn = fn if isinstance(fn, dict) else None
    prs = [int(x) for x in a.priority.split(",")] if a.priority else None
    man = manifest(fn, a.shards, prs, cfg=cfg, throughput=tp)
    dest = a.out or os.path.join(os.environ.get("PROD_ART", "."), "manifest.json")
    if a.write or not a.check:
        save_json(dest, man)
        print("run list: %d jobs (%d shard jobs at %d shards), %d problems, %d expected cells"
              % (man["n_jobs"], man["n_shard_jobs"], man["shards"], man["total_problems"],
                 man["total_cells"]))
        for pr in sorted(man["by_priority"]):
            v = man["by_priority"][pr]
            print("  priority %d: %3d jobs, %6d problems, %8d cells"
                  % (pr, v["jobs"], v["problems"], v["cells"]))
        for b in sorted(man["by_block"]):
            v = man["by_block"][b]
            print("  block %-3s %-28s %3d jobs, %6d problems, %8d cells, %7s GPU-hours"
                  % (b, man["block_names"].get(b, ""), v["jobs"], v["problems"], v["cells"],
                     man["estimated_gpu_hours"].get(b, "n/a")
                     if "estimated_gpu_hours" in man
                     else man["estimated_gpu_hours_by_block"].get(b, "n/a")))
        print("wrote", dest)
    if a.check:
        man2 = load_json(a.manifest, None) if a.manifest else man
        ck = check(a.cells or ".", man2)
        print("manifest check: %s" % ck["counts"])
        for r in ck["rows"]:
            if r["state"] != "complete":
                print("  %-10s %-52s %d/%d" % (r["state"], r["tag"], r["rows_found"],
                                               r["expected_cells"]))
        save_json(os.path.join(os.environ.get("PROD_ART", "."), "manifest_check.json"), ck)
    return man


if __name__ == "__main__":
    main()
