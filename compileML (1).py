import ast

def parse_ml_ab_file(input_path, output_path):
    with open(input_path, 'r') as infile:
        lines = infile.readlines()

    xyz_blocks = []
    block = []
    for line in lines:
        if line.strip() == "":
            if block:
                xyz_blocks.append(block)
                block = []
        else:
            block.append(line.strip())
    if block:
        xyz_blocks.append(block)

    with open(output_path, 'w') as outfile:
        for block in xyz_blocks:
            atoms = []
            energy = None
            forces = []

            for line in block:
                if line.startswith("energy="):
                    energy = float(line.split("=", 1)[1])
                elif line.startswith("forces="):
                    forces = ast.literal_eval(line.split("=", 1)[1])
                elif len(line.split()) == 4:
                    element, x, y, z = line.split()
                    atoms.append((element, float(x), float(y), float(z)))

            # Sanity check
            assert len(atoms) == len(forces), "Mismatch between atoms and forces"

            # Write header
            outfile.write(f"{len(atoms)}\n")
            forces_str = "[" + ", ".join(
                f"[{f[0]:.6f}, {f[1]:.6f}, {f[2]:.6f}]" for f in forces
            ) + "]"
            outfile.write(f"energy={energy:.12f} forces={forces_str}\n")

            # Write atoms
            for atom in atoms:
                element, x, y, z = atom
                outfile.write(f"{element:<2} {x:.7f} {y:.7f} {z:.7f}\n")

    print(f"✅ Converted file saved to {output_path}")

# Usage
parse_ml_ab_file("/mnt/data/ML_AB", "/mnt/data/converted_mace.xyz")

