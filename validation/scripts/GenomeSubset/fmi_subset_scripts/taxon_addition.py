# import argparse

# ### Read the key file containing the genomes and their identifiers ###
# def read_key_file(key_file):
#     key_mapping = {}
#     with open(key_file, 'r') as file:
#         for line in file:
#             line = line.strip()
#             if line:
#                 parts = line.split('/')
#                 if len(parts) == 2:
#                     key_mapping[parts[0]] = parts[1]
#     return key_mapping

# ### Rename each header ###
# def rename_headers(fasta_file, key_mapping, output_file):
#     ### Open the input and output files ###
#     with open(fasta_file, 'r') as infile, open(output_file, 'w') as outfile:
#         for line in infile:
#             line = line.strip()
#             if line.startswith('>'):
#                 # Process the header and if a match rename it #
#                 header = line[1:]
#                 prefix = header.split('_')[0]
#                 # The format used in renaming #
#                 if prefix in key_mapping:
#                     new_header = f">{header}_{key_mapping[prefix]}"
#                     outfile.write(f"{new_header}\n")
#                 else:
#                     outfile.write(f">{header}\n")
#             else:
#                 # Write the sequence lines #
#                 outfile.write(line + '\n')

# ### Main function call with arg parse and print statements ###
# def main():
#     parser = argparse.ArgumentParser(description='Rename headers in FASTA file based on a key')
#     parser.add_argument('fasta_file', help='Path to the input FASTA file')
#     parser.add_argument('key_file', help='Path to the key file')
#     parser.add_argument('output_file', help='Path to the output FASTA file with renamed headers')
#     args = parser.parse_args()

#     key_mapping = read_key_file(args.key_file)
#     print(f"Number of mappings in key file: {len(key_mapping)}")

#     rename_headers(args.fasta_file, key_mapping, args.output_file)
#     print(f"Header renaming complete. Results written to {args.output_file}")

# if __name__ == "__main__":
#     main()




import argparse

##### Renames headers by adding the taxa identifier to the end of each header #####

### Read the key file containing the genomes and their identifiers ###
def read_key_file(key_file):
    key_mapping = {}
    with open(key_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split('\t|\t')
                if len(parts) == 2:
                    key_mapping[parts[1]] = parts[0]
    return key_mapping

### Rename each header ###
def rename_headers(fasta_file, key_mapping, output_file):
    ### Open the input and output files ###
    with open(fasta_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if line.startswith('>'):
                # Process the header and if a match rename it #
                header = line[1:]
                parts = header.split('_')
                prefix = parts[0]
                suffix = parts[1]
                # The format used in renaming #
                if prefix in key_mapping:
                    new_header = f">{prefix}-orf{suffix}_{key_mapping[prefix]}"
                    outfile.write(f"{new_header}\n")
                else:
                    outfile.write(f">{header}\n")
            else:
                # Write the sequence lines #
                outfile.write(line + '\n')

# def rename_headers(fasta_file, key_mapping, output_file):
#     with open(fasta_file, 'r') as infile, open(output_file, 'w') as outfile:
#         for line in infile:
#             line = line.strip()
#             if line.startswith('>'):
#                 # Process the header and if a match rename it
#                 header = line[1:]  # Remove '>'
#                 prefix, suffix = header.rsplit('_', 1)  # Split by last '_'
#                 # Check if prefix is in key_mapping, if yes, rename header
#                 new_suffix = key_mapping.get(prefix, suffix)  # Use default suffix if prefix not found
#                 # new_header = f">{prefix}_{suffix}_{new_suffix}"
#                 new_header = f">{prefix}_{new_suffix}"
#                 outfile.write(f"{new_header}\n")
#             else:
#                 # Write sequence lines
#                 outfile.write(line + '\n')


### Main function call with arg parse and print statements ###
def main():
    parser = argparse.ArgumentParser(description='Rename headers in FASTA file based on a key')
    parser.add_argument('fasta_file', help='Path to the input FASTA file')
    parser.add_argument('key_file', help='Path to the key file')
    parser.add_argument('output_file', help='Path to the output FASTA file with renamed headers')
    args = parser.parse_args()

    key_mapping = read_key_file(args.key_file)
    print(f"Number of mappings in key file: {len(key_mapping)}")

    rename_headers(args.fasta_file, key_mapping, args.output_file)
    print(f"Header renaming complete. Results written to {args.output_file}")

if __name__ == "__main__":
    main()
