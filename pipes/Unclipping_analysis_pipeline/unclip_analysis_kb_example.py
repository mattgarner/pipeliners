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







# Mark/remove duplicate reads
deduplicate_bamfile = "/software/bin/picard -T MarkDuplicates I= " + analysis_dir + sample_name + "_sorted.bam O= " + analysis_dir + sample_name + "_rmdups.bam AS=true M=" + analysis_dir + sample_name + "_rmdup.csv"

# Index the bam file so it can be viewed in IGV later on
index = "/software/bin/samtools index " + analysis_dir + sample_name + "_rmdups.bam"

# HIV alignment fix
alignment_fixing_HIV = "/software/packages/HIV-pipeline/scripts/bam_fix_indels.pl " + analysis_dir + sample_name + "_rmdups.bam " + analysis_dir + sample_name + "_fixed.bam"

# Index the new bam file so it can be viewed in IGV later on
index_fix = "/software/bin/samtools index " + analysis_dir + sample_name + "_fixed.bam"

# Run unclip bamfile
unclip_bamfile = "/software/bin/scripts/bam_unclip_bases.pl " + analysis_dir + sample_name + ".bam"

#------------------------------------------------------------
#------------------------------------------------------------
# Sort the unclipped bamfile with samtools
sort_bam_2 = "/software/bin/samtools sort " + analysis_dir + sample_name_unclipped + ".bam " + analysis_dir + sample_name_unclipped + "_sorted"

# Mark/remove duplicate reads
deduplicate_bamfile_2 = "/software/bin/picard -T MarkDuplicates I= " + analysis_dir + sample_name_unclipped + "_sorted.bam O= " + analysis_dir + sample_name_unclipped + "_rmdups.bam AS=true M=" + analysis_dir + sample_name_unclipped + "_rmdup.csv"

# Index the bam file so it can be viewed in IGV later on
index_2 = "/software/bin/samtools index " + analysis_dir + sample_name_unclipped + "_rmdups.bam"

# HIV alignment fix
alignment_fixing_HIV_2 = "/software/packages/HIV-pipeline/scripts/bam_fix_indels.pl " + analysis_dir + sample_name_unclipped + "_rmdups.bam " + analysis_dir + sample_name_unclipped + "_fixed.bam"

# Index the new bam file so it can be viewed in IGV later on
index_fix_2 = "/software/bin/samtools index " + analysis_dir + sample_name_unclipped + "_fixed.bam"

# Run unclip bamfile
unclip_bamfile_2 = "/software/bin/scripts/bam_unclip_bases.pl " + analysis_dir + sample_name_unclipped + ".bam"



#------------------------------------------------------------
# Make directory
#system_call("DIRECTORY", make_analysis_directory)

# Process raw fastq files
#system_call("DE-ADAPT2", remove_adapters_2)
#system_call("DE-ADAPT1", remove_adapters_1)

# Align to reference
#system_call("SMALT ALIGNMENT", smalt)
system_call("samfile > bamfile", sam_to_bam)
# Regular pipeline
system_call("sort_bam_1", sort_bam_1)   
system_call("deduplicate_bamfile", deduplicate_bamfile)
system_call("index", index)
system_call("HIV_fix", alignment_fixing_HIV)
system_call("Index fixed", index_fix)

# Unclip bamfile and proceed with rest of analysis 
system_call("unclip", unclip_bamfile)
# Rest of pipeline
system_call("sort_bam_2", sort_bam_2)   
system_call("deduplicate_bamfile2", deduplicate_bamfile_2)
system_call("index2", index_2)
system_call("HIV_fix2", alignment_fixing_HIV_2)
system_call("Index fixed2", index_fix_2)
#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
