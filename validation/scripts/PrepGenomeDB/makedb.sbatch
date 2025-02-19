#!/usr/bin/env bash
#SBATCH --job-name=make_db
#SBATCH --time 5-0                         
#SBATCH -p sched_mit_chisholm              
#SBATCH -c 1                               
#SBATCH -o logs/%j.out
#SBATCH -e logs/%j.err

source activate data

prosyn_classification="data/GorgAMZ_classification.xlsx"
genome_sources="path/to/all/genomes"  # path to dir with all genomes in database

python3 MakeGenomeDB.py $prosyn_classification $genome_sources