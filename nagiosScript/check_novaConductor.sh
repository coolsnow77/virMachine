#!/bin/bash

#nagios   nova-conductor status  service 

novaNet=`service nova-conductor  status | grep running`

#echo $novaNet

if  [ x"$novaNet" != x'' ];then
	echo "LY nova-conductor run OK"
	exit 0
else
	echo "Critical LY nova-conductor stop "
	exit 2
fi
