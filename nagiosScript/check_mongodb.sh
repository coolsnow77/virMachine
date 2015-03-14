#!/bin/bash

#nagios mongodb  service 

novaNet=`service mongodb  status | grep running`

#echo $novaNet

if  [ x"$novaNet" != x'' ];then
	echo "LY mongodb run OK"
	exit 0
else
	echo "Critical LY mongodb stop "
	exit 2
fi
