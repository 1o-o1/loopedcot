#!/bin/bash
# README step 3 under Slurm: the launcher inside one multi-GPU allocation. Plan the queue first (on
# the login node, section "Slurm" of the README), then submit from the repository root:
#   sbatch slurm/run.sbatch
# When the time limit ends the job, submit it again: stranded and failed jobs are re-queued and every
# job resumes from its per-problem checkpoint. Never have two of these running on the same queue.
#SBATCH --job-name=loopedcot
#SBATCH --gres=gpu:8
#SBATCH --cpus-per-task=32
#SBATCH --mem=256G
#SBATCH --time=24:00:00
#SBATCH --output=logs/slurm-run-%j.out
# add --partition=... / --account=... as your cluster requires; match --gres to --gpus below
cd "$SLURM_SUBMIT_DIR"
# conda instead of .venv: uncomment and adapt, so env.sh keeps your interpreter
# source /opt/conda/etc/profile.d/conda.sh && conda activate loopedcot && export PROD_PYTHON=$(which python)
source env.sh
NGPU=$($PROD_PYTHON -c "import torch; print(torch.cuda.device_count())")
echo "allocation: $NGPU GPU(s), CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
$PROD_PYTHON -m prod.launcher --run --gpus=$NGPU --workers-per-gpu=2
