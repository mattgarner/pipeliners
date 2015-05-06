# Pipeline for producing clipped and unclipped bamfiles from sample_name's
# 23st April 2015
# Nicholas S. Gleadall - ng384@cam.ac.uk

# print "Hello World!"

#------------------------------------------------------------
# Importing Modules

import sys
import subprocess
import os
import re

import pipeliners

#------------------------------------------------------------
# Setting globals

# Software bin loaction
bin = "/software/bin/"

def cutadapt( infile, outfile):
    return( "/software/packages/cutadapt-1.1/bin/cutadapt -b TGTAGAACCATGTCGTCAGTGT -b AGACCAAGTCTCTGCTACCGT "  + infile  +" | gzip -c  > analysis/" + outfile)

def smalt( infile1, infile2, outfile):

    # Align the reads to the reference (run smalt-0.7.6 to see all options)
    return "/software/bin/smalt_0.7.6 map -f samsoft /refs/HIV/K03455_s1k6 " + infile1 + " " + infile2 + "| samtools view -Sb -  > " + outfile

def remove_adapters(infile1,infile2,outfile1,outfile2):

	# remove the sequencing adaptors
	return = "/software/packages/cutadapt-1.1/bin/cutadapt -b TGTAGAACCATGTCGTCAGTGT -b AGACCAAGTCTCTGCTACCGT " + infile1 + " > " + outfile1
	return = "/software/packages/cutadapt-1.1/bin/cutadapt -b TGTAGAACCATGTCGTCAGTGT -b AGACCAAGTCTCTGCTACCGT " + infile2 + " > " + outfile2

def sam_to_bam(infile, outfile):

	return =  "/software/bin/samtools view -Sb " + infile + " " + outfile  

def sort_bamfile(infile, outfile):

	# sort bamfile
	return = "/software/bin/samtools sort " + infile + ".bam " + outfile + "_sorted"

def deduplicate_bamfile(infile, outfile, outcsv): 

	# Mark/remove duplicate reads
	return = "/software/bin/picard -t MarkDuplicates I= " + infile + " O= " + outfile + " AS=true M=" + outcsv 

def index_bamfile(infile):	
	# Index the bam file so it can be viewed in IGV later on
	index = "/software/bin/samtools index " + infile

def unclip_bamfile(infile):
	# Run unclip bamfile
	unclip_bamfile = "/software/bin/scripts/bam_unclip_bases.pl " + infile + ".bam"


#------------------------------------------------------------
# Define fastq's and get sample names. 

# Gets location of fastq
if (len(sys.argv) == 1):
    print "Needs an sample name as input"
    exit();
 

sample_name = sys.argv[1]    
sample_name = re.sub(r"(.*).1.fq.gz", r"\1", sample_name)
sample_name_unclipped = sample_name + "_unclipped"
sample_ra   = sample_name + "_ra"

pipeliners.system_call('mkdir', "mkdir -p analysis")
pipeliners.system_call('cutadapt1', cutadapt( sample_name+".1.fq.gz", sample_ra+".1.fq.gz"))
pipeliners.system_call('cutadapt2', cutadapt( sample_name+".2.fq.gz", sample_ra+".2.fq.gz"))
pipeliners.system_call('smalt', smalt( sample_ra+".1.fq.gz", sample_ra+"_ra.1.fq.gz", sample_name+"_mapped.bam"))

exit()



#------------------------------------------------------------
# Commands to be executed

# Make analysis directory














