#!/usr/bin/env python
#
# A script to facilitate shutdown of windows systems.
# Run this on the windows system as a daemon. Then 
# send it SHUTDOWN via UDP and the system will be shutdown.
# This would be a severe security risk in any other environment.
# but it circumvents the odd Windows permissions requirements
# in modern systems.
#
# Val Schmidt
# Center for Coastal and Ocean Mapping
# University of New Hampshire
#

import socket as S
import os
import time

s = S.socket(S.AF_INET,S.SOCK_DGRAM)
s.bind(("stormc",9999))

data,addr = s.recvfrom(1024)
if data == 'SHUTDOWN':
    time.sleep(1)    
    s.sendto('GOING DOWN',('192.168.100.255',9999))
    os.system('shutdown -h now')
