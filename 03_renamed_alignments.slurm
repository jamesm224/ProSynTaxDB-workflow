#!/bin/bash

#Parsing Command
ALIGNMENTDIR=/pool001/jmullet/gorgcycogamz20230927/alignments_test

##### Load Input Files #####
directory=${ALIGNMENTDIR}

##### Loop through the files in the directory #####
for file in "$directory"/*; do
    if [ -f "$file" ]; then
        
        ##### Use sed to remove the "_NODE_" string and everything after it #####
        sed -i -r 's/_NODE_.+//' "$file"
        echo "Processed '$file'"
    fi
done

##### Cleanup and Waiting steps #####
date
wait
echo "Step 3 Done"

##### Optional step for pipeline extension #####
#rm /pool001/jmullet/gorgcycogamz20230927/03_completion_flag.txt
