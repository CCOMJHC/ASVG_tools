#!/usr/type/env python

# Val Schmidt
# Center for Coastal and Ocean Mapping
# University of New Hampshire
# 2017


import datetime as dt
import url
import json
import requests
from requests.auth import HTTPBasicAuth

payload = {'user':'unmanned','password':'unmanned'}
r = requests.get("http://192.168.100.51/status.json",auth=("unmanned","unmanned"))

data = r.json()

