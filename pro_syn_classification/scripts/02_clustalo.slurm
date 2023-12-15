#!/usr/bin/env bash
#SBATCH --job-name=02clustalo
#SBATCH --output=logs/slurm-%x-%A-%a.out
#SBATCH --error=logs/slurm-%x-%A-%a.err
#SBATCH -n 1
#SBATCH -t 0-01:30:00
#SBATCH -p sched_mit_chisholm
#SBATCH --mem-per-cpu=12500
#SBATCH --chdir=/pool001/jmullet/gorgcycogamz20230927/scripts
#SBATCH --array=1-425%10

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
    #echo $COUNT
    then
        cat ${BLASTDIR}/${GENOME}_blastp_cycog6_tophit.out | awk '{print $1,$3}' | grep ${CYCOG} | awk '{print $1}' >> ${CYCOG}_gene_iid.lst
    fi
done

##### Remove old _complete.faa files #####
rm *_complete.faa

##### Create new .faa files for each _original.faa file #####
for file in *_original.faa; do
    if [ -e "$file" ]; then
        new_file="${file%_original.faa}_complete.faa"
        cp "$file" "$new_file"
        echo "Created $new_file"
    fi
done

##### Subsets proteins contained in the CyCOG gene list #####
seqtk subseq ${FULLPROTEIN} ${CYCOG}_gene_iid.lst >> ${CYCOG}_complete.faa
sed -i -r 's/_NODE.+_[0-9]+$//' ${CYCOG}_complete.faa

##### Aligning Genomes to CyCOGs using ClustalO #####
clustalo -i ${CYCOG}_complete.faa \
  -o ${ALIGNMENTDIR}/${CYCOG}_clustalo_aligned.fasta \
  --output-order=input-order

##### Cleanup and Waiting steps #####
conda deactivate
date
wait
echo "Step_1_part_2 Done"
#touch /pool001/jmullet/gorgcycogamz20230927/02_completion_flag.txt
