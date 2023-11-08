#!/usr/bin/env bash
#SBATCH --job-name=01.2blastp
#SBATCH --output=logs/slurm-%x-%A-%a.out
#SBATCH --error=logs/slurm-%x-%A-%a.err
#SBATCH -N 1
#SBATCH --exclusive
#SBATCH -t 0-00:20:00
#SBATCH -p sched_mit_chisholm
#SBATCH --mem=250000
#SBATCH --chdir=/pool001/jmullet/gorgcycogamz20230927/scripts
#SBATCH --array=2-2%1

##### Load Input Files #####
WORKDIR=$1
CYCOGBLASTDIR=$2
NAMESFILE=$3
INPUTDIR=$4
BLASTDIR=$5

##### PARSE ARRAY ID #####
GENOMENAME=$(cat ${NAMESFILE} | awk -v LINENUMBER=${SLURM_ARRAY_TASK_ID} '{if ( NR == LINENUMBER ) {print $1}}')

##### Script Preparation #####
hostname
date
cd ${WORKDIR}/
mkdir ${BLASTDIR}
cd ${BLASTDIR}
eval "$(conda shell.bash hook)"  
conda activate biopython_project

##### FIND CYCOG6 MATCHES FOR EACH GORG PROTEIN IN EACH PRO,SYN,CYANO GENOME #####
##### USE EVALUE OF 0.001 WHICH IS DEFAULT FOR PANX DIAMOND SEARCH FOR HOMOLOGY #####
blastp \
    -db ${CYCOGBLASTDIR}/CyCOG6 \
    -query ${INPUTDIR}/${GENOMENAME}.faa \
    -out ${GENOMENAME}_blastp_cycog6.out \
    -evalue 0.001 \
    -num_threads 20 \
    -outfmt "6 qseqid sseqid evalue bitscore pident qcovs qcovhsp"

##### RETAIN ONLY THE BEST HIT USING AWK #####
cat ${GENOMENAME}_blastp_cycog6.out | awk -F "\t" '!seen[$1]++' > ${GENOMENAME}_blastp_cycog6_tophit.out

##### REPLACE THE PIPE WITH A TAB TO MAKE A TAB DELIMITED FILE WITH CYCOG6 MATCH IN COLUMN 3 #####
sed -i -r 's/\|/\t/' ${GENOMENAME}_blastp_cycog6_tophit.out

##### Cleanup and Waiting steps #####
conda deactivate
date
wait
echo "Step 1.2 Done"
touch ${WORKDIR}/02_completion_flag.txt
rm ${WORKDIR}/01_completion_flag.txt
