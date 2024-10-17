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

James Mullet & Nhi N. Vo 
10/16/24 
"""
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

    # filter for cols 
    df = df[['read_name', 'cycog_iid', 'alignment_length']]

    return df 

def process_genus_df(df, rank):
    """
    Returns df with cols [rank, genus, read_name]: 
        - rank: subclade or subsubclade values
        - genus: genus of classified read (pro or syn)
        - read_name: name of read classified as pro/syn 
    """
    # remove phage & viral rows
    df = df[~df['genus'].str.contains('phage')]
    df = df[~df['genus'].str.contains('virus')]

    # filter for cols needed 
    df = df[[rank, 'genus', 'read_name']]

    # fill NAs in cols with "unclassified" 
    df = df.fillna(value={rank: 'unclassified'})
    df[rank] = df[rank].replace('', 'unclassified')

    # rename col 
    df = df.rename(columns={rank: 'clade'})

    return df

def import_read_classification(fpath):
    """
    """
    df = pd.read_table(fpath, names=['read_name', 'classification'])

    if len(df) == 0:
        print('No reads classified as Pro or Syn in sample.')
        # return empty df 
        df = pd.DataFrame({
            'read_name': [], 'genus': [], 'classification': []
        })

        return df

    # Obtain data for each rank of classification
    df['classification'] = df['classification'].str.split(';')  # split column containing full classification 
    df['genus'] = df['classification'].str.get(8) 
    df['clade'] = df['classification'].str.get(9)
    df['subclade'] = df['classification'].str.get(10)
    df['subsubclade'] = df['classification'].str.get(11)

    # Remove leading and trailing whitespace 
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df['genus'] = df['genus'].astype(str)  # convert to str type for lines below

    # subset to obtain dfs of reads classified as pro and syn
    dfs = []
    if 'Prochlorococcus' in df['genus'].unique():
        print(f"\nProcessing Prochlorococcus reads in sample... ")
        pro_df = df[df['genus'].str.contains('Prochlorococcus', case=False, na=False)].copy()
        pro_df = process_genus_df(pro_df, 'subclade') 
        dfs.append(pro_df)
    else: 
        print(f'Sample does not have any Prochlorococcus reads.')

    if 'Synechococcus' in df['genus'].unique():
        print(f"\nProcessing Synechococcus reads in sample... ")
        syn_df = df[df['genus'].str.contains('Synechococcus', case=False, na=False)].copy()
        syn_df = process_genus_df(syn_df, 'subsubclade')
        dfs.append(syn_df)
    else: 
        print(f'Sample does not have any Synechococcus reads')

    df = pd.concat(dfs)

    return df

def cycog_normalize(df, cycog_list):
    """
    """
    # filter df for cycogs in list
    df = df[df['cycog_iid'].isin(cycog_list)]

    # group by classification and normalize each group
    classification_groups = df.groupby(['genus', 'clade'])

    normalized_data = {
        'genus': [], 
        'clade': [], 
        'alignment_length': [], 
        'genome_equivalents': [], 
    }

    for (genus, classification), cdf in classification_groups:
        # sum alignment length 
        sum_alnm_len = cdf['alignment_length'].sum()

        # obtain_genome_equivalence
        total_cycog_len = 359404.6391
        genome_equivalents = sum_alnm_len / total_cycog_len

        normalized_data['genus'].append(genus)
        normalized_data['clade'].append(classification)
        normalized_data['alignment_length'].append(sum_alnm_len)
        normalized_data['genome_equivalents'].append(genome_equivalents)

    df = pd.DataFrame(normalized_data)

    return df

def main():
    # obtain snakemake input and output paths 
    diamond_fpath = Path(snakemake.input['diamond_out'])  # path to diamond blast output 
    cycog_fpath = Path(snakemake.input['cycog_file'])  # path to 424 cycog len
    read_name_taxa_fpath = Path(snakemake.input['read_name_taxa_file'])  # path to file that maps read name to its taxa 
    normalized_output_fpath = snakemake.output['normalized_output']  # normalized output fpath 

    # obtain sample name from diamond file path 
    sample_name = diamond_fpath.stem

    # obtain list of 424 cycog iid
    cycog_df = pd.read_table(cycog_fpath,header=None, names=['cycog_iid','mean_length'])
    cycog_list = cycog_df['cycog_iid'].values.tolist()

    # import diamond output file 
    diamond_df = import_diamond_output(diamond_fpath)    

    # import readname and their taxon 
    read_classification_df = import_read_classification(read_name_taxa_fpath)

    # combine classification with blast results
    df = pd.merge(diamond_df, read_classification_df, on='read_name', how='inner')

    # normalize each clade 
    if len(df) > 0:
        df = cycog_normalize(df, cycog_list)
    else:
        # make empty df
        df = pd.DataFrame({
            'genus': [], 'clade': [], 'alignment_length': [], 'genome_equivalents': [], 
        })

    df['sample_name'] = sample_name

    # reorder column name to match aggregate rule in downsream
    df = df[['sample_name', 'genus', 'clade', 'alignment_length', 'genome_equivalents']]

    # save samples normalized df without column names (headers)
    df.to_csv(normalized_output_fpath, sep='\t', index=False, header=False)


main()
