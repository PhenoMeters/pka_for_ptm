#!/bin/sh
#SBATCH -A proteometer
#SBATCH -t 01:00:00
#SBATCH -N 1
#SBATCH --job-name="partition_db"
#SBATCH -o out.log
#SBATCH -e err.txt
#SBATCH --mail-user=alexandria.im@pnnl.gov
#SBATCH --mail-type END
#SBATCH --cpus-per-task=64

# approximate run time for 100 is 1 min
module purge
module load gcc/7.5.0

module load python/miniconda23.3.1

source /share/apps/python/miniconda23.3.1/etc/profile.d/conda.sh
conda activate /qfs/projects/proteometer/pypka_conda

python partition_uniprot_csv.py /people/imal967/ppi/sandbox /rcfs/projects/proteometer/alphafold_db 50 /rcfs/projects/proteometer/already_made.csv


