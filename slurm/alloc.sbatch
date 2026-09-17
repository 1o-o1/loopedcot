#!/bin/bash
# The allocator on every finished natural-stop grid (CPU only). From the repository root:
#   sbatch slurm/alloc.sbatch
# Writes artifacts/alloc_<task>_<model>/{cards.json, results.json, table1.md} and the collected
# artifacts/alloc_all_tables.md. A pair whose grid is incomplete prints SKIP; re-run later.
#SBATCH --job-name=loopedcot_alloc
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32gb
#SBATCH --time=02:00:00
#SBATCH --output=logs/alloc_%j.out
# add --partition=... / --account=... as your cluster requires
set -u
cd "${SLURM_SUBMIT_DIR:-$(dirname "$0")/..}"
mkdir -p logs
# conda instead of .venv: uncomment and adapt, so env.sh keeps your interpreter
# source /opt/conda/etc/profile.d/conda.sh && conda activate loopedcot && export PROD_PYTHON=$(which python)
source env.sh
MODELS="${MODELS:-ouro_1_4b_base ouro_1_4b_think ouro_2_6b_base ouro_2_6b_think huginn_0125 mcleish_llama32_r32}"
TASKS="${TASKS:-gsm8k math500 svamp aqua csqa arc strategyqa bbh mmlu hellaswag}"
for M in $MODELS; do
  for T in $TASKS; do
    $PROD_PYTHON -m alloc.cli --cells "$PROD_ART" --task "$T" --checkpoint "$M" --model-config prod/config.yaml --accounting "${ACCOUNTING:-both}" --budget-basis "${BASIS:-prompt}" \
        --out "$PROD_ART/alloc_${T}_${M}" || echo "SKIP $T $M"
  done
done
for d in "$PROD_ART"/alloc_*/; do echo "## $(basename "$d")"; cat "$d/table1.md"; echo; done > "$PROD_ART/alloc_all_tables.md"
echo DONE
