#!/bin/bash
#
# A script to shutdown mystique (linux box on CW4)

echo "Password: asvuser"
ssh -t asvuser@192.168.100.112 'sudo shutdown -h now'
