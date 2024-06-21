#!/usr/bin/env nextflow

process normalization {
    publishDir "${params.outputdir}/pro_normalized_read_counts"
    
    input:
    file script
    file input_values

    output:
    path "*.csv",           emit:normalized_counts

    script:

    """
    source /home/jmullet/mambaforge/bin/activate /home/jmullet/mambaforge/envs/read_normalization_env

    python3 $script --diamond_outputs "${params.outputdir}/pro_diamond_outputs" --total_cycog_input "${params.cycogs}"

    """
}
