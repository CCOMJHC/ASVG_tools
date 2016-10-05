#!/usr/bin/python

import sys
import datetime

for line in sys.stdin:
    dts = datetime.datetime.utcnow().isoformat()
    print dts +'\t' + line
