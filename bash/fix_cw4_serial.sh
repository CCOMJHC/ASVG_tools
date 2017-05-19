#!/bin/bash
#
# For an unknown reason, a loss of power the the linux computer can sometimes cause 
# the digi driver's serial server configuration to be corrupted and lost. When this 
# happens all serial communications will be lost - GPS, heading, on the boat, UHF
# communications on the OTB. 
#
# These lines will reconfigure the system for the boat.
# 
# Val Schmidt
# Center for Coastal and Ocean Mapping
# University of New Hampshire
# 2017

# Control container port server
sudo /usr/bin/dgrp/config/dgrp_cfg_node init  -v -v -e never aa 192.168.10.40 4

# Mast box port server
sudo /usr/bin/dgrp/config/dgrp_cfg_node init  -v -v -e never bb 192.168.10.41 4
