rule normalize_reads:
    input:
        diamond_out = scratch_dict["diamond_blast"] / "{sample}" / "{sample_clade}.tsv",
        cycog_file = config["input"]["cycog_file"], 
    output:
        normalized_output = scratch_dict["count_normalization"]["normalized_counts"] / "{sample}" / "{sample_clade}.tsv",
    conda:
        "../envs/python.yaml"
    script:
        "../scripts/normalize_all_cycog.py"
