"""
Purpose: to extract read names of each clade into its own file. 
    - i.e. [sname]_names.out --> [sname]_[genus]_[rank]_[clade]_reads.txt
        - rank: either subclade (for Pro) or subsubclade (for Syn)
        - e.g. test1_Prochlorococcus_subclade_AMZ-III_reads.txt

09/16/24
Authors: J.Mullet, N.N.Vo
"""
import pandas as pd
from pathlib import Path

def process_genus_df(df, rank, sample_name, output_dir):
    """
    For each classification of a specified rank (e.g. "Prochlorococcus subclade HLI" if rank=='subclade'): 
        - Save names of reads (fastq sequence headers) of reads with that classification 
        - e.g. save all reads in the current sample classified as "Prochlorococcus subclade HLI" into a file 
    """
    df = df[[rank, 'genus', 'read']]

    # fill NAs in cols with "unclassified" 
    df = df.fillna(value={rank: 'unclassified'})
    df[rank] = df[rank].replace('', 'unclassified')

    # group by the specified rank (subclade or subsubclade)
    rank_groups = df.groupby([rank])

    # for each rank_classification (e.g. AMZ-I)
    for index, rdf in rank_groups:
        # genus of classification (Pro or Syn)
        genus = rdf.iloc[0]['genus']
        
        # obtain classification:  kaiju classification + string edit
        classification = index[0].replace(" ", "_").replace("/", "_")  
        
        # in rows where there are no classification, call them 'unclassified' 
        if classification == 'unclassified':
            classification = f'{genus}_{rank}_unclassified'  
        
        print(f"\ndf.head() of {classification}:")
        print(rdf.head())

        # output_path = Path(output_dir)
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        rdf[['read']].to_csv(f"{output_dir}/{sample_name}_{classification}_reads.txt", sep='\t', index=False, header=None)

def process_kaiju_names(fpath, output_dir):
    """
    Prepares input names.out file from kaiju for data parsing. 
    Parses DataFrame from names.out file to save as csv files containing reads for each classification.
    """
    # Obtain name of sample from file path 
    sample_name = fpath.name.replace('_names.out', '') 
    print(f"Processing sample: {sample_name}")
    print(f"Sample path: {fpath}")
    
    # Import and process names.out kaiju file 
    df = pd.read_table(fpath, header=None, usecols=[1,3], names=['read', 'taxa'])
    df['sample_name'] = sample_name

    # Obtain data for each rank of classification
    df['taxa'] = df['taxa'].str.split(';')  # split column containing full classification 
    df['genus'] = df['taxa'].str.get(8) 
    df['clade'] = df['taxa'].str.get(9)
    df['subclade'] = df['taxa'].str.get(10)
    df['subsubclade'] = df['taxa'].str.get(11)

    # Remove leading and trailing whitespace 
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Subset to obtain dfs of reads classified as pro and syn
    pro_df = df[df['genus'].str.contains('Prochlorococcus', case=False, na=False)].copy()
    syn_df = df[df['genus'].str.contains('Synechococcus', case=False, na=False)].copy()

    # Process each genus df and save read files 
    print("\nProcessing Prochlorococcus reads... ")
    process_genus_df(pro_df, 'subclade', sample_name, output_dir)  
    
    print("\nProcessing Synechococcus reads... ")
    process_genus_df(syn_df, 'subsubclade', sample_name, output_dir)

def main():
    # input path to kaiju name file 
    fpath = Path(snakemake.input['kaiju_out'])
    # output path to directory for .csv file 
    output_dir = snakemake.output['binned_header_dir']
    
    # process the input [sample_name]_names.out file from kaiju
    process_kaiju_names(fpath, output_dir)

if __name__ == "__main__":
    main()
