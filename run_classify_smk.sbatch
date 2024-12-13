#!/usr/bin/env bash
#SBATCH --job-name=classify-smk
#SBATCH --time 2-0                        
#SBATCH --partition sched_mit_chisholm              
#SBATCH --cpus-per-task 1                                
#SBATCH -o logs/%j.out
#SBATCH -e logs/%j.err

eval "$(conda shell.bash hook)"
conda activate snakemake

snakemake --profile profile 
