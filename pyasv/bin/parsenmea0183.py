# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 06:24:47 2016

@author: vschmidt
"""

import _mypath
import sys
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--directory",
                    action = "store",
                    default = ".",
                    help = "CCSCM/scm-vp/directory")
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

########################## NMEA 0183 ##################################        
GPStypestoparse = ['GGA','RMC','VTG'] # Not currently parsing GSV or GLL

# Specify the output directory name.
# Default is the cwd ('./'). -i gives the input directory. 
if outputdir == 'i':
    outputdir = os.path.join(directory,'device')

for logtype in GPStypestoparse:
    cmd = ('gpsparser.py ',
           ' -d ' + os.path.join(directory,'device') + '::.nmea0183',
    ' -s ' + logtype + ' -o ' + outputdir)
   
    if verbose > 1:
        print "Executing: " + cmd

    try:
        os.system(cmd)
    except:
        print "Failed executing: " + cmd