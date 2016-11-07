#!/bin/bash
#
# Val Schmidt
# Center for Coastal and Ocean Mapping
# University of New Hampshire
# Copyright 2016
#
#
# TO DO:

if [ -e ~/.ASVG_tools.conf ]; then
	source ~/.ASVG_tools.conf
else
	echo "Unable to config .ASVG_tools.conf in home directory."
	exit
fi

DOCW4=0
DOCSV=0
DO2000=0
DO0183=0
PRINTHELP=0
GOTOUTPUT=0

while getopts ":rewqhd:o:" opt; do

    case $opt in 
	r) 
	    DOCW4=1
	    ;;
	e)
	    DOCSV=1
	    ;;
	w)
	    DO2000=1
	    ;;
	q)
	    DO0183=1
	    ;;
	d) 
	    ccscm=`realpath ${OPTARG}`
	    ;;
	o)  
	    GOTOUTPUT=1
	    outputdir=${OPTARG}
	    ;;
	h)
	    PRINTHELP=1
	    ;;
	a) 
	    DOCW4=1
	    DOCSV=1
	    DO2000=1
	    DO0183=1
	    ;;
	\?)
	    echo "Invalid option: $OPTARG" >&2
	    exit 1
	    ;;
	:)
	    echo "Option -$OPTARG requires an argument." >&2
	    exit 1
	    ;;
    esac

done

echo $DOCW4
echo $DOCSV
echo $DO2000
echo $DO0183
echo $PRINTHELP
echo $ccscm
echo $outputdir


if [ "$PRINTHELP" == 1 ]; then

    echo ""
    echo "USAGE: "
    echo "    cworker_log_extractor.sh [-r|-e|-w|-q|-a] [-h] -d <path/to/ccscm> \ "
    echo "           -o [/path/to/output/dir]"
    echo ""
    echo "  -r extracts the CW4 logs from their binary form to CSV files."
    echo "  -e parses the CSV files, modifies the parameters names and produces .mat files. (calls parsecsv.py)"
    echo "     NOTE: If -e is called without -r, it is assumed that the CW4 files are already parsed. "
    echo "           In this case, the argument to -d should be /path/to/extracted_logs/"
    echo "           and -o should probably be the same to put the results in the same directory."
    echo "  -w extracts data from the nmea2000 log files. (calls parsenmea2000.py)"
    echo "  -q extracts data from the nmea1830 log files. (calls parsenmea0183.py, which in turn calls gpsparser.py)"
    echo "  -a does all of these. "
    echo ""
    echo ""
    echo "Logs will be extracted for the selected log directories"
    echo "into /path/to/output/dir/extracted_logs/ producing CSV"
    echo "files for each of the standard log types. If the output"
    echo "directory is omitted, the current working directory is used."
    echo ""
    exit 1
fi


if [ "$outputdir" == "" ]; then
    echo "You must specify an output directory (-o <path>)." >&2
    exit 1
fi

# An environment varialbe we'll eventually set.
#ASVG_TOOLS="/home/asvuser/gitsrc/ASVG_tools/"

if [ "$ASVG_TOOLS" = "" ]; then
    echo "Set environment variable ASVG_TOOLS to the ASVG_tool/ directory."
    echo "e.g. export ASVG_TOOLS=/path/to/ASVG_tool/"
    exit 1
fi

# The first argument is the path to the ccscm log directory. 
#ccscm=$1

if [ ! -e "$ccscm" ]; then
    echo "Could not find $ccscm"
    echo "Exiting..."
    exit 
fi 


#ccscm=`readlink -f "$ccscm"`

# The second argument is the directory into which the extact data will
# go.
#tmp=$2

#if [ "$outputdir" == "" ]; then
#    tmp=`pwd`
#    echo "Setting default output directory to "
#    echo "    $tmp/extracted_logs"
#fi
#outputdir="$tmp/extracted_logs/"
outputdir=`realpath "$outputdir"`

# TODO: Check to see that the output directory exist and either fail
# or make it.   

# Inquire for the directory of logs that are to be parsed. It is not
# yet clear what causes a rotation of logging directory by ASV. For
# now logs are extracted on a directory basis. 

# In this case we have presumably already extracted CSV files,
# we will have selected the "extract_logs" directory for input.
if [ "$DOCSV" == "1" ] && [ "$DOCW4" == "0" ]; then
    alllogdirs=`ls -1 ${ccscm}`
else
    alllogdirs=`ls -1 "${ccscm}/scm-vp"`
fi

# Get a list of the logs that actually have data and display them.
logswithdata=()
echo "I have detected logs in these directories:"
for logdir in ${alllogdirs[@]}; do
    
    if [ "$DOCW4" == "1" ] || [ "$DO2000" == "1" ] || [ "$DO0183" == "1" ]; then
	
	if [ -e "$ccscm/scm-vp/$logdir/smState.smx" ]; then
	    logswithdata=( ${logswithdata[@]} $logdir )
	    echo "$logdir"
	fi
    else
	if [ -e "$ccscm/$logdir/engine.csv" ]; then
	    logswithdata=( ${logswithdata[@]} $logdir )
	    echo "$logdir"
	fi
    fi
