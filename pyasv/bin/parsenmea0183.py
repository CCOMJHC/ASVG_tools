#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 06:24:47 2016

@author: vschmidt

REQUIRES unix commands cat and strings.
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
parser.add_argument("-l",'--log_device',
                    action = "store",
                    default = 'a',
                    help = 'Device index to parse (e.g. #.nmea0183)')
                    
# Get list of files to parse.
args = parser.parse_args()
directory =         args.directory
dryrun =            args.dryrun
verbose =           args.verbosity
outputdir =         args.outputdir
log_device =        args.log_device.split(',')


########################## NMEA 0183 ##################################        
GPStypestoparse = ['GGA','RMC','VTG'] # Not currently parsing GSV or GLL
NMEA_Devices = ['3','6']  # Hard coded options here. 3 is factory GPS, 6 is POSMV

# Handle manually specified device to parse.
if log_device[0] == 'a':
    devices_to_parse = NMEA_Devices
else:
    devices_to_parse = log_device
    

thisdir = os.path.dirname(__file__)
gpsparser = os.path.join(thisdir,'../lib/gpsparser/gpsparser/gpsparser.py')

# Specify the output directory name.
# Default is the cwd ('./'). -i gives the input directory. 
# Note the grep removes non-ASCII characters, which come with the AIS logs.
# NOTE: Device 3 is the onboard GPS.
for device in devices_to_parse:
    for logtype in GPStypestoparse:
        cmd = ('/bin/cat ' + os.path.join(os.path.join(directory,'device'),'*' + device + '.nmea0183') 
               + ' | strings | ' + gpsparser + ' -s ' + logtype + ' -o ' + 
               os.path.join(outputdir,logtype + '.txt'))
               #cmd = ('/bin/cat ' + os.path.join(os.path.join(directory,'device'),'*nmea0183') 
               #       + ' | perl -pe \'s/[^[:ascii:]]//g\' | ' + gpsparser + ' -s ' + logtype + ' -o ' + 
               #       os.path.join(outputdir,logtype + '.txt'))
               
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
            
