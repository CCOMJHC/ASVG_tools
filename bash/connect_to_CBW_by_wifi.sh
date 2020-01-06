#!/bin/bash

ssh -t field@mystiquew 'socat TCP-LISTEN:20080,fork TCP:192.168.100.212:80'
echo "Connect to CBW with: http://192.168.101.112:20080"

