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
import re

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
                      'magnetic_variation',
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
nmea2000fieldnames = [["log_timestamp","log_date","log_time",
                       "CAN_data","CAN_data_size","pgn","source", 
                       "priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "sequence_id","time_source","day",
                       "time_of_day","timestamp","CAN_data",
                       "CAN_data_size","pgn","source",
                       "priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "database_version","product_code",
                       "model_id","software_version","model_version",
                       "model_serial","certification_level","load_equivalency",
                       "CAN_data","CAN_data_size","pgn",
                       "source","priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "sequence_id","heading_sensor_reading","deviation",
                       "variation","heading_sensor_reference","CAN_data",
                       "CAN_data_size","pgn","source",
                       "priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "sequence_id","rate_of_turn","CAN_data",
                       "CAN_data_size","pgn","source",
                       "priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "sequence_id","yaw","pitch",
                       "roll","CAN_data","CAN_data_size",
                       "pgn","source","priority",
                       "destination"],

                      ["log_timestamp","log_date","log_time",
                       "sequence_id","variation_source","age_of_service",
                       "variation","CAN_data","CAN_data_size",
                       "pgn","source","priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "engine_instance","engine_speed","engine_boost_pressure",
                       "engine_tilt","CAN_data","CAN_data_size",
                       "pgn","source","priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "engine_instance","engine_oil_pressure",
                       "engine_oil_temperature","engine_temperature",
                       "alternator_potential","fuel_rate",
                       "total_engine_hours","engine_coolant_pressure",
                       "fuel_pressure","engine_tilt","check_engine",
                       "over_temperature","low_oil_pressure"],

                      ["log_timestamp","log_date","log_time",
                       "transmission_instance","transmission_gear",
                       "transmission_oil_pressure","transmission_oil_temperature",
                       "check_temperature","over_temperature",
                       "low_oil_pressure","low_oil_level",
                       "sail_drive","CAN_data","CAN_data_size",
                       "pgn","source","priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "instance","trip_fuel_used",
                       "average_fuel_rate","economy_fuel_rate",
                       "inst_fuel_economy","CAN_data","CAN_data_size",
                       "pgn","source","priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "fluid_instance","fluid_type","fluid_level",
                       "tank_capacity","CAN_data","CAN_data_size",
                       "pgn","source","priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "sequence_id","dc_instance","dc_type",
                       "state_of_charge","state_of_health","time_remaining",
                       "ripple_voltage","cumulative_charge_drawn",
                       "CAN_data","CAN_data_size",
                       "pgn","source","priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "battery_instance","battery_voltage","battery_current",
                       "battery_case_temperature","sequence_id",
                       "CAN_data","CAN_data_size",
                       "pgn","source","priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "sequence_id","water_speed",
                       "ground_speed",#"referenced_type",
                       "speed_direction","CAN_data","CAN_data_size",
                       "pgn","source","priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "sequence_id","transducer_water_depth",
                       "transducer_offset","maximum_depth_range",
                       "CAN_data","CAN_data_size","pgn",
                       "source","priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "measurement_day","measurement_time_of_day",
                       "cumulative_distance","distance_since_reset",
                       "CAN_data","CAN_data_size","pgn",
                       "source","priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "latitude","longitude",
                       "CAN_data","CAN_data_size","pgn",
                       "source","priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "sequence_id","cog_reference",
                       "course_over_ground","speed_over_ground",
                       "CAN_data","CAN_data_size",
                       "pgn","source","priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "sequence_id","timestamp",
                       "date","time","position_day",
                       "position_time_of_day","latitude",
                       "longitude","altitude","system_type",
                       "gnss_method","gnss_integrity",
                       "space_vehicles","horizontal_dop",
                       "positional_dop","geoidal_separation",
                       "reference_stations","CAN_data"],

                      ["log_timestamp","log_date","log_time",
                       "timestamp","date","time","day",
                       "time_of_day","local_time_offset",
                       "CAN_data","CAN_data_size","pgn",
                       "source","priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "sequence_id","residual_mode",
                       "space_vehicles","CAN_data","CAN_data_size",
                       "pgn","source","priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "sequence_id","wind_speed",
                       "wind_direction","wind_reference",
                       "CAN_data","CAN_data_size","pgn",
                       "source","priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "sequence_id","water_temperature",
                       "ambient_temperature","atmospheric_pressure",
                       "CAN_data","CAN_data_size","pgn",
                       "source","priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "sequence_id","temperature_instance",
                       "humidity_instance","temperature",
                       "humidity","atmospheric_pressure",
                       "CAN_data","CAN_data_size","pgn",
                       "source","priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "sequence_id","temperature_instance",
                       "temperature_source","actual_temperature",
                       "control_temperature","CAN_data",
                       "CAN_data_size","pgn","source",
                       "priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "sequence_id","humidity_instance",
                       "humidity_source","actual_humidity",
                       "control_humidity","CAN_data",
                       "CAN_data_size","pgn","source",
                       "priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "sequence_id","pressure_instance",
                       "pressure_source","pressure","CAN_data",
                       "CAN_data_size","pgn",
                       "source","priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "sequence_id","temperature_instance",
                       "temperature_source","actual_temperature",
                       "control_temperature","CAN_data","CAN_data_size",
                       "pgn","source","priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "requested_pgn","CAN_data",
                       "CAN_data_size","pgn",
                       "source","priority","destination"],

                      ["log_timestamp","log_date","log_time",
                       "identity_number","manufacturer_code",
                       "device_instance","device_function","device_class",
                       "system_instance","industry_group",
                       "CAN_data","CAN_data_size","pgn",
                       "source","priority","destination"]
                  ]

