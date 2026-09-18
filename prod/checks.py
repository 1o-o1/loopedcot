"""checks.py: completeness, parse rates, and the PP2 checks JSON.

  python -m prod.checks --cells=DIR [--manifest=FILE] [--out=FILE]      # per-run completeness
  python -m prod.checks --pp2 [--out=../checks.json]                    # the brief's checks fields

Per-run checks (the thing every full-N job must satisfy before its numbers are used):
  * every (problem, cap) present for every depth, against the manifest's expected row count
  * forced parse rate at or above 0.9 at every depth and cap (gate G2's rule)
  * natural-stop distribution present, and the share of traces that hit the horizon
  * costs present on every row (layer_passes and layer_passes_promptfree)
  * split labels present and the calibration set exactly 100 questions per task (or 100 of 254 for
    AQuA), which is the split of record

The PP2 checks JSON collects the gate outputs the brief names:
  G0_batched_equals_batch1, G1_paths_validated, G1_mismatches, G2_parse_rate_min,
  G3_reproduction_max_dev, G4_flops_reproduction, G5_dry_run_complete, throughput_tokens_per_s,
  run_list_size, estimated_gpu_hours, review_pack_written, ready_for_full_N
"""
import argparse
import glob
import os
import numpy as np

from .common import ART, BATCH_WIDTH, N_CAL, load_json, package_hashes, save_json
from .manifest import check as manifest_check, manifest, protocol_of_tag
from .score import Cells, load_cells
from .tasks import TASK_ORDER, data_hashes, task_cfg

def parse_cells_name(fn):
    """(model, task, protocol, k, rest) from a cells filename.

    The task is matched against the registry rather than by a regex: both model names and task names
    contain underscores ("ouro_1_4b_base", "bbh_date_understanding"), so a non-greedy regex split
    puts the boundary in the wrong place (it read "ouro" / "1_4b_base_gsm8k").

    The protocol tag is whatever `manifest.protocol_of_tag` recognises, which is the one list of
    tags in the package (`manifest.PROTOCOL_TAGS`). This function used to know only "natural" and
    "forced", so a continuation grid (`natural2`, `natural2h`) parsed as no file at all and was
    dropped from the run silently -- unchecked rather than failed. A continuation grid is now
    checked by exactly the rules its natural-stop parent is checked by, under its own key, because
    it is its own grid and never a shard of that parent.
    """
    if not (fn.startswith("cells_") and fn.endswith(".jsonl")):
        return None
    body = fn[len("cells_"):-len(".jsonl")]
    proto = protocol_of_tag(body)
    if proto is None:
        return None
    marker = "_%s_k" % proto
    i = body.rfind(marker)
    if i < 0:
        return None
    head, tail = body[:i], body[i + len(marker):]
    kpart = tail.split("_", 1)
    try:
        k = int(kpart[0])
    except ValueError:
        return None
    rest = kpart[1] if len(kpart) > 1 else ""
    for t in sorted(TASK_ORDER, key=len, reverse=True):
        if head.endswith("_" + t):
            return head[:-(len(t) + 1)], t, proto, k, rest
    return None


