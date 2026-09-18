#!/bin/bash
# Chain-continuation runs (prod.generate --continue-chains): one Slurm job per (model, task, depth), one GPU
# each, ALL submitted at once so the scheduler fills every free GPU on every node. Run from anywhere:
#   bash slurm/continue_chains.sh c1      # think-tag continuation: 2 Thinking checkpoints x 10 tasks x depths 1-4 = 80 jobs
#   bash slurm/continue_chains.sh c2      # horizon 4096 -> 8192 for every (model, task, depth) whose natural grid ran
#                                         # into the horizon on >= 5% of problems (83 jobs); a Thinking pair waits for
#                                         # its c1 job (afterok) and continues from the natural2 cells
#   bash slurm/continue_chains.sh status  # finished / failed counts, and the last 30 log lines of every failed job
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
# (model:task:depth) whose natural grid reached the 4096 horizon on >= 5% of problems (share of problems with no
# natural stop before the horizon at the cap-4096 rows, computed from the cells files on 2026-09-17).
HITLIST="${HITLIST:-ouro_1_4b_think:aqua:1 ouro_1_4b_think:aqua:2 ouro_1_4b_think:aqua:3 ouro_1_4b_think:aqua:4 ouro_1_4b_think:arc:1 ouro_1_4b_think:arc:2 ouro_1_4b_think:bbh:1 ouro_1_4b_think:bbh:2 ouro_1_4b_think:bbh:3 ouro_1_4b_think:bbh:4 ouro_1_4b_think:csqa:1 ouro_1_4b_think:csqa:2 ouro_1_4b_think:csqa:3 ouro_1_4b_think:csqa:4 ouro_1_4b_think:gsm8k:1 ouro_1_4b_think:gsm8k:2 ouro_1_4b_think:hellaswag:1 ouro_1_4b_think:hellaswag:2 ouro_1_4b_think:hellaswag:3 ouro_1_4b_think:hellaswag:4 ouro_1_4b_think:math500:1 ouro_1_4b_think:math500:2 ouro_1_4b_think:math500:3 ouro_1_4b_think:math500:4 ouro_1_4b_think:mmlu:1 ouro_1_4b_think:mmlu:2 ouro_1_4b_think:mmlu:3 ouro_1_4b_think:mmlu:4 ouro_1_4b_think:strategyqa:1 ouro_1_4b_think:strategyqa:2 ouro_1_4b_think:strategyqa:3 ouro_1_4b_think:strategyqa:4 ouro_1_4b_think:svamp:1 ouro_1_4b_think:svamp:2 ouro_1_4b_think:svamp:3 ouro_1_4b_think:svamp:4 ouro_2_6b_think:aqua:1 ouro_2_6b_think:aqua:2 ouro_2_6b_think:aqua:3 ouro_2_6b_think:aqua:4 ouro_2_6b_think:arc:1 ouro_2_6b_think:bbh:1 ouro_2_6b_think:bbh:2 ouro_2_6b_think:csqa:1 ouro_2_6b_think:csqa:2 ouro_2_6b_think:gsm8k:1 ouro_2_6b_think:hellaswag:1 ouro_2_6b_think:hellaswag:2 ouro_2_6b_think:math500:1 ouro_2_6b_think:math500:2 ouro_2_6b_think:math500:3 ouro_2_6b_think:math500:4 ouro_2_6b_think:mmlu:1 ouro_2_6b_think:mmlu:2 ouro_2_6b_think:strategyqa:1 ouro_2_6b_think:strategyqa:2 ouro_2_6b_think:svamp:1 ouro_2_6b_think:svamp:2 ouro_2_6b_think:svamp:3 ouro_2_6b_think:svamp:4 mcleish_llama32_r32:aqua:1 mcleish_llama32_r32:aqua:2 mcleish_llama32_r32:bbh:1 mcleish_llama32_r32:bbh:2 mcleish_llama32_r32:bbh:4 mcleish_llama32_r32:bbh:8 mcleish_llama32_r32:gsm8k:1 mcleish_llama32_r32:gsm8k:2 mcleish_llama32_r32:hellaswag:1 mcleish_llama32_r32:hellaswag:2 mcleish_llama32_r32:math500:1 mcleish_llama32_r32:math500:2 mcleish_llama32_r32:math500:4 mcleish_llama32_r32:math500:8 mcleish_llama32_r32:mmlu:1 mcleish_llama32_r32:mmlu:2 mcleish_llama32_r32:mmlu:4 mcleish_llama32_r32:mmlu:8 mcleish_llama32_r32:strategyqa:1 mcleish_llama32_r32:strategyqa:2 mcleish_llama32_r32:strategyqa:4 mcleish_llama32_r32:strategyqa:8 mcleish_llama32_r32:svamp:1}"

submit() {  # submit <name> <time> <dependency or ""> <command...>
  local name="$1" time="$2" dep="$3"; shift 3
  sbatch --parsable $EXTRA ${dep:+--dependency=afterok:$dep} --job-name="$name" --gres=gpu:1 \
    --cpus-per-task="$CPUS" --mem="$MEM" --time="$time" --output="logs/${name}.out" \
    --wrap="cd '$ROOT' && $* ; echo RC=\$?"
}

case "$MODE" in
  c1)
    : > logs/c1_jobs.txt
    for M in ouro_1_4b_think ouro_2_6b_think; do for T in gsm8k math500 svamp aqua csqa arc strategyqa bbh mmlu hellaswag; do for K in 1 2 3 4; do
      jid=$(submit "c1_${T}_${M}_k${K}" "$TIME_C1" "" "$PROD_PYTHON -m prod.generate --model=$M --task=$T --k=$K --protocol=natural --out=$PROD_ART --continue-chains=think_tag --protocol-tag=natural2 --horizon=4096 --old-horizon=4096 --caps=$CAPS_C1 --no-extra-caps --no-think-tag-is-stop")
      echo "$M $T $K $jid" >> logs/c1_jobs.txt
    done; done; done
    echo "c1: $(wc -l < logs/c1_jobs.txt) jobs submitted (ids in logs/c1_jobs.txt)" ;;
  c2)
    n=0
    for item in $HITLIST; do
      IFS=: read -r M T K <<< "$item"
      dep=""; src=""
      if [[ "$M" == ouro_* ]]; then
        [ -f logs/c1_jobs.txt ] || { echo "run c1 first: logs/c1_jobs.txt missing"; exit 1; }
        dep=$(awk -v m="$M" -v t="$T" -v k="$K" '$1==m && $2==t && $3==k {print $4}' logs/c1_jobs.txt)
        [ -n "$dep" ] || { echo "no c1 job recorded for $M $T k$K; skipped"; continue; }
        src="--continue-from-cells=$PROD_ART/cells_${M}_${T}_natural2_k${K}.jsonl"
      fi
      submit "c2_${T}_${M}_k${K}" "$TIME_C2" "$dep" "$PROD_PYTHON -m prod.generate --model=$M --task=$T --k=$K --protocol=natural --out=$PROD_ART --continue-chains=horizon --protocol-tag=natural2h --horizon=8192 --old-horizon=4096 --caps=$CAPS_C2 --no-extra-caps $src" > /dev/null
      n=$((n + 1))
    done
    echo "c2: $n jobs submitted" ;;
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
  *)
    echo "usage: bash slurm/continue_chains.sh c1|c2|status"; exit 1 ;;
esac
