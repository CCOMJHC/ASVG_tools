#!/bin/bash
# 
# Val Schmidt
# Center for Coastal and Ocean Mapping
# University of New Hampshire
# Copyright 2016

echo "Pull data from VS [y/n]?"
read dovs
echo "Pull data from VP [y/n]?"
read dovp

if [ "$dovs" == 'y' ]; then
	# Pull data from vs.
	ssh vs "tar -cpf - ccscm" | pv -rab | tar -xpf - -C /home/unmanned/data/vs/
fi

if [ "$dovp" == 'y' ]; then
	# Pull data from vp
	ssh vpc "tar -cpf - ccscm" | pv -rab | \
		tar -xpf - -C /home/unmanned/data/vp/
fi
