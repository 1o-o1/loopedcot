#!/bin/bash
# The allocator v6 pass and its live check on the cluster. Run from anywhere:
#   bash slurm/v6.sh alloc            # CPU job array: alloc.cli on every (task, model) pair of the natural grid -> artifacts/alloc_v6_<task>_<model>/
#   bash slurm/v6.sh alloc natural2   # the same on the think-tag continuation grids that are complete (Thinking checkpoints) -> alloc_v6n2_*
#   bash slurm/v6.sh alloc natural2h  # the same on the horizon-extension grids that are complete -> alloc_v6h_*
#   bash slurm/v6.sh live             # GPU jobs: prod.live_check, both arms x both fractions, every pair except huginn_0125 and
#                                     # ouro_2_6b_think on gsm8k/svamp; a Thinking pair reads alloc_v6n2 and waits until it exists;
#                                     # the first job of a pair carries --preflight; a pair with a live_${V}_*.FAILED.json is stopped
#   bash slurm/v6.sh status           # what is done, running, failed; the stderr tail of every FAILED live check
#   bash slurm/v6.sh collect          # Table 1 rows per pair, the gated deviation lines, the pooled live-minus-grid per arm and fraction
# Every job log ends with RC=<exit code>, and the batch job exits with it. Re-running any mode only submits what is missing.
# Knobs: V (v6; V=v7 renames every output alloc_v7_* / live_v7_*) LIVE_ALL (1 = no pair excluded from live) ALLOC_CPUS (4) ALLOC_MEM (32gb) ALLOC_TIME (03:00:00) LIVE_TIME (24:00:00) LIVE_MEM (64gb) SBATCH_EXTRA MODELS TASKS
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
source "$ROOT/env.sh"
mkdir -p logs
MODE="${1:-}"; PROTO="${2:-natural}"
V="${V:-v6}"                      # allocator version in every output name: alloc_<V>_*, live_<V>_*; V=v7 for the v7 pass
MODELS="${MODELS:-ouro_1_4b_base ouro_1_4b_think ouro_2_6b_base ouro_2_6b_think mcleish_llama32_r32 huginn_0125}"
TASKS="${TASKS:-gsm8k math500 svamp aqua csqa arc strategyqa bbh mmlu hellaswag}"
ARMS="avg_gated_equation_resolved avg_gated_lookup"
BUDGETS="0.5 1.0"
ALLOC_CPUS="${ALLOC_CPUS:-4}"; ALLOC_MEM="${ALLOC_MEM:-32gb}"; ALLOC_TIME="${ALLOC_TIME:-03:00:00}"
LIVE_TIME="${LIVE_TIME:-24:00:00}"; LIVE_MEM="${LIVE_MEM:-64gb}"
EXTRA="${SBATCH_EXTRA:-}"
ALLOC_FLAGS="--model-config prod/config.yaml --accounting all --avg-budget --promptfree --boot 2000"

case "$PROTO" in
  natural)   PREFIX=alloc_${V} ;;
  natural2)  PREFIX=alloc_${V}n2 ;;
  natural2h) PREFIX=alloc_${V}h ;;
  *) echo "unknown protocol $PROTO (natural, natural2, natural2h)"; exit 1 ;;
esac

exclude_arg() { [ -s logs/bad_nodes.txt ] && echo "--exclude=$(paste -sd, logs/bad_nodes.txt)"; }
in_queue() { squeue -u "$USER" -h -n "$1" -o %j | grep -qx "$1"; }
alloc_done() { $PROD_PYTHON -c "import json,sys; r=json.load(open(sys.argv[1])); sys.exit(0 if r.get('picks') else 1)" "$PROD_ART/${1}_${2}_${3}/results.json" 2>/dev/null; }
grid_complete() {  # grid_complete <model> <task> <protocol>: every meta of that grid says cells_written >= cells_expected > 0
  $PROD_PYTHON - "$PROD_ART" "$1" "$2" "$3" <<'EOF'
import glob, json, sys
art, m, t, proto = sys.argv[1:]
metas = glob.glob("%s/meta_%s_%s_%s_k*.json" % (art, m, t, proto))
ok = bool(metas)
for p in metas:
    j = json.load(open(p))
    ok = ok and int(j.get("cells_written", 0)) >= int(j.get("cells_expected", 0)) > 0
sys.exit(0 if ok else 1)
EOF
}
alloc_dir_of() { case "$1" in ouro_*think) echo "$PROD_ART/alloc_${V}n2_${2}_${1}" ;; *) echo "$PROD_ART/alloc_${V}_${2}_${1}" ;; esac; }
live_pair_wanted() {  # the pairs the live check runs on; LIVE_ALL=1 lifts the exclusions (e.g. for the natural2 grids)
  [ "${LIVE_ALL:-0}" = 1 ] && return 0
  case "$1" in huginn_0125) return 1 ;; ouro_2_6b_think) case "$2" in gsm8k|svamp) return 1 ;; esac ;; esac; return 0
}

