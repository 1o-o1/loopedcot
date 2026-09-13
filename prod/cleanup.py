"""Cleanup for a cells directory (PP3b task 4): shrink completed jobs' cells files, drop their
per-problem trace checkpoints, and gzip stale logs.

  python -m prod.cleanup --cells=DIR                          # dry run: print bytes that would free
  python -m prod.cleanup --cells=DIR --apply                  # do it
  python -m prod.cleanup --cells=DIR --manifest=artifacts/manifest.json --apply
  python -m prod.cleanup --logs=logs --apply                  # gzip logs older than a day

(a) For every `cells_<tag>.jsonl` whose job is COMPLETE (see below), write `cells_<tag>.slim.jsonl`
    with the long text fields (`answer_text`, `trace_text`) dropped from every row. Every numeric
    field, both parsed answers (`pred`, `trace_answer`), the labels (`correct`, `trace_correct`,
    `correct_v2`, `split`, `kind`, `gold`, ...) and the natural-stop position (`natural_stop`,
    `stop_marker`) are kept untouched -- only the two named text fields are removed, and only if
    present. The header row (`_header: true`) is copied verbatim. `--apply` REPLACES the original
    file with the slim one; without it the original is untouched and the slim file is written
    alongside it so it can be inspected before committing.
(b) Deletes `trace_<tag>_*.jsonl`, the per-problem generation checkpoints, for the same complete
    jobs -- `prod.generate` only reads a trace file to resume an INCOMPLETE job, so once every cell
    is written it is never read again. `--apply` required; a dry run only lists them and sums bytes.
(c) gzips every `*.log` under `--logs` older than `--older-than-hours` (default 24) that is not
    already gzipped, and removes the original with `--apply`.

COMPLETE means the job's own `meta_<tag>.json` says `cells_written >= cells_expected > 0`. When
`--manifest` is given (the production run list, `prod.manifest --write`'s output), a tag is complete
only if the manifest ALSO expects that many cells for it -- a 20-problem smoke run's meta says "done"
for the 20 it was given, but the production job for the same tag is still open, and `--manifest` is
how the two are told apart.

Nothing here reads or writes `prod/tasks/data/`, `s33/`, or a cells directory's `*.slim.jsonl` twice
(a tag already slimmed is skipped, not re-processed).
"""
import argparse
import gzip
import glob
import json
import os
import re
import shutil
import time

from .common import ART, LOGS, load_json, save_json

LONG_TEXT_FIELDS = ("answer_text", "trace_text")
CELLS_RE = re.compile(r"^cells_(?P<tag>.+)\.jsonl$")


# ------------------------------------------------------------------ (a) slim the cells files
def slim_row(row):
    """Drop the long text fields, keep everything else (numeric fields, both parsed answers, the
    labels, the natural-stop position) exactly as they are."""
    if not isinstance(row, dict):
        return row
    out = {k: v for k, v in row.items() if k not in LONG_TEXT_FIELDS}
    return out


def slim_file(src, dst):
    """Write `dst` as `src` with the long text fields stripped from every non-header row.

    Returns (src_bytes, dst_bytes, n_rows). Never touches `src`.
    """
    src_bytes, dst_bytes, n_rows = 0, 0, 0
    with open(src, encoding="utf-8") as fin, open(dst, "w", encoding="utf-8") as fout:
        for line in fin:
            raw = line.rstrip("\n")
            if not raw:
                continue
            src_bytes += len(line.encode("utf-8"))
            try:
                row = json.loads(raw)
            except Exception:                                 # noqa: BLE001
                fout.write(line if line.endswith("\n") else line + "\n")
                dst_bytes += len(line.encode("utf-8"))
                continue
            if isinstance(row, dict) and row.get("_header"):
                out_line = json.dumps(row) + "\n"
            else:
                out_line = json.dumps(slim_row(row)) + "\n"
                n_rows += 1
            fout.write(out_line)
            dst_bytes += len(out_line.encode("utf-8"))
    return src_bytes, dst_bytes, n_rows


# ------------------------------------------------------------------ completeness
def job_complete(cells_dir, tag, manifest_by_tag=None):
    """(complete, cells_expected, cells_written, reason)."""
    meta = load_json(os.path.join(cells_dir, "meta_%s.json" % tag), None)
    if not meta:
        return False, None, None, "no meta_%s.json" % tag
    ce, cw = meta.get("cells_expected"), meta.get("cells_written")
    if not ce or cw is None:
        return False, ce, cw, "meta has no cells_expected/cells_written (job still running?)"
    if cw < ce:
        return False, ce, cw, "partial: %d/%d cells" % (cw, ce)
    if manifest_by_tag is not None:
        want = manifest_by_tag.get(tag)
        if want is not None and int(want) != int(ce):
            return False, ce, cw, ("meta says done at %d cells but the manifest expects %d for "
                                   "this tag (a smoke/partial-N run, not the production job)"
                                   % (ce, want))
    return True, ce, cw, "complete"


def load_manifest_expected(path):
    """{tag: expected_cells} from a `prod.manifest --write` output, shard jobs preferred."""
    man = load_json(path, None)
    if not man:
        return None
    jobs = man.get("shard_jobs") or man.get("jobs") or []
    return {j["tag"]: j["expected_cells"] for j in jobs if "tag" in j}


# ------------------------------------------------------------------ (b) trace checkpoints
def trace_files_for(cells_dir, tag):
    """Per-problem generation checkpoints for one job. Never a `chains_<model>_<task>_k<k>.jsonl`
    sidecar (Fix 1, PP3b): those carry no tag in their name and the glob below cannot match one, but
    the filter is kept anyway as an explicit guarantee that cleanup never deletes a chains file."""
    found = sorted(glob.glob(os.path.join(cells_dir, "trace_%s_*.jsonl" % tag)))
    return [f for f in found if not os.path.basename(f).startswith("chains_")]