# Below are lists of the fields available for each of the log types above.
nmea2000essentialfieldnames = [["log_timestamp",
                       "CAN_data","CAN_data_size","pgn","source", 
                       "priority","destination"],

                      ["log_timestamp",
                       "sequence_id","time_source","day",
                       "time_of_day","timestamp"],

                      ["log_timestamp",
                       "database_version","product_code",
                       "model_id","software_version","model_version",
                       "model_serial","certification_level","load_equivalency"],

                      ["log_timestamp",
                       "sequence_id","heading_sensor_reading","deviation",
                       "variation"],

                      ["log_timestamp",
                       "sequence_id","rate_of_turn"],

                      ["log_timestamp",
                       "sequence_id","yaw","pitch",
                       "roll"],

                      ["log_timestamp",
                       "sequence_id","variation_source","age_of_service",
                       "variation"],

                      ["log_timestamp",
                       "engine_instance","engine_speed","engine_boost_pressure",
                       "engine_tilt"],

                      ["log_timestamp",
                       "engine_instance","engine_oil_pressure",
                       "engine_oil_temperature","engine_temperature",
                       "alternator_potential","fuel_rate",
                       "total_engine_hours","engine_coolant_pressure",
                       "fuel_pressure","engine_tilt","check_engine",
                       "over_temperature","low_oil_pressure"],

                      ["log_timestamp",
                       "transmission_instance","transmission_gear",
                       "transmission_oil_pressure","transmission_oil_temperature",
                       "check_temperature","over_temperature",
                       "low_oil_pressure","low_oil_level",
                       "sail_drive"],

                      ["log_timestamp",
                       "instance","trip_fuel_used",
                       "average_fuel_rate","economy_fuel_rate",
                       "inst_fuel_economy"],

                      ["log_timestamp",
                       "fluid_instance","fluid_type","fluid_level",
                       "tank_capacity"],

                      ["log_timestamp",
                       "sequence_id","dc_instance","dc_type",
                       "state_of_charge","state_of_health","time_remaining",
                       "ripple_voltage","cumulative_charge_drawn"],

                      ["log_timestamp",
                       "battery_instance","battery_voltage","battery_current",
                       "battery_case_temperature","sequence_id"],

                      ["log_timestamp",
                       "sequence_id","water_speed"],

                      ["log_timestamp",
                       "sequence_id","transducer_water_depth",
                       "transducer_offset"],

                      ["log_timestamp",
                       "measurement_day","measurement_time_of_day",
                       "cumulative_distance","distance_since_reset"],

                      ["log_timestamp",
                       "latitude","longitude",],

                      ["log_timestamp",
                       "sequence_id","cog_reference",
                       "course_over_ground","speed_over_ground",],

                      ["log_timestamp",
                       "sequence_id","timestamp",
                       "date","time","position_day",
                       "position_time_of_day","latitude",
                       "longitude","altitude","system_type",
                       "gnss_method","gnss_integrity",
                       "space_vehicles","horizontal_dop",
                       "positional_dop","geoidal_separation",
                       "reference_stations"],

                      ["log_timestamp",
                       "timestamp","date","time","day",
                       "time_of_day","local_time_offset"],

                      ["log_timestamp",
                       "sequence_id","residual_mode",
                       "space_vehicles"],

                      ["log_timestamp",
                       "sequence_id","wind_speed",
                       "wind_direction","wind_reference"],

                      ["log_timestamp",
                       "sequence_id","water_temperature",
                       "ambient_temperature","atmospheric_pressure"],

                      ["log_timestamp",
                       "sequence_id","temperature_instance",
                       "humidity_instance","temperature",
                       "humidity","atmospheric_pressure"],

                      ["log_timestamp",
                       "sequence_id","temperature_instance",
                       "temperature_source","actual_temperature",
                       "control_temperature"],

                      ["log_timestamp",
                       "sequence_id","humidity_instance",
                       "humidity_source","actual_humidity",
                       "control_humidity"],

                      ["log_timestamp",
                       "sequence_id","pressure_instance",
                       "pressure_source","pressure"],

                      ["log_timestamp",
                       "sequence_id","temperature_instance",
                       "temperature_source","actual_temperature",
                       "control_temperature"],

                      ["log_timestamp",
                       "requested_pgn"],

                      ["log_timestamp",
                       "identity_number","manufacturer_code",
                       "device_instance","device_function","device_class",
                       "system_instance","industry_group"]
                  ]

