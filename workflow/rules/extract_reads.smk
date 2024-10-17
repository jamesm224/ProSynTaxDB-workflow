rule kaiju_name_extract:
    input:
        kaiju_name = scratch_dict["classified_kaiju_read_output"] / "{sample}_names.out",
    output:
        read_name_file = scratch_dict["prosyn_reads"]["read_name"] / "{sample}.txt", 
        read_name_taxa_file = scratch_dict["prosyn_reads"]["read_name_classification"] / "{sample}_classification.txt", 
    shell:
        """
        # obtain name of reads whose classification contains Pro/Syn 
        grep -E "Prochlorococcus|Synechococcus" {input.kaiju_name} | cut -f2 > {output.read_name_file}

        # obtain name and full taxonomic classification of reads whose classification contains Pro/Syn 
        grep -E "Prochlorococcus|Synechococcus" {input.kaiju_name} | cut -f2,4 > {output.read_name_taxa_file}
        """

rule extract_fastq_reads:
    """
    Note: commented out reverse read extraction: diamond blast does not take paired
    end reads, only 1 sequence. 
    """
    input: 
        r1 = scratch_dict["trimmed_reads"] / "{sample}_1_trimmed.fastq.gz",
        # r2 = scratch_dict["trimmed_reads"] / "{sample}_2_trimmed.fastq.gz",
        prosyn_read_name = scratch_dict["prosyn_reads"]["read_name"] / "{sample}.txt", 
    output:
        fwd_prosyn_reads = scratch_dict["prosyn_reads"]["extracted_reads"] / "{sample}_fwd.fastq", 
        # reverse_reads = scratch_dict["read_binning"]["binned_reads"] / "{sample}" / "{sample_clade}_rev.fastq",
    conda:
        "../envs/seqtk.yaml"
    shell:
        """
        seqtk subseq {input.r1} {input.prosyn_read_name} > {output.fwd_prosyn_reads}
        """
        # seqtk subseq {input.r2} {input.clade_read_headers} > {output.reverse_reads}
