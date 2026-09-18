#!/bin/bash
# Stage 5 of the S36 training recipe: the evaluation grid, one array task per (arm, task).
#   sbatch slurm/grids_s36.sbatch                   (R can be exported before submitting)
# Tasks 0-3 are budget_longest on {gsm8k, math500, csqa, aqua}, tasks 4-7 uniform_longest on the
# same four. One run_grid call writes both protocols for one depth: the no-limit pass, generated to
# horizon 4096 and scored at the caps of record {0, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096}, in
# $R/artifacts/cells_<task>_s36_<arm>_k<k>.jsonl, which is the base grids' cells format; and the
# budgeted passes {0, 32, 128, 512, 2048}, each with its own Budget line and a hard stop, in
# cells_budget_<task>_s36_<arm>_k<k>.jsonl. The horizon and the caps are not command-line flags:
# they come from train/config.yaml (eval_horizon, eval_standard_caps). Depths follow the recipe:
# MATH500 at k=4 and k=2, AQuA at k=4 and k=1, the rest at k=4. Rows resume per (question, budget,
# cap), so a re-submission after a time limit continues.
#
# Follow-up, CPU only, once all four tasks of an arm have finished (run it per arm, from the
# repository root, after sourcing env.sh):
#   $PROD_PYTHON -m train.analysis --name=s36_budget_longest --ref=ouro_1_4b_base \
#       --ref-dir=$PROD_ART --root=$R
#   $PROD_PYTHON -m train.analysis --name=s36_uniform_longest --ref=ouro_1_4b_base \
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
# Time basis: train/README.md prices the grid at 5.9 h per arm for all four tasks, 1.12 h per task
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

ARMS=(budget_longest uniform_longest)
TASKS=(gsm8k math500 csqa aqua)
I="${SLURM_ARRAY_TASK_ID:-0}"
ARM="${ARMS[$((I / 4))]}"
TASK="${TASKS[$((I % 4))]}"
NAME="s36_$ARM"                           # the adapter train.py wrote, and the cells file name
case "$TASK" in
  math500) KS="4 2" ;;
  aqua)    KS="4 1" ;;
  *)       KS="4" ;;
esac
echo "[s36 grids] task $I: arm=$ARM name=$NAME grid_task=$TASK depths=$KS root=$R"

RC=0
for K in $KS; do
  $PROD_PYTHON -m train.run_grid "$NAME" "$TASK" --arm="$ARM" --k=$K \
      --budgets=0,32,128,512,2048,none --no-wait --root=$R
  RC=$?
  [ "$RC" -eq 0 ] || break
done
echo "RC=$RC"
exit $RC
