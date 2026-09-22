#!/usr/bin/env bash
# One (model, task, depth, shard) job. EVERY hyperparameter is an argument; 
#
#   ./run.sh --model=ouro_1_4b_base --task=gsm8k --k=4 [options]
#
# Required
#   --model=NAME        ouro_1_4b_base | ouro_1_4b_think | ouro_2_6b_base | ouro_2_6b_think
#                       | huginn_0125 | mcleish_llama32_r32
#   --task=NAME         gsm8k math500 svamp aqua csqa arc bbh_date_understanding
#                       bbh_logical_deduction_five_objects
#                       bbh_tracking_shuffled_objects_three_objects bbh_sports_understanding
#   --k=INT             loop count
# Protocol
#   --protocol=natural|forced       default natural
#   --caps=LIST                     default 0,16,32,64,128,256,512,1024,2048,4096
#   --extra-caps=LIST               EMPTY by default. The extra caps {48,96,192,384} are dropped;
#                                   the `extra` row field survives and is always false
#   --horizon=INT                   default 4096 for BOTH protocols
#   --no-eos-cut                    use the alternate cut rule, needed to reproduce two earlier
#                                   runs exactly
# Sharding and size
#   --shard=INT --shards=INT        default 0 / 1
#   --n=INT                         first N problems of the shard (smoke and forced runs)
# Execution
#   --gpu=INT                       CUDA_VISIBLE_DEVICES, default unset (all)
#   --mem-fraction=FLOAT            default 0.85 (the Spark rule)
#   --batch-cap=INT                 default 32
#   --batch-width=INT               force an exact batch width (to match an earlier run's width)
#   --no-mask                       raven families only: skip the padding mask (batch-1 control)
#   --adapter=DIR                   LoRA adapter directory (S32 tag convention)
#   --tag-loops / --tag-tokens      S32 control line
#   --out=DIR                       artifacts directory, default $PROD_ART or ../artifacts
#   --python=PATH                   interpreter, default $PROD_PYTHON or python
#   --detach                        setsid nohup, log to $PROD_LOGS (the Spark rule for long jobs)
#
# Environment honoured: PROD_ART PROD_LOGS PROD_PYTHON PROD_MEM_FRACTION PROD_BATCH_CAP
#                       HF_HOME HF_HUB_OFFLINE
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
PY="${PROD_PYTHON:-python}"
OUT="${PROD_ART:-$ROOT/artifacts}"
LOGDIR="${PROD_LOGS:-$ROOT/logs}"
GPU=""
DETACH=0
ARGS=()

for a in "$@"; do
  case "$a" in
    --gpu=*)     GPU="${a#*=}" ;;
    --python=*)  PY="${a#*=}" ;;
    --out=*)     OUT="${a#*=}"; ARGS+=("$a") ;;
    --detach)    DETACH=1 ;;
    *)           ARGS+=("$a") ;;
  esac
done

mkdir -p "$OUT" "$LOGDIR"
export HF_HUB_OFFLINE="${HF_HUB_OFFLINE:-1}"
export PROD_ART="$OUT"
export PROD_LOGS="$LOGDIR"
export PYTORCH_CUDA_ALLOC_CONF="${PYTORCH_CUDA_ALLOC_CONF:-expandable_segments:True}"
[ -n "$GPU" ] && export CUDA_VISIBLE_DEVICES="$GPU"

# the tag mirrors prod/generate.py's, so the log sits beside the artifacts it wrote
tagof() {
  local m t k pr sh shs
  m=$(printf '%s\n' "${ARGS[@]}" | sed -n 's/^--model=//p' | tr '+' '-')
  t=$(printf '%s\n' "${ARGS[@]}" | sed -n 's/^--task=//p')
  k=$(printf '%s\n' "${ARGS[@]}" | sed -n 's/^--k=//p')
  pr=$(printf '%s\n' "${ARGS[@]}" | sed -n 's/^--protocol=//p'); pr=${pr:-natural}
  sh=$(printf '%s\n' "${ARGS[@]}" | sed -n 's/^--shard=//p'); shs=$(printf '%s\n' "${ARGS[@]}" | sed -n 's/^--shards=//p')
  if [ -n "${shs:-}" ] && [ "${shs:-1}" != "1" ]; then
    printf '%s_%s_%s_k%s_s%sof%s' "$m" "$t" "$pr" "$k" "${sh:-0}" "$shs"
  else
    printf '%s_%s_%s_k%s' "$m" "$t" "$pr" "$k"
  fi
}
TAG="$(tagof)"
LOG="$LOGDIR/${TAG}.log"

echo "[run.sh] $TAG"
echo "[run.sh] out=$OUT log=$LOG gpu=${GPU:-all} python=$PY"
echo "[run.sh] $PY -m prod.generate ${ARGS[*]}"

cd "$ROOT"
if [ "$DETACH" = "1" ]; then
  # Spark rule: anything over a few minutes runs detached with stdin closed so an ssh drop cannot
  # take it down, and the job checkpoints per problem so a kill is resumable.
  setsid nohup "$PY" -m prod.generate "${ARGS[@]}" >>"$LOG" 2>&1 < /dev/null &
  echo "[run.sh] detached pid $! -> $LOG"
else
  "$PY" -m prod.generate "${ARGS[@]}" 2>&1 | tee -a "$LOG"
fi
