#!/usr/bin/env python

from optparse import OptionParser
import sys
import subprocess
from Bio.Blast.Applications import NcbiblastpCommandline
from Bio import SeqIO
import os
from Bio.Align.Applications import ClustalwCommandline

def dowhat():
	print "Gives you an iterative mutations made from germline starting with most conserved.\n"

def call_clustal(string):
        cline = ClustalwCommandline("clustalw2", infile=string)
        process = subprocess.Popen(str(cline), shell=(sys.platform!="win32"), stdout=subprocess.PIPE)
        return process.communicate()[0]

def get_scores(logfile):
        for line in logfile.split("\n"):
                        if "Score:" in line:
                                return int(line.split(":")[-1])
def main():

        ####Parser options####
	parser = OptionParser()
	parser.add_option("-i", "--input", action="store", dest="input", help="input file to make phylotree")
	parser.add_option("-g", "--germline", action="store", dest="germline", help="germline fasta")
	parser.add_option("-o", "--output" , action="store", dest="output", help="the file where you want all your data")
	(options,args) = parser.parse_args()
	if len(sys.argv) < 2:
		dowhat()
		parser.print_help()
		exit()

	####Begin Declarations###

        #start an output file
	fileout = open(options.output, 'w').write("Your Sequence Results:\n\n")

        #parse germline sequence
	germobject = SeqIO.read(options.germline, "fasta")

        #parsexs target sequences
	SO = list(SeqIO.parse(options.input, "fasta"))

        #while there are sequences in the file
        while SO:
                #clustal score holder
                highestscore = 0
                #find best score method with current germline
                for sequence in SO:
                        #open and write
                        clustalhandle = open("clustalentry.fasta" , 'w')

                        SeqIO.write(germobject, clustalhandle, "fasta")

                        SeqIO.write(sequence, clustalhandle, "fasta")

                        clustalhandle.close
                        #close and reopen for reading by clustal
                        clustalhandle = open("clustalentry.fasta" , 'r')

                        #call clust all and return the log (the log contains the score)
                        current_log = call_clustal(clustalhandle.name)

                        clustalhandle.close
                        #get score from clustal log
                        current_score = get_scores(current_log)

                        #determine if that is the best scorer
                        if (current_score > highestscore):
                                highestscore = current_score
                                #save that sequence which scores best as a sequence object
                                sequence_in_question = sequence

                #reopen the clustal handle for one last iteration
                clustalhandle = open("clustalentry.fasta" , 'w')

                #add current germobject and highest scoring
                SeqIO.write(germobject, clustalhandle, "fasta")

                SeqIO.write(sequence_in_question, clustalhandle, "fasta")

                clustalhandle.close

                #open for reading by clustal
                clustalhandle = open("clustalentry.fasta")

                current_log = call_clustal(clustalhandle.name)
                
                current_score = get_scores(current_log)
                
                #append to output
                for line in open("clustalentry.aln"):
                        open(options.output, 'a').write(line)

                open(options.output, 'a').write("With Score of : " + str(current_score) + "\n")

                #remove best scorer
                SO.remove(sequence_in_question)
                #set germobject to best scorer
                germobject = sequence_in_question

        
                
def cleanup():
        os.remove("clustalentry.aln")
        os.remove("clustalentry.fasta")
        os.remove("clustalentry.dnd")

if __name__ == "__main__":
	main()
	cleanup()
