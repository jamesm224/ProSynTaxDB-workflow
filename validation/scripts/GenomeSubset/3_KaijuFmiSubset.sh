#!/usr/bin/env bash
#SBATCH --job-name=fmi_subset
#SBATCH --time 2-0           
#SBATCH -p sched_mit_chisholm
#SBATCH -c 10                 
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem 90G
#SBATCH --array=1-10%5
#SBATCH -o logs/fmi_subset.%a.%j.out
#SBATCH -e logs/fmi_subset.%a.%j.err

date
echo CPU requested: ${SLURM_CPUS_PER_TASK}
echo SLURM array task ID: ${SLURM_ARRAY_TASK_ID}

# path to fasta with all the proteins 
fasta_file=path/to/ProSynTax.faa

# output directory 
outdir=path/to/output/directory
mkdir -p ${outdir}

# obtain subset number
i=${SLURM_ARRAY_TASK_ID}
echo "Processing subset number $i"

### 1. Obtain gene header from genomes that will be use for simulation ### 
simulation_genome_list="data/GenomeSubset/simulation_set_${i}.txt"
headers_to_remove="${outdir}/headers2remove_${i}.lst"

date
echo Extracting headers from genomes to be removed... 
python3 fmi_subset_scripts/extract_headers.py "$simulation_genome_list" "$fasta_file" "$headers_to_remove"
echo Header extraction complete! 
date 

### 2. Remove headers obtained above from Classification fasta file ### 
subsetted_faa="${outdir}/subsetted_MARMICRODB2_viruses_${i}.faa"

date
echo Removing genes in genomes to be used in read simulation... 
python3 fmi_subset_scripts/remove_sequences.py "$fasta_file" "$headers_to_remove" "$subsetted_faa"
echo .faa file removal complete! 
date 

### 3. Make FMI file 
eval "$(conda shell.bash hook)"
conda activate kaiju

bwt_ouput="${outdir}/subsetted_MARMICRODB2_viruses_${i}"

date
echo Making fmi file using kaiju... 
kaiju-mkbwt -n ${SLURM_CPUS_PER_TASK} -o ${bwt_ouput} ${subsetted_faa}
kaiju-mkfmi ${bwt_ouput}
echo fmi generation complete! 
date 

conda deactivate 

### 4. Remove temp files ### 
echo Removing temp files ... 
rm ${headers_to_remove}  # file with headers to remove 
rm ${subsetted_faa}  # filtered .faa file 
rm "${outdir}/subsetted_MARMICRODB2_viruses_${i}.sa"  # temp file from kaiju 

echo "Completed processing subset number $i"
