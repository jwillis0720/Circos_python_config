#!/usr/bin/env python

import sys
print "script <input.txt> <output.txt>"

handle = open(sys.argv[2], 'w')

for item in open(sys.argv[1]):
	string = ""
	string = item.split('\t')[1]
	GI = item.split('\t')[0]
	CDR = string.split(' ')[1]
	codon = string.split(' ')[4]
	sequence = string.split(' ')[7]
	codon_number = string.split(' ')[8]
#	codon_formated = codon_number.split('')[0]
	full_list=[GI,CDR,codon,sequence,codon_number[1]]
	handle.write(','.join(full_list) + "\n")
handle.close()
