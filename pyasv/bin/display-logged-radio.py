#!/usr/bin/env python

import sys
import numpy as np
import matplotlib.pyplot as plt
import time
import json
import datetime

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

def getItem(data,path):
    if len(path) == 1:
        return data[path[0]]
    return getItem(data[path[0]],path[1:])


infile = open(sys.argv[1])
newline = True
jsonbuffer = ''

times = []
datasets = {}

for di in data_items:
    datasets[di[0]]=[]

for l in infile.readlines():
    if newline:
        ts,l = l.split(',',1)
        ts = datetime.datetime.strptime(ts,"%Y-%m-%dT%H:%M:%S.%f")
        newline = False
    if len(l.strip()) == 0:
        data = json.loads(jsonbuffer)
        times.append(ts)
        for di in data_items:
            datasets[di[0]].append(getItem(data,di[1]))
        newline = True
        jsonbuffer = ''
    else:
        jsonbuffer += l

for di in data_items:
    plt.plot(times,datasets[di[0]],label=di[0])

plt.legend()
plt.show()
