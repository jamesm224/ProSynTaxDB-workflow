checkpoint bin_headers:
    """
    Extract the reads for each clade into its own .fastq file. 

    Note: bin_headers is a checkpoint instead of a rule because: 
        - The output files are unknown (each output file = clades present in sample)
        - checkpoint allows for running snakemake without specifying output file i.e. expand()
        as checkpoint allows for re-evaluation of DAG. 
    """
    input:
        kaiju_out = scratch_dict["classified_kaiju_read_output"] / "{sample}_names.out",
    output:
        binned_header_dir = directory(scratch_dict["read_binning"]["binned_headers"] / "{sample}"),
    conda:
        "../envs/python.yaml"
    script:
        "../scripts/bin_headers.py"


rule extract_binned_reads:
    """
    For each binned clade: 
        - Obtain read name using bin_headers output 
        - Extract those reads from trimmed .fastq file

    Note: commented out reverse read extraction: diamond blast does not take paired
    end reads, only 1 sequence. 
    """
    input: 
        r1 = scratch_dict["trimmed_reads"] / "{sample}_1_trimmed.fastq.gz",
        # r2 = scratch_dict["trimmed_reads"] / "{sample}_2_trimmed.fastq.gz",
        clade_read_headers = scratch_dict["read_binning"]["binned_headers"] / "{sample}" / "{sample_clade}_reads.txt", 
    output:
        forward_reads = temp(scratch_dict["read_binning"]["binned_reads"] / "{sample}" / "{sample_clade}_fwd.fastq"),
        # reverse_reads = scratch_dict["read_binning"]["binned_reads"] / "{sample}" / "{sample_clade}_rev.fastq",
    conda:
        "../envs/seqtk.yaml"
    shell:
        """
        seqtk subseq {input.r1} {input.clade_read_headers} > {output.forward_reads}
        """
        # seqtk subseq {input.r2} {input.clade_read_headers} > {output.reverse_reads}
