#!/bin/bash
#SBATCH --job-name=train_mace
#SBATCH --partition=skygpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --gpus-per-node=2
#SBATCH --mem=40GB
#SBATCH --time=24:00:00
##SBATCH --constraint=cpu_gen_broadwell ##cascadelake
#SBATCH --constraint=cpu_gen_cascadelake

module load anaconda3/2023.09-0
source activate mace_env

python train_model2.py