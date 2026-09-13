"""Launcher: shard the run list over N GPUs, resume from per-problem checkpoints, write checks.

  python -m prod.launcher --plan --gpus=8 --shards=8            # write the queue, run nothing
  python -m prod.launcher --run --gpus=8 --shards=8 [--priority=1,2] [--dry-run-n=20]
  python -m prod.launcher --run --gpus=8 --workers-per-gpu=2    # PP3 decision 1
  python -m prod.launcher --status

`--workers-per-gpu N` (default 1) gives each GPU N slots. Workers on the same GPU are SEPARATE
PROCESSES with the same CUDA_VISIBLE_DEVICES (the launcher only supervises them), so an OOM in one
cannot take the other down. Placement is memory-aware: every job carries an estimate

    est_bytes = params * 2 (bf16 weights) + batch_width * (horizon + prompt allowance) * KV/token
    KV bytes per token = 2 * kv_heads * head_dim * 2 * cached layer entries at depth k
    cached layer entries = 24k (Ouro-1.4B) | 48k (Ouro-2.6B) | 4+4k (Huginn) | 8+6k (McLeish)

and a slot claims a job only if the GPU's RUNNING SUM (the jobs its slots hold right now) stays
under `--util` x the device memory (0.85 by default, the Spark rule; the device size is read from
`torch.cuda.mem_get_info` at start, or given by `--device-gb`). A job whose estimate exceeds the
ceiling on its own can never be placed: those are listed in `launcher_plan.json["unplaceable"]`,
printed, and left in the queue rather than run into an OOM.

With `--workers-per-gpu=1` this is exactly PP2's behaviour plus a printed estimate. Each worker pulls the next job off a FILE-BASED queue (an atomic rename of a
claim file), sets CUDA_VISIBLE_DEVICES to its own GPU, and runs `prod.generate` in a subprocess so an
OOM or a crash cannot take the queue down with it. Per-problem checkpoints mean a killed worker's job
is simply re-claimed and resumed; no row is generated twice because the cells file is re-read on
start and a (problem, cap) already present is skipped.

The Spark is single-tenant for GPU work (LEDGER 2026-09-04 S1: "two heavy jobs overlapping killed
both processes silently and froze ssh" on the GB10's unified memory), so `--gpus=1` is the only
setting used there and the eight-way queue is for the cluster node.

Nothing here launches a cluster job. `--run` executes locally on the host it is invoked on, and
`--dry-run-n` caps every job at N problems, which is what gate G5 uses.

Three behaviours gate G5 fixed (2026-09-12):
  * a killed worker's claim is re-queued on the next `--run` (`requeue_claimed`). Without it the job
    sat in `claimed/` forever and the run list could never complete.
  * `--only=SUBSTR[,SUBSTR]` restricts the plan to the named jobs, so G5's queue is exactly the two
    paths the brief asks for instead of a whole priority class.
  * `--run` no longer re-plans an existing queue. It did, and since a bare `--run` carries none of
    the planning filters, G5's restart step silently replaced a two-job N=20 queue with the whole
    294-job FULL-N run list and started a 1319-problem job on the Spark. Planning now happens on
    `--plan`, or on a `--run` that finds no queue.
"""
import argparse
import json
import os
import subprocess
import sys
import time

from . import config as cfgmod
from .common import ART, BATCH_WIDTH, LOGS, load_json, save_json
from .manifest import manifest

QUEUE = "queue"


def queue_dir(root=None):
    d = os.path.join(root or ART, QUEUE)
    for sub in ("todo", "claimed", "done", "failed"):
        os.makedirs(os.path.join(d, sub), exist_ok=True)
    return d


