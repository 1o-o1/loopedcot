#!/bin/bash
# The live allocator check on one GPU: rank from the calibration rows, pick one cell per evaluation
# prompt at BUDGET x the default cost, generate once at that cell, report live against offline.
#   sbatch slurm/live.sbatch            (MODEL, TASK, BUDGET, N can be exported before submitting)
#SBATCH --job-name=loopedcot_live
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64gb
#SBATCH --gres=gpu:1
#SBATCH --time=02:00:00
#SBATCH --output=logs/live_%j.out
# add --partition=... / --account=... as your cluster requires
set -u
cd "${SLURM_SUBMIT_DIR:-$(dirname "$0")/..}"
mkdir -p logs
# conda instead of .venv: uncomment and adapt, so env.sh keeps your interpreter
# source /opt/conda/etc/profile.d/conda.sh && conda activate loopedcot && export PROD_PYTHON=$(which python)
source env.sh
MODEL="${MODEL:-ouro_1_4b_base}"; TASK="${TASK:-gsm8k}"; BUDGET="${BUDGET:-0.5}"; N="${N:-}"
$PROD_PYTHON -m prod.live_check --model="$MODEL" --task="$TASK" --cells="$PROD_ART" --budget-fraction="$BUDGET" ${N:+--n=$N}
echo DONE
