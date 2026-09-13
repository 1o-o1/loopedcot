#!/usr/bin/env bash
# One-shot environment setup. Run from the repository root. No token is used.
#   .venv/   python environment (torch comes from the machine's own install via --system-site-packages)
#   hf/      the six checkpoints at pinned revisions (public repos, about 38 GB)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
export HF_HOME="$ROOT/hf"
python3 -m venv "$ROOT/.venv" --system-site-packages
"$ROOT/.venv/bin/pip" install --no-cache-dir -r "$ROOT/requirements.txt"
"$ROOT/.venv/bin/python" - <<'PY'
import torch, transformers
assert transformers.__version__ == "4.56.2", transformers.__version__
assert torch.cuda.is_available(), "torch is not a CUDA build or no GPU is visible"
print("torch", torch.__version__, "cuda", torch.version.cuda, "gpus", torch.cuda.device_count(), "transformers", transformers.__version__)
PY
mkdir -p "$HF_HOME" "$ROOT/artifacts" "$ROOT/logs"
"$ROOT/.venv/bin/python" -m prod.install_models
"$ROOT/.venv/bin/python" -m prod.install_models --verify
export HF_HUB_OFFLINE=1
"$ROOT/.venv/bin/python" -m prod.tasks.freeze --verify
echo
echo "environment ready. Before every later command run:  source env.sh"
