#!/bin/bash

source ~/.bashrc

dts=$(date -u "+%Y-%m-%dT%H-%M-%S")
filename="/tmp/snap_{dts}.png"
import -window root ${filename}
#socat gopen:snap_${dts}.png udp-sendto:localhost:8888