def device_bytes(n_gpus, device_gb=None):
    """Per-GPU memory in bytes: measured, or `--device-gb` when torch is unavailable."""
    if device_gb:
        return {g: int(float(device_gb) * 1024 ** 3) for g in range(n_gpus)}, "--device-gb"
    try:
        import torch
        if not torch.cuda.is_available():
            raise RuntimeError("no cuda")
        out = {}
        for g in range(min(n_gpus, torch.cuda.device_count())):
            _free, total = torch.cuda.mem_get_info(g)
            out[g] = int(total)
        for g in range(len(out), n_gpus):
            out[g] = out[0]
        return out, "torch.cuda.mem_get_info"
    except Exception as e:                                    # noqa: BLE001
        return {}, "unavailable: %r" % (e,)


def estimate(rec, cfg):
    """The per-job memory estimate of decision 1, in bytes.

    Ruling Q12: the width is the job's own `batch_width` field when the manifest set one (it always
    does, from `cfgmod.batch_width_for`), and the per-(model, k) override table otherwise -- so the
    estimate is correct even for a job record built without going through `prod.manifest`.
    """
    bw = rec.get("batch_width") or cfgmod.batch_width_for(rec["model"], rec["k"], cfg)
    return cfgmod.job_bytes(rec["model"], rec["k"], bw,
                            rec.get("horizon") or cfg["horizon"], cfg=cfg)


def plan(gpus, shards, priorities=None, forced_n=None, dry_run_n=None, root=None,
         extra_args=None, only=None, cfg=None, workers_per_gpu=1, device_gb=None):
    cfg = cfg or cfgmod.defaults()
    man = manifest(forced_n, shards, priorities, cfg=cfg)
    q = queue_dir(root)
    stale = [f for f in os.listdir(os.path.join(q, "todo")) if f.endswith(".json")]
    for f in stale:
        os.remove(os.path.join(q, "todo", f))
    if stale:
        print("[launcher] cleared %d job file(s) of the previous plan from todo/" % len(stale))
    busy = os.listdir(os.path.join(q, "claimed"))
    if busy:
        print("[launcher] WARNING: %d claimed job(s) in %s; a launcher may still be running on "
              "this queue" % (len(busy), q), flush=True)
    if only:
        keep = [x for x in only if x]
        man["shard_jobs"] = [j for j in man["shard_jobs"]
                             if any(x in j["tag"] for x in keep)]
    # heaviest first: the queue is greedy, so the long jobs start while the short ones fill in
    jobs = sorted(man["shard_jobs"], key=lambda j: (j["priority"], -j["n"] * j["k"]))
    written = []
    for n, j in enumerate(jobs):
        cmd = ["python", "-m", "prod.generate", "--model=%s" % j["model"],
               "--task=%s" % j["task"], "--k=%d" % j["k"], "--protocol=%s" % j["protocol"],
               # the pin is generate.py's default too; the queue states it so that a job record
               # read months later says at which width its rows were produced (rulings Q6 iv)
               "--batch-width=%d" % j.get("batch_width", BATCH_WIDTH)]
        if j.get("shards", 1) > 1:
            cmd += ["--shard=%d" % j["shard"], "--shards=%d" % j["shards"]]
        if dry_run_n:
            cmd += ["--n=%d" % dry_run_n]
        elif j["n"] != j.get("n_full", j["n"]):
            cmd += ["--n=%d" % j["n"]]
        if j["protocol"] == "forced":
            cmd += ["--n=%d" % (dry_run_n or j["n"])]
            # a forced job continues from the chain its natural-stop twin stored (PP3b Fix 1); rows
            # without a stored chain, or whose prompt hash differs, fall back to full generation
            cmd += ["--resume-from-chains"]
        cmd += list(extra_args or [])
        rec = {"order": n, "tag": j["tag"], "priority": j["priority"], "model": j["model"],
               "task": j["task"], "k": j["k"], "protocol": j["protocol"], "n": j["n"],
               "horizon": j.get("horizon"), "batch_width": j.get("batch_width"),
               "expected_cells": j["expected_cells"], "cmd": cmd}
        rec["est_bytes"] = estimate(rec, cfg)
        rec["est_gb"] = round(rec["est_bytes"] / 1024 ** 3, 3)
        p = os.path.join(q, "todo", "%05d_%s.json" % (n, j["tag"]))
        save_json(p, rec)
        written.append(rec)
    dev, dev_src = device_bytes(gpus, device_gb)
    ceiling = int(cfg["mem_util"] * min(dev.values())) if dev else None
    unplaceable = ([{"tag": r["tag"], "est_gb": r["est_gb"]} for r in written
                    if r["est_bytes"] > ceiling] if ceiling else [])
    save_json(os.path.join(root or ART, "launcher_plan.json"),
              {"gpus": gpus, "workers_per_gpu": workers_per_gpu, "shards": shards,
               "priorities": priorities, "dry_run_n": dry_run_n, "n_jobs": len(written),
               "queue": q, "config": cfg, "config_sha256": cfgmod.digest(cfg),
               "device_bytes": dev, "device_bytes_source": dev_src,
               "mem_util": cfg["mem_util"],
               "slot_ceiling_gb": round(ceiling / 1024 ** 3, 2) if ceiling else None,
               "est_gb_min_max": [min((r["est_gb"] for r in written), default=None),
                                  max((r["est_gb"] for r in written), default=None)],
               "unplaceable": unplaceable,
               "total_expected_cells": sum(r["expected_cells"] for r in written)})
    if unplaceable:
        print("[launcher] %d job(s) do not fit alone under %.2f x device memory and will NOT be "
              "placed: %s" % (len(unplaceable), cfg["mem_util"],
                              ", ".join(u["tag"] for u in unplaceable[:6])), flush=True)
    return written, q


