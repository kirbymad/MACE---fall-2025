# MACE Project - Gomez Lab Fall 2025

This repository contains the MACE (Machine learning Accelerated Computational Environment) project for the Gomez Lab, with contributions from Shirui and Melissa.

## Project Structure

```
MACE_Project/
├── scripts/           # Python scripts for data processing and training
├── configs/           # Configuration files for MACE training
├── data/              # Input data files (ML_AB, energies, xyz files)
├── models/            # Trained MACE models (gitignored)
├── outputs/           # Training outputs and logs (gitignored)
├── ML_AB2             # ML_AB data file from Melissa
├── MakeInputFile.py   # Data conversion script from Shirui
├── train_model.py     # Training script
├── eval.py            # Evaluation script
└── README.md          # This file
```

## Files from Shirui and Melissa

✅ **Files already uploaded:**
- `ML_AB2` - ML_AB data file from Melissa
- `MakeInputFile.py` - Data conversion script from Shirui
- `train_model.py` - Training script
- `eval.py` - Evaluation script
- `solvent_configs.xyz` - Example input data file
- `config.yml` - Configuration file
- `useful commands.docx` - Documentation
- `mace_Shirui and Melissa.docx` - Project documentation

## Setup Instructions

### 1. Environment Setup
```bash
# Run the conda environment setup script
bash scripts/setup_conda_env.sh
```

### 2. Data Preparation
```bash
# Convert ML_AB and energy files to xyz format
python MakeInputFile.py --ml_ab_file ML_AB2 --energy_file data/energies.txt --output data/training_data.xyz
```

### 3. Training
```bash
# Train the MACE model
bash train_mace.sh
```

## Notes

- Large data files are already in the repository
- Model files and outputs are gitignored to keep the repository size manageable
- Update the configuration files with your specific parameters (atomic numbers, E0 values, etc.)

## Memory Issues

If you encounter memory issues during training:
1. Reduce batch size in the configuration file
2. Use gradient accumulation
3. Consider using mixed precision training
4. Monitor GPU memory usage with `nvidia-smi`
