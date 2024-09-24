#!/usr/bin/env bash
#SBATCH --job-name=classify-smk
#SBATCH --time 5:00:00                         # wall clock limit
#SBATCH -p sched_mit_chisholm               # partition selection
#SBATCH -c 1                                # tasks (essentially threads)
#SBATCH -o logs/%j.out
#SBATCH -e logs/%j.err

eval "$(conda shell.bash hook)"
conda activate snakemake

snakemake --profile profile 
