import pandas as pd
import argparse
from pathlib import Path
import subprocess
import re

##### Prep the Arg Parse Script #####
def parse_args():
    parser = argparse.ArgumentParser(description='Process Kaiju output for specific clades')
    parser.add_argument('--kaiju_input', type=str, required=True, help='Path to the Kaiju input directory')
    parser.add_argument('--reads', type=str, required=True, help='Path to the Reads input directory')
    # parser.add_argument('--output_dir', type=str, required=True, help='Path to the output directory for CSV files')
    return parser.parse_args()

def main():
    args = parse_args()
    kaiju_input = args.kaiju_input
    reads = args.reads

    for quant_file in Path(kaiju_input).glob('*.csv'):
        file_path = str(quant_file)
        print(file_path)
        stem = quant_file.stem
        sample_name = re.sub(r'_names.*$', '', stem)
        # print(sample_name)
        # print(reads)
        seqtk_command=f"seqtk subseq {reads}/{sample_name}_trimmed.fastq.gz file_path > /orcd/data/chisholm/001/bioinfo/projects/24_updated_GORG_AMZ_classifier/test_output/pro_binned_reads/{sample_name}_forward.fastq"
        subprocess.run(seqtk_command, shell=True)
# Seqtk command using subprocess
    # subprocess.run(seqtk_command, shell=True)

    # output_path = f"{sample_name}_{clade_name}_reads.csv"
            
    # output_df.to_csv(output_path, index=False, header=None)

##### Main Function Call #####
if __name__ == "__main__":
    main()
