import os
import sys
import glob
from pathlib import Path
import pandas as pd

name = "multisub_pka"

account = "proteometer"
time = "4-0"
queue = "slurm"
node = '1'
core = "64"
out = "out"
err = "err"
mail = "song.feng@pnnl.gov"  # will send a email once finished or terminated or failed
modules = ["gcc/7.5.0", "python/miniconda23.3.1"]
extras = [
        "source /share/apps/python/miniconda23.3.1/etc/profile.d/conda.sh",
        "conda activate /qfs/projects/proteometer/pypka_conda",
        "export PATH=/qfs/projects/proteometer/pypka_conda/bin:$PATH",
        ]

pyscript_file = "/qfs/projects/proteometer/pka_for_ptm/pypka_script_chunk.py"

AF_structure_dir = os.path.abspath(sys.argv[1])
AF_pka_dir = os.path.abspath(sys.argv[2])
work_dir = os.path.abspath(sys.argv[3])
chunk_num = int(sys.argv[4])
# current_dir = os.getcwd()
# pyscript_file_ori = os.path.join(current_dir, "pypka_script_chunk.py")

structure_names = [Path(file_path).stem for file_path in glob.glob(AF_structure_dir + "/*.pdb")]
pka_names = [Path(file_path).stem for file_path in glob.glob(AF_pka_dir + "/*.csv")]

names2anlayze = list(set(structure_names) - set(pka_names))

slurm_template = f"#!/bin/sh\n#SBATCH -A {account}\n#SBATCH -t {time}\n#SBATCH -N {node}\n#SBATCH --cpus-per-task={core}\n#SBATCH -p {queque}"

for i in range(chunk_num):
    chunk_name = f"uniprot4pka_{i}"
    pdb_list_filename = f"{chunk_name}.csv"
    work_dir_i = f"{work_dir}/{chunk_name}"
    os.system(f"mkdir {work_dir_i}")
    new_pyscript_file = os.path.join(work_dir_i, os.path.basename(pyscript_file))
    os.system(f"cp {pyscript_file} {new_pyscript_file}")
    files2analyze = [os.path.join(AF_structure_dir, name + ".pdb") for name in names2anlayze[i::chunk_num]]
    files2analyze = pd.DataFrame({"pdb_path": files2analyze})
    pdb_list_filepath = os.path.join(work_dir_i, pdb_list_filename)
    files2analyze.to_csv(pdb_list_filepath)
    # create slurm script
    slurm = [slurm_template]
    slurm.append(f"\n#SBATCH -o {out}_{pdb_list_filename}.txt\n#SBATCH -e {err}_{pdb_list_filename}.txt\n#SBATCH --mail-user={mail}\n#SBATCH --mail-type END\n \nmodule purge\n")
    for module in modules:
        slurm.append(f"module load {module}\n\n")
    for extra in extras:
        slurm.append(f"{extra}\n")
    slurm.append(f"cd {work_dir_i}\n\n")

    slurm.append(f"python {new_pyscript_file} {core} {pdb_list_filepath} {AF_pka_dir}\n")

    slurm_filename = f"{work_dir_i}/{chunk_name}.sbatch"
    print(slurm_filename)
    with open(slurm_filename, 'w') as sbatch:
        sbatch.write(''.join(slurm))
    submission = "sbatch {}".format(slurm_filename) 
    os.system(submission)
