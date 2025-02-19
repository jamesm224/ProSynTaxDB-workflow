"""
Purpose: to create inputs for read simulation (individual input for each subset). 
    - Concatenate all reformatted genomes of a clade into 1 fasta file 

"""
import os
import argparse
import subprocess
import pandas as pd 
from pathlib import Path 

# COMMAND LINE ARGUMENTS:
parser = argparse.ArgumentParser()
parser.add_argument("genome2ecotype", help="Path to genome2ecotype.tsv file generated in PrepGenomeDB step.")
parser.add_argument("reformatted_genomes", help="Path to directory with reformatted genomes from PrepGenomeDB step.")
parser.add_argument("outdir", help="Path to directory for output.")
args = parser.parse_args()

def obtain_metadata(df, subset_list, outdir):
    """
    Filter genome list to subset list and save: 
        1. df with filtered genome2ecotype 
        2. filtered unique ecotypes 

    params:
    df: full/complete genome2ecotype df 
    subset_list: list of genomes for simulation; i.e. genomes to keep 
    outdir: directory for .tsv file output 
    """
    # filter df for subset genomes
    df = df[df['Genome'].isin(subset_list)]

    # obtain list of unique ecotype 
    unique_ecotype = df['Clade'].unique()
    unique_ecotype = pd.DataFrame(unique_ecotype)

    # save filtered genome2ecotype df and unique ecotypes 
    df.to_csv(f'{outdir}/genome2ecotype.tsv', sep='\t', index=False)
    unique_ecotype.to_csv(f'{outdir}/unique_ecotypes.tsv', sep='\t', index=False, header=None)

    return df

def concatenate_files(file_paths, output_file):
    """
    Combines contents of all files in a list into 1 file. 

    params:
    file_paths: list of paths to genomes (if a clade) to concat
    output_file: path to output file  
    """
    # Use the cat command to concatenate files
    command = ['cat'] + file_paths  # Construct the command
    with open(output_file, 'w') as outfile:
        subprocess.run(command, stdout=outfile)

def group_clade_fastas(df, indir, outdir):
    """
    Group all genomes in 1 clade into 1 fasta file. 

    params:
    df: genome2ecotype df 
    indir: input dir with all reformatted genomes
    outdir: output dir to put concatenated genomes 
    """
    clade_groups = df.groupby(['Clade'])
    for index, cdf in clade_groups:
        clade = index[0]

        # obtain list of genome names 
        genomes = cdf['Genome'].values.tolist()  

        # obtain list of paths to genomes for concat 
        genome_paths = [f'{indir}/{genome}.fna' for genome in genomes]   

        out_fpath = f'{outdir}/{clade}.fna'
        concatenate_files(genome_paths, out_fpath)

def group_group_fastas(df, indir, outdir):
    """
    Group all genomes in 1 gruop (i.e. pro/syn/hets) into 1 fasta file. 

    params:
    df: genome2ecotype df 
    indir: input dir with all reformatted genomes
    outdir: output dir to put concatenated genomes 
    """
    group_groups = df.groupby(['Group'])
    for index, cdf in group_groups:
        group = index[0]

        # obtain list of genome names 
        genomes = cdf['Genome'].values.tolist()  

        # obtain list of paths to genomes for concat 
        genome_paths = [f'{indir}/{genome}.fna' for genome in genomes]   

        out_fpath = f'{outdir}/{group}.fna'
        concatenate_files(genome_paths, out_fpath)


def main():
    g2e_df = args.genome2ecotype
    g2e_df = pd.read_table(g2e_df)

    reformatted_genomes = args.reformatted_genomes

    outdir = args.outdir

    for i in range(10):
        i+=1  # start at 1 instead of 0
        i = str(i)

        genome_list = f"data/1.GenomeSubset/simulation_set_{i}.txt"
        subset_list = pd.read_table(genome_list, names=['Genome'])['Genome'].values.tolist()

        subset_outdir = f'{outdir}/subset_{i}'
        Path(subset_outdir).mkdir(exist_ok=True, parents=True)

        # 1. obtain simulation set metadata 
        filtered_g2e = obtain_metadata(g2e_df, subset_list, subset_outdir)

        # 2. Group all subsetted genomes in a clade into 1 fasta file
        grouped_clade_outdir = f"{subset_outdir}/GroupedCladeFasta"
        Path(grouped_clade_outdir).mkdir(exist_ok=True, parents=True)

        group_clade_fastas(filtered_g2e, reformatted_genomes, grouped_clade_outdir)
        print(f'Completed clade concat on genomes in subset #{i}!')

        # 3. Group all subsetted genomes in a group into 1 fasta file (i.e. pro/syn/het)
        grouped_group_outdir = f"{subset_outdir}/GroupedGroupFasta"
        Path(grouped_group_outdir).mkdir(exist_ok=True, parents=True)

        group_group_fastas(filtered_g2e, reformatted_genomes, grouped_group_outdir)
        print(f'Completed group concat on genomes in subset #{i}!')


main()