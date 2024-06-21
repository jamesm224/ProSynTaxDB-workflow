process kaiju {
    tag "$sample"
    publishDir "${params.outputdir}/classified_kaiju_read_output"

    input:
    tuple val(sample), path(read_1), path(read_2)
    path(nodes)
    path(names)
    path(fmi)

    output:
    path "*_kaiju.txt",           emit:raw_kaiju
    path "*_kaiju.krona",         emit:krona_out
    path "*_names.out",           emit:taxon_names
    path "*_output.kaiju_summary",           emit:genus_table
    
    script:
    def reverse_read_path = read_2 ? "-j ${read_2}" : ""
    """
    source /home/jmullet/mambaforge/bin/activate /home/jmullet/mambaforge/envs/kaiju

    kaiju -z 8 -m 11 -s 65 -E 0.05 -x \
        -e 5 -t ${nodes} -f ${fmi} \
        -i ${read_1} ${reverse_read_path} -o ${sample}_kaiju.txt
    
    kaiju2krona -t ${nodes} -n ${names} \
        -i ${sample}_kaiju.txt -o ${sample}_kaiju.krona

    kaiju-addTaxonNames -t ${nodes} -n ${names} \
        -i  ${sample}_kaiju.txt -p -o ${sample}_names.out

    kaiju2table -t ${nodes} -n ${names} -r genus \
        -o ${sample}_output.kaiju_summary \
        ${sample}_kaiju.txt -u
    """
}