def run_checks(cells_dir, min_parse=0.9):
    groups = {}
    for fp in sorted(glob.glob(os.path.join(cells_dir, "cells_*.jsonl"))):
        m = parse_cells_name(os.path.basename(fp))
        if not m:
            continue
        groups.setdefault((m[0], m[1], m[2]), []).append(fp)
    out = {"cells": cells_dir, "paths": {}, "problems": []}
    for (model, task, protocol), files in sorted(groups.items()):
        rows = load_cells(files)
        c = Cells(rows, drop_extra=False)
        pr = c.parse_rate()
        nst = c.nstop
        cal = int(sum(1 for s in c.split if s == "cal"))
        # the split of record draws 100 calibration questions from the WHOLE task, so the count only
        # has to equal 100 when the run covers the whole task; a smoke or a shard sees a subset
        n_full = task_cfg(task)["n_full"] if task in TASK_ORDER else None
        whole_task = n_full is not None and len(c.idx) == n_full
        want_cal = min(N_CAL, len(c.idx)) if whole_task else None
        rec = {"files": [os.path.basename(f) for f in files], "n_problems": len(c.idx),
               "ks": c.ks, "Bs": c.Bs, "n_rows": len(rows),
               "complete": c.complete(), "n_missing_cells": len(c.missing()),
               "min_forced_parse_rate": float(np.min(pr)),
               "min_forced_parse_rate_excl_B0":
                   float(np.min(pr[:, [j for j, b in enumerate(c.Bs) if b > 0]]))
                   if any(b > 0 for b in c.Bs) else None,
               "parse_rate_pass": bool(np.min(pr[:, [j for j, b in enumerate(c.Bs) if b > 0]])
                                       >= min_parse) if any(b > 0 for b in c.Bs) else None,
               "natural_stop_mean": float(np.nanmean(nst)),
               "frac_at_horizon": float(np.nanmean(nst >= max(c.Bs))),
               "costs_present": bool(not np.isnan(c.passes).any()
                                     and not np.isnan(c.passes_pf).any()),
               "n_cal": cal, "n_eval": int(len(c.idx) - cal),
               "covers_whole_task": bool(whole_task), "task_n_full": n_full,
               "cal_size_as_of_record": (bool(cal == want_cal) if want_cal is not None else None),
               "acc_v2_by_cap": {str(c.Bs[j]): float(np.nanmean(c.acc[:, j, :]))
                                 for j in range(len(c.Bs))}}
        key = "%s/%s/%s" % (model, task, protocol)
        out["paths"][key] = rec
        for field, ok in (("complete", rec["complete"]),
                          ("parse_rate_pass", rec["parse_rate_pass"]),
                          ("costs_present", rec["costs_present"]),
                          ("cal_size_as_of_record", rec["cal_size_as_of_record"])):
            if ok is False:
                out["problems"].append({"path": key, "check": field})
    out["pass"] = not out["problems"]
    return out


# The only assumption in the wall-clock projection. GB10 (the Spark) against one cluster GPU:
# dense bf16 compute about 250 against 990 TFLOPS (4.0x) and memory bandwidth about 273 GB/s against
# 4.8 TB/s (17.6x). Prefill is compute bound and decoding at width 16 is bandwidth bound, so the true
# factor lies between; 4.0 is taken as the conservative floor and every hour below is quoted at it.
# STATED AS AN ASSUMPTION: nothing in this package has run on a 141 GB cluster GPU.
CLUSTER_FACTOR = 4.0


# Brief PP2 asks for `estimated_gpu_hours` "from measurements, not from the 4070": a laptop 8 GB
# 4070 smoke is in the artifacts tree and must not enter the projection.
EXCLUDE_DEVICES = ("4070",)


