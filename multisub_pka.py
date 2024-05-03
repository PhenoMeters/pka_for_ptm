import os, shutil, sys
import glob
from pathlib import Path

name = "multisub_pka"

account = "proteometer"
time = "72:00:00" 
time = "4-0" 
queque = "shared"
node = '1'
core = "64" 
out = "out_"
err = "err_"
mail = "alexandria.im@pnnl.gov" # will send a email once finished or terminated or failed
modules = ["gcc/7.5.0", "python/miniconda23.3.1"]
extras = [
        "source /share/apps/python/miniconda23.3.1/etc/profile.d/conda.sh", 
        "conda activate /qfs/projects/proteometer/pypka_conda",
        "export PATH=/qfs/projects/proteometer/pypka_conda/bin:$PATH",
        ]

workdir = "/people/imal967/ppi/sandbox"
pka_result_dir = "/rcfs/projects/proteometer/pka_db/"
pyscript_file = "/people/imal967/git_repos/ProCaliper-example/pypka_script_chunk.py"

slurm_template = "#!/bin/sh\n#SBATCH -A {}\n#SBATCH -t {}\n#SBATCH -N {}\n#SBATCH --cpus-per-task={}\n#SBATCH -p {}".format(account, time, node, core, queque)

uniprot_name_files = glob.glob(workdir + "/uniprot4pka*")

for input_dir in uniprot_name_files:

    ## Create subwork dir if not exist
    sub_dir = input_dir
    sub_file_name = sub_dir.split("/")[-1]
    full_file_dir = input_dir + "/" + sub_file_name +".csv"
    command = "cp " + pyscript_file + " " + sub_dir 
    os.system(command)
    
    slurm = [slurm_template]
    slurm.append("\n#SBATCH -o {}{}.txt\n#SBATCH -e {}{}.txt\n#SBATCH --mail-user={}\n#SBATCH --mail-type END\n \nmodule purge\n".format(out, sub_file_name, err, sub_file_name, mail))
    for module in modules:
        slurm.append("module load {}\n\n".format(module))
    for extra in extras:
        slurm.append("{}\n".format(extra))
    slurm.append("cd {}\n\n".format(sub_dir))

    slurm.append("python {} {} {} {}\n".format(pyscript_file, core, full_file_dir, pka_result_dir))

    filename = "{}/{}.sbatch".format(sub_dir, sub_dir.split("/")[-1])
    print(filename)
    with open(filename, 'w') as sbatch:
        sbatch.write(''.join(slurm))

    ### Before uncommenting the following, try to run this script and check if some of the slurm script are generated correctly.
    submission = "sbatch {}".format(filename) 
    os.system(submission)
