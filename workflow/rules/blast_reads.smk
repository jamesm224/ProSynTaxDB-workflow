rule blast_reads:
    input:
        fwd_binned_reads= scratch_dict["read_binning"]["binned_reads"] / "{sample}" / "{sample_clade}_fwd.fastq",
        diamond_db = Path(config["input"]["diamond_file"]),
    output:
        diamond_out = scratch_dict["diamond_blast"] / "{sample}" / "{sample_clade}.tsv",
    conda:
        "../envs/blast.yaml"
    shell:
        """
        diamond blastx \
            --query {input.fwd_binned_reads} \
            --db {input.diamond_db} \
            --out {output.diamond_out} \
            --threads {resources.cpus_per_task} \
            --outfmt 6 qseqid sseqid pident nident length qstart qend sstart send evalue bitscore
        """
