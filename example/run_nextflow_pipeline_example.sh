#!/bin/bash
#SBATCH --job-name=nextflow          # used to name partition #
#SBATCH -p partition                 # partition selection #
#SBATCH -n 20                        # tasks (essentially threads) #
#SBATCH --mem 250G                   # amount of memory desired #
#SBATCH --time 10:00:00              # time for slurm script #
#SBATCH --output=slurm-%x-%A-%a.out  # output slurm file #
#SBATCH --error=slurm-%x-%A-%a.err   # error slurm file #


nextflow run updated_run.nf \
    --input_reads '/orcd/data/chisholm/001/chisholmlab/experiment_repository/2024/240515Chi/*/*_{1,2}_sequence.fastq' \
    --nodes /pool001/jmullet/gorgcycogamz20230927/updated_GORG_work/final_database_files/final_ncbi_pro_nodes.dmp \
    --names /pool001/jmullet/gorgcycogamz20230927/updated_GORG_work/final_database_files/final_ncbi_pro_names.dmp \
    --fmi /pool001/jmullet/gorgcycogamz20230927/updated_GORG_work/final_database_files/final_MARMICRODB2_virus.fmi \
    --outputdir /orcd/data/chisholm/001/bioinfo/projects/24_updated_GORG_AMZ_classifier/5_15_test \
    --dmnd /pool001/jmullet/blast/cycog6/CyCOG6.dmnd \
    --cycogs /orcd/data/chisholm/001/bioinfo/projects/24_updated_GORG_AMZ_classifier/bin/combined_mean_length.tsv \
    --bin /orcd/data/chisholm/001/bioinfo/projects/24_updated_GORG_AMZ_classifier/bin \
    --max_cpus 30 \
    --max_memory 500G
