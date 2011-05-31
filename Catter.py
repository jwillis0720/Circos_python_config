#!/usr/bin/python

import glob
import os
import sys
from zipfile import ZipFile

#########ARGUMENT CHECK###################
if(len(sys.argv)<2):
	print('Usage: python Bryans_Cat.py <output_file> <zipped file>')
	sys.exit()

########Global Variables############
files = []
direc = sys.argv[2][:-4]  ##set up new directory
output = sys.argv[1]
newfile = open(output,'w')
######Functions##########
def check_direc(dir_in_question):
	if(os.path.exists(dir_in_question) == False):
		os.mkdir(dir_in_question)
        pass

def unzip_mode(zip_file):
	check_direc(direc)
	z = ZipFile(zip_file)
	z.extractall(path=direc)  #unzip files to the parent directory
	for file in os.listdir(direc):
	    if file.endswith('.seq'):
	       files.append(direc + '/' + file)  ##adds the file from anywhere
	return files
def sent_direct_mode(argument):
      for file in argument:
	      if file.endswith('.seq'):
	      	files.append(sys.argv[2]+file)
      return files

def concatonator(argument):
        for file in argument:
                newfile.write('>'+file+'\n')
                for line in open(file):
                        newfile.write(line)
                newfile.write('\n\n')


###Main#####
if __name__ == '__main__':
        if(sys.argv[2].endswith('zip')):
                files = unzip_mode(sys.argv[2]) #unzips if need be
        else: 
                files = sent_direct_mode(sys.argv[2]) #if only passed a directory of sequences
        concatonator(files)
######make new file###
##        for file in files:
##            newfile.write('>'+file+'\n')
##            for line in open(file):
##                newfile.write(line)
##            newfile.write('\n\n')
##        newfile.close()
