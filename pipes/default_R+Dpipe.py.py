#!

# Pipeline for producing clipped and unclipped bamfiles from sample_name's
# 23st April 2015
# Nicholas S. Gleadall - ng384@cam.ac.uk
# Kim Brugger - kim@brugger.dk

# print "Hello World!"

#------------------------------------------------------------
# Importing Modules

import datetime
dt = datetime.datetime.now()
time_stamp = dt.strftime("%d.%m.%Y_%H.%M.%S")

import sys
import subprocess
import os
import re
sys.path.append("/data/VMshare/github/pipeliners/modules")

import pipeliners



#------------------------------------------------------------
# Setting globals / functions

def cutadapt( infile, outfile):
	# Removes sequencing adapters
    return "/software/packages/cutadapt-1.1/bin/cutadapt -b TGTAGAACCATGTCGTCAGTGT -b AGACCAAGTCTCTGCTACCGT "  + infile  + " | gzip -c  > " + outfile

def smalt( adir, infile1, infile2, outfile):
    # Align the reads to the reference (run smalt-0.7.6 to see all options)
    return "cd " + adir + " ; /software/bin/smalt_0.7.6 map -f samsoft /refs/HIV/K03455_s1k6 " + infile1 + " " + infile2 + " > " + outfile

def sam_to_bam( adir, infile, outfile):
	# Converts samfile to bamfile 
	return "cd " + adir + " ; /software/bin//samtools view -Sb " + infile + " -o " + outfile

def sort_bamfile( adir, infile, outfile):
	# Sorts bamfile
	return "cd " + adir + " ; /software/bin/samtools sort " + infile + " " + outfile

def deduplicate_bamfile( adir, infile, outfile, outcsv):
	# Marks and soft clips duplicate reads
	return "cd " + adir + " ; /software/bin/picard -T MarkDuplicates I= " + infile + " O= " + outfile + " AS=true M= " + outcsv

def index_bamfile( adir, infile):
	# Index's the bam file so it can be viewed in IGV later on
	return "cd " + adir + " ; /software/bin/samtools index " + infile
	
def HIV_alignment_fix( adir, infile, outfile):
	# Fix's HIV specific alignment issues
	return "cd " + adir + " ; /software/packages/HIV-pipeline/scripts/bam_fix_indels.pl " + infile + " " + outfile

def unclip_bamfile( adir, infile):
	# Run's kims unclipping script
	return "cd " + adir + " ; /software/bin/scripts/bam_unclip_bases.pl " + infile


#------------------------------------------------------------
# Define fastq's and get sample names.
# Checks all argv's are present
if (len(sys.argv) == 2):
    print "Need's analysis directory name and sample directory path as input"
    exit()

# setup analysis directory
analysis_dir = sys.argv[1] + "_" + time_stamp
print "PLEASE NOTE! The output folder, containing your data, will be named - " + analysis_dir
os.makedirs(analysis_dir)
analysis_directory = analysis_dir + "/"

# setup directory containing fastq's and get them
indir = sys.argv[2]
for sample in os.listdir(indir):
	if sample.endswith(".1.fq.gz"):
		sample_name = re.sub(r"(.*).1.fq.gz", r"\1", sample)
		sample_name_uc = sample_name + "_unclipped"
	else:
		continue

# Preparation of bamfile + unclipped bamfile  
pipeliners.system_call('Cut Adapters', cutadapt(sample_name + ".1.fq.gz", analysis_directory + sample_name + "_ar.1.fq.gz"))
pipeliners.system_call('Cut Adapters', cutadapt(sample_name + ".2.fq.gz", analysis_directory + sample_name + "_ar.2.fq.gz"))
exit()

pipeliners.system_call('SMALT alignment', smalt(analysis_directory, sample_name + "_ar.1.fq.gz", sample_name + "_ar.2.fq.gz", sample_name + ".sam"))
pipeliners.system_call('Convert samfile to bamfile', sam_to_bam(analysis_directory, sample_name + ".sam", sample_name + ".bam"))

pipeliners.system_call('Unclipping bamfile', unclip_bamfile(analysis_directory, sample_name + ".bam"))

# Bamfile processing pipeline 
pipeliners.system_call('Sort the bamfile', sort_bamfile(analysis_directory, sample_name+ ".bam", sample_name + "_sorted"))
#pipeliners.system_call('Deduplicate bamfile', deduplicate_bamfile(sample_name + "_sorted.bam", sample_name + "_rmdups.bam", sample_name + "_rmdup.csv"))
pipeliners.system_call('Index bamfile', index_bamfile(analysis_directory, sample_name + "_sorted.bam"))
pipeliners.system_call('Fix HIV alignment', HIV_alignment_fix(analysis_directory, sample_name + "_sorted.bam", sample_name + "_fixed.bam"))
pipeliners.system_call('Index bamfile', index_bamfile(analysis_directory, sample_name + "_fixed.bam"))

# Bamfile_unclipped processing pipeline 
pipeliners.system_call('Sort the unclipped bamfile', sort_bamfile(analysis_directory, sample_name_uc+ ".bam", sample_name_uc + "_sorted"))
#pipeliners.system_call('Deduplicate unclipped bamfile', deduplicate_bamfile(sample_name_uc + "_sorted.bam", sample_name_uc + "_rmdups.bam", sample_name_uc + "_rmdup.csv"))
pipeliners.system_call('Index unclipped bamfile', index_bamfile(analysis_directory, sample_name_uc + "_sorted.bam"))
pipeliners.system_call('Fix HIV alignment (unclipped)', HIV_alignment_fix(analysis_directory, sample_name_uc + "_sorted.bam", sample_name_uc + "_fixed.bam"))
pipeliners.system_call('Index unclipped fixed bamfile', index_bamfile(analysis_directory, sample_name_uc + "_fixed.bam"))


exit()
