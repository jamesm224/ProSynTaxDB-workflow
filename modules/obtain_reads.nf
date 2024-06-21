process obtain_reads {
    tag "$sample"
    publishDir "${params.outputdir}/pro_binned_reads"

    input:
    tuple val(sample), path(r1), path(r2)
    file script
    file binned_reads
    

    output:
    path "*_forward.fastq",           emit:forward_reads
    path "*_reverse.fastq",           emit:reverse_reads

    script:

    """
    source /home/jmullet/mambaforge/bin/activate /home/jmullet/mambaforge/envs/read_normalization_env
    output=\$(bash ${script} "${params.outputdir}/pro_binned_reads" "${r1}" "${r2}")
    
    echo "\$output"

    echo "\$output" | while read -r file_path; do
        if [[ "\$file_path" == *"_forward.fastq" ]]; then
            ln -s "\$file_path" .
        elif [[ "\$file_path" == *"_reverse.fastq" ]]; then
            ln -s "\$file_path" .
        fi
    done

    """
}
