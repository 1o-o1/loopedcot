#!/bin/bash
# Stage 5 of the S36 training recipe: the evaluation grid, one array task per (variant, task).
#   sbatch slurm/grids_s36.sbatch                   (R can be exported before submitting)
# Array index i takes variant i/4 of VARIANTS and task i%4, so one variant is four indices: with
# the default list, tasks 0-3 are budget_longest on {gsm8k, math500, csqa, aqua} and tasks 4-7
# uniform_longest on the same four (--array=0-7). Other lists, one index per (variant, task):
#   sbatch --array=0-7  --export=ALL,VARIANTS="nobudget nocut" slurm/grids_s36.sbatch
#   sbatch --array=0-3  --export=ALL,VARIANTS="plain_sft" slurm/grids_s36.sbatch
#   sbatch --array=0-15 --export=ALL,VARIANTS="nobudget nocut plain_sft plain_sft_mix" slurm/grids_s36.sbatch
#
# One run_grid call writes both protocols for one depth: the no-limit pass, generated to horizon
# 4096 and scored at the caps of record {0, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096}, in
# $R/artifacts/cells_<task>_s36_<variant>_full_k<k>.jsonl, which is the base grids' cells format;
# and the budgeted passes {0, 32, 128, 512, 2048}, each with its own Budget line and a hard stop, in
# cells_budget_<task>_s36_<variant>_full_k<k>.jsonl. The horizon and the caps are not command-line
# flags: they come from train/config.yaml (eval_horizon, eval_standard_caps). Depths follow the
# recipe: MATH500 at k=4 and k=2, AQuA at k=4 and k=1, the rest at k=4. Rows resume per (question,
# budget, cap), so a re-submission after a time limit continues.
# DEPTHS="1 2 3 4" overrides the per-task depth list (the same list for every task).
#
# EVAL_ROWS (default `production`) chooses the rows. `production` evaluates every row of
# prod/tasks/data/rows_<task>.jsonl at full N -- gsm8k 1319, math500 500, csqa 1221, aqua 254 --
# labelled cal or eval by the harness's own split function, and its files carry the `_full` label
# above, so a full-N grid never lands on the S32-subset files. EVAL_ROWS=s32 restores the 300 eval
# plus 100 cal subset and the unlabelled names. SEED works as in slurm/variant_s36.sbatch: here it
# only selects the run name and the stage-2 manifest the exemplars are checked against.
#
# Under EVAL_ROWS=s32, CSQA and AQuA read their question rows from $R/artifacts/data32_<task>.jsonl
# (the shared harness's split_rows) and GSM8K and MATH500 come straight from their Hugging Face
# datasets; put those two files in place before tasks 2, 3, 6 and 7 run. Under `production` all four
# tasks read the frozen harness rows in the checkout and need neither.
#
# Follow-up, CPU only, once all four tasks of a variant have finished (run it per variant, from the
# repository root, after sourcing env.sh; drop the _full when EVAL_ROWS=s32 wrote the grid):
#   $PROD_PYTHON -m train.analysis --name=s36_budget_longest_full --ref=ouro_1_4b_base \
#       --ref-dir=$PROD_ART --root=$R
#   $PROD_PYTHON -m train.analysis --name=s36_uniform_longest_full --ref=ouro_1_4b_base \
#       --ref-dir=$PROD_ART --root=$R
# analysis.py loads the reference as <ref-dir>/cells_<task>_<ref>_k<k>.jsonl (or the _fixed_
# variant). This repository's production grid is artifacts/cells_ouro_1_4b_base_<task>_natural_k<k>
# .jsonl, so those files have to be reachable under the loader's spelling before the command runs.
#SBATCH --job-name=s36_grids
#SBATCH --array=0-7
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64gb
#SBATCH --time=08:00:00
#SBATCH --output=logs/s36_grids_%A_%a.out
# add --partition=... / --account=... as your cluster requires
# Time basis: train/README.md prices the grid at 5.9 h per variant for all four tasks, 1.12 h per task
# at k=4 plus 1.4 h for the extra MATH500 and AQuA depths; the longest single task here is MATH500
# at two depths.
set -u
cd "${SLURM_SUBMIT_DIR:-$(dirname "$0")/..}"
mkdir -p logs
# conda instead of .venv: uncomment and adapt, so env.sh keeps your interpreter
# source /opt/conda/etc/profile.d/conda.sh && conda activate loopedcot && export PROD_PYTHON=$(which python)
source env.sh
export CLUSTER=1                          # a Slurm job owns its GPU and never waits for an idle one
R="${R:-$PROD_ART/s36}"

VARIANTS="${VARIANTS:-budget_longest uniform_longest}"   # space-separated; index i takes i/4
VLIST=($VARIANTS)
TASKS=(gsm8k math500 csqa aqua)
I="${SLURM_ARRAY_TASK_ID:-0}"
VARIANT="${VLIST[$((I / 4))]}"
TASK="${TASKS[$((I % 4))]}"
EVAL_ROWS="${EVAL_ROWS:-production}"          # production = full N and the harness's own split
DEFAULT_SEED="$(awk '/^seed:/{print $2; exit}' train/config.yaml)"
SEED="${SEED:-$DEFAULT_SEED}"                 # the config's seed is today's run names
SEEDARG=""
SEEDTAG=""
if [ "$SEED" != "$DEFAULT_SEED" ]; then SEEDARG="--seed=$SEED"; SEEDTAG="_seed$SEED"; fi
NAME="s36_${VARIANT}${SEEDTAG}"               # the adapter train.py wrote, and the cells file name
if [ -n "${DEPTHS:-}" ]; then
  KS="$DEPTHS"                              # one list for every task, e.g. DEPTHS="1 2 3 4"
else
  case "$TASK" in                           # default: the depths the S36 grids were run at
    math500) KS="4 2" ;;
    aqua)    KS="4 1" ;;
    *)       KS="4" ;;
  esac
fi
echo "[s36 grids] task $I: variant=$VARIANT name=$NAME grid_task=$TASK depths=$KS rows=$EVAL_ROWS seed=$SEED root=$R"

RC=0
for K in $KS; do
  $PROD_PYTHON -m train.run_grid "$NAME" "$TASK" --variant="$VARIANT" --k=$K \
      --eval-rows="$EVAL_ROWS" $SEEDARG --budgets=0,32,128,512,2048,none --no-wait --root=$R
  RC=$?
  [ "$RC" -eq 0 ] || break
done
echo "RC=$RC"
exit $RC
