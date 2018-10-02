#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 06:24:47 2016

@author: vschmidt
"""

import _mypath
import sys
import os
import argparse
import fnmatch
import pandas as pd

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--directory",
                    action = "store",
                    default = ".",
                    help = "CCSCM/scm-vp/directory")
parser.add_argument("-x", "--dryrun",
                    action = "store_true",
                    default = False,
                    help = "Look for log files, don't parse or convert them.")
parser.add_argument("-v", "--verbosity",
                    action = "count",
                    default = 0,
                    help = "Specify verbosity, -v, -vv -vvv, etc.")
parser.add_argument("-o", "--outputdir",
                    action = "store",
                    default = ".",
                    help = "Specify the output directory for parsed MATLAB files. 'i' = put files in input log directory [default='.']")
parser.add_argument("-t", "--type",
                    action = "store",
                    default = "all",
                    help = "Specify the type of logs to parse [default=all]")

# Get list of files to parse.
args = parser.parse_args()
directory =         args.directory
dryrun =            args.dryrun
verbose =           args.verbosity
outputdir =         args.outputdir
type =              args.type

if verbose >= 1:
    print("Arguments:")
    arguments = vars(args)
    for key, value in arguments.iteritems():
        print("\t%s:\t\t%s" % (key,str(value)))

###################### NMEA 2000 #################################    
# A list of the NMEA 2000 log types supported by the ASV Global readnmea2000 tool
# which extract logs from their proprietary log file format. 
nmea2000logtypes = ['paramGroup',
'pgn126992',
'pgn126996',
'pgn127250',
'pgn127251',
'pgn127257',
'pgn127258',
'pgn127488',
'pgn127489',
'pgn127493',
'pgn127497',
'pgn127505',
'pgn127506',
'pgn127508',
'pgn128259',
'pgn128267',
'pgn128275',
'pgn129025',
'pgn129026',
'pgn129029',
'pgn129033',
'pgn129540',
'pgn130306',
'pgn130310',
'pgn130311',
'pgn130312',
'pgn130313',
'pgn130314',
'pgn130316',
'pgn59904',
'pgn60928',
]

# The text title of each pgn code listed above. Note the list above is
# not the complete list, but rather the complete list supported by the
# ASV Global readnmea2000 tool.  
nmea2000logsummary = ['parameters',
'system_time',
'product_info',
'vessel_heading',
'rate_of_turn',
'attitude',
'magnetic_variation'
'engine_parameters',
'engine_parameters_dynamic',
'transmission_parameters_dynamic',
'trip_parameters_engine',
'fluid_level',
'dc_detailed_status',
'battery_status',
'speed_water_referenced',
'water_depth',
'distance_log',
'position_rapid_update',
'cog_sog_rapid_update',
'attitude_delta_high_precision_rapid_update',
'gnss_position_data',
'date_time',
'gnss_sats_in_view',
'wind_data',
'environmental_parameters_1',
'environmental_parameters_2',
'temperature',
'humidity',
'actual_pressure',
'unknown'
'iso_request',
'iso_address_claim'
]

# Below are lists of the fields available for each of the log types above.
nmea2000fieldnames = [	["log_timestamp","log_date","log_time","CAN_data",
                        "CAN_data_size","pgn","source", "priority",
                        "destination"],

	["log_timestamp","log_date","log_time","sequence_id","time_source","day",
          "time_of_day","timestamp","CAN_data","CAN_data_size","pgn","source",
          "priority","destination"],

	["log_timestamp","log_date","log_time","database_version","product_code",
      "model_id","software_version","model_version","model_serial",
      "certification_level","load_equivalency","CAN_data","CAN_data_size",
      "pgn","source","priority","destination"],
      
	["log_timestamp","log_date","log_time","sequence_id",
      "heading_sensor_reading","deviation","variation",
      "heading_sensor_reference","CAN_data","CAN_data_size","pgn","source",
      "priority","destination"],

	["log_timestamp","log_date","log_time","sequence_id","rate_of_turn",
      "CAN_data","CAN_data_size","pgn","source","priority","destination"],

	["log_timestamp","log_date","log_time","sequence_id","yaw","pitch",
      "roll","CAN_data","CAN_data_size","pgn","source","priority",
      "destination"],

	["log_timestamp","log_date","log_time","sequence_id",
      "variation_source","age_of_service","variation","CAN_data",
      "CAN_data_size","pgn","source","priority","destination"],

	["log_timestamp","log_date","log_time","engine_instance","engine_speed",
      "engine_boost_pressure","engine_tilt","CAN_data","CAN_data_size","pgn",
      "source","priority","destination"],

	["log_timestamp","log_date","log_time","engine_instance",
      "engine_oil_pressure","engine_oil_temperature","engine_temperature",
      "alternator_potential","fuel_rate","total_engine_hours",
      "engine_coolant_pressure","fuel_pressure","engine_tilt","check_engine",
      "over_temperature","low_oil_pressure"],
      
      ["log_timestamp","log_date","log_time","transmission_instance",
      "transmission_gear","transmission_oil_pressure",
      "transmission_oil_temperature","check_temperature","over_temperature",
      "low_oil_pressure","low_oil_level","sail_drive","CAN_data",
      "CAN_data_size","pgn","source","priority","destination"],
      
      ["log_timestamp","log_date","log_time","instance","trip_fuel_used",
      "average_fuel_rate","economy_fuel_rate","inst_fuel_economy","CAN_data",
      "CAN_data_size","pgn","source","priority","destination"],

	["log_timestamp","log_date","log_time","fluid_instance","fluid_type",
      "fluid_level","tank_capacity","CAN_data","CAN_data_size","pgn","source",
      "priority","destination"],

	["log_timestamp","log_date","log_time","sequence_id","dc_instance",
      "dc_type","state_of_charge","state_of_health","time_remaining",
      "ripple_voltage","cumulative_charge_drawn","CAN_data","CAN_data_size",
      "pgn","source","priority","destination"],
      
	["log_timestamp","log_date","log_time","battery_instance",
      "battery_voltage","battery_current","battery_case_temperature",
      "sequence_id","CAN_data","CAN_data_size","pgn","source","priority",
      "destination"],

	["log_timestamp","log_date","log_time","sequence_id","water_speed",
      "ground_speed","referenced_type","speed_direction","CAN_data",
      "CAN_data_size","pgn","source","priority","destination"],

	["log_timestamp","log_date","log_time","sequence_id",
      "transducer_water_depth","transducer_offset","maximum_depth_range",
      "CAN_data","CAN_data_size","pgn","source","priority","destination"],

	["log_timestamp","log_date","log_time","measurement_day",
      "measurement_time_of_day","cumulative_distance","distance_since_reset",
      "CAN_data","CAN_data_size","pgn","source","priority","destination"],

	["log_timestamp","log_date","log_time","latitude","longitude",
      "CAN_data","CAN_data_size","pgn","source","priority","destination"],

	["log_timestamp","log_date","log_time","sequence_id","cog_reference",
      "course_over_ground","speed_over_ground","CAN_data","CAN_data_size",
      "pgn","source","priority","destination"],

	["log_timestamp","log_date","log_time","sequence_id","timestamp",
      "date","time","position_day","position_time_of_day","latitude",
      "longitude","altitude","system_type","gnss_method","gnss_integrity",
      "space_vehicles","horizontal_dop","positional_dop","geoidal_separation",
      "reference_stations","CAN_data"],
      
	["log_timestamp","log_date","log_time","timestamp","date","time","day",
      "time_of_day","local_time_offset","CAN_data","CAN_data_size","pgn",
      "source","priority","destination"],

	["log_timestamp","log_date","log_time","sequence_id","residual_mode"
     ,"space_vehicles","CAN_data","CAN_data_size","pgn","source","priority",
     "destination"],

	["log_timestamp","log_date","log_time","sequence_id","wind_speed",
      "wind_direction","wind_reference","CAN_data","CAN_data_size","pgn",
      "source","priority","destination"],

	["log_timestamp","log_date","log_time","sequence_id",
      "water_temperature","ambient_temperature","atmospheric_pressure",
      "CAN_data","CAN_data_size","pgn","source","priority","destination"],

	["log_timestamp","log_date","log_time","sequence_id",
      "temperature_instance","humidity_instance","temperature",
      "humidity","atmospheric_pressure","CAN_data","CAN_data_size","pgn",
      "source","priority","destination"],

	["log_timestamp","log_date","log_time","sequence_id",
      "temperature_instance","temperature_source","actual_temperature",
      "control_temperature","CAN_data","CAN_data_size","pgn","source",
      "priority","destination"],

	["log_timestamp","log_date","log_time","sequence_id",
      "humidity_instance","humidity_source","actual_humidity",
      "control_humidity","CAN_data","CAN_data_size","pgn","source",
      "priority","destination"],

	["log_timestamp","log_date","log_time","sequence_id",
      "pressure_instance","pressure_source","pressure","CAN_data",
      "CAN_data_size","pgn","source","priority","destination"],

	["log_timestamp","log_date","log_time","sequence_id",
      "temperature_instance","temperature_source","actual_temperature",
      "control_temperature","CAN_data","CAN_data_size","pgn","source",
      "priority","destination"],

	["log_timestamp","log_date","log_time","requested_pgn","CAN_data",
      "CAN_data_size","pgn","source","priority","destination"],

	["log_timestamp","log_date","log_time","identity_number",
      "manufacturer_code","device_instance","device_function","device_class",
      "system_instance","industry_group","CAN_data","CAN_data_size","pgn",
      "source","priority","destination"]
]

## NEW STRATEGY
# Iniitally I wanted to process each file individually for all log
# types. While this is good for auditing what has been parsed and what
# has not, it retains the mess of logs that ASV Global has created. I
# think it better to try to clean them up here. So lets make this
# simplier. 

# A list of the commands to execute - for calling in parallel
cmds_to_execute = []

# Check to see if parallel is installed and in the path.
USEPARALLEL = any(os.access(os.path.join(path, 'parallel'), os.X_OK) for path in os.environ["PATH"].split(os.pathsep))
if USEPARALLEL:
    print("Found BASH parallel. Using it!")
else:
    print("Did not find BASH parallel. To extract NMEA2000 logs faster try")
    print("  sudo yum install parallel")


# Get a summary of the available logs types. 
cmd = ('/bin/cat ' + 
       os.path.join(os.path.join(directory,'device'),'*.nmea2000') + ' | ' + 
       ' readnmea2000 -t paramGroup=pgn | tr \' \' \'\n\' | ' +
       ' sort | uniq -c | awk \'{print $2, "\t",$1}\' > ' + 
       outputdir + '/nmea2000_logsummary.txt')
if verbose >= 1:
    print "Getting summary info. Executing " + cmd

try:
    os.system(cmd)
except:
    print "Unable to execute: " + cmd
    sys.exit()

# For each logtype present, parse them. 
for line in file(outputdir + '/nmea2000_logsummary.txt','r'):
    pgncnt = line.split('\t')
    pgn = 'pgn' + pgncnt[0].rstrip()
    pgnnum = pgncnt[1].rstrip()

    if verbose >=1:
        print "PGN: " + pgn + ', NUM: ' + pgnnum

    # If the pgn parsed from above is not in our list, skip it.
    if nmea2000logtypes.count(pgn) == 0:
        if verbose >= 1:
            print 'PGN unknown: ' + pgn
        continue

    # Create the commdand to cat the nmea 2000 logs into the reader. 
    cmd = ('/bin/cat ' + 
           os.path.join(os.path.join(directory,'device'),'*.nmea2000') +
           ' | readnmea2000 -t ' + pgn + '=')

    # Append the fields to extract.
    for field in nmea2000fieldnames[nmea2000logtypes.index(pgn)]:
        cmd += field + ','

    # Create the output file and write the field name header.
    outputfile = os.path.join(outputdir,
                              ('nmea2000_'+ 
                               nmea2000logsummary[nmea2000logtypes.index(pgn)]
                               + '_' + pgn + '.txt'))

    if verbose >= 1:
        print 'Opening: ' + outputfile

    fid = open(outputfile,'w')
    fid.write(' '.join(nmea2000fieldnames[nmea2000logtypes.index(pgn)])+"\n")
    fid.close()

    # Modify the extraction command to append to the output file. 
    cmd += ' >> ' + outputfile
    if verbose >= 1:
        print 'Executing ' + cmd

    # Tally the list of commands to execute for parallel operation later.
    cmds_to_execute.append(cmd)

    # If not executing in parallel, execute them one at a time here.
    if not USEPARALLEL:
        if not dryrun:
            os.system(cmd)
        else:
            print("DRYRUN, would execute: " + cmd)

if USEPARALLEL:
    # Use bash parallel to execute the extraction simultaneously.
    cmd = 'parallel --will-cite --xapply --load 90% --noswap --jobs 0 --joblog - {} ::: ' + " ".join("'" + item + "'" for item in cmds_to_execute)

    # Execute them
    if not dryrun:
        os.system(cmd)
    else:
        print("DRYRUN, would execute: " + cmd)

    
    
