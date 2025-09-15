#!/bin/bash
# Setup script for MACE conda environment on Unity cluster
# This script creates a conda environment with all necessary dependencies

echo "Setting up MACE conda environment on Unity cluster..."

# Load conda module on Unity cluster
module load conda/latest

# Create conda environment with Python 3.11 (newest stable version)
conda create -n mace python=3.11 -y

# Activate the environment
conda activate mace

# Upgrade pip
pip install --upgrade pip

# Install PyTorch (newest version with CUDA support for Unity cluster)
# Note: Adjust CUDA version based on Unity's available CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install MACE and dependencies
pip install mace-torch

# Install additional scientific computing packages
pip install numpy scipy matplotlib pandas
pip install ase  # Atomic Simulation Environment
pip install h5py  # For handling large datasets

# Install LAMMPS interface (if needed)
pip install lammps

echo "MACE environment setup complete!"
echo "To activate: module load conda/latest && conda activate mace"
