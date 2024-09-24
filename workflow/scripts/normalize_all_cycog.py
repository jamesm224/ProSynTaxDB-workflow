"""
Purpose: Normalization of classified read count using 424 CyCOG. 
    - Input: tab-delimited diamond blast output file
        - Blast results of reads classified in a clade (of a sample) against CyCOG database. 
    - Output: tab delimited file (no headers): [sample, genus, clade, alignment_len, genome_equivalents]
        - Note: output file is 1 line 
        - alignment_len = sum of alignment length of unique hits
        - genome_equivalents = alignment_len / 359404.6391
            
Steps:
    - Obtain unique hit per read
        - Sort by alignment length and keep highest alignment length per read
    - Filter for hits to 424 cycog list 
    - Sum up alignment length 
    - Divide alignment length by 359404.6391
        - 359404.6391 = sum of 424 CyCOG mean length

09/16/24 - James Mullet, Nhi N. Vo
"""
import numpy as np
import os
import pandas as pd
from pathlib import Path

def import_diamond_output(diamond_fpath):
    """
    Returns df of alignment length of all reads. 
    """
    # obtain headers for df (string from blast_reads rule)
    cols = [elem for elem in "qseqid sseqid pident nident length qstart qend sstart send evalue bitscore".split(" ")]
    df = pd.read_table(
        diamond_fpath, 
        header = None, 
        names = cols, 
    )

    # rename cols
    df = df.rename(columns={
        "qseqid": "read_name", 
        "sseqid": "cycog_name", 
        "length": "alignment_length", 
    })

    # obtain cycog id from diamond blast sseqid (cycog_name)
    df['cycog_iid'] = df['cycog_name'].str.split('|').str[1]

    # sort and remove duplicate to obtain best match 
    df = df.sort_values(by=['pident'], ascending=[False])
    df = df.drop_duplicates(subset='read_name', keep='first')  # keep hit with highest pident

    return df 

def cycog_normalize(df, cycog_list):
    """
    Returns:
        - sum_alnm_len: sum of alignment length of reads mapped to 424 cycogs. 
        - genome_equivalents: 
    """
    # filter df for cycogs in list
    df = df[df['cycog_iid'].isin(cycog_list)]

    # sum alignment length 
    sum_alnm_len = df['alignment_length'].sum()

    # obtain_genome_equivalence
    total_cycog_len = 359404.6391
    genome_equivalents = sum_alnm_len / total_cycog_len

    return sum_alnm_len, genome_equivalents

def main():
    """
    """
    # obtain snakemake input and output paths 
    diamond_fpath = Path(snakemake.input['diamond_out'])  # path to diamond blast output 
    cycog_fpath = Path(snakemake.input['cycog_file'])  # path to 424 cycog len
    normalized_output_fpath = snakemake.output['normalized_output']  # normalized output fpath 

    # obtain filename metadata 
    sample = diamond_fpath.parent.name  # sample name (parent dir of diamond output)
    genus = diamond_fpath.stem.split('_')[-3]  
    clade = diamond_fpath.stem.split('_')[-1] 

    # obtain list of 424 cycog iid
    cycog_df = pd.read_table(cycog_fpath,header=None, names=['cycog_iid','mean_length'])
    cycog_list = cycog_df['cycog_iid'].values.tolist()

    # import diamond output file
    df = import_diamond_output(diamond_fpath)

    # calculate alignment length and genome equivalents 
    sum_alnm_len, genome_equivalent = cycog_normalize(df, cycog_list)

    # save data into tsv file (with NO headers)
    with open(normalized_output_fpath, 'w') as file:
        file.write(f"{sample}\t{genus}\t{clade}\t{sum_alnm_len}\t{genome_equivalent}\n")


main()
