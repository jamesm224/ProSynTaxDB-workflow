import pandas as pd
import argparse
from pathlib import Path

##### Prep the Arg Parse Script #####
def parse_args():
    parser = argparse.ArgumentParser(description='Process Kaiju output for specific clades')
    parser.add_argument('--kaiju_input', type=str, required=True, help='Path to the Kaiju input directory')
    # parser.add_argument('--output_dir', type=str, required=True, help='Path to the output directory for CSV files')
    return parser.parse_args()

##### Main Function #####
def main():
    args = parse_args()
    
    # Define the target genus
    pro = 'Prochlorococcus'

    # Define a list of dictionaries, each containing the clade list and the corresponding dictionary
    # clade_dicts = [
        ### MARMICRODB Only ###
        # {'clade_list': ['Prochlorococus subclade AMZ-I'], 'output_dict': {}},
        # {'clade_list': ['Prochlorococus subclade AMZ-II'], 'output_dict': {}},
        # {'clade_list': ['Prochlorococus subclade AMZ-III'], 'output_dict': {}},
        # {'clade_list': ['Prochlorococus subclade HLI'], 'output_dict': {}},
        # {'clade_list': ['Prochlorococus subclade HLII-HLVI'], 'output_dict': {}},
        # {'clade_list': ['Prochlorococus subclade HLII'], 'output_dict': {}},
        # {'clade_list': ['Prochlorococus subclade HLIII-HLIV'], 'output_dict': {}},
        # {'clade_list': ['Prochlorococus subclade LLI'], 'output_dict': {}},
        # {'clade_list': ['Prochlorococus subclade LLII.III'], 'output_dict': {}},
        # {'clade_list': ['Prochlorococus subclade LLIV'], 'output_dict': {}},
        # {'clade_list': ['Prochlorococus subclade LLVII'], 'output_dict': {}},
        # {'clade_list': ['Prochlorococus subclade LLVIII'], 'output_dict': {}},
        # {'clade_list': ['unclassified'], 'output_dict': {}},

        # Add more dictionaries for other clades as needed
    # ]
    clade_dicts = [
        {'clade_list': ['Prochlorococcus subclade AMZ-I'], 'output_dict': {}}, #
        {'clade_list': ['Prochlorococcus subclade AMZ-II'], 'output_dict': {}}, #
        {'clade_list': ['Prochlorococcus subclade AMZ-III'], 'output_dict': {}}, #
        {'clade_list': ['Prochlorococcus subclade HLI'], 'output_dict': {}}, #
        {'clade_list': ['Prochlorococcus subclade HLII-HLVI'], 'output_dict': {}}, #
        {'clade_list': ['Prochlorococcus subclade HLIII-HLIV'], 'output_dict': {}},
        {'clade_list': ['Prochlorococcus subclade LLI'], 'output_dict': {}},
        {'clade_list': ['Prochlorococcus subclade LLII-LLIII'], 'output_dict': {}},
        {'clade_list': ['Prochlorococcus subclade LLIV'], 'output_dict': {}},
        {'clade_list': ['Prochlorococcus subclade LLVII'], 'output_dict': {}},
        {'clade_list': ['Prochlorococcus subclade LLVIII'], 'output_dict': {}},
        {'clade_list': ['unclassified'], 'output_dict': {}},

        # Add more dictionaries for other clades as needed
    ]

    # kaiju_input = "/orcd/data/chisholm/001/bioinfo/projects/23_metaG_composition/process_kaiju_out/GORG_v2_run/results/complete_GORG_output"
    kaiju_input = args.kaiju_input

    # Process each input file for each clade
    for clade_dict in clade_dicts:
        clade_list = clade_dict['clade_list']
        output_dict = clade_dict['output_dict']

        # for quant_file in Path(kaiju_input).glob('*_output_kaiju_names.txt'):
        #     sample_name = quant_file.stem.replace('_output_kaiju_names.txt', '')
        for quant_file in Path(kaiju_input).glob('*_names.out'):
            sample_name = quant_file.stem.replace('_names.out', '')

            try:
                df = pd.read_csv(quant_file, sep='\t', header=None, names=['Column1', 'read', 'Column3', 'taxa'])
                df_input = df.copy()
                df_input['sample_name'] = sample_name
                df_input = df_input.dropna(subset=['taxa'])
                df_input['taxa'] = df_input['taxa'].str.split(';')

                ### Marmicrodb v1 ###
                # df_input['genus'] = df_input['taxa'].str.get(7)
                # df_input['clade'] = df_input['taxa'].str.get(8)
                # df_input['subclade'] = df_input['taxa'].str.get(9)
                # df_input['subsubclade'] = df_input['taxa'].str.get(10)

                ### Marmicrodb v2.0 ###
                df_input['genus'] = df_input['taxa'].str.get(8)
                df_input['clade'] = df_input['taxa'].str.get(9)
                df_input['subclade'] = df_input['taxa'].str.get(10)
                df_input['subsubclade'] = df_input['taxa'].str.get(11)

                df_input['subclade'] = df_input['subclade'].fillna('unclassified')
                subset_df = df_input[['read', 'genus', 'subclade','sample_name']]
                # subset_df = subset_df.dropna(subset=['clade'])
                subset_df['genus'] = subset_df['genus'].str.strip()
                subset_df['subclade'] = subset_df['subclade'].str.strip()
                # Subset to find only values where the "Genus" column contains the target genus
                pro_df = subset_df[subset_df['genus'].str.contains(pro, case=False, na=False)]
                clade_reads = pro_df[pro_df['subclade'].isin(clade_list)]
                output_df = clade_reads[['read']]
                output_dict[sample_name] = output_df
                print(output_df)
                # clade_reads = subset_df[subset_df['subclade'].isin(clade_list)]
                print(clade_reads)
                # output_df = clade_reads[['read']]
                # output_dict[sample_name] = output_df

            except Exception as e:
                print(f"An error occurred while reading {quant_file}: {e}")

    # Save the output for each clade
    for clade_dict in clade_dicts:
        clade_list = clade_dict['clade_list']
        output_dict = clade_dict['output_dict']
        print(output_dict)
        for sample_name, output_df in output_dict.items():
            clade_name = clade_list[0].replace(" ", "_").replace("/", "_")  # Adjust clade name if needed
            # output_df.to_csv(f"/orcd/data/chisholm/001/bioinfo/projects/23_metaG_composition/process_kaiju_out/normalization_workflow/results/binned_reads/{sample_name}_{clade_name}_reads.csv", index=False, header=None)
            output_path = f"{sample_name}_{clade_name}_reads.csv"
            
            output_df.to_csv(output_path, index=False, header=None)

    
##### Main Function Call #####
if __name__ == "__main__":
    main()