def requeue_claimed(q, older_than=0.0):
    """Move stale claims back to `todo`.

    A worker that is killed (or a node that dies) leaves its claim file in `claimed/`, and `claim()`
    only ever takes from `todo`, so without this the job is never run again -- the failure gate G5
    exists to catch. Re-running a claimed job is always safe: `prod.generate` re-reads its cells file
    on start and skips every (problem, cap) already written, so a resumed job adds the missing rows
    and no duplicates.

    `older_than` guards the case of a SECOND launcher process starting while the first is still
    working: pass a value larger than the longest expected job, or --no-requeue.
    """
    n = []
    # failed/ is re-queued too: a job that exited non-zero (OOM at batch 1, a node fault) resumes
    # from its per-problem checkpoint exactly like a stranded claim, which is what the README says
    for sub in ("claimed", "failed"):
        for fn in sorted(os.listdir(os.path.join(q, sub))):
            src = os.path.join(q, sub, fn)
            if older_than and (time.time() - os.path.getmtime(src)) < older_than:
                continue
            try:
                os.rename(src, os.path.join(q, "todo", fn))
            except OSError:
                continue
            n.append(fn)
    if n:
        print("[launcher] re-queued %d stale claim(s) / failed job(s): %s"
              % (len(n), ", ".join(x[6:-5] for x in n[:6])), flush=True)
    return n


class GpuBudget(object):
    """Admission control for the slots of one node (PP3 decision 1).

    A GPU has `budget` bytes (`mem_util` x its device memory) and `workers_per_gpu` slots. A slot
    may claim a job only while the GPU's RUNNING SUM -- the estimates of the jobs its slots hold at
    that instant -- stays under the budget. The sum is held in this process because the launcher
    supervises every slot on the node; the jobs themselves are separate processes.

    `budget=None` disables admission control entirely, which is what `--workers-per-gpu=1` with no
    measurable device gives, and is exactly PP2's behaviour.
    """

    def __init__(self, budgets):
        import threading
        self.budgets = dict(budgets or {})
        self.running = {g: 0 for g in self.budgets}
        self.lock = threading.Lock()
        self.cv = threading.Condition(self.lock)
        self.blocked = []

    def budget(self, gpu):
        return self.budgets.get(gpu)

    def try_take(self, gpu, nbytes):
        b = self.budgets.get(gpu)
        if b is None:
            return True
        with self.lock:
            if self.running.get(gpu, 0) + int(nbytes) <= b:
                self.running[gpu] = self.running.get(gpu, 0) + int(nbytes)
                return True
        return False

    def release(self, gpu, nbytes):
        if self.budgets.get(gpu) is None:
            return
        with self.cv:
            self.running[gpu] = max(0, self.running.get(gpu, 0) - int(nbytes))
            self.cv.notify_all()

    def idle(self, gpu):
        return self.budgets.get(gpu) is None or self.running.get(gpu, 0) == 0

    def wait(self, timeout=5.0):
        with self.cv:
            self.cv.wait(timeout)


