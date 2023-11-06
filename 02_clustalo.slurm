#!/usr/bin/env bash
#SBATCH --job-name=02clustalo
#SBATCH --output=logs/slurm-%x-%A-%a.out
#SBATCH --error=logs/slurm-%x-%A-%a.err
#SBATCH -n 1
#SBATCH -t 0-00:30:00
#SBATCH -p sched_mit_chisholm
#SBATCH --mem-per-cpu=12500
#SBATCH --chdir=/pool001/jmullet/gorgcycogamz20230927/scripts
#SBATCH --array=1-425%1

###########---'''SBATCH --array=1-425%5'''##########------

##### Load Input Files #####
WORKDIR=$1
NAMESFILE=$2
BLASTDIR=$3
FULLPROTEIN=$4
ALIGNMENTDIR=$5
CYCOGANNOTATIONS=$6

##### PARSE ARRAY ID #####
CYCOG=$(cat ${CYCOGANNOTATIONS} | awk -v LINENUMBER=${SLURM_ARRAY_TASK_ID} '{if ( NR == LINENUMBER ) {print $1}}')

##### Script Preparation #####
hostname
date
eval "$(conda shell.bash hook)"
conda activate biopython_project
cd ${WORKDIR}/cycogfaa/

##### Append genomes to CyCOG gene list ##### 
for GENOME in `cat ${NAMESFILE}`
do
    COUNT=$(cat ${BLASTDIR}/${GENOME}_blastp_cycog6_tophit.out | awk '{print $1,$3}' | grep ${CYCOG} | wc -l)
    if [ $COUNT -eq 1 ]
    then
        cat ${BLASTDIR}/${GENOME}_blastp_cycog6_tophit.out | awk '{print $1,$3}' | grep ${CYCOG} | awk '{print $1}' >> ${CYCOG}_gene_iid.lst
    fi
done

##### Subsets proteins contained in the CyCOG gene list #####
seqtk subseq ${FULLPROTEIN} ${CYCOG}_gene_iid.lst >> ${CYCOG}.faa
sed -i -r 's/_NODE.+_[0-9]+$//' ${CYCOG}.faa
sed -r 's/_NODE.+_[0-9]+$//' ${CYCOG}.faa
seqkit rmdup -s < ${CYCOG}.faa > ${CYCOG}.cleaned.faa

##### Aligning Genomes to CyCOGs using ClustalO #####
clustalo -i ${CYCOG}.cleaned.faa \
  -o ${ALIGNMENTDIR}/${CYCOG}_clustalo_aligned.fasta \
  --output-order=input-order

##### Cleanup and Waiting steps #####
conda deactivate
date
wait
echo "Step_1_part_2 Done"
rm ${WORKDIR}/02_completion_flag.txt
#touch /pool001/jmullet/gorgcycogamz20230927/02_completion_flag.txt
