#!/bin/bash

# First argument is the parent directory
directory=$1

# Need to check that the directry exists.

depth_outfile=`basename $directory`"_depth.txt"
temp_outfile=`basename $directory`"_temp.txt"

echo $depth_outfile

find $directory -type f | grep _4.nmea2000 | xargs cat | readnmea2000 -t pgn128267=log_timestamp,transducer_water_depth | sed 's/ /\t/g' > $depth_outfile
find $directory -type f | grep _4.nmea2000 | xargs cat | readnmea2000 -t pgn130311=log_timestamp,temperature | sed 's/ /\t/g' > $temp_outfile