case "$MODE" in
  alloc)
    LIST="logs/${PREFIX}_pairs.txt"; : > "$LIST"
    for M in $MODELS; do for T in $TASKS; do
      if [ "$PROTO" != natural ]; then
        case "$PROTO:$M" in natural2:ouro_*think) ;; natural2:*) continue ;; esac   # natural2 exists for the Thinking checkpoints only
        ls "$PROD_ART"/meta_${M}_${T}_${PROTO}_k*.json >/dev/null 2>&1 || continue   # this pair has no such grid at all: not part of the run
        grid_complete "$M" "$T" "$PROTO" || { echo "  not complete yet: $PROTO $T $M"; continue; }
      fi
      alloc_done "$PREFIX" "$T" "$M" && { echo "  done   $PREFIX $T $M"; continue; }
      in_queue "${PREFIX}_${T}_${M}" && { echo "  queued $PREFIX $T $M"; continue; }
      echo "$M $T" >> "$LIST"
    done; done
    n=$(wc -l < "$LIST")
    [ "$n" -gt 0 ] || { echo "$PREFIX: nothing to submit"; exit 0; }
    jid=$(sbatch --parsable $EXTRA --job-name="${PREFIX}" --array="0-$((n - 1))" --cpus-per-task="$ALLOC_CPUS" --mem="$ALLOC_MEM" \
      --time="$ALLOC_TIME" --output="logs/${PREFIX}_%A_%a.out" \
      --wrap="cd '$ROOT' && . '$ROOT/env.sh' && line=\$(sed -n \$((SLURM_ARRAY_TASK_ID + 1))p '$ROOT/$LIST') && set -- \$line && M=\$1 && T=\$2 && echo \"pair \$T \$M\" && $PROD_PYTHON -m alloc.cli --cells \"\$PROD_ART\" --task \"\$T\" --checkpoint \"\$M\" --protocol $PROTO $ALLOC_FLAGS --out \"\$PROD_ART/${PREFIX}_\${T}_\${M}\"; rc=\$?; echo RC=\$rc; exit \$rc")
    echo "$PREFIX: $n pairs in job array $jid (logs/${PREFIX}_${jid}_<i>.out)" ;;
  live)
    n=0
    for M in $MODELS; do for T in $TASKS; do
      live_pair_wanted "$M" "$T" || continue
      ad=$(alloc_dir_of "$M" "$T")
      [ -f "$ad/results.json" ] || { echo "  waiting $T $M: no $(basename "$ad")/results.json yet"; continue; }
      if ls "$PROD_ART"/live_${V}_${T}_${M}_*.FAILED.json >/dev/null 2>&1; then
        echo "  STOPPED $T $M: $(ls "$PROD_ART"/live_${V}_${T}_${M}_*.FAILED.json | xargs -n1 basename | paste -sd,) (see: bash slurm/v6.sh status)"; continue
      fi
      first=1
      for ARM in $ARMS; do for B in $BUDGETS; do
        name="live_${V}_${T}_${M}_${ARM}_b${B}"; out="$PROD_ART/live_${V}_${T}_${M}_${ARM}_b${B}.json"
        [ -f "$out" ] && { first=0; continue; }
        in_queue "$name" && { first=0; continue; }
        pre=""; [ "$first" = 1 ] && pre="--preflight"; first=0
        sbatch --parsable $EXTRA $(exclude_arg) --job-name="$name" --gres=gpu:1 --cpus-per-task=8 --mem="$LIVE_MEM" --time="$LIVE_TIME" \
          --output="logs/${name}.out" \
          --wrap="echo node=\$(hostname); cd '$ROOT' && . '$ROOT/env.sh' && $PROD_PYTHON -m prod.live_check --model=$M --task=$T --cells=\"\$PROD_ART\" --alloc-dir='$ad' --budget-fraction=$B --arm $ARM $pre --out='$out'; rc=\$?; echo RC=\$rc; exit \$rc" > /dev/null
        n=$((n + 1))
      done; done
    done; done
    echo "live: $n jobs submitted" ;;
  status)
    for pfx in alloc_${V} alloc_${V}n2 alloc_${V}h; do
      d=$(ls -d "$PROD_ART"/${pfx}_*/ 2>/dev/null | wc -l); ok=0
      for r in "$PROD_ART"/${pfx}_*/results.json; do [ -f "$r" ] && grep -q '"picks"' "$r" && ok=$((ok + 1)); done
      echo "$pfx: $ok pairs with picks ($d directories); array logs failed: $(grep -l '^RC=[1-9]' logs/${pfx}_*_*.out 2>/dev/null | wc -l)"
    done
    all=$(ls logs/live_${V}_*.out 2>/dev/null | wc -l); fin=$(grep -l "^RC=" logs/live_${V}_*.out 2>/dev/null | wc -l); ok=$(grep -l "^RC=0" logs/live_${V}_*.out 2>/dev/null | wc -l)
    echo "live: $all started, $fin finished, $ok ok, $((fin - ok)) failed, $((all - fin)) running; results: $(ls "$PROD_ART"/live_${V}_*.json 2>/dev/null | grep -vc FAILED); queued/running: $(squeue -u "$USER" -h | wc -l)"
    for f in "$PROD_ART"/live_${V}_*.FAILED.json; do
      [ -f "$f" ] || continue
      echo "== FAILED $(basename "$f")"
      $PROD_PYTHON - "$f" <<'EOF'
