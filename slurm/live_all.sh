#!/bin/bash
# Submits one GPU job per (checkpoint, dataset, arm, budget) for the live allocator check.
# From the repository root, after `source env.sh`:   bash slurm/live_all.sh
# Skips every GSM8K lookup run (those were submitted earlier with slurm/live.sbatch) and every run
# whose output file already exists, so it can be re-run to fill gaps. Runs nothing itself.
# MODELS / TASKS / ARMS / BUDGETS can be exported before running to narrow the set.
set -u
MODELS="${MODELS:-ouro_1_4b_base ouro_1_4b_think ouro_2_6b_base ouro_2_6b_think mcleish_llama32_r32 huginn_0125}"
TASKS="${TASKS:-gsm8k math500 svamp aqua csqa arc strategyqa bbh mmlu hellaswag}"
ARMS="${ARMS:-lookup avg_gated_lookup}"
BUDGETS="${BUDGETS:-0.5 1.0}"
EXTRA="${SBATCH_EXTRA:-}"          # e.g. SBATCH_EXTRA="--partition=gpu --account=lab"
n=0
for M in $MODELS; do
  for T in $TASKS; do
    for ARM in $ARMS; do
      for B in $BUDGETS; do
        [ "$ARM" = lookup ] && [ "$T" = gsm8k ] && continue
        OUT="$PROD_ART/live_${T}_${M}_${ARM}_b${B}.json"
        [ -e "$OUT" ] && continue
        TL=12:00:00; [ "$M" = huginn_0125 ] && TL=36:00:00
        sbatch $EXTRA --job-name="live_${M}_${T}_${ARM}_${B}" --gres=gpu:1 --cpus-per-task=8 --mem=64gb \
          --time="$TL" --output=logs/live_%j.out \
          --wrap="source env.sh && \$PROD_PYTHON -m prod.live_check --model=$M --task=$T --cells=\$PROD_ART --budget-fraction=$B --arm $ARM --out=$OUT"
        n=$((n + 1))
      done
    done
  done
done
echo "submitted $n live jobs"
