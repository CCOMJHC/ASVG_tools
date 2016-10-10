#!/bin/bash
#
# A script to generate an export configuration file to dump most all logs from the C-Worker. 
# USAGE:
#
#    create_export_config <outputdirectory>
#
# outputdirectory = path to the directory into which the extracted data will be place. 

TEMPLATE=/home/unmanned/gitsrc/ASVG_tools/bash/template_export_config.exs
cat $TEMPLATE | sed s:OUTPUTDIR:$1:g
