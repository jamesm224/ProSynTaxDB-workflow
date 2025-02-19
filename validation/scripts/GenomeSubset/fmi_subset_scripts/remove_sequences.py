import argparse

##### Remove all Headers and Sequences found in the headers file #####
##### Output filtered fasta to new dataframe #####

### Obtain the headers used in the search ###
def read_headers_from_lst(lst_file):
    with open(lst_file, 'r') as file:
        # Remove the '>' character from the beginning of each header #
        headers_set = {line.strip()[1:] for line in file if line.strip()}
    return headers_set

### Remove sequences and headers that match the above headers ###
def remove_sequences(fasta_file, headers, output_file):
    current_header = ""
    current_sequence = ""
    total_lines = 0
    removed_headers = 0
    # Open Fasta #
    with open(fasta_file, 'r') as infile:
        # Open Output file #
        with open(output_file, 'w') as outfile:
            for line in infile:
                total_lines += 1
                # Only search for lines containing headers #
                if line.startswith('>'):
                    if current_header and current_sequence:
                        total_lines += 1
                        if current_header not in headers:
                            # Write the header and sequence to the output file #
                            outfile.write(f">{current_header}\n{current_sequence}\n")
                        else:
                            removed_headers += 1
                            print(f"Removed header: {current_header}")
                    current_header = line.strip()[1:]
                    current_sequence = ""
                else:
                    current_sequence += line.strip()

            # Add the last sequence if its header is not in the headers set #
            if current_header and current_sequence:
                total_lines += 1
                if current_header not in headers:
                    # Write the header and sequence to the output file
                    outfile.write(f">{current_header}\n{current_sequence}\n")
                else:
                    removed_headers += 1
                    print(f"Removed header: {current_header}")

    print(f"Total lines in FASTA file: {total_lines}")
    print(f"Removed headers: {removed_headers}")

### Main call script with some arg parse and print scripts for debugging ###
def main():
    parser = argparse.ArgumentParser(description='Remove FASTA sequences based on headers listed in a .lst file')
    parser.add_argument('fasta_file', help='Path to the input FASTA file')
    parser.add_argument('lst_file', help='Path to the .lst file containing headers')
    parser.add_argument('output_file', help='Path to the output file to store remaining sequences')
    args = parser.parse_args()

    headers_set = read_headers_from_lst(args.lst_file)
    print(f"Number of headers in .lst file: {len(headers_set)}")

    remove_sequences(args.fasta_file, headers_set, args.output_file)
    print(f"Removal complete. Results written to {args.output_file}")

if __name__ == "__main__":
    main()