# ------------------------------------------------------------------ (c) logs
def stale_logs(logs_dir, older_than_hours=24.0):
    now = time.time()
    out = []
    if not os.path.isdir(logs_dir):
        return out
    for fn in sorted(os.listdir(logs_dir)):
        if not fn.endswith(".log"):
            continue
        p = os.path.join(logs_dir, fn)
        if (now - os.path.getmtime(p)) >= older_than_hours * 3600.0:
            out.append(p)
    return out


# ------------------------------------------------------------------ driver
def run(cells_dir, manifest_path=None, logs_dir=None, older_than_hours=24.0, apply=False):
    manifest_by_tag = load_manifest_expected(manifest_path) if manifest_path else None
    report = {"cells_dir": cells_dir, "manifest": manifest_path, "apply": bool(apply),
             "cells": [], "traces": [], "logs": [],
             "bytes_freed_cells": 0, "bytes_freed_traces": 0, "bytes_freed_logs": 0}

    for fp in sorted(glob.glob(os.path.join(cells_dir, "cells_*.jsonl"))):
        fn = os.path.basename(fp)
        if fn.endswith(".slim.jsonl"):
            continue
        m = CELLS_RE.match(fn)
        if not m:
            continue
        tag = m.group("tag")
        complete, ce, cw, reason = job_complete(cells_dir, tag, manifest_by_tag)
        rec = {"tag": tag, "file": fn, "complete": complete, "cells_expected": ce,
              "cells_written": cw, "reason": reason}
        if complete:
            slim_path = fp[:-len(".jsonl")] + ".slim.jsonl"
            src_b, dst_b, n_rows = slim_file(fp, slim_path)
            freed = max(0, src_b - dst_b)
            rec.update({"slim_file": os.path.basename(slim_path), "src_bytes": src_b,
                       "slim_bytes": dst_b, "bytes_freed": freed, "n_rows": n_rows})
            report["bytes_freed_cells"] += freed
            if apply:
                os.replace(slim_path, fp)
                rec["applied"] = True
            trs = trace_files_for(cells_dir, tag)
            tr_bytes = sum(os.path.getsize(t) for t in trs)
            report["traces"].append({"tag": tag, "files": [os.path.basename(t) for t in trs],
                                     "bytes": tr_bytes, "deleted": bool(apply and trs)})
            report["bytes_freed_traces"] += tr_bytes
            if apply:
                for t in trs:
                    os.remove(t)
        report["cells"].append(rec)

    logs_dir = logs_dir or LOGS
    for p in stale_logs(logs_dir, older_than_hours):
        b = os.path.getsize(p)
        gz = p + ".gz"
        entry = {"file": os.path.basename(p), "bytes": b, "gzipped": False}
        if apply:
            with open(p, "rb") as fin, gzip.open(gz, "wb") as fout:
                shutil.copyfileobj(fin, fout)
            gz_b = os.path.getsize(gz)
            os.remove(p)
            entry.update({"gzipped": True, "gz_bytes": gz_b, "bytes_freed": max(0, b - gz_b)})
            report["bytes_freed_logs"] += max(0, b - gz_b)
        else:
            # dry run: gzip's typical ratio on a text log is ~loose; report the raw bytes at stake
            # (the whole file, since nothing is written) rather than guess a compressed size.
            report["bytes_freed_logs"] += b
        report["logs"].append(entry)

    report["bytes_freed_total"] = (report["bytes_freed_cells"] + report["bytes_freed_traces"]
                                   + report["bytes_freed_logs"])
    report["n_complete_jobs"] = sum(1 for r in report["cells"] if r["complete"])
    report["n_jobs_seen"] = len(report["cells"])
    return report


def main(argv=None):
    p = argparse.ArgumentParser(prog="prod.cleanup")
    p.add_argument("--cells", default=None, help="cells directory (default artifacts/)")
    p.add_argument("--manifest", default=None,
                   help="prod.manifest --write output; a tag counts complete only if this also "
                        "expects that many cells for it")
    p.add_argument("--logs", default=None, help="logs directory (default the package's logs/)")
    p.add_argument("--older-than-hours", dest="older_than_hours", type=float, default=24.0)
    p.add_argument("--apply", action="store_true",
                   help="without this: dry run, print the bytes that would be freed, touch nothing "
                        "but the new *.slim.jsonl files")
    p.add_argument("--out", default=None)
    a = p.parse_args(argv)
    cells_dir = a.cells or ART
    rep = run(cells_dir, a.manifest, a.logs, a.older_than_hours, a.apply)
    dest = a.out or os.path.join(cells_dir, "cleanup_report.json")
    save_json(dest, rep)
    print("[cleanup] %s: %d/%d jobs complete; bytes freed: cells=%d traces=%d logs=%d total=%d%s"
          % (cells_dir, rep["n_complete_jobs"], rep["n_jobs_seen"], rep["bytes_freed_cells"],
             rep["bytes_freed_traces"], rep["bytes_freed_logs"], rep["bytes_freed_total"],
             "" if a.apply else " (DRY RUN -- pass --apply to actually free them)"))
    for r in rep["cells"]:
        if not r["complete"]:
            print("  skip  %-56s %s" % (r["tag"], r["reason"]))
        else:
            print("  slim  %-56s %8d -> %8d bytes (%d rows)"
                  % (r["tag"], r["src_bytes"], r["slim_bytes"], r["n_rows"]))
    print("wrote", dest)
    return rep


if __name__ == "__main__":
    main()
