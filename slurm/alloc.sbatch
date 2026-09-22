#!/bin/bash
# The allocator on every finished natural-stop grid, CPU only, pairs run in parallel.
#   sbatch slurm/alloc.sbatch                       (MODELS, TASKS, JOBS can be exported before submitting)
# Writes artifacts/${PREFIX}_<task>_<model>/{cards.json, results.json, table1_cap.md, table1_expected.md,
# table1_realised.md} and the collected artifacts/${PREFIX}_all_tables_expected.md. A pair whose grid is
# incomplete prints SKIP in this job's log; its own output is in logs/alloc_<task>_<model>.log.
#SBATCH --job-name=loopedcot_alloc
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=256
#SBATCH --mem=512gb
#SBATCH --time=02:00:00
#SBATCH --output=logs/l_alloc_%j.out
# add --partition=... / --account=... as your cluster requires
set -u
cd "${SLURM_SUBMIT_DIR:-$(dirname "$0")/..}"
mkdir -p logs
# conda instead of .venv: uncomment and adapt, so env.sh keeps your interpreter
# source /opt/conda/etc/profile.d/conda.sh && conda activate loopedcot && export PROD_PYTHON=$(which python)
source env.sh
MODELS="${MODELS:-ouro_1_4b_base ouro_1_4b_think ouro_2_6b_base ouro_2_6b_think huginn_0125 mcleish_llama32_r32}"
TASKS="${TASKS:-gsm8k math500 svamp aqua csqa arc strategyqa bbh mmlu hellaswag}"
JOBS="${JOBS:-16}"                       # pairs run at once; each pair is one process
PREFIX="${PREFIX:-alloc_v3}"               # output directory prefix: artifacts/<PREFIX>_<task>_<model>

run_pair() {
  $PROD_PYTHON -m alloc.cli --cells "$PROD_ART" --task "$2" --checkpoint "$1" --model-config prod/config.yaml \
      --accounting all --avg-budget --out "$PROD_ART/${PREFIX}_${2}_${1}" > "logs/alloc_${2}_${1}.log" 2>&1 \
      && echo "DONE $2 $1" || echo "SKIP $2 $1 (see logs/alloc_${2}_${1}.log)"
}
export -f run_pair
export PROD_PYTHON PROD_ART PREFIX
for M in $MODELS; do for T in $TASKS; do echo "$M $T"; done; done | xargs -P "$JOBS" -n 2 bash -c 'run_pair "$0" "$1"'

for d in "$PROD_ART"/${PREFIX}_*/; do
  [ -f "$d/table1_expected.md" ] && { echo "## $(basename "$d")"; cat "$d/table1_expected.md"; echo; }
done > "$PROD_ART/${PREFIX}_all_tables_expected.md"
echo ALL_DONE
