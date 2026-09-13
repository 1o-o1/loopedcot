# source this file from the repository root before running anything
export HF_HOME="$PWD/hf"
export HF_HUB_OFFLINE=1
export PROD_ART="$PWD/artifacts"
export PROD_LOGS="$PWD/logs"
export PROD_PYTHON="$PWD/.venv/bin/python"
export PYTORCH_CUDA_ALLOC_CONF="${PYTORCH_CUDA_ALLOC_CONF:-expandable_segments:True}"
