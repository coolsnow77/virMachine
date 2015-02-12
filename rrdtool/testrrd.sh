#!/bin/bash
BIN="/usr/bin/rrdtool"
RRD="./test.rrd"
if ! test -e $RRD ;then 
    $BIN create  test.rrd -s 5 \ 
    DS:eth0:COUNTER:10:U:U \ 
    DS:cpu:GAUGE:10:U:U \ 
    DS:mem_total:GAUGE:10:U:U \ 
    DS:mem_free:GAUGE:10:U:U \ 
    DS:mem_buffer:GAUGE:10:U:U \ 
    DS:mem_cache:GAUGE:10:U:U \ 
    RRA:MAX:0.5:1:600 \ 
    RRA:MAX:0.5:5:600 \ 
    RRA:MAX:0.5:12:600 \ 
    RRA:AVERAGE:0.5:1:600 \ 
    RRA:AVERAGE:0.5:5:600 \ 
    RRA:AVERAGE:0.5:12:600 
fi 
while : 
do
    load=`awk '{print $1*100}' /proc/loadavg` 
    eth0=`grep -oP eth0:[0-9]+ /proc/net/dev` 
    mem_t=`awk '/MemTotal/{print $2}' /proc/meminfo` 
    mem_f=`awk '/MemFree/{print $2}' /proc/meminfo` 
    mem_b=`awk '/Buffers/{print $2}' /proc/meminfo` 
    mem_c=`awk '/Cached/{print $2;exit}' /proc/meminfo` 
    INFO=N:${eth0##*:}:$load:$mem_t:$mem_f:$mem_b:$mem_c 
$BIN update $RRD $INFO
    echo $INFO 
    echo $((i++)) 
    sleep 5 
done 
