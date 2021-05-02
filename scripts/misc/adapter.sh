#!/bin/bash

dn=`ifconfig tun0 2>/dev/null |  grep -P "10.10.*.* " | awk '{print $2}'`
nd=`ifconfig eth0 | grep -P "192.168.[0-9]{3}.[0-9]{3}" | awk '{print $2}'`

if [[ -z $dn ]]
then
	echo $nd 2>/dev/null
else
	echo $dn
fi
