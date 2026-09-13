# source this file from the repository root before running anything.
# A variable already set in your shell wins (e.g. a conda user exports PROD_PYTHON=$(which python) first).
export HF_HOME="${HF_HOME:-$PWD/hf}"
export HF_HUB_OFFLINE=1
export PROD_ART="${PROD_ART:-$PWD/artifacts}"
export PROD_LOGS="${PROD_LOGS:-$PWD/logs}"
export PROD_PYTHON="${PROD_PYTHON:-$PWD/.venv/bin/python}"
export PYTORCH_CUDA_ALLOC_CONF="${PYTORCH_CUDA_ALLOC_CONF:-expandable_segments:True}"
