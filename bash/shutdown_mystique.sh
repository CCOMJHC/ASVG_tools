#!/bin/bash
#
# A script to shutdown mystique (linux box on CW4)

echo "Password for field: "
ssh -t field@192.168.100.112 'sudo shutdown -h now'