def claim(q, worker, gpu=0, budget=None):
    """Atomically take the first todo file that FITS. os.rename is atomic on one filesystem, so two
    workers cannot claim the same job.

    Without a budget this is PP2's "lowest-numbered todo file", unchanged. With one, a job whose
    estimate does not fit in the GPU's remaining budget is skipped and left in `todo` for whoever
    frees memory next; a job that does not fit even on an IDLE gpu is unplaceable and is reported
    (it is never silently run into an OOM, and never silently dropped).
    """
    skipped = []
    need = 0
    for fn in sorted(os.listdir(os.path.join(q, "todo"))):
        src = os.path.join(q, "todo", fn)
        if budget is not None:
            try:
                rec0 = load_json(src, {})
            except (OSError, ValueError):
                continue                  # another slot renamed it between listdir and open
            need = int(rec0.get("est_bytes") or 0)
            if not budget.try_take(gpu, need):
                skipped.append((fn, need, budget.idle(gpu)))
                continue
        dst = os.path.join(q, "claimed", fn)
        try:
            os.rename(src, dst)
        except OSError:
            if budget is not None:
                budget.release(gpu, need)     # another slot got it first; give the bytes back
            continue
        rec = load_json(dst, {})
        rec["worker"] = worker
        rec["gpu"] = gpu
        rec["claimed_at"] = time.strftime("%FT%T")
        save_json(dst, rec)
        return dst, rec
    if budget is not None:
        # a job that does not fit on an IDLE gpu can never be placed: say so once, loudly.
        for fn, need, was_idle in skipped:
            if was_idle:
                budget.blocked.append({"job": fn[6:-5], "est_gb": round(need / 1024 ** 3, 3),
                                       "gpu": gpu,
                                       "budget_gb": round(budget.budget(gpu) / 1024 ** 3, 2)})
        if skipped and not any(x[2] for x in skipped):
            return "WAIT", None
    return None, None


def visible_gpu_id(gpu, parent=None):
    """The CUDA_VISIBLE_DEVICES value for slot `gpu`: the gpu-th entry of the parent's own visible
    list when one is set (a Slurm allocation, or a user-restricted shell), else the bare index."""
    parent = os.environ.get("CUDA_VISIBLE_DEVICES") if parent is None else parent
    vis = [x.strip() for x in str(parent).split(",") if x.strip()] if parent else []
    if vis and int(gpu) < len(vis):
        return vis[int(gpu)]
    return str(gpu)


