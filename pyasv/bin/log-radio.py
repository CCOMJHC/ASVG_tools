#!/usr/bin/env python

import urllib
import time
import datetime

radio_url = 'http://unmanned:unmanned@192.168.100.51/status.json'

while True:
    c = urllib.urlopen(radio_url)
    data = c.read()
    print datetime.datetime.utcnow().isoformat()+','+data

    time.sleep(1)

