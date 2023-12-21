#!/bin/bash
#SBATCH --job-name=kaiju
#SBATCH --time 15:00:00                        # wall clock limit
#SBATCH -p sched_mit_chisholm               # partition selection
#SBATCH -n 30                              # tasks (essentially threads)
#SBATCH --output=logs/slurm-%x-%A-%a.out
#SBATCH --error=logs/slurm-%x-%A-%a.err

##### Ensure you have a Kaiju Conda Environment Installed before usage #####
##### Define where your input files are and where you want the output directory is #####
SAMPLEDIR=/path/to/input/reads
OUTPUTDIR=/path/to/output

##### Specify what DB you would like to use for Kaiju #####
nodes_file='/path/to/nodes/gorgcycogamz_nodes.dmp'
names_file='/path/to/names/gorgcycogamz_names.dmp'
kaiju_database='/path/to/fmi_file/GORG_v2_pro_edition.fmi'

cd ${SAMPLEDIR}

##### Define your samples to easily run them in kaiju #####
##### Adjust the {$1} written twice in the line with your suffix #####

### Examples are commented below for contigs and forward/reverse reads ###
# samples=`ls *{$1} | awk '{split($_,x,"{$1}"); print x[1]}' | sort | uniq`
# samples=`ls *.out | awk '{split($_,x,".out"); print x[1]}' | sort | uniq`
# samples=`ls *_1_trimmed.fastq.gz | awk '{split($_,x,"_1_trimmed.fastq.gz"); print x[1]}' | sort | uniq`

cd ${OUTPUTDIR}

##### Loop Through Samples - comment everything except echo ${sample} to ensure samples are loading correctly #####
for sample in ${samples}
  do 
      ##### Run Kaiju - for one input File #####
      # kaiju -z 20 -a greedy -e 5 -m 11 -s 65 -E 0.05 -x -t ${nodes_file} -f ${kaiju_database} -i ${WORKDIR}/${sample}_final_contigs.fa -o ${OUTPUTDIR}/${sample}_output.kaiju
        
      ##### Run Kaiju - for two input File #####
      # kaiju -z 20 -a greedy -e 5 -m 11 -s 65 -E 0.05 -x -t ${nodes_file} -f ${kaiju_database} -i ${SAMPLEDIR}/${sample}_1_trimmed.fastq.gz -j ${SAMPLEDIR}/${sample}_2_trimmed.fastq.gz -o ${OUTPUTDIR}/${sample}.out
        
      ##### Convert output to informative outputs #####
      kaiju2krona -t ${nodes_file} -n ${names_file} -i ${OUTPUTDIR}/${sample}.out -o ${OUTPUTDIR}/${sample}.kaiju.krona
      kaiju2table -t ${nodes_file} -n ${names_file} -r species -m 1.0 -o ${OUTPUTDIR}/${sample}_output.kaiju_summary ${OUTPUTDIR}/${sample}_output.kaiju
      kaiju-addTaxonNames -t ${nodes_file} -n ${names_file} -i  ${OUTPUTDIR}/${sample}.out -p -o ${OUTPUTDIR}/${sample}.names.out
        
      ##### Optional naming step for easy Pandas parsing #####
      # awk -F',' -v OFS='\t' '{print "'${sample_name}'", $0}' ${OUTPUTDIR}/${sample}_output.kaiju.krona > ${OUTPUTDIR}/${sample}_output.renamed.kaiju.krona
echo ${sample}
done
