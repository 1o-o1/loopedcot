#!/bin/bash
# The forced protocol carried on to horizon 8192: the same 64 cells as the forced grid of record (the
# four Ouro checkpoints x {gsm8k, math500, csqa, aqua} x depths 1-4), forced budgets 0..4096 plus
# 8192, every question. Each job copies the finished 4096 job's trace checkpoint (ids plus forced
# state, $PROD_ART/trace_<tag>_*.jsonl) into $PROD_ART/forced8k and runs prod.generate with
# --extend-forced-horizon, which re-opens every row and keeps injecting "Wait," from token 4096 to
# 8192; the first 4096 tokens are never regenerated. The 4096 forced grid is never touched.
# SHARDS must stay 2, the sharding the 4096 run used (its files end in _s0of2/_s1of2): the job
# refuses when the checkpoint does not hold every row of its shard.
#   sbatch --nice=1000 slurm/forced8k.sbatch         # 128 jobs, at most 16 at a time (two nodes)
# Array index i: shard i % 2, then cell i / 2 = depth, task, model in that order.
# Time basis: about 0.6 of a from-scratch 4096 forced shard per job (half the tokens, longer contexts).
#SBATCH --job-name=forced8k
#SBATCH --array=0-127%16
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
SHARDS="${SHARDS:-2}"
MODELS=(ouro_1_4b_base ouro_1_4b_think ouro_2_6b_base ouro_2_6b_think)
TASKS=(gsm8k math500 csqa aqua)
KS=(1 2 3 4)
I="${SLURM_ARRAY_TASK_ID:-0}"
S=$((I % SHARDS)); C=$((I / SHARDS))
K="${KS[$((C % 4))]}"; T="${TASKS[$(((C / 4) % 4))]}"; M="${MODELS[$((C / 16))]}"
OUT="$PROD_ART/forced8k"
mkdir -p "$OUT"
TAG="${M}_${T}_forced_k${K}_s${S}of${SHARDS}"
n=0
for f in "$PROD_ART"/trace_${TAG}_*.jsonl; do
  [ -e "$f" ] || continue
  [ -e "$OUT/$(basename "$f")" ] || cp "$f" "$OUT/"
  n=$((n + 1))
done
echo "[forced8k] task $I: model=$M task=$T k=$K shard=$S/$SHARDS out=$OUT trace files=$n"
[ "$n" -gt 0 ] || { echo "no trace checkpoint $PROD_ART/trace_${TAG}_*.jsonl: the 4096 forced job's traces are gone, nothing to extend"; exit 4; }
$PROD_PYTHON -m prod.generate --model "$M" --task "$T" --k "$K" --protocol forced \
  --forced-horizon 8192 --forced-budgets 0,16,32,64,128,256,512,1024,2048,4096,8192 \
  --extend-forced-horizon --shard "$S" --shards "$SHARDS" --out "$OUT"
RC=$?
echo "RC=$RC"
exit $RC
