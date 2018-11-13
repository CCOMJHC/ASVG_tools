#!/bin/bash
#
# Val Schmidt
# Center for Coastal and Ocean Mapping
# University of New Hampshire
# Copyright 2016-2018
#
#
# TO DO:

if [ -e ~/.ASVG_tools.conf ]; then
	source ~/.ASVG_tools.conf
else
	echo "Unable to config .ASVG_tools.conf in home directory."
	exit
fi

function asv_exec {
    if [ "$2" == 1 ]; then
	echo "      Executing:   $1"
    fi
    eval "$1"
}
export -f asv_exec

DOCW4=0
DOCSV=0
DO2000=0
DO0183=0
PRINTHELP=0
GOTOUTPUT=0
VERBOSE=0
PARALLEL=0

while getopts ":rewqhad:o:v" opt; do

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
	v)
	    VERBOSE=1
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

# Execute in parallel if the parallel program exists.
if [ -x "$(command -v parallel)" ]; then
    echo "Extracting using gnu parallel."
    PARALLEL=1
else
    echo "Gnu parallel command does not exist."
    echo "Continuing with single processor extraction."
    echo "Install gnu parallel to speed things up"
    echo "sudo yum install parallel"
    PARALLEL=0
fi

if [ "$VERBOSE" == 1 ]; then
echo "DO CW4: $DOCW4"
echo "DO CSV: $DOCSV"
echo "DO N2K: $DO2000"
echo "DO N18: $DO0183"
echo "DO HEL: $PRINTHELP"
echo "VERBOS: $VERBOSE"
echo "IN DIR: $ccscm"
echo "OU DIR: $outputdir"
fi

# Exporting these to make them globally accessible. 
# probably not good bash programming practice.
export ccscm
export VERBOSE


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
    echo "           and -o should probably2018-04-20T16-46-be the same to put the results in the same directory."
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

# The first argument is the path to the ccscm log directory. 
#ccscm=$1

if [ ! -e "$ccscm" ]; then
    echo "Could not find $ccscm"
    echo "Exiting..."
    exit 
fi 

# We need to specify an output directory, unless we are parsing CSV files. These
# files are generated when we extract the logs using the ASV Global command line tool,
# hence the output directory must have already been created. So this case is handled below
if [[ "$outputdir" == "" ]] && [[ "$DO2000" == 1 || "$DOCW4" == 1 || "$DO1083" == 1 ]]; then
    echo "You must specify an output directory (-o <path>)." >&2
    exit 1
fi

# If we are asking to parse the CSV files generated from extracting data from the CW4
# and that is all, then $ccscm will either be the path to extracted_logs, or possibly the
# directory above it. Code below expects the directory above it so handle that here. 
if [[ "$outputdir" == "" ]] && [[ "$DOCW4" == 0 && "$DOCSV" == 1 ]]; then

    if [ `basename $ccscm` == "extracted_logs" ]; then
       outputdir=`dirname "$ccscm"`
    elif [ ! -d $ccscm/extracted_logs ]; then
       echo "Cannot find the extract_logs/ directory from which to read data. Exiting."
       exit
    else
       outputdir="$ccscm"
    fi
fi

outputdir=`realpath "$outputdir"`
if [ "$VERBOSE" == 1 ]; then
echo "Revised OUT DIR: $outputdir"
fi
echo ""


# An environment varialbe we'll eventually set.
#ASVG_TOOLS="/home/asvuser/gitsrc/ASVG_tools/"

if [ "$ASVG_TOOLS" = "" ]; then
    echo "Set environment variable ASVG_TOOLS to the ASVG_tool/ directory."
    echo "e.g. export ASVG_TOOLS=/path/to/ASVG_tool/"
    exit 1
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

# TODO: Check to see that the output directory exist and either fail
# or make it.   

# Inquire for the directory of logs that are to be parsed. It is not
# yet clear what causes a rotation of logging directory by ASV. For
# now logs are extracted on a directory basis. 

# In this case we have presumably already extracted CSV files,
# we will have selected the "extract_logs" directory for input.
if [ "$DOCSV" == "1" ] && [ "$DOCW4" == "0" ]; then
    alllogdirs=`ls -1 ${ccscm}/extracted_logs`
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
	if [ -e "$ccscm/extracted_logs/$logdir/engine.csv" ]; then
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
	echo "Extracting ASV C-Worker Binary Logs..."
        echo "Creating export configuration..."