done

# Get the user's selection. 
echo "Type (cut/paste) the directory(s) to process, with 'Enter' after
each. Or type '*' to process all of them. Type'q' to quit."
read datadir
while [ "$datadir" != 'q' ]; do

    if [ "$datadir" == '*' ]; then
	datadirs=( ${logswithdata[@]} )
	datadir="q"
    else

	# This checking may not be necessary since I am now only listing
	# directories that have data. Maybe some other checking is worth
	# while here?
	# echo "Checking $ccscm/$datadir..."
	if [ "$DOCW4" == 1 ]; then
	    if [ -e "$ccscm/scm-vp/$datadir" ]; then
                datadirs=( "${datadirs[@]}" $datadir )
	    else
    		echo "That data directory does not exist. Try again. ('q' to quit)."
	    fi
	else
	    datadirs=( "${datadirs[@]}" $datadir )
	fi

	read datadir
    
    fi # End check for '*'

done

if [ "$DOCW4" == 1 ]; then
    if [ ! -e /usr/local/bin/data-export-cli ]; then
	echo "Unable to find the data export tool: data-export-cli"
	exit
    fi
fi


# Process the data. 
for datadir in ${datadirs[@]}; do


    echo "Extracting ASV C-Worker Binary Logs..."
    # Define and create the output directory.
    complete_outputdir="${outputdir}/extracted_logs/${datadir}"
    outputspec="$complete_outputdir/configs/${datadir}_export_config.exs"
    if [ "$DOCW4" = "1" ]; then
	echo "mkdir $complete_outputdir"
	mkdir -p "$complete_outputdir/configs/"
	fi

    # Capture where the command was executed from.
    cwd=`pwd`

    if [ "$DOCW4" == 1 ]; then
	# A bug in data-export-cli utility will not support multiple
	# exports in a single file. So separate export configuration files
	# had to be generated for each. This line hails from a time when
	# we expected to be able to do it in a single go.
	#cd "$complete_outputdir/configs"
	${ASVG_TOOLS}/bash/create_export_config.sh "$complete_outputdir" > "$outputspec"
	echo "$outputspec"
	# Go to the output directory and create the config files.
	#cd $complete_outputdir

	pwd

	# Then find all the config files we generated and process each.
	echo "Processing $datadir..."
	echo "   /usr/local/bin/data-export-cli -d \""${ccscm}/scm-vp/${datadir}"\" \
     	    -x \""${outputspec}"\" 2>&1 >> \""${complete_outputdir}/export.log\"""

	#/usr/local/bin/data-export-cli -d \""${ccscm}/scm-vp/${datadir}"\" \
     	#    -x \""${outputspec}"\" 2>&1 >> \""${complete_outputdir}/export.log\""

	/usr/local/bin/data-export-cli -d "${ccscm}/scm-vp/${datadir}" -x "${outputspec}"

	# In this block, separate processes were launched for each export
	# and these were monitored for completion.
	# This was useful when running separate exports was required.
	# It no longer is, so we run just the ingle line above.
	# configstoprocess=`find . -type f | grep export_config.exs`
	# for config in ${configstoprocess[@]}; do
	# 	echo "Processing $config"
	# 	data-export-cli -d "$ccscm/scm-vp/$datadir" \
	# 	    -x "$config" 2>&1 >> $complete_outputdir/export.log &
	# done
	#
	# secs=0
	# procs=`jobs | grep Running`
	# while [ "$procs" != "" ]; do
	#
	# 	echo "Processing $datadir, ${secs}s elapsed..."
	# 	sleep 1
	# 	secs=`echo "$secs+1" | bc`
	# 	tput cuu 1
	# 	procs=`jobs | grep Running`

	# done

    fi
    # Note the escaped quotes in these lines help the code handle spaces in a file or directory name.
    # These have to be stripped off however inside the python code.

    if [ "$DOCSV" == 1 ]; then
	echo ""
	echo "Parsing CSV files for MATLAB."
	if [ "$DOCW4" == 1 ]; then
	    ${ASVG_TOOLS}/pyasv/bin/parsecsv.py -d \""${complete_outputdir}"\" -o i -vv
	else
	    ${ASVG_TOOLS}/pyasv/bin/parsecsv.py -d \""${ccscm}/${datadir}"\" -o \""${outputdir}/${datadir}"\" -vv
	fi
	echo ""
    fi

    if [ "$DO0183" = 1 ]; then
	echo ""
	echo "Parsing nmea0183 logs..."
	${ASVG_TOOLS}/pyasv/bin/parsenmea0183.py -d \""${ccscm}/scm-vp/${datadir}"\" -o \""${complete_outputdir}"\"
	echo ""
    fi

    if [ "$DO2000" = 1 ]; then
	echo "Parsing nmea2000 logs..."
	${ASVG_TOOLS}/pyasv/bin/parsenmea2000.py -d \""${ccscm}/scm-vp/${datadir}"\" -o \""${complete_outputdir}"\"
    fi

    echo ""
    echo "Export of $datadir complete."
    # Go back to the original location.
    cd "$cwd"

done
