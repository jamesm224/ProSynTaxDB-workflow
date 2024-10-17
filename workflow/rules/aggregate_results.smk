rule aggregate_normalized_samples:
    """
    Combines normalized output for all samples. 
    """
    input:
        expand(scratch_dict['count_normalization']['normalized_counts'] / "{sample}.tsv", sample=SAMPLES), 
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
