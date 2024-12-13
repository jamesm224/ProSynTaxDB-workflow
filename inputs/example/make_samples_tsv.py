"""
Example script to make samples.tsv file as input for snakemake pipeline. 
    - Script assumes that all read files are in input directory.
    - Edit script accordingly if read files are stored in a 
    different file structure.

Required columns: ['sample', 'forward read', 'reverse read']

12/13/24
"""
import pandas as pd 
from pathlib import Path 

# path to directory with raw read files 
READ_DIR = "raw_reads"

def main():
    sample_dict = {}  # dict to store data for output .tsv

    # cycle through each file in directory 
    for fpath in Path(READ_DIR).glob('*fastq'):
        fname = fpath.stem  # obtain file name (e.g. ProSyn-s2_2)
        read_type = fname.split('_')[-1]  # obtain read type (i.e. '1' or '2')
        fname = fname.split('_')[0]  # remove read type from file name 

        # edit file path to be relative to snakemake workdir 
        # note: full path to file also works 
        fpath = f'inputs/example/{fpath}'

        # add file data to dict 
        if fname not in sample_dict:
            sample_dict[fname] = {}
            sample_dict[fname][f"R{read_type}_path"] = fpath 
        else:
            sample_dict[fname][f"R{read_type}_path"] = fpath 

    # make df of samples.tsv
    df = pd.DataFrame.from_dict(sample_dict, orient="index").reset_index()

    df = df.rename(columns={
        "index": "sample", 'R1_path': 'forward read', 'R2_path': 'reverse read'
    })

    df.to_csv('../samples.tsv', sep='\t', index=False) 

main()