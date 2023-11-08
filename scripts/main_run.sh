#!/bin/bash
#SBATCH -p sched_mit_chisholm               # partition selection
#SBATCH -n 1
#SBATCH --output=logs/slurm-%x-%A-%a.out
#SBATCH --error=logs/slurm-%x-%A-%a.err

##### SET PATH VARIABLES #####
WORKDIR=/pool001/jmullet/gorgcycogamz20230927
CYCOGBLASTDIR=/pool001/jmullet/blast/cycog6
NAMESFILE=/pool001/jmullet/gorgcycogamz20230927/info/total_amz_gorg_syn_genomes.lst
INPUTDIR=/pool001/jmullet/gorgcycogamz20230927/protein_directories/total_proteins
BLASTDIR=/pool001/jmullet/gorgcycogamz20230927/blastp_test
FULLPROTEIN=/pool001/jmullet/gorgcycogamz20230927/base_files/Total_amz_gorg_syn_fourgenome.faa
ALIGNMENTDIR=/pool001/jmullet/gorgcycogamz20230927/alignments_test
CYCOGANNOTATIONS=/pool001/jmullet/gorgcycogamz20230927/info/sccg_count_annotation_threshold100.txt

##### Optional Steps for initial runs #####
#cp /nfs/chisholmlab002/pmberube/databases/gorgcycogamz20230905/phylogeny/cycog6markers/archive/${CYCOG}.faa .
#mkdir logs

##### Function to wait for a file to exist #####
wait_for_prior_script_completion() {
  local file_path="$1"
  while [ ! -f "$file_path" ]; do
    inotifywait -q -e create -e moved_to "$(dirname "$file_path")" 2>/dev/null
  done 
  }

#####BLAST Genomes against CyCOGS #####
sbatch 01_blastp.slurm ${WORKDIR} ${CYCOGBLASTDIR} ${NAMESFILE} ${INPUTDIR} ${BLASTDIR}

wait_for_prior_script_completion ${WORKDIR}/01_completion_flag.txt
echo "Step 1 Done"
wait

##### Optional BLAST for Big Script > 500 genomes #####
##### Parallel runs have job limits of 500 so processing more than 500 samples just #####
##### copy the following extension script and add as many as needed! #####
sbatch 01.2_blastp_extended_genomes.slurm ${WORKDIR} ${CYCOGBLASTDIR} ${NAMESFILE} ${INPUTDIR} ${BLASTDIR}

wait_for_prior_script_completion ${WORKDIR}/02_completion_flag.txt
echo "Step 1.2 Done"
wait

##### Align Proteins to CyCOGs #####
sbatch 02_clustalo.slurm ${WORKDIR} ${NAMESFILE} ${BLASTDIR} ${FULLPROTEIN} ${ALIGNMENTDIR} ${CYCOGANNOTATIONS}
wait
echo "Step 2 Done"

##### Optional Renaming Step #####
# wait_for_file /pool001/jmullet/gorgcycogamz20230927/02_completion_flag.txt
# sbatch 03_renamed_alignments.sh -a alignments_test
# wait
# echo "Step 3 Done"
