#!/bin/bash
# The live allocator check on one GPU: rank from the calibration rows, pick one cell per evaluation
# prompt at BUDGET x the default cost, generate once at that cell, report live against offline.
#   sbatch slurm/live.sbatch   (MODELS, TASKS, BUDGETS, N can be exported before submitting)
# Default: both Ouro-1.4B checkpoints on GSM8K at 0.5, 0.75 and 1.0 of the default cost, six runs,
# one file each: artifacts/live_<task>_<model>_<arm>_b<budget>.json; needs alloc.sbatch's output first
#SBATCH --job-name=loopedcot_live
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64gb
#SBATCH --gres=gpu:1
#SBATCH --time=08:00:00
#SBATCH --output=logs/live_%j.out
# add --partition=... / --account=... as your cluster requires
set -u
cd "${SLURM_SUBMIT_DIR:-$(dirname "$0")/..}"
mkdir -p logs
# conda instead of .venv: uncomment and adapt, so env.sh keeps your interpreter
# source /opt/conda/etc/profile.d/conda.sh && conda activate loopedcot && export PROD_PYTHON=$(which python)
source env.sh
MODELS="${MODELS:-ouro_1_4b_base ouro_1_4b_think}"
TASKS="${TASKS:-gsm8k}"
BUDGETS="${BUDGETS:-0.5 0.75 1.0}"
N="${N:-}"                       # e.g. N=100 for a smoke
ARM="${ARM:-lookup}"
ALLOC_PREFIX="${ALLOC_PREFIX:-alloc_v5}"   # picks are read from artifacts/<ALLOC_PREFIX>_<task>_<model>/
for M in $MODELS; do
  for T in $TASKS; do
    for B in $BUDGETS; do
      $PROD_PYTHON -m prod.live_check --model="$M" --task="$T" --cells="$PROD_ART" --alloc-dir="$PROD_ART/${ALLOC_PREFIX}_${T}_${M}" --arm "$ARM" --budget-fraction="$B" --out="$PROD_ART/live_${T}_${M}_${ARM}_b${B}.json" ${N:+--n=$N} || echo "FAILED $M $T $B"
    done
  done
done
echo DONE
