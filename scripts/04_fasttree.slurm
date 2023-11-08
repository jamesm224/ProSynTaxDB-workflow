#!/bin/bash
#SBATCH --job-name=04fasttree
#SBATCH --output=logs/slurm-%x-%j.out
#SBATCH --error=logs/slurm-%x-%j.err
#SBATCH -n 20
#SBATCH --exclusive
#SBATCH -t 1-00:00:00
#SBATCH -p sched_mit_chisholm
#SBATCH --mem=250000
#SBATCH --chdir=/nfs/chisholmlab001/jmullet/projects/23_gorg/scripts

##### Load Input Files #####
WORKDIR=/pool001/jmullet/gorgcycogamz20230927
INPUT_FASTA=/pool001/jmullet/gorgcycogamz20230927/phylogeny/syn_subset_tree.fas
PHYLIPCONVERT=/pool001/jmullet/gorgcycogamz20230927/scripts/fasta_to_phyliprelaxed.py

##### Script Preparation #####
hostname
date
mkdir ${WORKDIR}/phylogeny/
cd ${WORKDIR}/phylogeny/

##### Convert Fasta to Phylip File #####
cat ${INPUT_FASTA} | sed 's/?/-/g' > ${INPUT_FASTA}.faa
conda activate biopython_project
python3 ${PHYLIPCONVERT} \
    ${WORKDIR}/phylogeny/${INPUT_FASTA}.faa \
    ${WORKDIR}/phylogeny/${INPUT_FASTA}.phy

##### Create Phylogeny with FastTree #####
FastTreeMP -n 100 -boot 100 -lg -out fasttree_${INPUT_FASTA}.nwk ${INPUT_FASTA}.phy

##### Cleanup and Waiting steps #####
conda deactivate
date
