process blast_sequences {
    publishDir "${params.outputdir}/pro_diamond_outputs"

    input:
    file script
    file forward_reads
    file reverse_reads

    output:
    path "*.tsv",           emit:blasted_reads

    script:

    """
    source /home/jmullet/mambaforge/bin/activate /home/jmullet/mambaforge/envs/read_normalization_env
    output=\$(bash ${script} ${params.outputdir}/pro_binned_reads ${params.outputdir}/pro_diamond_outputs ${params.dmnd})
    
    echo "\$output" | while read -r file_path; do
        if [[ "\$file_path" == *".tsv" ]]; then
            ln -s "\$file_path" .
        fi
    done
    """
}
