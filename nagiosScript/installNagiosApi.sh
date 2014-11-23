#!/bin/bash

# this is install nagios api 8090 file script
python  setup.py install
yum  install  libffi-devel
easy_install  `cat  requirements.txt  | awk -F'==' '{print $1}'`

cp  nagios-api  /etc/init.d/

chkconfig nagios-api  on
/etc/init.d/nagios-api  start
