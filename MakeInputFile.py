import re

def split_mlab_config(mlab_path):
    # Read ML_AB and split into blocks of configs
    with open(mlab_path, "r") as f:
        content = f.read()
        raw_blocks = content.split("Configuration num.")[1:]
    return raw_blocks

def get_NumOfAtoms(blcok_config):
    match = re.search(r'The number of atoms.*?(\d+)', blcok_config, re.DOTALL)
    if match:
        return int(match.group(1))
    else:
        raise ValueError("No 'num of atoms' followed by an integer found.")

def get_AtomType_and_AtomNum(blcok_config):
    atom_counts = {}
    lines = blcok_config.strip().splitlines()

    # Step 1: Find the section header
    start_index = None
    for i, line in enumerate(lines):
        if "Atom types and atom numbers" in line:
            start_index = i + 1  # Start after the header line
            break

    if start_index is None:
        raise ValueError("No 'Atom types and atom numbers' section found.")

    # Step 2: Skip dashed line(s)
    while start_index < len(lines) and set(lines[start_index].strip()) == {"-"}:
        start_index += 1

    # Step 3: Parse following lines until a non-matching line is encountered
    pattern = r'^([A-Z][a-z]?)\s+(\d+)$'
    for line in lines[start_index:]:
        line = line.strip()
        match = re.match(pattern, line)
        if match:
            atom = match.group(1)
            count = int(match.group(2))
            atom_counts[atom] = count
        else:
            break  # Stop if line doesn't match the expected format

    return atom_counts

def get_xyz_coordinates(block_config):
    lines = block_config.strip().splitlines()

    # Step 1: Locate the start of the atomic positions section
    start_index = None
    for i, line in enumerate(lines):
        if "Atomic positions (ang.)" in line:
            start_index = i + 1
            break

    if start_index is None:
        raise ValueError("No 'Atomic positions (ang.)' section found.")

    # Step 2: Skip dashed lines
    while start_index < len(lines) and re.match(r"^-+$", lines[start_index].strip()):
        start_index += 1

    # Step 3: Collect coordinate lines until next section (marked by ======= or other headers)
    atomic_positions = []
    for line in lines[start_index:]:
        if re.match(r"^[=\-*]+$", line.strip()) or "Total energy" in line or "Forces" in line:
            break  # end of the coordinate block
        if line.strip():
            # Parse three floats
            parts = line.strip().split()
            if len(parts) == 3:
                coords = list(map(float, parts))
                atomic_positions.append(coords)

    return atomic_positions

def get_totalE(blcok_config):
    match = re.search(r'Total energy \(eV\).*?([-+]?\d+\.\d+)', blcok_config, re.DOTALL)
    if match:
        return float(match.group(1))
    else:
        raise ValueError("No 'totalE' found.")
    
def get_forces_xyz(block_config):
    lines = block_config.strip().splitlines()

    # Step 1: Find the start of the Forces section
    start_index = None
    for i, line in enumerate(lines):
        if "Forces (eV ang.^-1)" in line:
            start_index = i + 1
            break

    if start_index is None:
        raise ValueError("No 'Forces (eV ang.^-1)' section found.")

    # Step 2: Skip dashed lines
    while start_index < len(lines) and re.match(r"^-+$", lines[start_index].strip()):
        start_index += 1

    # Step 3: Collect force lines until the next section
    forces = []
    for line in lines[start_index:]:
        if re.match(r"^[=\-*]+$", line.strip()) or "Stress" in line:
            break  # end of forces block
        if line.strip():
            values = list(map(float, line.strip().split()))
            if len(values) == 3:
                forces.append(values)

    return forces

def write_inputdatafile(mlab_path, output_path):
    raw_blocks = split_mlab_config(mlab_path)
    
    # Open the output file to write the formatted data
    with open(output_path, "w") as out:
        
        config_index= 0 
        for block_config in raw_blocks:
            config_index = config_index + 1
            #print(block_config)
            NumOfAtoms = get_NumOfAtoms(block_config)
            #print(NumOfAtoms)
            TotalE = get_totalE(block_config)
            #print(TotalE)
            AtomDict = get_AtomType_and_AtomNum(block_config)
            #print(AtomDict)
            xyz_coord_list = get_xyz_coordinates(block_config)
            #print(xyz_coord_list)
            forces_list = get_forces_xyz(block_config)
            #print(forces_list)

            out.write(str(NumOfAtoms)+ "\n")
            out.write('Properties=species:S:1:pos:R:3:molID:I:1:forces_xtb:R:3 Nmols=1' + ' energy_xtb=' + str(TotalE) + ' pbc="T T T"'+ "\n")
            
            atoms = AtomDict.keys()
            num = 0 
            lowerbound = 0
            for atom in atoms:
                num = int(AtomDict[atom]) + num
                for i in range(lowerbound, int(num)):
                    out.write(atom + "      " + str(xyz_coord_list[i][0]) + "      " + str(xyz_coord_list[i][1]) + "     " + str(xyz_coord_list[i][2]) + "      " + str(0) + "      " + str(forces_list[i][0]) + "      " + str(forces_list[i][1]) + "      " + str(forces_list[i][2]) + "\n")
                    lowerbound = num
            
            print(config_index)

write_inputdatafile("ML_AB2", "Y_BaZrO3_input_data.xyz")
