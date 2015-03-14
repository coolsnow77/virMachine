#!/bin/bash

#nagios nova-network  service 

novaNet=`service nova-network  status | grep running`

#echo $novaNet

if  [ x"$novaNet" != x'' ];then
	echo "LY nova-network run OK"
	exit 0
else
	echo "Critical LY nova-network stop "
	exit 2
fi
