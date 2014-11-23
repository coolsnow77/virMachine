#!/bin/bash
# boot nagios api file
port=8090
pa1='/usr/local/nagios/var'
nagios-api -p $port -c $pa1/rw/nagios.cmd \
        -s $pa1/status.dat -l $pa1/nagios.log
