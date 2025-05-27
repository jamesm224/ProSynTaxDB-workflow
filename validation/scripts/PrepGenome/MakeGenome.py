"""
Purpose: 
    1. to create genome2ecotype.tsv: links/maps genomes to their ecotype. 
    2. to reformat FASTA file to fit with mason2 requirements and output into 
    1 directory: data/ReformattedGenomes    
        - mason wants all lines in FASTA file to be the same length. 
"""
import os
import argparse
import subprocess
from pathlib import Path
import pandas as pd

# COMMAND LINE ARGUMENTS:
parser = argparse.ArgumentParser()
parser.add_argument("prosyn_classification", help="Excel file with classification for genomes in pipeline.")
parser.add_argument("genome_sources", help="Folder to FASTA files for all genomes.")
args = parser.parse_args()

def create_g2e(prosyn_classification, genome_sources):
    """
    To create a table that maps genome names (file names) to their ecotype. 

    params:
    GORG_classification: path to excel table with pro/syn genome name to clade classification 
    """
    prosyn_df = pd.read_excel(
        prosyn_classification, 
        header=None, 
        skiprows=1, 
        names=['Genome', 'Clade', 'Group']
    )
    prosyn_df.loc[prosyn_df['Group'] == 'Virus', 'Clade'] = 'Virus'
    prosyn_genomes = prosyn_df['Genome'].values.tolist()

    # list of het genomes for Heterotroph genomes table
    het_genomes = []

    # cycle through all genome FASTA files in genome dir 
    for fpath in Path(genome_sources).glob('*'):
        source = fpath.parent.parent.name
        genome = fpath.stem

        if genome in prosyn_genomes:
            # skip genome (omit from het list) if in prosyn list
            continue
        
        # add genome to het list
        het_genomes.append(genome)

    het_df = pd.DataFrame({
        "Genome": het_genomes, 
        "Clade": "Heterotroph", 
        "Group": "Heterotroph", 
    })

    g2e_df = pd.concat([prosyn_df, het_df])

    # remove leading/trailing whitespace
    g2e_df = g2e_df.map(lambda x: x.strip() if isinstance(x, str) else x)  
    
    g2e_df.to_csv('data/genome2ecotype.tsv', sep='\t', index=False)

    return g2e_df


def reformat_fna(df, in_dir, out_dir, line_length):
    """
    Reformat downloaded fna files so that all sequence lines are the same length. 
    (same number of character each line)

    params:
    df: genome2ecotype df 
    in_dir: input dir of genomes 
    out_dir: output dir for genomes 
    line_length: how long to make each sequence line 
    """
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    # obtain list of genome to reformat
    genomes = df['Genome'].values.tolist()

    # cycle through all genomes in dir 
    for fna_fpath in Path(in_dir).glob('*'):
        fname = fna_fpath.name
        genome_name = fna_fpath.stem

        if genome_name not in genomes:
            # skip genomes not in list 
            print(f"Skipping genome {genome_name}. Reason: not in genome list.")
            continue 

        with open(fna_fpath, 'r') as input_file, open(f'{out_dir}/{genome_name}.fna', 'w') as output_file:
            seq_lines = []
            for line in input_file:
                line = line.strip()
                if not line or line.startswith('>'):
                    # ignore header lines and blank lines
                    continue 
                seq_lines.append(line.strip())
            
            combined_seq = ''.join(seq_lines)
            # split combined lines into lines of specified len
            split_lines = [combined_seq[i:i+line_length] for i in range(0, len(combined_seq), line_length)]

            # write the split lines to the output file
            output_file.write(f'>{genome_name}\n')
            for split_line in split_lines:
                output_file.write(split_line + '\n')

    print('Reformatted all genomes!')


def main(): 
    prosyn_classification = args.prosyn_classification
    genome_sources = args.genome_sources 

    ### 1. Obtain genome2ecotype.tsv ### 
    g2e_df = create_g2e(prosyn_classification, genome_sources)

    ### 2. Reformat fasta files to fit mason read simulator input requirements ### 
    reformatted_genome_outdir = "data/ReformattedGenomes"
    reformat_fna(g2e_df, genome_sources, reformatted_genome_outdir, 70)


if __name__ == "__main__": 
    main()
