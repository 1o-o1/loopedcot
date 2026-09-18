#!/bin/bash
# Chain-continuation runs (prod.generate --continue-chains): one Slurm job per (model, task, depth), one GPU
# each, ALL submitted at once so the scheduler fills every free GPU on every node. Run from anywhere:
#   bash slurm/continue_chains.sh c1      # think-tag continuation: 2 Thinking checkpoints x 10 tasks x depths 1-4 = 80 jobs
#   bash slurm/continue_chains.sh c2      # horizon 4096 -> 8192 on the ten (model, task, depth) below; a Thinking job
#                                         # waits for its c1 job (afterok) and continues from the natural2 cells
#   bash slurm/continue_chains.sh c2more  # the four extra k=2 Thinking jobs, only once c2 is done and GPUs are idle
#   bash slurm/continue_chains.sh status  # finished / failed counts, and the last 30 log lines of every failed job
#   bash slurm/continue_chains.sh report  # per c2 job: rows continued, share stopped before 8192, accuracy at caps 4096 and 8192
# Every job log ends with RC=<exit code of prod.generate>. Outputs: cells_<model>_<task>_natural2_k<K>.jsonl (c1)
# and cells_<model>_<task>_natural2h_k<K>.jsonl (c2) beside the natural grid, plus their meta files.
# Knobs (export before running): TIME_C1 (24:00:00) TIME_C2 (48:00:00) MEM (64gb) CPUS (8) SBATCH_EXTRA HITLIST
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
source "$ROOT/env.sh"
mkdir -p logs
MODE="${1:-}"
TIME_C1="${TIME_C1:-24:00:00}"; TIME_C2="${TIME_C2:-48:00:00}"; MEM="${MEM:-64gb}"; CPUS="${CPUS:-8}"
EXTRA="${SBATCH_EXTRA:-}"
CAPS_C1="0,16,32,64,128,256,512,1024,2048,4096"
CAPS_C2="0,16,32,64,128,256,512,1024,2048,4096,8192"
# The horizon-extension set (model:task:depth): the deepest depths of the two tasks whose chains run into the
# 4096 horizon most (MATH500, AQuA) on the Thinking checkpoints, and McLeish's deepest depth on MATH500 and
# StrategyQA. The full >= 5% horizon-hit list is 83 jobs and was cut to these ten on 2026-09-17.
HITLIST="${HITLIST:-ouro_1_4b_think:math500:4 ouro_1_4b_think:math500:3 ouro_1_4b_think:aqua:4 ouro_1_4b_think:aqua:3 ouro_2_6b_think:math500:4 ouro_2_6b_think:math500:3 ouro_2_6b_think:aqua:4 ouro_2_6b_think:aqua:3 mcleish_llama32_r32:math500:8 mcleish_llama32_r32:strategyqa:8}"
HITLIST_MORE="ouro_1_4b_think:math500:2 ouro_1_4b_think:aqua:2 ouro_2_6b_think:math500:2 ouro_2_6b_think:aqua:2"

width_for() {  # the batch width for 8192-token sequences: half the width the 4096 grid used for this model/depth
  case "$1:$2" in
    ouro_2_6b_think:3|ouro_2_6b_think:4|ouro_2_6b_base:3|ouro_2_6b_base:4) echo 4 ;;   # 4096 override is 8
    huginn_0125:16) echo 4 ;; huginn_0125:32) echo 2 ;;                                 # 4096 overrides 8 and 4
    *) echo 8 ;;                                                                         # config batch_width 16
  esac
}

submit() {  # submit <name> <time> <dependency or ""> <command...>
  local name="$1" time="$2" dep="$3"; shift 3
  sbatch --parsable $EXTRA ${dep:+--dependency=afterok:$dep} --job-name="$name" --gres=gpu:1 \
    --cpus-per-task="$CPUS" --mem="$MEM" --time="$time" --output="logs/${name}.out" \
    --wrap="cd '$ROOT' && $* ; echo RC=\$?"
}

submit_c2() {  # submit_c2 <list>
  local n=0 M T K dep src
  for item in $1; do
    IFS=: read -r M T K <<< "$item"
    dep=""; src=""
    if [[ "$M" == ouro_* ]]; then
      [ -f logs/c1_jobs.txt ] || { echo "run c1 first: logs/c1_jobs.txt missing"; exit 1; }
      dep=$(awk -v m="$M" -v t="$T" -v k="$K" '$1==m && $2==t && $3==k {print $4}' logs/c1_jobs.txt)
      [ -n "$dep" ] || { echo "no c1 job recorded for $M $T k$K; skipped"; continue; }
      src="--continue-from-cells=$PROD_ART/cells_${M}_${T}_natural2_k${K}.jsonl"
    fi
    submit "c2_${T}_${M}_k${K}" "$TIME_C2" "$dep" "$PROD_PYTHON -m prod.generate --model=$M --task=$T --k=$K --protocol=natural --out=$PROD_ART --continue-chains=horizon --protocol-tag=natural2h --horizon=8192 --old-horizon=4096 --caps=$CAPS_C2 --no-extra-caps --batch-width=$(width_for "$M" "$K") $src" > /dev/null
    n=$((n + 1))
  done
  echo "c2: $n jobs submitted"
}

