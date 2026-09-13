#!/bin/bash
# Plan the queue (README section 3, first command) as a Slurm job. From the repository root:
#   sbatch slurm/plan.sbatch
# Output in logs/plan_<jobid>.out: "queued 262 jobs ..." and, if any, an "unplaceable" list.
# One GPU is requested only so the launcher measures the real device memory; on the login node the
# same command runs without a job by adding --device-gb=<GB per card>.
#SBATCH --job-name=loopedcot_plan
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32gb
#SBATCH --gres=gpu:1
#SBATCH --time=00:10:00
#SBATCH --output=logs/plan_%j.out
# add --partition=... / --account=... / --mail-user=... as your cluster requires

set -euo pipefail
cd "${SLURM_SUBMIT_DIR:-$(dirname "$0")/..}"
mkdir -p logs

# conda instead of .venv: uncomment and adapt, so env.sh keeps your interpreter
# source /opt/conda/etc/profile.d/conda.sh && conda activate loopedcot && export PROD_PYTHON=$(which python)
source env.sh

# --placement-horizon: tokens per row the memory estimate assumes; 2048 on 96 GB cards lets a k=3/4
# job share a card with a k=1/2 job and never with another long-chain job (README section 6)
srun $PROD_PYTHON -m prod.launcher --plan --gpus=8 --workers-per-gpu=2 --placement-horizon=2048
