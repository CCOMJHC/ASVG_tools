#!/bin/bash
#
# A script to generate an export configuration file to dump most all logs from the C-Worker. 
# USAGE:
#
#    create_export_config <outputdirectory>
#
# outputdirectory = path to the directory into which the extracted data will be place. 

cat $HOME/bin/template_export_config.exs | sed s:OUTPUTDIR:$1:g
