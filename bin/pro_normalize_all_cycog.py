##### Load Packages #####
import numpy as np
import os
import pandas as pd
import argparse
from pathlib import Path

##### 2. Total 424 CyCOG Normalization #####

### Define Arg Parse Script ###
def parse_args():
    parser = argparse.ArgumentParser(description='Total Cycog Read Count Normalization Script')
    parser.add_argument('--diamond_outputs', type=str, required=True, help='Path to the directory containing Diamond output files')
    parser.add_argument('--total_cycog_input', type=str, required=True, help='Path to the total cycog input TSV file')
    # parser.add_argument('--normalized_output', type=str, required=True, help='Path to the output directory for normalized CSV files')
    return parser.parse_args()

### Define Primary Function ###
def main():
    args = parse_args()

    # Define Input Read Variables #
    diamond_outputs = args.diamond_outputs
    total_cycog_input = args.total_cycog_input
    # normalized_output = args.normalized_output

    ### Load CyCOG key ###
    total_cycog_key=pd.read_csv(total_cycog_input,sep='\t',header=None, names=['cycog_iid','mean_length'])
    total_cycog_key
    # print(total_cycog_key)

    # List of unique suffixes  - MARMICRODBv2#
    suffixes = ['_Prochlorococcus_subclade_AMZ-I_reads.tsv', '_Prochlorococcus_subclade_AMZ-II_reads.tsv', '_Prochlorococcus_subclade_AMZ-III_reads.tsv',
                '_Prochlorococcus_subclade_HLI_reads.tsv', '_Prochlorococcus_subclade_HLII-HLVI_reads.tsv', '_Prochlorococcus_subclade_HLIII-HLIV_reads.tsv',
                '_Prochlorococcus_subclade_LLI_reads.tsv', '_Prochlorococcus_subclade_LLII-LLIII_reads.tsv', '_Prochlorococcus_subclade_LLIV_reads.tsv',
                '_Prochlorococcus_subclade_LLVII_reads.tsv', '_Prochlorococcus_subclade_LLVIII_reads.tsv', 
                '_Prochlorococcus_subsubclade_HLVI_reads.tsv','_Prochlorococcus_subsubclade_HLII_reads.tsv','_Prochlorococcus_subsubclade_HLIII_reads.tsv',
                '_Prochlorococcus_subsubclade_HLIV_reads.tsv','_Prochlorococcus_subsubclade_LLIII_reads.tsv','_Prochlorococcus_subsubclade_LLII_reads.tsv',
                '_unclassified_reads.tsv']

    # Create a temp List #
    all_cycog_output_dfs = []

    for suffix in suffixes:
        # Loop through files with the current suffix
        # for quant_file in Path(diamond_outputs).rglob('*.tsv'):
        for quant_file in Path(diamond_outputs).glob(f'*{suffix}'):

            # Process each file individually
            filename = quant_file.parts[-1]
            filename = filename.replace('.tsv', '')

            # Check if the file is empty before trying to read it #
            with quant_file.open() as f: 
                first_line = f.readline()
                if not first_line.strip():
                    print(f"Skipped the file {quant_file} as it is empty.")
                    continue
                else:
                    try:
                        # Read each diamond output file #
                        df = pd.read_csv(quant_file, sep='\t', header=None,
                                         names=['read_name', 'query', 'seq_id', 'alignment_length', 'mismatch_num',
                                                'gap_open', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore'])
                        df_input = df.copy()
                        df_input['filename'] = filename
                    except Exception as e:
                        print(f"An error occurred while reading {quant_file}: {e}")
                        continue

            # Further processing for the individual DataFrame #
            df_input['cycog_iid'] = df_input['query'].str.split('|').str[1]
            df_input = df_input.drop_duplicates(subset='read_name')

            ### Find the total core cycog hits in each diamond file ###
            total_cycog_hits = df_input[['filename', 'cycog_iid', 'alignment_length']]
            total_cycog_hits['mean_length'] = total_cycog_hits['cycog_iid'].map(total_cycog_key.set_index('cycog_iid')['mean_length'])
            # total_cycog_hits.loc[:, 'sample_name'] = total_cycog_hits['filename'].str.split('.').str[0]
            total_cycog_hits.loc[:, 'sample_name'] = total_cycog_hits['filename'].str.split('.names_').str[0]
            # total_cycog_hits['Clade'] = total_cycog_hits['filename'].str.split('_subclade_').str[1]
            total_cycog_hits['Clade']= total_cycog_hits['filename'].str.split('.names_').str[1]
            # total_cycog_hits['Clade'] = total_cycog_hits['filename'].str.rsplit('Prochlorococcus_subclade_', n=1).str[1]
            total_cycog_hits = total_cycog_hits.dropna(subset=['mean_length'])
            total_cycog_hits['genome_equivalents']=total_cycog_hits['alignment_length']/total_cycog_hits['mean_length']

            ### Obtain the genome equivalents for each Clade per Sample ###
            temp_cycogs=total_cycog_hits.groupby(['sample_name', 'Clade'])['genome_equivalents'].median().reset_index()
            # temp_cycogs['genome_equivalents']=temp_cycogs['alignment_length']/359404.6391
            # temp_cycogs
            print(temp_cycogs)
            # Save the output file for the current suffix
            # output_filename = Path(normalized_output) / f'total_cycog_read_count_normalization_{suffix.replace(".tsv", ".csv")}'
            # temp_cycogs.to_csv(output_filename, index=False)
            # print(f'Saved output file: {output_filename}')
            all_cycog_output_dfs.append(temp_cycogs)
            # print(all_cycog_output_dfs)

    # Optionally, you can combine the results from all suffixes into a single file
    combined_output_df = pd.concat(all_cycog_output_dfs, ignore_index=True)
    # combined_output_filename = Path(normalized_output) / 'total_cycog_read_count_normalization_combined.csv'
    # combined_output_df.to_csv(combined_output_filename, index=False)
    # combined_output_filename = Path(normalized_output) / 'total_pro_cycog_read_count_normalization_combined.csv'
    combined_output_filename = 'total_pro_cycog_read_count_normalization_combined.csv'
    combined_output_df.to_csv(combined_output_filename, index=False)
    print(f'Saved combined output file: {combined_output_filename}')

if __name__ == "__main__":
    main()
