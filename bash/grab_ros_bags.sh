#!/bin/bash

# Val Schmidt
# Center for Coastal and Ocean Mapping
# University of New Hampshire
# 2017

# TO DO:
# Add the ability to get all logs, logs for a range of dates, or just for today.
RSYNC=/usr/bin/rsync
if [ -e ~/.ASVG_tools.conf ]; then
        source ~/.ASVG_tools.conf
else
        echo "Unable to config .ASVG_tools.conf in home directory."
        exit
fi


if [ ! -e "${ASVG_CW4LOGDIR}" ]; then
	mkdir -p "${ASVG_CW4LOGDIR}"
fi 

$RSYNC -rav field@mystiquec:rosbags ${ASVG_CW4LOGDIR}
