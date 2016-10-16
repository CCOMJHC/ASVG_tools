#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 06:24:47 2016

@author: vschmidt
"""

import _mypath
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
                    help = "Specify the output directory for parsed MATLAB files. [default='.']")

# Get list of files to parse.
args = parser.parse_args()
directory =         args.directory
dryrun =            args.dryrun
verbose =           args.verbosity
outputdir =         args.outputdir

########################## NMEA 0183 ##################################        
GPStypestoparse = ['GGA','RMC','VTG'] # Not currently parsing GSV or GLL

thisdir = os.path.dirname(__file__)
gpsparser = os.path.join(thisdir,'../lib/gpsparser/gpsparser/gpsparser.py')
# Specify the output directory name.
# Default is the cwd ('./'). -i gives the input directory. 
# Note the grep removes non-ASCII characters, which come with the AIS logs.
for logtype in GPStypestoparse:
    cmd = ('/bin/cat ' + os.path.join(os.path.join(directory,'device'),'*nmea0183') 
           + ' | perl -pe \'s/[^[:ascii:]]//g\' | ' + gpsparser + ' -s ' + logtype + ' -o ' + 
           os.path.join(outputdir,logtype + '.txt'))
    #cmd = (gpsparser + 
    #       ' -g ' + os.path.join(directory,'device') + '::nmea0183' +
    #' -s ' + logtype + ' -o ' + outputdir)
   
    if verbose >= 1:
        print "Executing: " + cmd
        
    if not dryrun:
        try:
            os.system(cmd)
        except:
            print "Failed executing: " + cmd
            
