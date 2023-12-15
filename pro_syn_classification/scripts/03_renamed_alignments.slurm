#!/bin/bash
#SBATCH --job-name=03rename_alignments
#SBATCH --output=logs/slurm-%x-%A-%a.out
#SBATCH --error=logs/slurm-%x-%A-%a.err

##### Parsing Command #####
ALIGNMENTDIR=/pool001/jmullet/gorgcycogamz20230927/alignments_renamed_output
cd ${ALIGNMENTDIR}

##### Load Input Files #####
directory=${ALIGNMENTDIR}

##### Loop through the files in the directory #####
for file in "$directory"/*; do
    if [ -f "$file" ]; then
        
        ### Use sed to remove the "_NODE_" string and everything after it ###
        #sed -i -r 's/_NODE_.+//' "$file"

        ### Use seqkit to remove duplicates ###
        seqkit rmdup -D -i "$file" -o "$file".renamed.fasta
        echo "Processed '$file'"
    fi
done

##### Cleanup and Waiting steps #####
date
wait
echo "Step 3 Done"

##### Optional step for pipeline extension #####
#rm /pool001/jmullet/gorgcycogamz20230927/03_completion_flag.txt
