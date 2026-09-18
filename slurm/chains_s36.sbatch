#!/bin/bash
# Stage 1 of the S36 training recipe: generate the base model's own correct chains, one array
# task per (source, prompt).
#   sbatch slurm/chains_s36.sbatch                 (R can be exported before submitting)
# The eight tasks are the four sources {gsm8k, math, csqa, aqua} crossed with the two exemplar
# blocks {standard, short}. Each writes $R/artifacts/chains_<source>_<A|B>_k4.jsonl and resumes per
# pool question, so a re-submission after a time limit picks up where it stopped. Run once: every
# variant reads the same chains.
#SBATCH --job-name=s36_chains
#SBATCH --array=0-7
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64gb
#SBATCH --time=04:00:00
#SBATCH --output=logs/s36_chains_%A_%a.out
# add --partition=... / --account=... as your cluster requires
# Time basis: train/README.md prices all chain generation at 14.8 h contended / 4.5 h idle for both
# prompts of all four sources; the largest single (source, prompt) task is MATH at about 2.7 h
# contended. 04:00:00 covers it on a card this job owns.
set -u
cd "${SLURM_SUBMIT_DIR:-$(dirname "$0")/..}"
mkdir -p logs
# conda instead of .venv: uncomment and adapt, so env.sh keeps your interpreter
# source /opt/conda/etc/profile.d/conda.sh && conda activate loopedcot && export PROD_PYTHON=$(which python)
source env.sh
export CLUSTER=1                          # a Slurm job owns its GPU and never waits for an idle one
R="${R:-$PROD_ART/s36}"

SOURCES=(gsm8k math csqa aqua)
PROMPTS=(standard short)
I="${SLURM_ARRAY_TASK_ID:-0}"
SRC="${SOURCES[$((I / 2))]}"
PROMPT="${PROMPTS[$((I % 2))]}"
echo "[s36 chains] task $I: source=$SRC prompt=$PROMPT root=$R"

$PROD_PYTHON -m train.chains "$SRC" --prompt="$PROMPT" --no-wait --root=$R
RC=$?
echo "RC=$RC"
exit $RC