def gpu_hour_estimate(cells_dir, man=None, cluster_factor=CLUSTER_FACTOR,
                      exclude_devices=EXCLUDE_DEVICES):
    """Project the full run list's hours from the measured seconds per problem of the smokes.

    Per (model, task, depth, protocol) the smoke gives `meta["seconds"]` (the WHOLE job: generation,
    the forced read-out passes and the cut dedup) minus `meta["load_seconds"]` (the one-off model
    load, which a full-N job amortises but a 20-problem smoke does not). That divided by the smoke's
    problem count is the seconds per problem, and a full-N job is

        load_seconds + seconds_per_problem * N_full        (on the SPARK)
        the same divided by cluster_factor                    (projected for one cluster GPU)

    Where a (model, task, depth) was not measured, the fallback is stated per job in `basis`:
      1  the same (model, depth) averaged over the tasks that were measured
      2  the same (model, task) at another depth, scaled by the ratio of layer passes per token
      3  the same family and depth
    A job with no basis at all is left null and counted, never silently filled in.
    """
    from .models import get as get_adapter
    man = man or manifest()
    obs, by_mk, by_fam = {}, {}, {}
    for p in sorted(glob.glob(os.path.join(cells_dir, "**", "meta_*.json"), recursive=True)):
        m = load_json(p, {})
        if not m.get("model") or not m.get("seconds") or not m.get("n_problems"):
            continue
        n = m["n_problems"]
        load = m.get("load_seconds") or 0.0
        spp = max(0.0, (m["seconds"] - load)) / n
        if spp <= 0:
            continue
        dev = str((m.get("env") or {}).get("device") or "")
        if any(x in dev for x in (exclude_devices or ())):
            continue
        fam = ("ouro" if str(m["model"]).startswith("ouro")
               else ("huginn" if "huginn" in str(m["model"]) else "mcleish"))
        rec = {"model": m["model"], "task": m.get("task"), "k": m.get("k"),
               "protocol": m.get("protocol", "natural"), "n": n,
               "seconds_per_problem": spp, "load_seconds": load,
               "tokens_per_s": ((m.get("passes") or {}).get("single") or {}).get("tokens_per_s"),
               "generated_tokens_per_problem": (
                   ((m.get("passes") or {}).get("single") or {}).get("generated_tokens") or 0) / n,
               "passes_per_token": m.get("passes_per_token"),
               "device": (m.get("env") or {}).get("device"),
               "batch_width": m.get("batch_width_pinned"), "peak_gb": m.get("peak_gb")}
        key = (m["model"], m.get("task"), m.get("k"), m.get("protocol", "natural"))
        # when the same cell was measured at more than one width (gate G0 ran width 8 and width 16),
        # the projection must use the PINNED production width, not whichever file globbed last
        prev = obs.get(key)
        if prev is not None and prev.get("batch_width") == BATCH_WIDTH                 and rec.get("batch_width") != BATCH_WIDTH:
            continue
        obs[key] = rec
        by_mk.setdefault((m["model"], m.get("k"), m.get("protocol", "natural")), []).append(rec)
        by_fam.setdefault((fam, m.get("k"), m.get("protocol", "natural")), []).append(rec)
    ppt_cache = {}

    def ppt(model, k):
        if (model, k) not in ppt_cache:
            try:
                ppt_cache[(model, k)] = get_adapter(model).passes_per_token(k)
            except Exception:                                      # noqa: BLE001
                ppt_cache[(model, k)] = None
        return ppt_cache[(model, k)]

    per_job, total_spark, total_cluster, missing = [], 0.0, 0.0, []
    for j in man["jobs"]:
        model, task, k, proto = j["model"], j["task"], j["k"], j["protocol"]
        fam = ("ouro" if model.startswith("ouro")
               else ("huginn" if "huginn" in model else "mcleish"))
        spp, basis, load = None, None, None
        r = obs.get((model, task, k, proto))
        if r:
            spp, basis, load = r["seconds_per_problem"], "measured (%s)" % r["device"], \
                r["load_seconds"]
        if spp is None and by_mk.get((model, k, proto)):
            rs = by_mk[(model, k, proto)]
            spp = float(np.mean([x["seconds_per_problem"] for x in rs]))
            load = float(np.mean([x["load_seconds"] for x in rs]))
            basis = "same model and depth, mean over %d measured task(s)" % len(rs)
        if spp is None:
            cand = [x for kk, x in obs.items() if kk[0] == model and kk[3] == proto]
            same_task = [x for x in cand if x["task"] == task] or cand
            if same_task:
                src = min(same_task, key=lambda x: abs((x["k"] or 1) - k))
                a_ppt, b_ppt = ppt(model, k), ppt(model, src["k"])
                if a_ppt and b_ppt:
                    spp = src["seconds_per_problem"] * (a_ppt / b_ppt)
                    load = src["load_seconds"]
                    basis = ("same model at k=%s scaled by layer passes per token %d/%d"
                             % (src["k"], a_ppt, b_ppt))
        if spp is None and proto == "forced":
            # A forced trace never stops: every row emits exactly `horizon` tokens (s13_common
            # suppresses every stop), so its generation cost is n * horizon / tokens_per_s and the
            # measured NATURAL generation rate at the same (model, depth) gives an analytic FLOOR.
            # It is a floor and not an estimate because the ten forced budgets each add a read-out
            # pass on top, and because a 4096-token context is slower per token than a 512-token one.
            cand = [x for kk, x in obs.items()
                    if kk[0] == model and kk[3] == "natural" and x.get("tokens_per_s")]
            same_k = [x for x in cand if x["k"] == k] or cand
            if same_k:
                src = min(same_k, key=lambda x: abs((x["k"] or 1) - k))
                rate = src["tokens_per_s"]
                a_ppt, b_ppt = ppt(model, k), ppt(model, src["k"])
                if a_ppt and b_ppt and src["k"] != k:
                    rate = rate * b_ppt / float(a_ppt)        # deeper loop, proportionally slower
                hz = 4096
                spp = hz / rate
                load = src["load_seconds"]
                basis = ("ANALYTIC FLOOR: %d forced tokens at the measured natural generation rate "
                         "of %s (model %s, k=%s, %.1f tok/s at width %s), read-out passes NOT "
                         "included" % (hz, "the same depth" if src["k"] == k else
                                       "k=%s scaled by layer passes per token" % src["k"],
                                       model, k, rate, src.get("batch_width")))
        if spp is None and by_fam.get((fam, k, proto)):
            rs = by_fam[(fam, k, proto)]
            spp = float(np.mean([x["seconds_per_problem"] for x in rs]))
            load = float(np.mean([x["load_seconds"] for x in rs]))
            basis = "same family and depth (%d measurement(s))" % len(rs)
        if spp is None:
            per_job.append({"tag": j["tag"], "n": j["n"], "spark_hours": None,
                            "cluster_hours": None, "basis": "NOT MEASURED"})
            missing.append(j["tag"])
            continue
        sec = (load or 0.0) + spp * j["n"]
        per_job.append({"tag": j["tag"], "n": j["n"], "priority": j["priority"],
                        "seconds_per_problem_spark": round(spp, 2),
                        "spark_hours": sec / 3600.0, "cluster_hours": sec / 3600.0 / cluster_factor,
                        "basis": basis})
        total_spark += sec / 3600.0
        total_cluster += sec / 3600.0 / cluster_factor
    by_family, by_priority = {}, {}
    for r, j in zip(per_job, man["jobs"]):
        if r["cluster_hours"] is None:
            continue
        fam = ("ouro" if j["model"].startswith("ouro")
               else ("huginn" if "huginn" in j["model"] else "mcleish"))
        for d, key in ((by_family, fam), (by_priority, "priority_%d" % j["priority"])):
            e = d.setdefault(key, {"jobs": 0, "problems": 0, "spark_hours": 0.0,
                                   "cluster_hours": 0.0})
            e["jobs"] += 1
            e["problems"] += j["n"]
            e["spark_hours"] += r["spark_hours"]
            e["cluster_hours"] += r["cluster_hours"]
    by_model_depth = {"%s/%s/k%s/%s" % (k[0], k[1], k[2], k[3]): {
        "seconds_per_problem": round(v["seconds_per_problem"], 2),
        "tokens_per_s": v["tokens_per_s"],
        "generated_tokens_per_problem": round(v["generated_tokens_per_problem"], 1),
        "n_smoke": v["n"], "peak_gb": v["peak_gb"], "batch_width": v["batch_width"]}
        for k, v in sorted(obs.items())}
    return {"cluster_factor": cluster_factor,
            "excluded_devices": list(exclude_devices or ()),
            "cluster_factor_is_an_assumption": True,
            "measured_on": sorted({v["device"] for v in obs.values() if v.get("device")}),
            "n_measured_cells": len(obs),
            "measured": by_model_depth,
            "per_job": per_job,
            "by_family": by_family, "by_priority": by_priority,
            "total_spark_hours": total_spark,
            "total_gpu_hours_at_measured_rate": total_cluster,
            "total_cluster_hours": total_cluster,
            "n_jobs_without_measurement": len(missing),
            "jobs_without_measurement": missing[:40]}


