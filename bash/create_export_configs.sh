#!/bin/bash
#
# A script to generate an export configuration file to dump most all logs from the C-Worker. 
# USAGE:
#
#    create_export_config <outputdirectory>
#
# outputdirectory = path to the directory into which the extracted data will be place. 

# THIS NEEDS TO BE AN ENV VARIABLE
TEMPLATEDIR=/home/unmanned/gitsrc/ASVG_tools/bash/

cat $TEMPLATEDIR/template_engine_export_config.exs | \
	sed s:OUTPUTDIR:$1:g > engine_export_config.exs
cat $TEMPLATEDIR/template_payload_export_config.exs | \
	sed s:OUTPUTDIR:$1:g > payload_export_config.exs
cat $TEMPLATEDIR/template_pilot_export_config.exs | \
	sed s:OUTPUTDIR:$1:g > pilot_export_config.exs
cat $TEMPLATEDIR/template_vehiclestate_export_config.exs | \
	sed s:OUTPUTDIR:$1:g > vehiclestate_export_config.exs
cat $TEMPLATEDIR/template_vehicle_export_config.exs | \
	sed s:OUTPUTDIR:$1:g > vehicle_export_config.exs
cat $TEMPLATEDIR/template_vehicle_processor_export_config.exs | \
	sed s:OUTPUTDIR:$1:g > vehicle_processor_export_config.exs
cat $TEMPLATEDIR/template_vs_remote_control_export_config.exs | \
	sed s:OUTPUTDIR:$1:g > vs_remote_control_export_config.exs
