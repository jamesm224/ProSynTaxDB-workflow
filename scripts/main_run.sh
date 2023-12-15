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

##### Define Waiting Function to ensure each step is finished sequentially #####
wait_for_job_completion() {
    local job_id="$1"
    while squeue -j $job_id --format="%T" | grep -q "R"; do
        echo "Waiting for job $job_id to complete..."
        sleep 10  # Sleep for 10 seconds
    done
    echo "Job $job_id completed."
}

##### 1. BLAST Genomes against CyCOGS #####
printf "\nBeginning Step 1\n"
export START_TIME_1=$(date +%s)

### Execute command and wait for all of the jobs to be completed ###
export JOBID_1=$(sbatch --export=ALL 01_blastp.slurm ${WORKDIR} ${CYCOGBLASTDIR} ${NAMESFILE} ${INPUTDIR} ${BLASTDIR} | awk '{print $4}')
echo "JOBID_1: $JOBID_1"

### Create completion flag for Step 1 ###
touch ${WORKDIR}/01_completion_flag.txt

### Monitor the progress and estimate completion time ###
echo "Waiting for job $JOBID_1 to complete..."
# While job is still running print elapsed time #
while squeue -j $JOBID_1 >/dev/null; do
    CURRENT_TIME=$(date +%s)
    ELAPSED_TIME=$((CURRENT_TIME - START_TIME_1))
    echo "Step 1 in progress, elapsed time: $ELAPSED_TIME seconds"
    # Check every 5 minutes for job completion #
    sleep 300  
done

printf "\nStep 1 Done\n"

##### 1.2 Optional BLAST for Big Script > 500 genomes #####
### Parallel runs have job limits of 500 so processing more than 500 samples ###
### just copy the following extension script and add as many as needed! ###
printf "\nBeginning Step 1.2\n"
export START_TIME_2=$(date +%s)

### Execute command and wait for all of the jobs to be completed ###
export JOBID_2=$(sbatch --dependency=afterok:$JOBID_1 --export=ALL 01.2_blastp_extended_genomes.slurm ${WORKDIR} ${CYCOGBLASTDIR} ${NAMESFILE} ${INPUTDIR} ${BLASTDIR} | awk '{print $4}')
echo "JOBID_2: $JOBID_2"

### Remove the completion flag for Step 1 and create completion flag for Step 1.2 ###
rm ${WORKDIR}/01_completion_flag.txt
touch ${WORKDIR}/02_completion_flag.txt

### Monitor the progress and estimate completion time ###
echo "Waiting for job $JOBID_2 to complete..."
# While job is still running print elapsed time #
while squeue -j $JOBID_2 >/dev/null; do
    CURRENT_TIME=$(date +%s)
    ELAPSED_TIME=$((CURRENT_TIME - START_TIME_2))
    echo "Step 1.2 in progress, elapsed time: $ELAPSED_TIME seconds"
    # Check every 5 minutes for job completion #
    sleep 300
done

printf "\nStep 1.2 Done\n"

# ##### Optional Step to remove potential stop codons #####
# printf "\nRemoving Stop Codons\n"
# /path/to/file/
# find . -type f -exec sed -i 's/\*//g' {} \;
# printf "\nCompleted Removing Stop Codons\n"

##### 2. Align Proteins to CyCOGs #####
printf "\nBeginning Step 2\n"
export START_TIME_3=$(date +%s)

### Execute command and wait for all of the jobs to be completed ###
export JOBID_3=$(sbatch --dependency=afterok:$JOBID_2 --export=ALL 02_clustalo.slurm ${WORKDIR} ${NAMESFILE} ${BLASTDIR} ${FULLPROTEIN} ${ALIGNMENTDIR} ${CYCOGANNOTATIONS} | awk '{print $4}')
echo "JOBID_3: $JOBID_3"

### Remove the completion flag for Step 1.2 and create completion flag for Step 2 ###
rm ${WORKDIR}/02_completion_flag.txt
touch ${WORKDIR}/03_completion_flag.txt

### Wait for all tasks to complete for Step 2 ###
echo "Waiting for job $JOBID_3 to complete..."
# While job is still running print elapsed time #
while squeue -j $JOBID_3 >/dev/null; do
    CURRENT_TIME=$(date +%s)
    ELAPSED_TIME=$((CURRENT_TIME - START_TIME_3))
    echo "Step 2 in progress, elapsed time: $ELAPSED_TIME seconds"
    # Check every 5 minutes for job completion #
    sleep 300
done

printf "\nStep 2 Done\n"

##### Optional Renaming Step #####
# wait_for_file /pool001/jmullet/gorgcycogamz20230927/02_completion_flag.txt
# sbatch 03_renamed_alignments.sh -a alignments_test
# wait
# echo "Step 3 Done"

##### Remove spaces after MEGA #####
# sed -i 's/>[[:graph:]][[:space:]]*/&>/; s/[[:space:]]*$//' your_fasta_file.fasta
# awk '/^>/ {gsub(/[[:space:]]/, "", $0); printf "%s\n", $0; next} 1' your_fasta_file.fasta > temp.fasta