case "$MODE" in
  c1)
    : > logs/c1_jobs.txt
    for M in ouro_1_4b_think ouro_2_6b_think; do for T in gsm8k math500 svamp aqua csqa arc strategyqa bbh mmlu hellaswag; do for K in 1 2 3 4; do
      jid=$(submit "c1_${T}_${M}_k${K}" "$TIME_C1" "" "$PROD_PYTHON -m prod.generate --model=$M --task=$T --k=$K --protocol=natural --out=$PROD_ART --continue-chains=think_tag --protocol-tag=natural2 --horizon=4096 --old-horizon=4096 --caps=$CAPS_C1 --no-extra-caps --no-think-tag-is-stop")
      echo "$M $T $K $jid" >> logs/c1_jobs.txt
    done; done; done
    echo "c1: $(wc -l < logs/c1_jobs.txt) jobs submitted (ids in logs/c1_jobs.txt)" ;;
  c2)      submit_c2 "$HITLIST" ;;
  c2more)  submit_c2 "$HITLIST_MORE" ;;
  status)
    for stage in c1 c2; do
      all=$(ls logs/${stage}_*.out 2>/dev/null | wc -l); ok=$(grep -l "^RC=0" logs/${stage}_*.out 2>/dev/null | wc -l)
      done_any=$(grep -l "^RC=" logs/${stage}_*.out 2>/dev/null | wc -l)
      echo "$stage: $all started, $done_any finished, $ok ok, $((done_any - ok)) failed, $((all - done_any)) running"
    done
    for f in logs/c1_*.out logs/c2_*.out; do
      [ -f "$f" ] || continue
      grep -q "^RC=" "$f" && ! grep -q "^RC=0" "$f" && { echo "== FAILED $f"; tail -30 "$f"; }
    done
    echo "queued/running: $(squeue -u "$USER" -h | wc -l)" ;;
  report)
    $PROD_PYTHON - "$PROD_ART" <<'EOF'
import glob, json, os, re, sys
art = sys.argv[1]
OLD, NEW = 4096, 8192
def stops(path, cap):
    """{row_idx: natural_stop} read off the rows at one cap (natural_stop is per problem)."""
    out = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if r.get("_header") or int(r["B"]) != cap:
                continue
            out[int(r.get("row_idx", r.get("idx")))] = r.get("natural_stop")
    return out
print("%-22s %-11s %2s %6s %8s %8s %8s %8s" % ("model", "task", "k", "cont.", "<8192", "acc4096", "acc8192", "d_pts"))
for mp in sorted(glob.glob(os.path.join(art, "meta_*_natural2h_k*.json"))):
    m = re.match(r"meta_(.+?)_(gsm8k|math500|svamp|aqua|csqa|arc|strategyqa|bbh|mmlu|hellaswag)_natural2h_k(\d+)\.json", os.path.basename(mp))
    if not m:
        continue
    model, task, k = m.group(1), m.group(2), int(m.group(3))
    meta = json.load(open(mp))
    cont = meta.get("continue") or {}
    n_cont = cont.get("n_selected")
    cells = mp.replace("meta_", "cells_").replace(".json", ".jsonl")
    src = cont.get("source_cells") or ""
    share = float("nan")
    if os.path.exists(cells) and os.path.exists(src):
        old = stops(src, OLD)
        new = stops(cells, NEW)
        hit = [i for i, s in old.items() if s is None or int(s) >= OLD]
        if hit:
            share = sum(1 for i in hit if new.get(i) is not None and int(new[i]) < NEW) / len(hit)
            n_cont = n_cont or len(hit)
    bb = meta.get("by_budget") or {}
    a4 = (bb.get(str(OLD)) or {}).get("acc_v2"); a8 = (bb.get(str(NEW)) or {}).get("acc_v2")
    f = lambda v: ("%8.1f" % (100 * v)) if isinstance(v, (int, float)) else "%8s" % "-"
    d = ("%+8.1f" % (100 * (a8 - a4))) if isinstance(a4, (int, float)) and isinstance(a8, (int, float)) else "%8s" % "-"
    print("%-22s %-11s %2d %6s %8s %s %s %s" % (model, task, k, n_cont if n_cont is not None else "-",
          ("%7.1f%%" % (100 * share)) if share == share else "-", f(a4), f(a8), d))
EOF
    ;;
  *)
    echo "usage: bash slurm/continue_chains.sh c1|c2|c2more|status|report"; exit 1 ;;
esac