import json, sys
j = json.load(open(sys.argv[1]))
def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if "stderr" in k and v: print("  %s%s:" % (path, k)); print("    " + str(v).replace("\n", "\n    ")[-2500:])
            else: walk(v, path + k + ".")
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, path + "%d." % i)
walk(j)
EOF
    done
    for f in logs/live_${V}_*.out; do [ -f "$f" ] && grep -q "^RC=" "$f" && ! grep -q "^RC=0" "$f" && { echo "== log $f"; tail -15 "$f"; }; done ;;
  collect)
    $PROD_PYTHON - "$PROD_ART" "$V" <<'EOF'
import glob, json, os, re, sys
art, V = sys.argv[1], sys.argv[2]
ROWS = ["default", "default_at_budget", "avg_gated_equation_resolved", "avg_gated_lookup", "equation_resolved", "lookup"]
for pfx in ("alloc_" + V, "alloc_" + V + "n2", "alloc_" + V + "h"):
    paths = sorted(glob.glob(os.path.join(art, pfx + "_*", "results.json")))
    if not paths:
        continue
    print("=" * 30, pfx, "expected accounting, accuracy pts at 0.25 / 0.5 / 0.75 / 1.0 x default cost, oracle gap at 1.0x")
    for p in paths:
        r = json.load(open(p)); t = r["table1_by_accounting"]["expected"]
        name = os.path.basename(os.path.dirname(p))[len(pfx) + 1:]
        print("-- %s  (n_eval %d, n_cal %d)" % (name, t.get("n_eval", 0), r.get("picks", {}).get("calibration", {}).get("n_cal", 0)))
        for arm in ROWS:
            row = t["rows"].get(arm)
            if not row:
                print("   %-28s -" % arm); continue
            acc = " ".join("%5.1f" % v if v == v else "  n/f" for v in row["acc_pts"])
            gap = row.get("oracle_gap_pts"); print("   %-28s %s   gap %s" % (arm, acc, ("%+.1f" % gap) if gap is not None else "-"))
        md = os.path.join(os.path.dirname(p), "table1_expected.md")
        if os.path.exists(md):
            for line in open(md, encoding="utf-8"):
                if line.startswith("- `avg_gated_") and ("deviated" in line or "reverted" in line):
                    print("   " + line.strip()[:400])
print("=" * 30, "live minus grid, pooled over pairs (points), realised price over budget (mean of pairs, %)")
pool = {}
for p in sorted(glob.glob(os.path.join(art, "live_%s_*.json" % V))):
    if p.endswith(".FAILED.json"):
        continue
    j = json.load(open(p))
    if j.get("live_acc") is None:
        continue
    k = (j["arm"], float(j["budget_fraction"])); n = int(j.get("n_live_rows") or 0)
    d = pool.setdefault(k, [0, 0.0, 0.0, [], []])
    d[0] += n; d[1] += j["live_acc"] * n; d[2] += j["grid_acc_same_rows"] * n; d[3].append(j["task"] + "/" + j["model"])
    if j.get("price_over_budget_pct") is not None: d[4].append(j["price_over_budget_pct"])
for (arm, b), (n, la, ga, pairs, pr) in sorted(pool.items()):
    print("%-28s %.2fx  n=%6d over %2d pairs  live %.2f  grid %.2f  delta %+.2f pts  price over budget %+.1f%%"
          % (arm, b, n, len(pairs), 100 * la / n, 100 * ga / n, 100 * (la - ga) / n, (sum(pr) / len(pr)) if pr else float("nan")))
fails = sorted(glob.glob(os.path.join(art, "live_%s_*.FAILED.json" % V)))
print("failed live checks: %d %s" % (len(fails), " ".join(os.path.basename(f) for f in fails)))
EOF
    ;;
  *) echo "usage: bash slurm/v6.sh alloc [natural|natural2|natural2h] | live | status | collect"; exit 1 ;;
esac
