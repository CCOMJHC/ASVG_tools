#!/bin/bash

# This must be run as root and only works for the "vs", in the 
# operator's telemetry box. 

sudo /usr/bin/dgrp/config/dgrp_cfg_node init -v -e never aa 192.168.50.40 4
