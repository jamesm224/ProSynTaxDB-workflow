"""
Purpose: to make composition config for read sim. 
    - Output .yaml file located in data/composition_config.yaml

Edit ratio list and composition config dict keys for different combinations, e.g.: 
    composition_config[fname] = {
        'Synechococcus': syn_ratio, 
        'Prochlorococcus': pro_ratio,
    }

"""
import yaml
import pandas as pd 
from pathlib import Path 

def main():   
    # list of percentage of Heterotroph 
    het_ratios = [99.9, 99.85, 99.8, 99.7, 99.6, 99.5, 99, 95, 90, 80, 70]

    # loop through each Syn percent and make sample composition 
    composition_config = {}  # dict to store samples 
    for het_ratio in het_ratios:
        syn_ratio = round(100 - het_ratio, 1)

        fname = f"{het_ratio}_Het_{syn_ratio}_Syn"

        composition_config[fname] = {
            'Heterotroph': het_ratio, 
            'Synechococcus': syn_ratio,
        }

    # save to YAML file
    Path('data').mkdir(parents=True, exist_ok=True)

    with open('data/composition_config.yaml', 'w') as file:
        yaml.dump(composition_config, file, default_flow_style=False)
    
main()