#!/bin/bash
#
# A script to generate an export configuration file to dump most all logs from the C-Worker. 
# USAGE:
#
#    create_export_config <outputdirectory>
#
# outputdirectory = path to the directory into which the extracted data will be place. 

#ASVG_TOOLS="/home/asvuser/gitsrc/ASVG_tools"
TEMPLATE="$ASVG_TOOLS/bash/template_export_config_7p1.exs"
DIR=`realpath $1`
cat $TEMPLATE | sed s:OUTPUTDIR:$DIR:g
