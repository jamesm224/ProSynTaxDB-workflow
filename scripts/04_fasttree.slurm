#!/bin/bash
#SBATCH --job-name=04fasttree
#SBATCH --output=logs/slurm-%x-%j.out
#SBATCH --error=logs/slurm-%x-%j.err
#SBATCH -n 20
#SBATCH --exclusive
#SBATCH -t 1-00:00:00
#SBATCH -p sched_mit_chisholm
#SBATCH --mem=250000
#SBATCH --chdir=/pool001/jmullet/gorgcycogamz20230927/scripts

##### Load Input Files #####
WORKDIR=/pool001/jmullet/gorgcycogamz20230927
INPUT_FASTA=/pool001/jmullet/gorgcycogamz20230927/phylogeny/total_updated_genomes.faa
filename=$(basename "$INPUT_FASTA")
variable="${filename%.*}"
fasta_input="${variable%.*}"

##### Script Preparation #####
hostname
date
#mkdir ${WORKDIR}/phylogeny/
cd ${WORKDIR}/phylogeny/

##### Convert Fasta to Phylip File #####
eval "$(conda shell.bash hook)"
conda activate biopython_project

##### Create Phylogeny with FastTree #####
FastTreeMP \
    -lg \
    -boot 100 \
    -out fasttree_${fasta_input}.nwk \
    ${fasta_input}.faa

##### Cleanup and Waiting steps #####
conda deactivate
date
