def aggregate_normalized_clade(wildcards):
    """
    Returns: list of files of all normalized [clade].tsv for a sample. 

    Notes: 
    - checkpoint_output = all the output from bin_headers
        - Unknown numbers of output files, hence the use of checkpoint. 
    - sample_clade = glob_wildcards(): obtain sample_clade variable from list of outputs
    from checkpoint_output. 
    """
    checkpoint_output = checkpoints.bin_headers.get(**wildcards).output[0]

    return expand(
        scratch_dict['count_normalization']['normalized_counts'] / "{sample}" / "{sample_clade}.tsv",
        sample = wildcards.sample,
        sample_clade = glob_wildcards(os.path.join(checkpoint_output, "{sample_clade}_reads.txt")).sample_clade
    )

rule aggregate_normalized_clades:
    """
    Combine normalized outputs for all clades in a sample. 
    """
    input:
        # obtain list of normalized clade output 
        aggregate_normalized_clade
    output:
        scratch_dict['count_normalization']['aggregated_normalized'] / "{sample}.tsv"
    shell:
        "cat {input} > {output}"

rule aggregate_normalized_samples:
    """
    Combine normalized output for all samples. 
    """
    input:
        expand(scratch_dict['count_normalization']['aggregated_normalized'] / "{sample}.tsv", sample=SAMPLES), 
    output:
        results_dict['final_normalized_count']
    shell:
        """
        # column headers for final results 
        header="sample_name\tgenus\tclade\talignment_length\tgenome_equivalents"

        # add header to final output file
        echo "$header" > {output}

        # combine aggregated normalized counts to file with header 
        cat {input} >> {output}
        """

rule aggregate_summary:
    """
    """
