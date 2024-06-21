#!/bin/bash
input_dir=$1
forward_read_inputs=$2
reverse_read_inputs=$3

# Ensure input directory is provided #
if [ -z "${input_dir}" ]; then
    echo "Error: Input directory not provided."
    echo "Usage: $0 <input_directory>"
    exit 1
fi


# Array to collect processed file paths #
forward_output_files=()
reverse_output_files=()

# Loop through each CSV file in the input directory #
for csv_file in "${input_dir}"/*.csv; do
    base_name=$(basename "${csv_file}" .csv)
    # sample_name=$(echo "${base_name}" | cut -d '_' -f 1)  # Adjust as per your sample name extraction logic
    sample_name=$(echo "${base_name}" | sed 's/_names.*//')

    echo "Processing file: ${csv_file}, base name: ${base_name}, sample name: ${sample_name}"
    reads=$(awk -F ',' '{print $1}' "${csv_file}")
    echo "Processing file: ${csv_file}, base name: ${base_name}, sample name: ${sample_name}"
    echo "${reads}"
    forward_output="${input_dir}/${base_name}_forward.fastq"
    reverse_output="${input_dir}/${base_name}_reverse.fastq"

    # Run seqtk read subsetting #
    seqtk subseq "${forward_read_inputs}" <(echo "${reads}") > "$forward_output"
    seqtk subseq "${reverse_read_inputs}" <(echo "${reads}") > "$reverse_output"
    
    # Add seqtk output file to the list of output files #
    forward_output_files+=("$forward_output")
    reverse_output_files+=("$reverse_output")
    
done

# Print output file paths for Nextflow to capture #
for forward_file in "${forward_output_files[@]}"; do
    echo "${forward_file}"
done

for reverse_file in "${reverse_output_files[@]}"; do
    echo "${reverse_file}"
done
