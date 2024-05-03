#!/bin/sh
#SBATCH -A proteometer
#SBATCH -t 05:00:00
#SBATCH -N 1
#SBATCH --job-name="gunzip_alphafold_db"
#SBATCH -o out.log
#SBATCH -e err.txt
#SBATCH --mail-user=alexandria.im@pnnl.gov
#SBATCH --mail-type END
#SBATCH --cpus-per-task=64

 
cd /people/imal967/ppi/data/alphafold_human_proteome_DB_pdb 
gunzip *.gz
mv ./*.pdb /rcfs/projects/proteometer/alphafold_db