class nmea2000parser:

    def __init__(self,directory='.'):
        self.DOPARALLEL = False
        self.DOHDF5 = False
        self.directory = directory
        self.outputdir = '.'
        self.type = 'all'
        self.verbose = False
        
        # Iniitalize a list of the commands to execute - for calling in parallel
        self.cmds_to_execute = []
        self.outputfilelist = []

    def get_logsummary(self):
        ''' 
        Use the readnmea2000 command to get a summary of the available log types.
        This must be run before creating extraction commands.
        '''
 
        # In some cases, the 'tr' bit below is required and others not. 
        # It is not clear why. 
        cmd = ('/bin/cat ' + 
               os.path.join(os.path.join(self.directory,'device'),'*.nmea2000') + ' 2>/dev/null | ' + 
               ' readnmea2000 -t paramGroup=pgn | tr \' \' \'\n\' | ' +
               ' sort | uniq -c | awk \'{print $2, "\t",$1}\' > ' + 
               self.outputdir + '/nmea2000_logsummary.txt')
        #cmd = ('/bin/cat ' +                
        #       os.path.join(os.path.join(self.directory,'device'),'*.nmea2000') + ' | ' + 
        #       ' readnmea2000 -t paramGroup=pgn | ' +
        #       ' sort | uniq -c | awk \'{print $2, "\t",$1}\' > ' + 
        #       self.outputdir + '/nmea2000_logsummary.txt')
        if verbose >= 1:
            print "Getting summary info. Executing " + cmd

        try:
            os.system(cmd)
        except:
            print "Unable to execute: " + cmd
            sys.exit()


    def create_extraction_commands(self,debugfields=False):
        '''
        Create BASH commands to extract the available log types.
        If debugfields is specified  the debug fields are  extracted.
        This must be run before executing the commands.
        It also populates a list of output file names for the parsed data.
        that are used in other routines to convert to other fomrats. 
        '''

        # For each logtype present, we create a new command.
        for line in file(self.outputdir + '/nmea2000_logsummary.txt','r'):
            
            # Extract the pgn number from the summary file.
            pgncnt = line.split('\t')
            pgn = 'pgn' + pgncnt[0].rstrip()
            pgnnum = pgncnt[1].rstrip()

            # If we are not asking to parse all log types
            # Skip all but the type we're looking for.            
            if self.type != 'all':
                if pgn != self.type:
                    continue
                
            if self.verbose >=1:
                print "PGN: " + pgn + ', NUM: ' + pgnnum

            # If the pgn parsed from above is not in our list of availabe ones, skip it.
            if nmea2000logtypes.count(pgn) == 0:
                if self.verbose >= 1:
                    print 'PGN unknown: ' + pgn
                continue

            # Create the output file and write the field name header.
            if logparser.DOHDF5:
                outputfile = os.path.join(self.outputdir,
                                      ('nmea2000_'+ 
                                       nmea2000logsummary[nmea2000logtypes.index(pgn)]
                                       + '_' + pgn + '.h5'))
            else:
                outputfile = os.path.join(self.outputdir,
                                      ('nmea2000_'+ 
                                       nmea2000logsummary[nmea2000logtypes.index(pgn)]
                                       + '_' + pgn + '.txt'))
                                      
            self.outputfilelist.append(outputfile)
            
            if verbose >= 1:
                print 'Opening: ' + outputfile

            fid = open(outputfile,'w')
            if not debugfields:
                fid.write(' '.join(nmea2000essentialfieldnames[nmea2000logtypes.index(pgn)])+"\n")         
            else:
                fid.write(' '.join(nmea2000fieldnames[nmea2000logtypes.index(pgn)])+"\n")
            fid.close()

            # Create the command to cat the nmea 2000 logs into the reader. 
            # cmd = ('/bin/cat ' + 
            #       os.path.join(os.path.join(directory,'device'),'*.nmea2000') +
            #       ' | readnmea2000 -t ' + pgn + '=')

            cmd = 'readnmea2000 -t ' + pgn + '='

            # Append the fields to extract.
            if not debugfields:
                for field in nmea2000essentialfieldnames[nmea2000logtypes.index(pgn)]:
                    cmd += field + ','                
                
            else:
                for field in nmea2000fieldnames[nmea2000logtypes.index(pgn)]:
                    cmd += field + ','


            # Modify the extraction command to append to the output file. 
            cmd += ' >> ' + outputfile

            # Tally the list of commands to execute for parallel operation later.
            self.cmds_to_execute.append(cmd)
            if verbose >= 1:
                print('   Queing Command:  ' + cmd)

    def extract_logs(self):
        '''
        Executes the commands generated by create_extraction_commands(),
        in parallel if possible.
        '''

        cmd_preamble = ('/bin/cat ' + 
                       os.path.join(os.path.join(directory,'device'),'*.nmea2000') + 
                       ' 2>/dev/null | ')


        # Check to see if parallel is installed and in the path.
        PARALLELEXISTS = any(os.access(os.path.join(path, 'parallel'), os.X_OK) for path in os.environ["PATH"].split(os.pathsep))

        # If parallel exists and it was requested use it. 
        if PARALLELEXISTS and self.DOPARALLEL:
            print("")            
            print("Found BASH parallel. Using it!")
            # Use bash parallel to execute the extraction simultaneously.
            cmd = 'parallel --bar --will-cite --xapply --load 90% --noswap --jobs 0 {} ::: ' + " ".join("'" + cmd_preamble + item + "'" for item in self.cmds_to_execute)

            # Execute them
            if not dryrun:
                print("")
                os.system(cmd)
            else:
                print("DRYRUN, would execute: " + cmd)

        else:
            if not PARALLELEXISTS:
                print("Did not find BASH parallel. To extract NMEA2000 logs faster try")
                print("  sudo yum install parallel")
                print("Extracting in sequence...")

            # If not executing in parallel, execute them one at a time here.
            for cmd in self.cmds_to_execute:
                if not dryrun:
                    if verbose >= 1:
                        print 'Executing ' + cmd_preamble + cmd
                    os.system(cmd_preamble + cmd)
                else:
                    print("DRYRUN, would execute: " + cmd_preamble + cmd)

    def convert_extracted_nmea2000_to_HDF5(self,fileandpath,removefiles=False):
        ''' A method to read the parsed NMEA2000 files and save to HDF5 '''
        
        # Read the data.
        data = pd.read_csv(fileandpath,delimiter = '\s+')
        
        outputfileandpath = fileandpath.replace('.txt','.hf')

        # Set the time column to the index. (useful for pandas)
        if 'log_timestamp in data.columns':
            data.log_timestamp = pd.to_datetime(data.log_timestamp,utc=True,unit='s')
            data.set_index('log_timestamp',inplace=True)
        
        # This bit of pandas magic will convert any column that was interpreted
        # as an column of objects, which happens in nmea data when it is unavailable,
        # to numeric values with the unavailable data set to NAN
        objcols = data.columns[data.dtypes.eq('object')]
        data[objcols] = data[objcols].apply(pd.to_numeric,errors='coerce')
            
        # Get the log type from the file name for the HDF table key. 
        if re.search(r'_([a-zA-Z_]+)_pgn',fileandpath):
            match = re.search(r'_([a-zA-Z_]+)_pgn',fileandpath)
            logtype = match.group(1)
        
            # Write the data.
            data.to_hdf(outputfileandpath,key = '/' + logtype, format='table')
            
            if removefiles:
                os.remove(fileandpath)



