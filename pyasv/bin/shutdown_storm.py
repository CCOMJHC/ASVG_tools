#!/usr/bin/env python

import socket as S

s = S.socket(S.AF_INET,S.SOCK_DGRAM)
# Shutdown
s.sendto("SHUTDOWN",('stormc',9999))
