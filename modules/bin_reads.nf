#!/usr/bin/env nextflow
process bin_reads {
    publishDir "${params.outputdir}/pro_binned_reads"
    
    input:
    file script
    file input_values

    output:
    path "*_reads.csv",           emit:binned_read_headers

    script:

    """
    source /home/jmullet/mambaforge/bin/activate /home/jmullet/mambaforge/envs/read_normalization_env

    python3 $script --kaiju_input "${params.outputdir}/classified_kaiju_read_output"
    """
}
