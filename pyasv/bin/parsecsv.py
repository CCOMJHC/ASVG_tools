#!/usr/bin/env python 
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 17:04:26 2016

@author: vschmidt

This script converts csv files extracted from ASV Global binary log files into 
.mat files usable by both MATLAB and python. 

"""

import _mypath
import asvlog
import sys
import os
import argparse
#import glob
import fnmatch

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--directory",
                    action = "store",
                    default = ".",
                    help = "Input log directory")
parser.add_argument("-x", "--dryrun",
                    action = "store_true",
                    default = False,
                    help = "Look for log files, don't parse or convert them.")
parser.add_argument("-v", "--verbosity",
                    action = "count",
                    default = 0,
                    help = "Specify verbosity, -v, -vv -vvv, etc.")
parser.add_argument("-o", "--outputdir",
                    action = "store",
                    default = ".",
                    help = "Specify the output directory for parsed MATLAB files. 'i' = put files in input log directory [default='.']")


# Get list of files to parse.
args = parser.parse_args()
directory =         args.directory
dryrun =            args.dryrun
verbose =           args.verbosity
outputdir =         args.outputdir

if directory.startswith('"') and directory.endswith('"'):
    directory = directory[1:-1]
if outputdir.startswith('"') and outputdir.endswith('"'):
    outputdir = outputdir[1:-1]

#filestoprocess = glob.glob(directory + '/*.csv')

# Recursively look for data files in the specified directory. 
csvfilestoprocess = []


if verbose >= 1:
    print("Arguments:")
    arguments = vars(args)
    for key, value in arguments.iteritems():
        print("\t%s:\t\t%s" % (key,str(value)))


######################### CSV LOGS #############################
for root, dirnames, filenames in os.walk(directory):
    for filename in fnmatch.filter(filenames,'*.csv'):
        csvfilestoprocess.append(os.path.join(root,filename))

# Process CSV data produced from the Data Export Tool.
for csvfile in csvfilestoprocess:

    print "Parsing " + csvfile
    # Define the asvlog object
    log = asvlog.asvlog.asvlog(csvfile)

    # Specify the output .mat file name.
    outmatfilename = os.path.basename(csvfile).replace('csv','mat')

    # Specify the output directory name.
    # Default is the cwd ('./'). -i gives the input directory. 
    if outputdir == 'i':
        outputdir = os.path.dirname(csvfile)
    
    try:
        if not dryrun:
            log.parse()
    except:
        statinfo = os.stat(csvfile)
        MB = statinfo.st_size / 1024 / 1024
        print "Failed parsing " + csvfile + " " + str(MB) +  " MB"
        continue
    # Save the data.
    print "Writing " + os.path.join(outputdir,outmatfilename)
    if not dryrun:
        log.save_to_mat(matfilename = os.path.join(outputdir,outmatfilename), verbosity=verbose )




