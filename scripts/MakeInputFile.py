#!/usr/bin/env python3
"""
MakeInputFile.py
Script to compile ML_AB data and energy files into xyz format for MACE training.

This script:
1. Reads ML_AB files containing atomic configurations
2. Reads energy files with final energies (without enthalpy) from OUTCAR files
3. Combines them into xyz format required by MACE
4. Optionally adds charges if available

Usage:
    python MakeInputFile.py --ml_ab_file path/to/ML_AB --energy_file path/to/energies.txt --output output.xyz
"""

import argparse
import numpy as np
import os
from ase import Atoms
from ase.io import write
import re

def parse_ml_ab_file(ml_ab_file):
    """
    Parse ML_AB file to extract atomic configurations.
    
    Args:
        ml_ab_file (str): Path to ML_AB file
        
    Returns:
        list: List of ASE Atoms objects
    """
    configurations = []
    
    with open(ml_ab_file, 'r') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for configuration header (usually contains number of atoms)
        if line.isdigit():
            num_atoms = int(line)
            i += 1
            
            # Skip comment line
            if i < len(lines):
                comment = lines[i].strip()
                i += 1
            
            # Read atomic positions
            positions = []
            symbols = []
            charges = []
            
            for j in range(num_atoms):
                if i < len(lines):
                    parts = lines[i].strip().split()
                    if len(parts) >= 4:
                        symbol = parts[0]
                        x, y, z = map(float, parts[1:4])
                        charge = float(parts[4]) if len(parts) > 4 else 0.0
                        
                        symbols.append(symbol)
                        positions.append([x, y, z])
                        charges.append(charge)
                        i += 1
            
            # Create ASE Atoms object
            if symbols and positions:
                atoms = Atoms(symbols=symbols, positions=positions)
                if charges and any(c != 0 for c in charges):
                    atoms.set_initial_charges(charges)
                configurations.append(atoms)
        else:
            i += 1
    
    return configurations

def parse_energy_file(energy_file):
    """
    Parse energy file containing final energies from OUTCAR files.
    
    Args:
        energy_file (str): Path to energy file
        
    Returns:
        list: List of energies
    """
    energies = []
    
    with open(energy_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                try:
                    energy = float(line)
                    energies.append(energy)
                except ValueError:
                    print(f"Warning: Could not parse energy value: {line}")
    
    return energies

def create_xyz_file(configurations, energies, output_file, charges=None):
    """
    Create xyz file in MACE format.
    
    Args:
        configurations (list): List of ASE Atoms objects
        energies (list): List of energies
        output_file (str): Output xyz file path
        charges (list, optional): List of charge arrays for each configuration
    """
    if len(configurations) != len(energies):
        raise ValueError(f"Number of configurations ({len(configurations)}) doesn't match number of energies ({len(energies)})")
    
    with open(output_file, 'w') as f:
        for i, (atoms, energy) in enumerate(zip(configurations, energies)):
            # Write number of atoms
            f.write(f"{len(atoms)}\n")
            
            # Write comment line with energy
            comment = f"energy={energy:.6f}"
            if charges and i < len(charges):
                charge_str = " ".join([f"{c:.3f}" for c in charges[i]])
                comment += f" charges={charge_str}"
            f.write(f"{comment}\n")
            
            # Write atomic coordinates
            for j, (symbol, pos) in enumerate(zip(atoms.get_chemical_symbols(), atoms.get_positions())):
                x, y, z = pos
                f.write(f"{symbol} {x:.6f} {y:.6f} {z:.6f}\n")

def main():
    parser = argparse.ArgumentParser(description='Convert ML_AB and energy files to xyz format for MACE')
    parser.add_argument('--ml_ab_file', required=True, help='Path to ML_AB file')
    parser.add_argument('--energy_file', required=True, help='Path to energy file')
    parser.add_argument('--output', required=True, help='Output xyz file path')
    parser.add_argument('--charges_file', help='Optional file containing charges for each configuration')
    
    args = parser.parse_args()
    
    # Check if input files exist
    if not os.path.exists(args.ml_ab_file):
        raise FileNotFoundError(f"ML_AB file not found: {args.ml_ab_file}")
    if not os.path.exists(args.energy_file):
        raise FileNotFoundError(f"Energy file not found: {args.energy_file}")
    
    print(f"Reading ML_AB file: {args.ml_ab_file}")
    configurations = parse_ml_ab_file(args.ml_ab_file)
    print(f"Found {len(configurations)} configurations")
    
    print(f"Reading energy file: {args.energy_file}")
    energies = parse_energy_file(args.energy_file)
    print(f"Found {len(energies)} energies")
    
    # Parse charges if provided
    charges = None
    if args.charges_file and os.path.exists(args.charges_file):
        print(f"Reading charges file: {args.charges_file}")
        # Implement charge parsing if needed
        # charges = parse_charges_file(args.charges_file)
    
    print(f"Creating xyz file: {args.output}")
    create_xyz_file(configurations, energies, args.output, charges)
    print("Conversion complete!")

if __name__ == "__main__":
    main()
