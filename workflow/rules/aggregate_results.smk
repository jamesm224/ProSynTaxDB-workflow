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
    Combines normalized outputs for all clades in a sample.
        - Each classified clade within a sample outputs a normalized file, 
        this step combines all of those files for a sample. 
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
    Combines normalized output for all samples. 
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
    Parses all _kaiju_summary files and obtain counts and percentage of taxons in genus_list. 
    Sum counts of remaining rows into "other_genus". 
    """
    input:
        kaiju_summary = expand(scratch_dict["classified_kaiju_read_output"] / "{sample}_kaiju_summary.tsv", sample=SAMPLES),  
    params:
        genus_list = config["classification_summary"]["genus_list"], 
    output:
        summary_oufpath = results_dict['summary_read_count'], 
    conda:
        "../envs/python.yaml"
    script:
        "../scripts/classification_summary.py"
