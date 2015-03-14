#!/bin/bash

#nagios memcached  service 

novaNet=`service memcached  status | grep running`

#echo $novaNet

if  [ x"$novaNet" != x'' ];then
	echo "LY memcached run OK"
	exit 0
else
	echo "Critical LY memcached stop "
	exit 2
fi
