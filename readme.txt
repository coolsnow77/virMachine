#!/bin/bash

1. get  instance  cpu

2. get instance  memory

3. get instance disk

4. get instance  bandwidth 

5. get  instance  DiskIO



#　 Domain Monitoring (help keyword 'monitor')
    domblkerror                    Show errors on block devices
    domblkinfo                     domain block device size information
    domblklist                     list all domain blocks
    domblkstat                     get device block stats for a domain
    domcontrol                     domain control interface state
    domif-getlink                  get link state of a virtual interface
    domiflist                      list all domain virtual interfaces
    domifstat                      get network interface stats for a domain
    dominfo                        domain information
    dommemstat                     get memory statistics for a domain
    domstate                       domain state
    list 



#  UserParameter=mysql.status[*],/bin/bash /usr/local/etc/checkmysqlperformance.sh $1 $2 

#  UserParameter=libvirt.status[*], /usr/bin/python  /usr/local/etc/mylibvirtutil.py $1 $2

#  python  mylibvirtutil.py  disk.root.total    3

#  python  mylibvirtutil.py  memory.total   10.66.32.67
#  python  mylibvirtutil.py   disk.write.bytes.rate  10.66.32.67 
#  python  mylibvirtutil.py   disk.read.bytes.rate  10.66.32.67
#  python  mylibvirtutil.py   memory.available 10.66.32.67 
#　python  mylibvirtutil.py   net.in 10.66.32.67 
