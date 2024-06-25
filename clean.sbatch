#!/bin/sh
#SBATCH -A proteometer
#SBATCH -t 10:00:00
#SBATCH -N 1
#SBATCH --job-name="TEST_clean_alphafold"
#SBATCH -o clean_out.log
#SBATCH -e clean_err.txt
#SBATCH --mail-user=alexandria.im@pnnl.gov
#SBATCH --mail-type END
#SBATCH --cpus-per-task=64

module purge
module load gcc/7.5.0

module load python/miniconda23.3.1

source /share/apps/python/miniconda23.3.1/etc/profile.d/conda.sh
conda activate /qfs/projects/proteometer/pypka_conda

python clean_pypka_csv.py /rcfs/projects/proteometer/pka_db /rcfs/projects/proteometer/human_AF_pKa /rcfs/projects/proteometer/alphafold_db/ 