if __name__ == '__main__':

    
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
                        help = "Specify the type of logs (by PGN) to parse [default='all'")
    parser.add_argument("-i",'--info',
                        action="store_true",
                        help = "List the supported log types and their fields, then exit")
    parser.add_argument("-5",'--hdf',
                        action="store_true",
                        default = False,
                        help = "Convert parsed files to hdf5 format.")
    parser.add_argument("-D",'--debug_parsing',
                        action="store_true",
                        default = False,
                        help = "Parses out all fields, including raw CAN data for debugging.")
 

                        
    # Get list of files to parse.
    args = parser.parse_args()
    directory =         args.directory
    dryrun =            args.dryrun
    verbose =           args.verbosity
    outputdir =         args.outputdir
    type =              args.type
    DOHDF5 =            args.hdf
    DODEBUG_FIELDS =    args.debug_parsing
    
    if verbose >= 1:
        print("Arguments:")
        arguments = vars(args)
        for key, value in arguments.iteritems():
            print("\t%s:\t\t%s" % (key,str(value)))

    if args.info:
        for t, s, n in zip(nmea2000logtypes,nmea2000logsummary,nmea2000fieldnames):
            print("%s:%s" % (s,t))
            for field in n:
               print("     %s" % field)
            print("")
        sys.exit()

    logparser = nmea2000parser(directory=directory)
    logparser.dryrun = dryrun
    logparser.verbose = verbose
    logparser.outputdir = outputdir
    logparser.DOPARALLEL = True
    logparser.DOHDF5 = DOHDF5
    logparser.type = type
    
    logparser.get_logsummary()
    if DODEBUG_FIELDS:
        logparser.create_extraction_commands(debugfields=True)
    else:
        logparser.create_extraction_commands()

    logparser.extract_logs()
    if logparser.outputfilelist.__len__() != 0 and DOHDF5:
        print("Converting to HDF5.")
        for outputfile in logparser.outputfilelist:
            logparser.convert_extracted_nmea2000_to_HDF5(outputfile,
                                                         removefiles=True)
    print("Done.")
