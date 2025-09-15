# MACE Project - Gomez Lab Fall 2025

This repository contains the MACE (Machine learning Accelerated Computational Environment) project for the Gomez Lab.

## Project Structure

```
MACE_Project/
├── scripts/           # Python scripts for data processing and training
├── configs/           # Configuration files for MACE training
├── data/              # Input data files (ML_AB, energies, xyz files)
├── models/            # Trained MACE models (gitignored)
├── outputs/           # Training outputs and logs (gitignored)
└── README.md          # This file
```

## Setup Instructions

### 1. Environment Setup
```bash
# Run the conda environment setup script
bash scripts/setup_conda_env.sh
```

### 2. Data Preparation
```bash
# Convert ML_AB and energy files to xyz format
python scripts/MakeInputFile.py --ml_ab_file data/ML_AB_file --energy_file data/energies.txt --output data/training_data.xyz
```

### 3. Training
```bash
# Train the MACE model
bash scripts/train_mace.sh
```

## Files from Shirui and Melissa

Please upload the following files to the appropriate directories:

### From Shirui:
- `MakeInputFile.py` (if different from the one in scripts/)
- Any additional data processing scripts
- Training configurations

### From Melissa:
- ML_AB files (place in `data/` directory)
- Energy files extracted from OUTCAR files (place in `data/` directory)
- Any additional data files

## Notes

- Large data files should be uploaded to a cloud storage service or use Git LFS
- Model files and outputs are gitignored to keep the repository size manageable
- Update the configuration files with your specific parameters (atomic numbers, E0 values, etc.)

## Memory Issues

If you encounter memory issues during training:
1. Reduce batch size in the configuration file
2. Use gradient accumulation
3. Consider using mixed precision training
4. Monitor GPU memory usage with `nvidia-smi`
