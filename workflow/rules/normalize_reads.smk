rule normalize_reads:
    input:
        diamond_out = scratch_dict["diamond_blast"] / "{sample}.tsv",
        read_name_taxa_file = scratch_dict["prosyn_reads"]["read_name_classification"] / "{sample}_classification.txt", 
        cycog_file = config["input"]["cycog_file"], 
    output:
        normalized_output = scratch_dict["count_normalization"]["normalized_counts"] / "{sample}.tsv",
    conda:
        "../envs/python.yaml"
    script:
        "../scripts/normalize_all_cycog.py"
