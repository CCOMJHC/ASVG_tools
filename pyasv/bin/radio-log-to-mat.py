#!/usr/bin/env python
#
# Roland Arsenault and Val Schmidt
# Center for Coastal and Ocean Mapping
# University of New Hampshire

import sys
import time
import json
import datetime
import numpy as np
import scipy.io

if sys.argv[1] == '-h':
	print('Usage:')
	print('   radio-log-to-mat.py <radio_log_file.log>')
	print('Produces: radio_log_file.mat')

# This dictionary defines the fields of interest to extract.
data_items = (
        ('snr 7',('remoteStatus',7,'demodStatus','snr',8)),
        ('sigLevA 7',('remoteStatus',7,'demodStatus','sigLevA',8)),
        ('sigLevB 7',('remoteStatus',7,'demodStatus','sigLevB',8)),
        ('sigLevA0 7',('remoteStatus',7,'demodStatus','sigLevA0')),
        ('sigLevB0 7',('remoteStatus',7,'demodStatus','sigLevB0')),
        ('snr 8',('remoteStatus',8,'demodStatus','snr',7)),
        ('sigLevA 8',('remoteStatus',8,'demodStatus','sigLevA',7)),
        ('sigLevB 8',('remoteStatus',8,'demodStatus','sigLevB',7)),
        ('sigLevA0 8',('remoteStatus',8,'demodStatus','sigLevA0')),
        ('sigLevB0 8',('remoteStatus',8,'demodStatus','sigLevB0')),
    )

# This method will dig into the data structure to extract the desired field. 
def getItem(data,path):
    if len(path) == 1:
        return data[path[0]]
    return getItem(data[path[0]],path[1:])

# Open the file and set up some variables. 
infile = open(sys.argv[1])
newline = True
jsonbuffer = ''

datasets = {}
sigdata = {}
datasets = {'times':[]}

for di in data_items:
    datasets[di[0]]=[]

alldata = {}

# Read the log file. The log file is simply a sequential list of time stamps followed by
# a JSON formatted block. Each line is considered in turn below, extracting the timestamp 
# and then line by line building the data block until the end of the data block is 
# reached.  The fields of interest are then extracted from the data block and appended
# to the datasets dictionary by their key as defined  above. 
for l in infile.readlines():
    if newline:
        ts,l = l.split(',',1)
        ts = datetime.datetime.strptime(ts,"%Y-%m-%dT%H:%M:%S.%f")
        newline = False
    if len(l.strip()) == 0:
        data = json.loads(jsonbuffer)
        #if alldata.__len__() == 0:
       	# 	for k,v in data.items():
       	# 		alldata[k] = []
        #for k,v in data.items():
        #	alldata[k].append(v)
        datasets['times'].append(time.mktime(ts.timetuple()))
        try:
        	for di in data_items:
	        	datasets[di[0]].append(getItem(data,di[1]))
    	except:
    		# If there was a failure extracting a field, abort and remove the associated 
    		# time stamp. This requires a full data set every time.
    		ts_reject = datetime.datetime.fromtimestamp(datasets['times'].pop())
    		print('Failed parsing a data item at ' + ts_reject.isoformat() + ' Moving on.')
    		
    		
        newline = True
        jsonbuffer = ''
    else:
        jsonbuffer += l

# Initialize data.
dd = {}
# Fix the field names to something understandable. 
for k in datasets.keys():
	dd[k.replace(' ','')]=np.array(datasets[k],dtype='double')

dd['metadata']=['Each radio in the Cobham IP radio is identified by number.',
'    BASE: 7',
'    CW4:  8',
'Each radio has two receive antennas, A and B.',
'',
'SNR7/8         8 bit integers give a qualitative SNR value.',
'sigLevelA07    Self noise level of the BASE radio (7), on Rcv channel A',
'sigLevelB07    Self noise level of the BASE radio (8), on Rcv channel B',
'sigLevelB08    Self noise level of the BASE radio (8), on Rcv channel B',
'sigLevelB08    Self noise level of the BASE radio (8), on Rcv channel B',
'sigLevA7       Signal level recvied by the BASE radio on channel A.',
'sigLevB7       Signal level recvied by the BASE radio on channel B.',
'sigLevA8       Signal level recvied by the CW4 radio on channel A.',
'sigLevA8       Signal level recvied by the CW4 radio on channel B.']
 
# Set-up for saving to a MATLAB structure. 
sigdata['cobham']=dd
# Save the data. 
scipy.io.savemat(sys.argv[1].replace('log','mat'),sigdata, oned_as='column')
