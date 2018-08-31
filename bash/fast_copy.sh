#!/bin/bash
#
# Val Schmidt
# CCOM/JHC
# Copyright 2017
#
# A script to facilitate fast(er) copy of many small files.

PRINTHELP=0

while getopts "h" opt; do

	case $opt in 
		h)
		PRINTHELP=1
	esac
done

if [ "$PRINTHELP" == 1 ]; then

	echo ""
	echo "  fast_copy.sh  [-h] copy/from/dir copy/to/dir"
	echo ""
	exit 1
fi

COPYFROM=$1
COPYTO=$2

echo "FROM: $COPYFROM"
echo "TO: $COPYTO"

COPY=`basename $COPYFROM`
DIR=`dirname $COPYFROM`

tar -cpf - -C "$DIR" "$COPY"  | pv -rab | tar -xpf - -C "$COPYTO"
