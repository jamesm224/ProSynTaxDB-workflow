rule kaiju_run:
    input:
        r1 = scratch_dict["trimmed_reads"] / "{sample}_1_trimmed.fastq.gz",
        r2 = scratch_dict["trimmed_reads"] / "{sample}_2_trimmed.fastq.gz",
        nodes = Path(config["input"]["nodes_file"]),
        names = Path(config["input"]["names_file"]),
        fmi = Path(config["input"]["fmi_file"]),
    output:
        scratch_dict["classified_kaiju_read_output"] / "{sample}_kaiju.txt", 
    conda:
        "../envs/kaiju.yaml"
    shell:
        """
        kaiju \
            -z {resources.cpus_per_task} \
            -m 11 -s 65 -E 0.05 -x \
            -e 5 -t {input.nodes} -f {input.fmi} \
            -i {input.r1} {input.r2} \
            -o {output}
        """

rule kaiju_name:
    """
    Returns [sample]_name.out file that contains cols: [classification, read_name, taxonid, full_taxa]
    
    Notes: 
        -p: print the full taxon path instead of just the taxon name.
    """
    input:
        kaiju = scratch_dict["classified_kaiju_read_output"] / "{sample}_kaiju.txt",
        nodes = Path(config["input"]["nodes_file"]),
        names = Path(config["input"]["names_file"]),
        fmi = Path(config["input"]["fmi_file"]),
    output:
        scratch_dict["classified_kaiju_read_output"] / "{sample}_names.out",      
    conda:
        "../envs/kaiju.yaml"
    shell:
        """
        kaiju-addTaxonNames \
            -t {input.nodes} \
            -n {input.names} \
            -i {input.kaiju} \
            -p -o {output}
        """


# other kaiju rules that aren't currently generated
rule kaiju_krona:
    input:
        kaiju = scratch_dict["classified_kaiju_read_output"] / "{sample}_kaiju.txt",
        nodes = Path(config["input"]["nodes_file"]),
        names = Path(config["input"]["names_file"]),
        fmi = Path(config["input"]["fmi_file"]),
    output:
        scratch_dict["classified_kaiju_read_output"] / "{sample}_kaiju.krona",
    conda:
        "../envs/kaiju.yaml"
    shell:
        "kaiju2krona -t {input.nodes} -n {input.names} "
        "-i {input.kaiju} -o {output} "


rule kaiju_summary_taxa:
    input:
        kaiju = scratch_dict["classified_kaiju_read_output"] / "{sample}_kaiju.txt",
        nodes = Path(config["input"]["nodes_file"]),
        names = Path(config["input"]["names_file"]),
        fmi = Path(config["input"]["fmi_file"]),
    output:
        scratch_dict["classified_kaiju_read_output"] / "{sample}_kaiju_summary.tsv", 
    conda:
        "../envs/kaiju.yaml"
    shell:
        "kaiju2table -t {input.nodes} -n {input.names} -r genus "
        "{input.kaiju} -o {output} "

rule classification_summary:
    input:
        kaiju_summary = scratch_dict["classified_kaiju_read_output"] / "{sample}_kaiju_summary.tsv", 
    output: 
