rule blast_reads:
    input:
        fwd_prosyn_reads= scratch_dict["prosyn_reads"]["extracted_reads"] / "{sample}_fwd.fastq", 
        diamond_db = Path(config["input"]["diamond_file"]),
    output:
        diamond_out = scratch_dict["diamond_blast"] / "{sample}.tsv",
    conda:
        "../envs/blast.yaml"
    shell:
        """
        diamond blastx \
            --query {input.fwd_prosyn_reads} \
            --db {input.diamond_db} \
            --out {output.diamond_out} \
            --threads {resources.cpus_per_task} \
            --outfmt 6 qseqid sseqid pident nident length qstart qend sstart send evalue bitscore
        """
