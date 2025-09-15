#!/bin/bash
#SBATCH --job-name=mace_training
#SBATCH --output=outputs/mace_training_%j.out
#SBATCH --error=outputs/mace_training_%j.err
#SBATCH --time=24:00:00
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4

# Unity cluster MACE training script
echo "Starting MACE training on Unity cluster..."
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURM_NODELIST"
echo "GPU: $CUDA_VISIBLE_DEVICES"

# Load required modules
module load conda/latest
module load cuda/11.8

# Activate conda environment
conda activate mace

# Check GPU availability
nvidia-smi

# Navigate to project directory
cd $SLURM_SUBMIT_DIR

# Run training
echo "Starting MACE training..."
python train_model.py

echo "Training completed!"
