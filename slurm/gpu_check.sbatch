#!/bin/bash
# README step 2 under Slurm: one 20-problem job on one GPU. Submit from the repository root:
#   sbatch slurm/gpu_check.sbatch
#SBATCH --job-name=loopedcot-check
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=00:30:00
#SBATCH --output=logs/slurm-check-%j.out
# add --partition=... / --account=... as your cluster requires
cd "$SLURM_SUBMIT_DIR"
source env.sh
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
$PROD_PYTHON -m prod.generate --model=ouro_1_4b_base --task=gsm8k --k=4 --n=20
