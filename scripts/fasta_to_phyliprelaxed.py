

import sys
from Bio import AlignIO

infile=sys.argv[1]
outfile=sys.argv[2]
input_handle = open(infile, "r")
output_handle = open(outfile, "w")

alignments = AlignIO.parse(input_handle, "fasta")
AlignIO.write(alignments, output_handle, "phylip-relaxed")

output_handle.close()
input_handle.close()
