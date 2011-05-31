#!/usr/bin/env python

from optparse import OptionParser
import sys
import subprocess
from Bio.Blast.Applications import NcbiblastpCommandline
from Bio import SeqIO
from Bio.Blast import NCBIStandalone
from shutil import copy
import os

def dowhat():
	print "Gives you an iterative mutations made from germline starting with most conserved.\n"

def populate_database(fasta_files):
        subprocess.call("makeblastdb -in "  + fasta_files + " -out temporary_database", shell=(sys.platform!="win32"))

def call_blast(commandline):
        subprocess.call(str(commandline), shell=(sys.platform!="win32"))

def main():
	parser = OptionParser()
	parser.add_option("-i", "--input", action="store", dest="input", help="input file to make phylotree")
	parser.add_option("-g", "--germline", action="store", dest="germline", help="germline fasta")
	parser.add_option("-o", "--output" , action="store", dest="output", help="the file where you want all your data")
	(options,args) = parser.parse_args()
	if len(sys.argv) < 2:
		dowhat()
		parser.print_help()
		exit()
	
	open(options.output, 'w').write("Your Sequence Results:\n\n")
	copy(options.input, "workable.fasta")
	copy(options.germline, "germ.fasta")
	

	

	list_of_database_files = SeqIO.to_dict(SeqIO.parse("workable.fasta", "fasta"))

        
	while list_of_database_files:
		list_of_database_files = SeqIO.to_dict(SeqIO.parse("workable.fasta", "fasta"))
		populate_database("workable.fasta")
		print "***DatabasePopulated***"
		
		newsequence_search = open("germ.fasta" , "r")	
		cline = NcbiblastpCommandline(matrix="PAM30", evalue="20", word_size="2", query="germ.fasta", cmd='blastp', db="temporary_database", out="blastout")	
		newsequence_search.close
		
		print "****Cline = *** --->", cline

		call_blast(cline)
        	print "***Call_blast_successful***"
		
		result_handle = open('blastout')
		print "***result handle successful***" 
		
		blast_parser = NCBIStandalone.BlastParser()
		print "***blast_parser****"
		
		blast_record = blast_parser.parse(result_handle)
       		print "***blast_record***"
		
		newsequence_search = open("germ.fasta", 'w')
		newsequence_search.write(">" + str(blast_record.alignments[0].title[2:]) + "\n"  + str(blast_record.alignments[0].hsps[0].sbjct))		
	
		current_object = blast_record.alignments[0].title[2:]
        	print current_object
		
		newfile = open(options.output, 'a')
		newfile.write(str(blast_record.alignments[0].hsps[0].query[:]) + "----> Query\n")
        	newfile.write(str(blast_record.alignments[0].hsps[0].match[:]) + "----> Score of: " + str(blast_record.alignments[0].hsps[0].score) + "\n")
		newfile.write(str(blast_record.alignments[0].hsps[0].sbjct[:]) + "----> Template\n\n")
	
		list_of_database_files.pop(current_object)
		SeqIO.write(list_of_database_files.values(), "workable.fasta", "fasta")		

if __name__ == "__main__":
	main()
