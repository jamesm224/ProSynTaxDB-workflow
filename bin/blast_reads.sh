#!/bin/bash
input_dir=$1
output_dir=$2
diamond=$3


# Ensure input directory is provided #
if [ -z "${input_dir}" ]; then
    echo "Error: Input directory not provided."
    echo "Usage: $0 <input_directory>"
    exit 1
fi

# Array to collect processed file paths #
blast_output_files=()

# Loop through each CSV file in the input directory #
for fastq_file in "${input_dir}"/*_forward.fastq; do
    base_name=$(basename "${fastq_file}" _forward.fastq)
    # sample_name=$(echo "${base_name}" | cut -d '_' -f 1)  # Adjust as per your sample name extraction logic
    sample_name=$(echo "${base_name}" | sed 's/_names.*//')
    blast_output="${output_dir}/${base_name}.tsv"
    forward_reads="${input_dir}/${base_name}_forward.fastq"
    reverse_reads="${input_dir}/${base_name}_reverse.fastq"
    echo "forward_reads: ${forward_reads}, reverse_reads: ${reverse_reads}"
    echo "Processing file: ${fastq_file}, base name: ${base_name}, sample name: ${sample_name}"
    if [[ -s "${forward_reads}" && -s "${reverse_reads}" ]]; then
        diamond blastx -d "${diamond}" -q "${forward_reads}" -p "${reverse_reads}" -o "${blast_output}"

        # Check if the BLAST output file is non-empty before adding it to the array #
        if [[ -s "${blast_output}" ]]; then
            blast_output_files+=("${blast_output}")
        else
            echo "BLAST output file ${blast_output} is empty. Skipping..."
            rm -f "${blast_output}"
        fi
    else
        echo "One or both FASTQ files for ${sample_name} are empty. Skipping..."
    fi
done

# Print output file paths for Nextflow to capture #
for blast_output_file in "${blast_output_files[@]}"; do
    echo "${blast_output_file}"
done
