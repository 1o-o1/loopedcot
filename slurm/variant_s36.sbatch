#!/bin/bash
# Stages 2 to 4 of the S36 training recipe for one variant: targets, then every gate, then training.
#   sbatch slurm/variant_s36.sbatch                     (R can be exported before submitting)
# The array index picks the i-th name in VARIANTS, which defaults to the two scheduled variants:
# task 0 is budget_longest (the recipe), task 1 is uniform_longest (the ablation: uniform T and a
# flat depth mix over the same targets). The four stages are chained with &&, so a failed gate never
# starts training. Writes $R/data/<variant>/, $R/gates/checks.json and the adapter
# $R/adapters/s36_<variant>/; training checkpoints every 100 steps and resumes on re-submission.
#
# Any other list of variants, one array index each:
#   sbatch --array=0-3 --export=ALL,VARIANTS="nobudget nocut plain_sft plain_sft_mix" slurm/variant_s36.sbatch
#
# A second seed of the same variant, which draws its own targets and shares no directory with the
# first: sbatch --array=0-1 --export=ALL,SEED=20260915 slurm/variant_s36.sbatch
# SEED defaults to train/config.yaml's own seed, which is today's draw and today's run names. Any
# other value keys stage 2's directory and manifest as <variant>_seed<n> and names the run
# s36_<variant>_seed<n>, so two seeds of one variant never overwrite each other.
#
# If only one GPU is free, submit `sbatch --array=0 slurm/variant_s36.sbatch` and then
# `sbatch --array=1 slurm/variant_s36.sbatch` after the first one finishes.
#
# Prerequisite: slurm/chains_s36.sbatch has finished all eight tasks. Gate V9 reads the S33
# screening record from train/data/v9_contamination.json, which ships with the package.
#SBATCH --job-name=s36_variant
#SBATCH --array=0-1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=70gb
#SBATCH --time=24:00:00
#SBATCH --output=logs/s36_variant_%A_%a.out
# add --partition=... / --account=... as your cluster requires
# Memory and time basis: train/README.md budgets 70 GB per variant and prices training at 9.1 h on an
# uncontended card (about 800 steps at 1.2M supervised tokens), 30 h while sharing it; targets and
# the CPU gates are seconds and the V4 preflight under a minute.
set -u
cd "${SLURM_SUBMIT_DIR:-$(dirname "$0")/..}"
mkdir -p logs
# conda instead of .venv: uncomment and adapt, so env.sh keeps your interpreter
# source /opt/conda/etc/profile.d/conda.sh && conda activate loopedcot && export PROD_PYTHON=$(which python)
source env.sh
export CLUSTER=1                          # a Slurm job owns its GPU and never waits for an idle one
R="${R:-$PROD_ART/s36}"

VARIANTS="${VARIANTS:-budget_longest uniform_longest}"   # space-separated; index i takes the i-th
VLIST=($VARIANTS)
I="${SLURM_ARRAY_TASK_ID:-0}"
VARIANT="${VLIST[$I]}"
DEFAULT_SEED="$(awk '/^seed:/{print $2; exit}' train/config.yaml)"
SEED="${SEED:-$DEFAULT_SEED}"                 # the config's seed is today's draw and today's names
SEEDARG=""
SEEDTAG=""
if [ "$SEED" != "$DEFAULT_SEED" ]; then SEEDARG="--seed=$SEED"; SEEDTAG="_seed$SEED"; fi
NAME="s36_${VARIANT}${SEEDTAG}"               # train.py's run name; run_grid and analysis use the same one
echo "[s36 variant] task $I: variant=$VARIANT seed=$SEED name=$NAME root=$R"

$PROD_PYTHON -m train.targets --variant="$VARIANT" $SEEDARG --root=$R \
  && $PROD_PYTHON -m train.gates --cpu --variant="$VARIANT" $SEEDARG --root=$R \
  && $PROD_PYTHON -m train.gates --v4 --variant="$VARIANT" $SEEDARG --no-wait --root=$R \
  && $PROD_PYTHON -m train.train "$NAME" --variant="$VARIANT" $SEEDARG --no-wait --root=$R
RC=$?
echo "RC=$RC"
exit $RC
