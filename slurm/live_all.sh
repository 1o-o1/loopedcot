#!/bin/bash
# Submits the live allocator checks as ONE Slurm job array, throttled to MAXJOBS running at once
# (default 56 = 7 nodes x 8 GPUs) and running PER_GPU live checks in parallel on each GPU.
#   bash <repo>/slurm/live_all.sh
# Every array task cd's into the repository root (absolute path from this file's location). Skips the
# GSM8K lookup runs (submitted earlier with slurm/live.sbatch) and any run whose output file exists,
# so it can be re-run to fill gaps. The run list is kept in logs/live_jobs_<timestamp>.txt.
# Knobs (export before running): MODELS TASKS ARMS BUDGETS PER_GPU MAXJOBS TIME SBATCH_EXTRA
#   PER_GPU=2 fits two Ouro-1.4B or McLeish checks on a 96 GB card; keep 1 for the 2.6B checkpoints.
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p "$ROOT/logs"
source "$ROOT/env.sh"
MODELS="${MODELS:-ouro_1_4b_base ouro_1_4b_think ouro_2_6b_base ouro_2_6b_think mcleish_llama32_r32 huginn_0125}"
TASKS="${TASKS:-gsm8k math500 svamp aqua csqa arc strategyqa bbh mmlu hellaswag}"
ARMS="${ARMS:-lookup avg_gated_lookup}"
BUDGETS="${BUDGETS:-0.5 1.0}"
PER_GPU="${PER_GPU:-1}"
MAXJOBS="${MAXJOBS:-56}"
TIME="${TIME:-12:00:00}"
EXTRA="${SBATCH_EXTRA:-}"          # e.g. SBATCH_EXTRA="--partition=gpu --account=lab"

LIST="$ROOT/logs/live_jobs_$(date +%Y%m%d_%H%M%S).txt"
: > "$LIST"
for M in $MODELS; do
  for T in $TASKS; do
    for ARM in $ARMS; do
      for B in $BUDGETS; do
        [ "$ARM" = lookup ] && [ "$T" = gsm8k ] && continue
        OUT="$PROD_ART/live_${T}_${M}_${ARM}_b${B}.json"
        [ -e "$OUT" ] && continue
        echo "$M $T $ARM $B $OUT" >> "$LIST"
      done
    done
  done
done
n=$(wc -l < "$LIST")
if [ "$n" -eq 0 ]; then echo "nothing to submit (every output file exists)"; exit 0; fi
chunks=$(( (n + PER_GPU - 1) / PER_GPU ))
echo "$n live checks in $chunks array tasks ($PER_GPU per GPU, at most $MAXJOBS running), list: $LIST"
sbatch $EXTRA --job-name=live_all --array="0-$((chunks - 1))%${MAXJOBS}" --gres=gpu:1 \
  --cpus-per-task=$((8 * PER_GPU)) --mem=$((64 * PER_GPU))gb --time="$TIME" \
  --output="$ROOT/logs/live_%A_%a.out" \
  --wrap="cd '$ROOT' && bash slurm/live_chunk.sh '$LIST' \$SLURM_ARRAY_TASK_ID $PER_GPU"
