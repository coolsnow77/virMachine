#!/bin/bash


#for  i in {1..4}
#for  i in {6..15}
for  i in {16..26}
do
  echo 192.168.71.$i
  scp   updateZ.sh  root@192.168.71.$i:/srv/
  scp   zabbix_agentd  root@192.168.71.$i:/srv/

  ssh   root@192.168.71.$i   "cd  /srv/  &&  source  updateZ.sh"
done 
