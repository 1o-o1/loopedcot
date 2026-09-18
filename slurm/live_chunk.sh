#!/bin/bash
# One array task of slurm/live_all.sh: runs PER_GPU lines of the run list in parallel on this GPU.
#   bash slurm/live_chunk.sh <list file> <array task id> <per gpu>
# The lines are read into an array first (no pipe): a `cmd | while` loop runs in a subshell, and
# background checks started there are not children of this script, so `wait` would return at once
# and Slurm would kill them with the job.
set -u
LIST="$1"; ID="$2"; PER="$3"
ALLOC_PREFIX="${ALLOC_PREFIX:-alloc_v5}"   # the alloc output the picks are read from
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
source "$ROOT/env.sh"
start=$((ID * PER + 1)); end=$((start + PER - 1))
mapfile -t LINES < <(sed -n "${start},${end}p" "$LIST")
pids=()
for line in "${LINES[@]}"; do
  [ -z "$line" ] && continue
  read -r M T ARM B OUT <<< "$line"
  LOG="$ROOT/logs/live_${T}_${M}_${ARM}_b${B}.log"
  echo "[chunk $ID] start $M $T $ARM $B -> $LOG"
  PYTHONUNBUFFERED=1 $PROD_PYTHON -m prod.live_check --model="$M" --task="$T" --cells="$PROD_ART" \
      --alloc-dir="$PROD_ART/${ALLOC_PREFIX}_${T}_${M}" \
      --budget-fraction="$B" --arm "$ARM" --out="$OUT" > "$LOG" 2>&1 &
  pids+=("$!:$M $T $ARM $B")
done
rc_all=0
for entry in "${pids[@]}"; do
  pid="${entry%%:*}"; what="${entry#*:}"
  if wait "$pid"; then echo "[chunk $ID] done $what"; else echo "[chunk $ID] FAILED $what"; rc_all=1; fi
done
echo "[chunk $ID] finished"
exit $rc_all