def pp2_checks(root=None, cells_dir=None):
    root = root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    art = cells_dir or os.environ.get("PROD_ART") or os.path.join(root, "artifacts")
    g0 = {}
    for p in sorted(glob.glob(os.path.join(art, "g0_batch_*.json"))):
        d = load_json(p, {})
        model = d.get("model") or os.path.basename(p)
        g0[model] = {"batched_equals_batch1": (d.get("verdict") or {}).get(
                         "batched_equals_batch1"),
                     "batched_width_stable": (d.get("verdict") or {}).get(
                         "batched_width_stable"),
                     "unpadded_equal_length_equals_batch1": (d.get("verdict") or {}).get(
                         "unpadded_equal_length_equals_batch1"),
                     "divergence_rate_by_k": {
                         k: (v.get("A_mask_w8", {}) or {}).get("divergence_rate")
                         for k, v in (d.get("phase1") or {}).items()},
                     "max_abs_delta_v2_pp": (d.get("phase2") or {}).get("max_abs_delta_v2_pp"),
                     "conclusion": (d.get("verdict") or {}).get("conclusion")}
    g0r = load_json(os.path.join(art, "g0_revised.json"), {})
    # the sweep writes its comparison beside its cells (artifacts/g1/), the older layout put it at
    # the artifacts root; take whichever exists, preferring the one with cells beside it
    g1 = (load_json(os.path.join(art, "g1", "g1_spike.json"), {})
          or load_json(os.path.join(art, "g1_spike.json"), {}))
    g2 = (load_json(os.path.join(art, "g2_parse.json"), {})
          or load_json(os.path.join(art, "g1", "g2_parse.json"), {}))
    g3 = load_json(os.path.join(art, "g3_score.json"), {})
    g4 = load_json(os.path.join(art, "g4_cost.json"), {})
    g5 = load_json(os.path.join(art, "g5_dryrun.json"), {})
    man = manifest()
    thr = {}
    for p in sorted(glob.glob(os.path.join(art, "**", "meta_*.json"), recursive=True)):
        m = load_json(p, {})
        if "4070" in str((m.get("env") or {}).get("device") or ""):
            continue                     # the laptop 4070 is not a production throughput datum
        for key, pas in (m.get("passes") or {}).items():
            if pas.get("tokens_per_s"):
                thr["%s/%s/k%s/%s" % (m.get("model"), m.get("task"), m.get("k"), key)] = \
                    pas["tokens_per_s"]
    for p in sorted(glob.glob(os.path.join(art, "g0_batch_*.json"))):
        d = load_json(p, {})
        for kk, v in (d.get("phase1") or {}).items():
            for arm in ("batch1", "A_mask_w8", "A_mask_w16"):
                if isinstance(v.get(arm), dict) and v[arm].get("tokens_per_s"):
                    thr["%s/g0/%s/%s" % (d.get("model"), kk, arm)] = v[arm]["tokens_per_s"]
    # recursive: the smoke metas live in subdirectories (artifacts/g1, artifacts_g5, g0_width/w*)
    est = (gpu_hour_estimate(art, man)
           if glob.glob(os.path.join(art, "**", "meta_*.json"), recursive=True) else {})
    review = os.path.join(root, "dev", "REVIEW.md")
    G1_OK = ("PASS", "MATCHED EXCEPT THE STRIP RULE")
    out = {
        # The criterion of record is the REVISED one (PLAN.md rulings Q6): batch-1 equality is no
        # longer a criterion, so `G0_batched_equals_batch1` keeps the batch-1 measurements as context
        # and `G0_revised` carries the verdict.
        "G0_batched_equals_batch1": g0,
        "G0_revised": {"pass": bool(g0r.get("pass")),
                       "criterion": g0r.get("criterion"),
                       "failing_clauses": g0r.get("failing_clauses"),
                       "per_model": {m: {c: v[c].get("pass") for c in v if c.startswith("clause")}
                                     for m, v in (g0r.get("models") or {}).items()},
                       "clause_iii": {m: {kk: v["clause_iii_width8_vs_width16"].get(kk)
                                          for kk in ("n", "widths", "max_abs_delta_v2_pp",
                                                     "max_flips_at_a_cap",
                                                     "trace_divergence_rate")}
                                      for m, v in (g0r.get("models") or {}).items()},
                       "clause_iv": g0r.get("clause_iv_batch_width_pinned")},
        "G1_paths_validated": [k for k, v in (g1.get("paths") or {}).items()
                               if v.get("status") in G1_OK],
        "G1_coverage": g1.get("coverage"),
        "G1_mismatches": [{"path": k, "status": v.get("status"),
                           "fields": v.get("mismatch_count_by_field"),
                           "causes": v.get("mismatch_causes")}
                          for k, v in (g1.get("paths") or {}).items()
                          if v.get("status") not in ((None,) + G1_OK)
                          and not str(v.get("status", "")).startswith("NOT RUN")],
        "G1_paths_not_run": [k for k, v in (g1.get("paths") or {}).items()
                             if str(v.get("status", "")).startswith("NOT RUN")],
        "G1_prompt_surface_exact": g1.get("prompt_surface_exact_on_every_compared_path"),
        "G1_cells_compared": g1.get("n_cells_compared_total"),
        "G1_aggregate_max_abs_acc_delta_pp": {
            k: (v.get("aggregates") or {}).get("max_abs_acc_delta_pp")
            for k, v in (g1.get("paths") or {}).items() if v.get("n_cells_compared")},
        "G1_matched_except_the_strip_rule": [k for k, v in (g1.get("paths") or {}).items()
                                             if v.get("status")
                                             == "MATCHED EXCEPT THE STRIP RULE"],
        "G2_parse_rate_min": g2.get("parse_rate_min_by_task", {}),
        "G2_flagged": g2.get("flagged", []),
        "G2_paths_measured": sorted((g2.get("paths") or {}).keys()),
        "G3_reproduction_max_dev": g3.get("max_deviation"),
        "G4_flops_reproduction": bool(g4.get("pass")),
        "G5_dry_run_complete": bool(g5.get("pass")),
        "throughput_tokens_per_s": thr,
        "run_list_size": man["n_jobs"],
        "estimated_gpu_hours": est.get("total_cluster_hours"),
        "estimated_gpu_hours_basis": {
            "unit": "GPU-hours for the whole run list",
            "measured_on": est.get("measured_on"),
            "spark_hours": est.get("total_spark_hours"),
            "cluster_factor_assumed": est.get("cluster_factor"),
            "cluster_factor_is_an_assumption": True,
            "n_measured_cells": est.get("n_measured_cells"),
            "n_jobs_without_measurement": est.get("n_jobs_without_measurement"),
            "by_family": est.get("by_family"), "by_priority": est.get("by_priority")},
        "review_pack_written": os.path.exists(review),
        "ready_for_full_N": False,
        # context a reader of checks.json needs
        "_meta": {"total_problems_in_run_list": man["total_problems"],
                  "total_expected_cells": man["total_cells"],
                  "by_priority": man["by_priority"],
                  "data_hashes": data_hashes(),
                  "package_hashes": package_hashes(),
                  "tasks": {t: task_cfg(t)["n_full"] for t in TASK_ORDER},
                  "gpu_hour_estimate_detail": est}}
    # G0 is judged by the revised criterion; G1 counts the strip-rule paths as validated, which the
    # rulings (Q8) explicitly waive, and requires every path in its table to have been compared.
    g1_full = bool(g1.get("pass")) and not (g1.get("coverage") or {}).get("paths_not_run", 1)
    gates_ok = [bool(g3.get("pass")), bool(g4.get("pass")), bool(g2.get("pass")),
                g1_full, bool(g5.get("pass")), bool(g0r.get("pass"))]
    out["ready_for_full_N"] = all(gates_ok) and out["review_pack_written"]
    out["_meta"]["gates_pass"] = {"G0": gates_ok[5], "G1": gates_ok[3], "G2": gates_ok[2],
                                  "G3": gates_ok[0], "G4": gates_ok[1], "G5": gates_ok[4]}
    return out


