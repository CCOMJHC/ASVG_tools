#!/bin/bash
#
# A script to push a file to another computer using socat.
#
# Val Schmidt
# Center for Coastal and Ocean Mapping
# University of New Hampshire
# 2017

if [ "$1" == "-h" ] || [ "$1" == "" ]; then
   echo ""
   echo "PITCH and CATCH are wrappers for socat that make sending a file from"
   echo "one computer easy, when the two computers have unrestricted networking"
   echo "between them. "
   echo ""
   echo "USAGE:"
   echo "   On the receiving computer execute:"
   echo "      ./catch.sh file/to/catch"
   echo ""
   echo "   On the sending computer execute:"
   echo "   ./pitch.sh /file/to/pitch address"
   echo ""
   echo "address:      IP address or hostname of computer to which to send file."
   echo ""
   exit 1
fi

SOCAT=`which socat`

$SOCAT TCP4-LISTEN:9999 $1
