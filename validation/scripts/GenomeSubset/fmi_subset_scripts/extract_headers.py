"""
Purpose: to extract headers (string after '>') in genomes to be removed (to be used in simulation). 

James Mullet
"""
import re
import sys

def extract_headers(genome_names_file, fasta_file, output_file):
    # Read genome names from the list file
    with open(genome_names_file, 'r') as f:
        genome_names = [line.strip() for line in f]

    # Open the fasta file for reading
    with open(fasta_file, 'r') as f_in:
        # Open the output file for writing
        with open(output_file, 'w') as f_out:
            # Iterate through each line in the fasta file
            for line in f_in:
                # Check if the current line is a header line
                if line.startswith('>'):
                    header = line.strip()
                    # Check if any genome name matches the header
                    if any(genome in header for genome in genome_names):
                        f_out.write(header + '\n')
                else:
                    continue

### Main Call of function and arg parse for bash usage ###
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python extract_headers.py <list_file> <fasta_file> <output_file>")
        sys.exit(1)

    list_file = sys.argv[1]
    fasta_file = sys.argv[2]
    output_file = sys.argv[3]

    extract_headers(list_file, fasta_file, output_file)