#!/usr/bin/env python 
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 17:04:26 2016

@author: vschmidt
"""

import _mypath
import asvlog
#import sys
import os
import argparse
import glob

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--directory",
                    action = "store",
                    default = ".",
                    help = "Log directory")
parser.add_argument("-x", "--dryrun",
                    action = "store_true",
                    default = False,
                    help = "Look for log files, don't parse or convert them.")
parser.add_argument("-v", "--verbosity",
                    action = "count",
                    default = 0,
                    help = "Specify verbosity, -v, -vv -vvv, etc.")


# Get list of files to parse.
args = parser.parse_args()
directory = args.directory
dryrun = args.dryrun
output_verbosity = args.verbosity

filestoprocess = glob.glob(directory + '/*.csv')

for csvfile in filestoprocess:
    
    print "Parsing " + csvfile
    log = asvlog.asvlog.asvlog(csvfile)
    
    if dryrun:
        continue

    try:    
        log.parse()
    except:
        statinfo = os.stat(csvfile)
        MB = statinfo.st_size / 1024 / 1024
        print "Failed parsing " + csvfile + " " + str(MB) +  " MB"
        continue
    log.save_to_mat(verbosity = output_verbosity)
    
    
    

