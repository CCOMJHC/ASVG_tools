#!/bin/bash
# 
# Val Schmidt
# Center for Coastal and Ocean Mapping
# University of New Hampshire
# Copyright 2016

echo ""
echo "Data from the CW4 is written in the following directory structure:"
echo "ccscm/"
echo "     /scm-vp/"
echo "            /<DATA_DIRECTORY>"
echo "            /<DATA_DIRECTORY>"
echo "            /etc."
echo "" 
echo "This structure will be maintained in the local copy, repeated"
echo "for each of the vp and vs. Thus you will get the following:"
echo ""  
echo "/vp/ccscm/"
echo "     /scm-vp/"
echo "            /<DATA_DIRECTORY>"
echo "            /<DATA_DIRECTORY>"
echo "            /etc."
echo "" 
echo "/vs/ccscm/"
echo "     /scm-vp/"
echo "            /<DATA_DIRECTORY>"
echo "            /<DATA_DIRECTORY>"
echo "            /etc."
echo "" 
echo "Type the full path where to put the vp/ and vs/ directories below."
echo "If you already have a data store (e.g you've copied data before"
echo "and the vp/ccscm/scm-vp/ and/or vs/ccscm/scm-vs/ directories "
echo "already exist), specify the path to their parent directory"
echo "If you do not, this structure will be created for you at the"
echo "location you specify."
echo -n ">"

read datastore
mkdir -p $datastore/vp/ccscm/scm-vp
vpdatastore="$datastore/vp/ccscm/scm-vp"
mkdir -p $datastore/vs/ccscm/scm-vs
vsdatastore="$datastore/vs/ccscm/scm-vs"

echo "Pull data from VS too [y/n]?"
read dovs
# Always do the vp
dovp=y

echo "Pull data over the Cobham/Wired [1] or Wifi [2] Networks?"
read network

if [ "$network" == 1 ]; then
	VP="192.168.100.10"
fi

if [ "$network" == 2 ]; then
	VP="192.168.101.10"
fi

echo "Rate limit? [y/N]?"
read RATELIMIT

echo "Reading available directories"
alllogdirs=`ssh unmanned@$VP ls -1 /home/unmanned/ccscm/scm-vp/`

for logdir in ${alllogdirs[@]}; do
	echo "$logdir"
done

# Get the user's selection. 
echo "Type (cut/paste) the directory(s) to pull, with 'Enter' after
each. Or type '*' to process all of them. Type'q' to quit."
read datadir
while [ "$datadir" != 'q' ]; do

    if [ "$datadir" == '*' ]; then
        datadirs=( ${logswithdata[@]} )
        datadir="q"
    else

        datadirs=( "${datadirs[@]}" $datadir )
        read datadir

    fi # End check for '*'

done



if [ "$dovs" == 'y' ]; then
	# Pull data from vs.
        for datadir in ${datadirs[@]}; do
		ssh unmanned@vs "tar -cpf - ccscm/scm-vs/$datadir" | pv -rab | tar -xpf - -C "$vsdatastore"
	done
fi

if [ "$dovp" == 'y' ]; then
	# Pull data from vp
        for datadir in ${datadirs[@]}; do

		echo "Transferring $datadir to $vpdatastore."
		ssh unmanned@$VP "tar -cpf - -C ccscm/scm-vp/ $datadir" \
		| pv -rab | tar -xpf - -C "$vpdatastore"
	done
fi
