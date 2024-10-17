"""
Purpose: to summarize read counts from kaiju_summary files.

09/20/24 - J.Mullet, N.N.Vo
"""
import pandas as pd 
from pathlib import Path 

def process_kaiju_summary(fpath, genus_list):
    """
    Returns a df from kaiju_summary file from fpath:
        - cols: ['taxon_name', 'reads', 'percent']
    Steps: 
        - Sum read counts from "cannot be assigned to a (non-viral) genus" and "unclassified"
        - For rows whose 'taxon_name' values are not in given genus_list: 
            - Sum read count ['reads']
        - Obtain percentage 

    genus_list: list of row values (genus) to keep from kaiju_summary. 
        - The remaining will be summed into 1 single "other_genus" group. 
    """
    df = pd.read_table(fpath)[['taxon_name', 'reads']]
    df['taxon_name'] = df['taxon_name'].str.strip()  # remove whitespace, if any 

    # convert "cannot be assigned to a (non-viral) genus" into "unclassified"
    df['taxon_name'] = df['taxon_name'].str.replace("cannot be assigned to a (non-viral) genus", "unclassified")

    # sum rows that are duplicates (i.e. "unclassified")
    df = df.groupby('taxon_name', as_index=False).sum()

    # filter to obtain rows to sum (rows NOT IN genus_list)
    other_df = df[~df['taxon_name'].isin(genus_list)]

    # sum values for "other_genus" row
    other_read_sum = other_df['reads'].sum()

    # create new row with sum values
    other_row = pd.DataFrame({
        "taxon_name": ["other_genus"], 
        "reads": [other_read_sum], 
    })

    # create final df
    dfs = [
        df[df['taxon_name'].isin(genus_list)],
        other_row
    ]

    df = pd.concat(dfs, ignore_index=True)

    # create percentage col 
    sum_read_count = df['reads'].sum()
    df['percent'] = (df['reads'] / sum_read_count) * 100

    return df

def reformat_df(df):
    """
    Returns a df with cols: [sample_name, summary_type, each value in genus_list]
        - summary_type: 'percent' or 'reads'
    """
    # convert cols ['reads', 'percent'] into row values in new col 'summary_type'
    df = pd.melt(
        df, 
        id_vars = ['taxon_name', 'sample_name'], 
        value_vars = ['reads', 'percent'], 
        var_name = 'summary_type', 
        value_name = 'value'
    )

    # long to wide
    df = df.pivot(index=['sample_name', 'summary_type'], columns='taxon_name', values='value').reset_index()
    df.columns.name = None  # remove index name 

    # sort before saving (to group 'percent'/'reads' rows together)
    df = df.sort_values(by=['summary_type'])

    return df


def main():
    """
    """
    # obtain input from snakemake  
    kaiju_summary_list = snakemake.input['kaiju_summary']  # list of fpath to [sample]_kaiju_summary.tsv files
    genus_list = snakemake.params['genus_list']  # list of genus to keep info 
    
    # fpath for output file 
    final_summary_outpath = snakemake.output['summary_oufpath']

    # list for storing summary df
    dfs = []

    for fpath in [Path(p) for p in kaiju_summary_list]:
        # sample name (from file name)
        sname = fpath.stem.replace('_kaiju_summary', '')

        # import and process kaiju summary df 
        df = process_kaiju_summary(fpath, genus_list)
        
        df['sample_name'] = sname

        dfs.append(df)

    df = pd.concat(dfs)

    # reformat df so that taxons in genus_list are column headers
    # (long to wide)
    # df = reformat_df(df)

    # save file
    df.to_csv(final_summary_outpath, sep='\t', index=False)

main()
