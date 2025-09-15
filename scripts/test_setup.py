#!/usr/bin/env python3
"""
Test MACE setup with dummy data to verify everything works
"""

import os
import numpy as np
from ase import Atoms
from ase.io import write

def create_dummy_training_data():
    """Create dummy XYZ data with proper energy and forces for testing"""
    
    # Create a simple water molecule
    atoms = Atoms('H2O', positions=[[0, 0, 0], [0.96, 0, 0], [0.48, 0.93, 0]])
    
    # Add dummy energy and forces
    atoms.info['energy_xtb'] = -76.0  # Dummy energy in eV
    atoms.arrays['forces_xtb'] = np.array([[0.1, 0.0, 0.0], 
                                          [-0.1, 0.0, 0.0], 
                                          [0.0, 0.0, 0.0]])  # Dummy forces
    
    return atoms

def main():
    print("🧪 Testing MACE Setup with Dummy Data")
    print("=" * 50)
    
    # Create test data
    print("Creating dummy training data...")
    test_atoms = create_dummy_training_data()
    
    # Write test files
    os.makedirs("data", exist_ok=True)
    write("data/test_train.xyz", [test_atoms] * 10)  # 10 identical structures
    write("data/test_valid.xyz", [test_atoms] * 2)   # 2 for validation
    
    print("✅ Test data created")
    print("Files created:")
    print("  - data/test_train.xyz (10 structures)")
    print("  - data/test_valid.xyz (2 structures)")
    
    # Test MACE import
    print("\nTesting MACE import...")
    try:
        from mace.cli.run_train import main as mace_run_train_main
        print("✅ MACE import successful")
    except ImportError as e:
        print(f"❌ MACE import failed: {e}")
        return False
    
    # Test data loading
    print("\nTesting data loading...")
    try:
        from ase.io import read
        atoms = read("data/test_train.xyz", ":")
        print(f"✅ Loaded {len(atoms)} structures")
        print(f"   Energy key present: {'energy_xtb' in atoms[0].info}")
        print(f"   Forces key present: {'forces_xtb' in atoms[0].arrays}")
        print(f"   Energy value: {atoms[0].info.get('energy_xtb', 'MISSING')}")
    except Exception as e:
        print(f"❌ Data loading failed: {e}")
        return False
    
    print("\n🎉 Setup test completed successfully!")
    print("\nNext steps:")
    print("1. Get energy file from Melissa")
    print("2. Convert ML_AB2 to proper XYZ format")
    print("3. Run actual training")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup test failed. Please check the errors above.")
        exit(1)
