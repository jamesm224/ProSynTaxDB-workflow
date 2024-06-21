#!/usr/bin/env nextflow
process bbduk {
    tag "$sample"
    publishDir "${params.outputdir}/trimmed_reads", mode: 'copy'

    input:
    tuple val(sample), path(r1), path(r2)


    output:
    tuple val(sample), path("${sample}_1_trimmed.fastq.gz"), path("${sample}_2_trimmed.fastq.gz")

    script:
    def reverse_read_input = r2 ? "in2=${r2}" : ""
    def reverse_read_output = r2 ? "out2=${sample}_2_trimmed.fastq.gz" : ""
    """
    source /home/jmullet/mambaforge/bin/activate /home/jmullet/mambaforge/envs/kaiju

    bbduk.sh threads=1 in1=${r1} ${reverse_read_input} \
    out1=${sample}_1_trimmed.fastq.gz ${reverse_read_output} \
    minlen=25 qtrim=rl trimq=10 \
    ref=/nfs/chisholmlab001/chisholmlab/genomic_resources/references/illumina/all_illumina_adapters.fa \
    ktrim=r k=23 mink=11 hdist=1
    """
}
