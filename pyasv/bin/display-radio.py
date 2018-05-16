#!/usr/bin/env python

import urllib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import json
import datetime

plotwindowhours = 6

radio_url = 'http://unmanned:unmanned@192.168.100.51/status.json'

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

needsInit = True
plots = {}

def updatePlot(pl,data,ts):
    pl.set_xdata(np.append(pl.get_xdata(), ts))
    pl.set_ydata(np.append(pl.get_ydata(), data))

def getItem(data,path):
    if len(path) == 1:
        return data[path[0]]
    return getItem(data[path[0]],path[1:])

while True:
    c = urllib.urlopen(radio_url)
    data = json.loads(c.read())
    now = datetime.datetime.utcnow()
    plotwindowstart = now-datetime.timedelta(plotwindowhours/24.0)
    plotwindowend = now + datetime.timedelta(1/24.0)
    if needsInit:
        for di in data_items:
            if di[0] == "snr 8" or di[0] == "snr 7":
                datapoint = getItem(data,di[1])/10
            else:
                datapoint = getItem(data,di[1])
            #plots[di[0]], = plt.plot([now,], [getItem(data,di[1]),],label=di[0])
            plots[di[0]], = plt.plot([now,], [datapoint,],label=di[0])
        plt.legend(loc='best')
        needsInit = False
    else:
        for di in data_items:
            if di[0] == "snr 8" or di[0] == "snr 7":
                datapoint = getItem(data,di[1])/10
            else:
                datapoint = getItem(data,di[1])
            updatePlot(plots[di[0]], datapoint, now)

    plt.axis([plotwindowstart, plotwindowend, -100, 50])
    plt.grid(True)
    plt.pause(1.0)


#data_buffer = []

#fig, ax = plt.subplots()
#line, = ax.plot(np.random.rand(10))
#ax.set_ylim(0, 1)


#def update(data):
    #line.set_ydata(data)
    #return line,


#def data_gen():
    #while True:
        #global data_buffer
        #while len(data_buffer) < 11:
            #data_buffer.append(np.random.rand(1))
        #data_buffer = data_buffer[-10:]
        #yield data_buffer

#ani = animation.FuncAnimation(fig, update, data_gen, interval=1000)
#plt.show()
