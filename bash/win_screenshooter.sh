#!/bin/bash
#
# screenshooter.sh
#
# A script to take screenshots at regular intervals.
# 
# Val Schmidt
# Center for Coastal and Ocean Mapping
# University of New Hampshire
# Copyright 2018

source /etc/profile
source /home/field/.profile

INTERVAL=60


/usr/bin/clear
# Create the log directory name for initial display
DAY=$(date -u "+%Y-%m-%d")
LOGDIR=~/data/other/screenshooter_${DAY}

# Display status
echo "--- SCREENSHOOTER ACTIVE ---"
echo "LOGDIR: $LOGDIR"
echo "INTERVAL: ${INTERVAL}s"
SPACE=(`df -kh | grep home`)
echo "SPACE AVAILABLE: ${SPACE[3]}"
echo "CTRL-C to Quit."
echo "OPTIONALLY, ENTER NEW INTERVAL: [RET]"

# Loop
while [ 1 ] ; do
    # Create the log directory
    DAY=$(date -u "+%Y-%m-%d")
    LOGDIR=~/data/other/screenshooter_${DAY}
    if [ ! -e $LOGDIR ]; then
        mkdir -p $LOGDIR
    fi
    
    # Take the screen shot
    dts=$(date -u "+%Y-%m-%dT%H-%M-%S")
    filename="${dts}_screenshot.png"
    #import -silent -window root ${filename}
    cd ${LOGDIR} 
    nircmdc savescreenshotfull ${filename}

    # Could use socat to make these available to ROS elsewhere.
    #socat gopen:snap_${dts}.png udp-sendto:localhost:8888
    #socat gopen:${filename} udp-sendto:localhost:8888

    # Optionally read in a new interval and update
    read -t $INTERVAL reply && INTERVAL=${reply}
    # No faster than 1 every 5 seconds to protect PC.
    if [ ${INTERVAL} -lt 5 ]; then 
        INTERVAL=5
    fi
    clear
    echo "--- SCREENSHOOTER ACTIVE ---"
    echo "LOGDIR: $LOGDIR"
    echo "INTERVAL: ${INTERVAL}s"
    SPACE=(`df -kh | grep home`)
    echo "SPACE AVAILABLE: ${SPACE[3]}"
    echo "CTRL-C to Quit."
    echo "OPTIONALLY, ENTER NEW INTERVAL: [RET]"
     
done
