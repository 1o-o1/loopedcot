#!/bin/bash
# The forced protocol at horizon 8192: the same 64 cells as the forced grid of record (the four Ouro
# checkpoints x {gsm8k, math500, csqa, aqua} x depths 1-4), forced budgets 0..4096 plus 8192, every
# question, generated from scratch (no continuation code path). Output goes to its own directory,
# $PROD_ART/forced8k, so the 4096 forced grid is never touched.
#   sbatch slurm/forced8k.sbatch                     # 256 jobs = 64 cells x 4 shards
#   SHARDS=2 sbatch --array=0-127 slurm/forced8k.sbatch
# Array index i: shard i % SHARDS, then cell i / SHARDS = depth, task, model in that order.
# Time basis: one shard of the 4096 forced grid, times about 2.5 (twice the tokens, longer contexts).
#SBATCH --job-name=forced8k
#SBATCH --array=0-255
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64gb
#SBATCH --time=48:00:00
#SBATCH --output=logs/forced8k_%A_%a.out
# add --partition=... / --account=... as your cluster requires
set -u
cd "${SLURM_SUBMIT_DIR:-$(dirname "$0")/..}"
mkdir -p logs
source env.sh
export CLUSTER=1
SHARDS="${SHARDS:-4}"
MODELS=(ouro_1_4b_base ouro_1_4b_think ouro_2_6b_base ouro_2_6b_think)
TASKS=(gsm8k math500 csqa aqua)
KS=(1 2 3 4)
I="${SLURM_ARRAY_TASK_ID:-0}"
S=$((I % SHARDS)); C=$((I / SHARDS))
K="${KS[$((C % 4))]}"; T="${TASKS[$(((C / 4) % 4))]}"; M="${MODELS[$((C / 16))]}"
OUT="$PROD_ART/forced8k"
mkdir -p "$OUT"
echo "[forced8k] task $I: model=$M task=$T k=$K shard=$S/$SHARDS out=$OUT"
$PROD_PYTHON -m prod.generate --model "$M" --task "$T" --k "$K" --protocol forced \
  --forced-horizon 8192 --forced-budgets 0,16,32,64,128,256,512,1024,2048,4096,8192 \
  --shard "$S" --shards "$SHARDS" --out "$OUT"
RC=$?
echo "RC=$RC"
exit $RC
