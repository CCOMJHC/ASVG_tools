#!/usr/bin/env python

import sys
import datetime
import HTMLParser
import matplotlib.pyplot as plt

headers = ('MAC Address','Noise Floor (dBm)','SNR (dB)','RSSI (dBm)','TX CCQ (%)','RX CCQ (%)','TX Rate','RX Rate','Signal Level')

datasets = {}

class WifiStatusParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.state = None
        self.dataValues = []
    
    def handle_starttag(self, tag, attrs):
        #print self.state
        #print "Encountered a start tag:", tag
        if self.state == 'inConnectionStatus':
            if tag == 'tr':
                self.state = 'preData'
        elif self.state == 'preData':
            if tag == 'tr':
                self.state = 'inData'
                self.dataValues.append([])
        elif self.state == 'inData':
            if tag == 'td':
                self.state = 'intd'
                

    def handle_endtag(self, tag):
        #print "Encountered an end tag :", tag
        if self.state == 'inData':
            if tag == 'tr':
                #print 'DATA:',self.dataValues[-1]
                self.state = 'preData'
                
        if self.state == 'intd':
            if tag == 'td':
                self.state = 'inData'
                

    def handle_data(self, data):
        #print "Encountered some data  :", data
        if self.state is None and data == 'Connection Status':
            self.state = 'inConnectionStatus'
        if self.state == 'intd':
            self.dataValues[-1].append(data)


def processHtml(data,ts):
    parser = WifiStatusParser()
    parser.feed(data)
    #print ts,parser.dataValues
    global datasets
    for dv in parser.dataValues:
        if not dv[0] in datasets:
            datasets[dv[0]] = {'times':[]}
            for h in headers:
                datasets[dv[0]][h]=[]
        datasets[dv[0]]['times'].append(ts)
        for i in range(1,len(headers)):
            if ' ' in dv[i]:
                value = float(dv[i].split()[0])
            elif '%' in dv[i]:
                value = float(dv[i][:-1])
            else:
                value = float(dv[i])
            datasets[dv[0]][headers[i]].append(value)
            
        

htmlbuffer = None

for l in open(sys.argv[1]).readlines():
    if ',' in l:
        ts,rest = l.split(',',1)
        try:
            ts = datetime.datetime.strptime(ts,"%Y-%m-%dT%H:%M:%S.%f")
            if htmlbuffer is not None:
                processHtml(htmlbuffer,ts)
            htmlbuffer = ''
            l = rest
        except ValueError:
            pass
    htmlbuffer += l
    
#print datasets

for mac in datasets.keys():
    print mac
    ds = datasets[mac]
    plt.figure()
    plt.title(mac)
    for i in range(1,len(headers)):
        plt.plot(ds['times'],ds[headers[i]],label=headers[i])
    plt.legend()
    
plt.show()
