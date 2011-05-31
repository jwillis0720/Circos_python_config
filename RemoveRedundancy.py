#!/usr/bin/env python

from Bio import SeqIO
import sys


if(len(sys.argv) < 2):
        print "Usage: RemoveRedundancy <input_fasta> <output_fasta>"
        sys.exit()

fasta_file = sys.argv[1]
dictionary = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta"))

bin = []
for value in dictionary.values():
	if str(value.seq) not in bin:
		bin.append(str(value.seq))

			
bin = set(bin)
file = open(sys.argv[2], 'w')


size = len(bin)

for i,thing in enumerate(bin):
        file.write(">Unique_Sequeunce_" + str(i) + "\n" + str(thing) + "\n")

print "Done..."

            
                                        
        
	
