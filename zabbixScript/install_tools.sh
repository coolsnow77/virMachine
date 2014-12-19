#!/bin/bash

mv  /etc/apt/sources.list /etc/apt/sorces.list.old
cp  sources.list  /etc/apt/
apt-get -y  update 
apt-get -y  install  python-setuptools python2.7-dev
easy_install  mysql-python xlsxwriter
mkdir  -p  ./zabbixpng
	
mv  /etc/apt/sources.list.old /etc/apt/sorces.list