def main(argv=None):
    p = argparse.ArgumentParser(prog="prod.checks")
    p.add_argument("--cells", default=ART)
    p.add_argument("--manifest", default=None)
    p.add_argument("--pp2", "--pp3", dest="pp2", action="store_true",
                   help="the brief's checks fields. --pp3 is an alias: the PP2 gate fields are "
                        "unchanged by PP3 and the PP3 fields are written by the PP3 build "
                        "(checks.json['PP3']), so one collector serves both.")
    p.add_argument("--min-parse", dest="min_parse", type=float, default=0.9)
    p.add_argument("--out", default=None)
    a = p.parse_args(argv)
    if a.pp2:
        out = pp2_checks(cells_dir=a.cells)
        dest = a.out or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                     "checks.json")
        save_json(dest, out)
        print("PP2 checks: gates %s; run list %d jobs; ready_for_full_N=%s"
              % (out["_meta"]["gates_pass"], out["run_list_size"], out["ready_for_full_N"]))
        print("wrote", dest)
        return out
    out = run_checks(a.cells, a.min_parse)
    if a.manifest:
        out["manifest"] = manifest_check(a.cells, load_json(a.manifest, {}))
    dest = a.out or os.path.join(a.cells, "checks_runs.json")
    save_json(dest, out)
    for k, v in out["paths"].items():
        print("%-46s n=%-5d complete=%-5s min parse %.3f cal=%d eval=%d"
              % (k, v["n_problems"], v["complete"], v["min_forced_parse_rate"], v["n_cal"],
                 v["n_eval"]))
    print("checks %s (%d problems) -> %s" % ("PASS" if out["pass"] else "FAIL",
                                             len(out["problems"]), dest))
    return out


if __name__ == "__main__":
    main()
