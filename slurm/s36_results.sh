#!/bin/bash
# After the S36 grid arrays finish: the analysis and the allocator (against the base reference) for every
# trained run whose production-split grids (_full) are complete. CPU only, minutes per run. Rerun any time:
# a run whose allocator outputs exist is skipped, the analysis is cheap and always refreshed.
#   bash slurm/s36_results.sh            # every run with complete grids
#   bash slurm/s36_results.sh s36_nocut  # one run
# Outputs: the analysis files train.analysis writes under $R, and $R/alloc_<name>_full_<task>/ (Table 1 of the
# trained model against the base model's default cost).
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
source "$ROOT/env.sh"
export CLUSTER=1
R="${R:-$PROD_ART/s36}"
TASKS="gsm8k math500 csqa aqua"
if [ $# -gt 0 ]; then names="$*"; else
  names=$(ls "$R"/artifacts/cells_gsm8k_*_full_k4.jsonl 2>/dev/null | sed -E 's|.*/cells_gsm8k_(.+)_full_k4\.jsonl|\1|' | sort -u)
fi
[ -n "$names" ] || { echo "no run has a production-split grid yet (looked for $R/artifacts/cells_gsm8k_*_full_k4.jsonl)"; exit 0; }
for N in $names; do
  ok=1
  for T in $TASKS; do [ -f "$R/artifacts/cells_${T}_${N}_full_k4.jsonl" ] || { echo "  $N: no $T grid yet"; ok=0; }; done
  [ "$ok" = 1 ] || { echo "skip $N: grids incomplete"; continue; }
  echo "== $N"
  $PROD_PYTHON -m train.analysis --name="${N}_full" --ref=ouro_1_4b_base --ref-dir="$PROD_ART" --root="$R" || echo "  analysis FAILED $N"
  for T in $TASKS; do
    out="$R/alloc_${N}_full_${T}"
    [ -f "$out/results.json" ] && { echo "  done alloc $T"; continue; }
    $PROD_PYTHON -m alloc.cli --cells "$R/artifacts" --task "$T" --checkpoint "${N}_full" --reference ouro_1_4b_base \
      --reference-cells "$PROD_ART" --layers-per-loop 24 --fixed-layers 0 --accounting all --avg-budget --promptfree \
      --out "$out" > "logs/alloc_${N}_full_${T}.log" 2>&1 && echo "  alloc $T ok" || echo "  alloc FAILED $N $T (see logs/alloc_${N}_full_${T}.log; if it refuses the reference, rerun without --reference)"
  done
done