fi

complete_outputdirs=()
outputspecs=()


# Create lists of the output directory and config script names
for datadir in ${datadirs[@]}; do
    # Define and create the output directory.
    complete_outputdir="${outputdir}/extracted_logs/${datadir}"
    outputspec="$complete_outputdir/configs/${datadir}_export_config.exs"
    echo "mkdir $complete_outputdir"
    mkdir -p "$complete_outputdir/configs/"

    # Capture a list of these for parallel execution later.
    complete_outputdirs=( "${complete_outputdirs[@]}" ${complete_outputdir} )
    outputspecs=( "${outputspecs[@]}" ${outputspec} )

    # Non parallel execution
    if [ "$DOCW4" == 1 ]; then
    	
    	CMD="${ASVG_TOOLS}/bash/create_export_config.sh ${complete_outputdir} > ${outputspec}"
    	asv_exec "${CMD}" "${VERBOSE}"
    fi

done

# Capture where the command was executed from.
CWD=`pwd`

function extract_cw4_binary_data() {

	# The original command before we made this parallel:
	# CMD="/usr/local/bin/data-export-cli -d ${ccscm}/scm-vp/${datadir} -x ${outputspec} >> ${complete_outputdir}/export.log 2>&1 &"
	CMD="/usr/local/bin/data-export-cli -d ${ccscm}/scm-vp/$1 -x $2 >> $3/export.log 2>&1"
	asv_exec "${CMD}" "${VERBOSE}"

}

export -f extract_cw4_binary_data
#export -f extract_data

# Execute the data extraction in parallel, being careful about memory (--noswap).
# and not exceeding the number of cores (--load).
if [ "$DOCW4" == 1 ] && [ "$PARALLEL" == 1 ] ; then
	echo "Launching data export processes..."
	if [ "$VERBOSE" == 1 ]; then
	    parallel --will-cite -v --xapply --load 90% --noswap --jobs 0 --joblog - extract_cw4_binary_data ::: ${datadirs[*]} ::: ${outputspecs[*]} ::: ${complete_outputdirs[*]}
        else
	    parallel --will-cite --xapply --load 90% --noswap --jobs 0 --joblog - extract_cw4_binary_data ::: ${datadirs[*]} ::: ${outputspecs[*]} ::: ${complete_outputdirs[*]}
        fi
fi

# Parse the data. 
for datadir in ${datadirs[@]}; do

    # Define and create the output directory.
    complete_outputdir="${outputdir}/extracted_logs/${datadir}"
    outputspec="$complete_outputdir/configs/${datadir}_export_config.exs"
    # If we extracted CW4 logs, then we made these directories already, so omit this.
    if [ "$DOCW4" == 0 ] ; then
        echo "mkdir $complete_outputdir"
        mkdir -p "$complete_outputdir/configs/"
    fi

    # Note the escaped quotes in these lines help the code handle spaces in a file or directory name.
    # These have to be stripped off however inside the python code.

    if [ "$DOCSV" == 1 ]; then
	echo ""
	echo "Parsing CSV files for MATLAB."
	CMD="${ASVG_TOOLS}/pyasv/bin/parsecsv.py -d \"${complete_outputdir}\" -o i"
	asv_exec "${CMD}" "${VERBOSE}"
	echo ""
    fi

    if [ "$DO0183" = 1 ]; then
	echo ""
	echo "Parsing nmea0183 logs..."
	CMD="${ASVG_TOOLS}/pyasv/bin/parsenmea0183.py -d \"${ccscm}/scm-vp/${datadir}\" -o \"${complete_outputdir}\""
	asv_exec "${CMD}" "${VERBOSE}"
	echo ""
    fi

    if [ "$DO2000" = 1 ]; then
	echo "Parsing nmea2000 logs..."
	CMD="${ASVG_TOOLS}/pyasv/bin/parsenmea2000.py -d ${ccscm}/scm-vp/${datadir} -o ${complete_outputdir}"
	asv_exec "${CMD}" "${VERBOSE}"
    fi

    echo ""
    echo "Export of $datadir complete."
    # Go back to the original location.
    cd "${CWD}"

done
