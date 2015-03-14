#!/bin/bash

apt-get  -y install python-setuptools
easy_install xmltodict

easy_install install pika

easy_install  python-libvirt

apt-get -y install libguestfs-tools  # select  no 


#PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
# */10  * * * *  python  /home/incito/myRabbitMQSend.py >/dev/null 2>&1  
# */10  * * * *  python  /home/incito/myRabbitMQRecv.py  >/dev/null  2>&1



#  compute 一定要安装ceilometer


virsh  dommemstat 5 --period 1000