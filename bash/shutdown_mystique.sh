#!/bin/bash
#
# A script to shutdown mystique (linux box on CW4)

echo "SHUTTING DOWN MYSTIQUE (Linux PC)"
echo "Connecting.... password: asvuser"
ssh -t asvuser@192.168.100.112 'sudo shutdown -h now'

