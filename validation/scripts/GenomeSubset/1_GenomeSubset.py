"""
Purpose: to subset genomes randomly 10 times for the specified group. 
"""
import argparse
import pandas as pd 
from pathlib import Path 

# COMMAND LINE ARGUMENTS:
parser = argparse.ArgumentParser()
parser.add_argument("genome2ecotype", help="Path to genome2ecotype.tsv file generated in PrepGenomeDB step.")
parser.add_argument("taxon_group", nargs="?", default="Prochlorococcus", help="Genome group for subsetting. [default: Prochlorococcus]")
parser.add_argument("subset_num", nargs="?", default=10, help="Number of times to subset genome. [default: 10]")
args = parser.parse_args()

N = args.subset_num  # create N random genome subsets 

def subset(clade_groups, iter):
    """
    Subset the genome2ecotype table into:
        - 20% for read simulation 

    params:
    clade_groups (DataFrameGroupBy object): grouped pandas df based on ["Clade"]
    iter (int): iteration of the loop (subset number)
        - Used as seed for random subsetting
        - Different iter will have different subsets, but the same 
        iter (if script was ran multiple times) will have the same subset. 
    """
    # empty lists for subset-ed genomes 
    df_20s = []

    # cycle through each clade and subset 
    for index, df in clade_groups:
        clade = index[0]

        # randomly select 20% of genomes for read simulation 
        df_20 = df.sample(frac=0.2, random_state=iter)
        df_20s.append(df_20)
    
    df_20 = pd.concat(df_20s)

    iter += 1  # so subset id start at 1 instead of 0 
    df_20[['Genome']].to_csv(f'data/GenomeSubset/simulation_set_{iter}.txt', index=False, header=False)


def main():
    # output dir for subset df 
    Path('data/GenomeSubset').mkdir(exist_ok=True, parents=True)

    # input genome2ecotype
    g2e_df = args.genome2ecotype
    g2e_df = pd.read_table(g2e_df)

    # filter for genomes of specified groups only 
    g2e_df = g2e_df[g2e_df['Group'] == args.taxon_group]

    # group by clade and subset N times
    clade_groups = g2e_df.groupby(['Clade'])

    for iter in range(N):
        subset(clade_groups, iter)


main()