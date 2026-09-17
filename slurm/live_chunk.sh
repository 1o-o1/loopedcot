#!/bin/bash
# One array task of slurm/live_all.sh: runs PER_GPU lines of the run list in parallel on this GPU.
#   bash slurm/live_chunk.sh <list file> <array task id> <per gpu>
set -u
LIST="$1"; ID="$2"; PER="$3"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
source "$ROOT/env.sh"
start=$((ID * PER + 1)); end=$((start + PER - 1))
sed -n "${start},${end}p" "$LIST" | while read -r M T ARM B OUT; do
  [ -z "${M:-}" ] && continue
  echo "[chunk $ID] start $M $T $ARM $B"
  ( $PROD_PYTHON -m prod.live_check --model="$M" --task="$T" --cells="$PROD_ART" --budget-fraction="$B" \
      --arm "$ARM" --out="$OUT" > "$ROOT/logs/live_${T}_${M}_${ARM}_b${B}.log" 2>&1 \
    && echo "[chunk $ID] done $M $T $ARM $B" || echo "[chunk $ID] FAILED $M $T $ARM $B (see logs/live_${T}_${M}_${ARM}_b${B}.log)" ) &
done
wait
echo "[chunk $ID] finished"
