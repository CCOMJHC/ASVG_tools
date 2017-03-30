#!/bin/bash
#
# This script executes a 'socat' command on the vp allowing forwarding of 
# browser traffic to the flir camera. 

echo "Setting up connection to FLIR. Enter password at prompts."
echo "Connect to FLIR on http://192.168.100.10:9000
ssh -e sudo socat TCP-LISTEN:9000,fork TCP:192.168.10.60:80