def run_worker(q, gpu, root=None, python=None, max_jobs=None, slot=0, budget=None):
    worker = "gpu%d" % gpu if slot == 0 and (budget is None or budget.budgets.get(gpu) is None)         else "gpu%d.w%d" % (gpu, slot)
    done = 0
    while max_jobs is None or done < max_jobs:
        path, rec = claim(q, worker, gpu, budget)
        if path == "WAIT":
            # every remaining job is too big for what this gpu has free RIGHT NOW, but its other
            # slots are working: wait for one of them to finish and look again.
            budget.wait()
            continue
        if rec is None:
            break
        est = int(rec.get("est_bytes") or 0)
        env = dict(os.environ)
        env["CUDA_VISIBLE_DEVICES"] = visible_gpu_id(gpu)
        env.setdefault("HF_HUB_OFFLINE", "1")
        env.setdefault("PROD_ART", root or ART)
        cmd = list(rec["cmd"])
        cmd[0] = python or sys.executable
        log = os.path.join(LOGS, "%s_%s.log" % (rec["tag"], worker))
        t0 = time.time()
        rc = 99
        try:
            with open(log, "a", encoding="utf-8") as f:
                f.write("\n=== %s %s\n%s\n" % (time.strftime("%FT%T"), worker, " ".join(cmd)))
                f.flush()
                rc = subprocess.call(cmd, stdout=f, stderr=subprocess.STDOUT, env=env,
                                     cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        finally:
            if budget is not None:
                budget.release(gpu, est)      # on every exit path, or the slot's GPU budget leaks
        rec.update({"returncode": rc, "seconds": round(time.time() - t0, 1), "log": log,
                    "finished_at": time.strftime("%FT%T")})
        dest = os.path.join(q, "done" if rc == 0 else "failed", os.path.basename(path))
        save_json(dest, rec)
        os.remove(path)
        done += 1
        print("[%s] %s rc=%d %.0fs -> %s" % (worker, rec["tag"], rc, rec["seconds"],
                                             os.path.basename(dest)), flush=True)
    return done


def status(root=None):
    q = queue_dir(root)
    out = {}
    for sub in ("todo", "claimed", "done", "failed"):
        files = sorted(os.listdir(os.path.join(q, sub)))
        out[sub] = {"n": len(files), "tags": [f[6:-5] for f in files[:40]]}
    fails = []
    for f in sorted(os.listdir(os.path.join(q, "failed"))):
        rec = load_json(os.path.join(q, "failed", f), {})
        fails.append({"tag": rec.get("tag"), "rc": rec.get("returncode"),
                      "log": rec.get("log")})
    out["failures"] = fails
    return out


def main(argv=None):
    p = argparse.ArgumentParser(prog="prod.launcher")
    p.add_argument("--plan", action="store_true")
    p.add_argument("--run", action="store_true")
    p.add_argument("--status", action="store_true")
    p.add_argument("--gpus", type=int, default=1)
    p.add_argument("--gpu-ids", dest="gpu_ids", default=None)
    p.add_argument("--workers-per-gpu", dest="workers_per_gpu", type=int, default=None,
                   help="slots per GPU (PP3 decision 1; default %d). Workers on one GPU are "
                        "separate processes with the same CUDA_VISIBLE_DEVICES and are admitted "
                        "only while the GPU's running memory estimate stays under --util x the "
                        "device memory." % cfgmod.WORKERS_PER_GPU)
    p.add_argument("--device-gb", dest="device_gb", type=float, default=None,
                   help="per-GPU memory in GB, instead of torch.cuda.mem_get_info")
    p.add_argument("--util", dest="util", type=float, default=None,
                   help="fraction of device memory a GPU's running sum may use (default %.2f)"
                        % cfgmod.MEM_UTIL)
    p.add_argument("--no-memory-placement", dest="mem_placement", action="store_false",
                   default=True, help="claim in queue order with no admission control (PP2)")
    p.add_argument("--shards", type=int, default=1)
    p.add_argument("--priority", default=None)
    p.add_argument("--dry-run-n", dest="dry_run_n", type=int, default=None)
    p.add_argument("--max-jobs", dest="max_jobs", type=int, default=None)
    p.add_argument("--root", default=None)
    p.add_argument("--python", default=None)
    p.add_argument("--extra", default="", help="extra arguments passed to every prod.generate call")
    p.add_argument("--only", default=None,
                   help="restrict the plan to jobs whose tag contains one of these substrings")
    cfgmod.add_args(p)
    p.add_argument("--no-requeue", dest="requeue", action="store_false", default=True,
                   help="do not move stale claims back to todo before running (a second concurrent "
                        "launcher on the same queue must pass this or --requeue-age)")
    p.add_argument("--requeue-age", dest="requeue_age", type=float, default=0.0,
                   help="only re-queue claims older than this many seconds")
    a = p.parse_args(argv)
    cfg = cfgmod.from_args(a)
    if a.util is not None:
        cfg["mem_util"] = float(a.util)
    wpg = int(a.workers_per_gpu or cfg.get("workers_per_gpu") or 1)
    cfg["workers_per_gpu"] = wpg
    prs = [int(x) for x in a.priority.split(",")] if a.priority else None
    fn = cfg["forced_block"].get("n")
    fn = fn if isinstance(fn, dict) else None
    extra = [x for x in a.extra.split() if x]
    if a.status:
        st = status(a.root)
        print(json.dumps({k: v["n"] if isinstance(v, dict) and "n" in v else v
                          for k, v in st.items()}, indent=2, default=str))
        save_json(os.path.join(a.root or ART, "launcher_status.json"), st)
        return st
    q = queue_dir(a.root)
    existing = sum(len(os.listdir(os.path.join(q, sub)))
                   for sub in ("todo", "claimed", "done", "failed"))
    # `--run` on its own must NEVER re-plan a queue that already exists. It used to, and because a
    # bare `--run` carries none of the `--plan` filters (--only, --priority, --dry-run-n) it silently
    # replaced a two-job N=20 queue with the whole 294-job FULL-N run list -- which is exactly what
    # gate G5 caught on 2026-09-12 when its restart step began a 1319-problem job. A queue is planned
    # when --plan is given, or when --run finds no queue at all.
    if a.plan or (a.run and existing == 0):
        if a.run and existing == 0 and not a.plan:
            print("[launcher] no queue under %s; planning one from these arguments" % q)
        written, q = plan(a.gpus, a.shards, prs, fn, a.dry_run_n, a.root, extra,
                          only=(a.only.split(",") if a.only else None), cfg=cfg,
                          workers_per_gpu=wpg, device_gb=a.device_gb)
        print("queued %d jobs in %s (%d gpu(s) x %d worker(s), config %s)"
              % (len(written), q, a.gpus, wpg, cfgmod.digest(cfg)[:12]))
        for r in written[:12]:
            print("  p%d %-52s %s" % (r["priority"], r["tag"], " ".join(r["cmd"][2:])))
        if len(written) > 12:
            print("  ... and %d more" % (len(written) - 12))
    elif a.run:
        print("[launcher] using the existing queue in %s (%d job files); pass --plan to rewrite it"
              % (q, existing))
    if a.run:
        if a.requeue:
            requeue_claimed(queue_dir(a.root), a.requeue_age)
        ids = ([int(x) for x in a.gpu_ids.split(",")] if a.gpu_ids else list(range(a.gpus)))
        budget = None
        if a.mem_placement and (wpg > 1 or a.device_gb):
            dev, src = device_bytes(max(ids) + 1, a.device_gb)
            if dev:
                budget = GpuBudget({g: int(cfg["mem_util"] * dev.get(g, min(dev.values())))
                                    for g in ids})
                print("[launcher] memory placement ON (%s, util %.2f): %s"
                      % (src, cfg["mem_util"],
                         {g: "%.1f GB" % (budget.budgets[g] / 1024 ** 3) for g in ids}), flush=True)
            else:
                print("[launcher] memory placement OFF: device memory %s; pass --device-gb" % src,
                      flush=True)
        slots = [(g, w) for g in ids for w in range(wpg)]
        if len(slots) == 1:
            run_worker(q, slots[0][0], a.root, a.python, a.max_jobs, slot=0, budget=budget)
        else:
            import threading
            ts = [threading.Thread(target=run_worker,
                                   args=(q, g, a.root, a.python, a.max_jobs, w, budget),
                                   name="gpu%d.w%d" % (g, w)) for (g, w) in slots]
            for t in ts:
                t.start()
            for t in ts:
                t.join()
        st = status(a.root)
        if budget is not None and budget.blocked:
            st["unplaceable"] = budget.blocked
            print("[launcher] %d job(s) never fit on an idle GPU and were left in the queue: %s"
                  % (len(budget.blocked),
                     ", ".join(b["job"] for b in budget.blocked[:6])), flush=True)
            save_json(os.path.join(a.root or ART, "launcher_status.json"), st)
        print(json.dumps({k: v["n"] for k, v in st.items()
                          if isinstance(v, dict) and "n" in v}, indent=2))
    return None


if __name__ == "__main__":
    main()
