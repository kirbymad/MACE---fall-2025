# MACE Project Action Plan - Going Forward

## 🎯 Current Status
- ✅ Environment set up (conda, ASE, MACE installed)
- ✅ Shirui's workflow reproduced and understood
- ✅ Stumbling blocks identified
- ❌ Missing energy data from Melissa
- ❌ Need proper data conversion

## 🚨 Critical Issues to Resolve

### 1. **Data Conversion Problem**
**Issue**: ML_AB2 file needs to be converted to XYZ with energies
**Missing**: Energy file from Melissa (extracted from OUTCAR files)
**Solution**: 
- Get energy file from Melissa
- Use MakeInputFile.py to convert ML_AB2 + energies → proper XYZ
- Ensure XYZ has `energy_xtb` and `forces_xtb` keys

### 2. **GPU Access**
**Issue**: No CUDA available on current node
**Solutions**:
- Use CPU for testing (already configured)
- Submit to GPU nodes via SLURM: `sbatch scripts/train_mace_unity.sh`
- Check available GPU resources: `sinfo -p gpu`

### 3. **Memory Issues** (mentioned in original notes)
**Potential Solutions**:
- Reduce batch size (currently 10, try 5 or 2)
- Use gradient accumulation
- Enable mixed precision training
- Monitor memory usage during training

## 📋 Immediate Next Steps

### Step 1: Get Energy Data
```bash
# Contact Melissa for:
# - Energy file extracted from OUTCAR files
# - Final energies without enthalpy values
# - Format: one energy per line, matching ML_AB2 configurations
```

### Step 2: Convert Data Properly
```bash
# Once energy file is available:
python MakeInputFile.py --ml_ab_file ML_AB2 --energy_file data/energies.txt --output data/Y_BaZrO3_input_data.xyz
```

### Step 3: Verify Data Format
```bash
# Check that XYZ file has required keys:
python -c "
from ase.io import read
atoms = read('data/Y_BaZrO3_input_data.xyz', ':1')
print('Info keys:', list(atoms[0].info.keys()))
print('Array keys:', list(atoms[0].arrays.keys()))
"
```

### Step 4: Test Training
```bash
# Test on CPU first:
python train_model2.py

# Then submit to GPU cluster:
sbatch scripts/train_mace_unity.sh
```

## 🔧 Configuration Adjustments Needed

### For Memory Issues:
```yaml
# In config.yml:
batch_size: 5  # Reduce from 10
max_num_epochs: 100  # Increase from 50
device: cpu  # For testing, then cuda for production
```

### For Better Training:
```yaml
# Consider these changes:
r_max: 2.0  # Increase from 1.0 (more interactions)
num_channels: 64  # Increase from 32 (more model capacity)
valid_fraction: 0.15  # Increase validation set
```

## 📊 Expected Workflow

1. **Data Preparation** (1-2 days)
   - Get energy file from Melissa
   - Convert ML_AB2 to proper XYZ format
   - Split into train/test sets

2. **Initial Training** (1 day)
   - Test on CPU with small batch size
   - Verify training works without errors
   - Check memory usage

3. **Production Training** (2-3 days)
   - Submit to GPU cluster
   - Monitor training progress
   - Adjust hyperparameters if needed

4. **Model Evaluation** (1 day)
   - Test trained model on test set
   - Calculate RMSE and other metrics
   - Compare with reference calculations

5. **LAMMPS Integration** (1-2 days)
   - Interface trained model with LAMMPS
   - Test energy minimization
   - Find transition states

## 🎯 Success Metrics

- **Training RMSE**: < 0.01 eV/atom (target)
- **Test RMSE**: < 0.02 eV/atom (target)
- **Forces RMSE**: < 0.1 eV/Å (target)
- **Training time**: < 24 hours on GPU
- **Memory usage**: < 32GB during training

## 🚨 Risk Mitigation

1. **Data Quality**: Verify energy values are reasonable
2. **Memory Issues**: Start with small batch sizes
3. **GPU Availability**: Have CPU fallback ready
4. **Training Convergence**: Monitor loss curves
5. **Model Validation**: Test on known systems first
