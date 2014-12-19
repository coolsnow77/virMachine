#!/bin/bash

#mkdir  -p  /etc/zabbix/
#cp  -Rf   /usr/local/etc/zabbix_agen*   /etc/zabbix/
/etc/init.d/zabbix-agent  stop
#cp  /usr/local/sbin/zabbix_agentd   /usr/local/sbin/zabbix_agentd.bak
cp  /usr/sbin/zabbix_agentd   /usr/sbin/zabbix_agentd.bak
#cp -Rf  zabbix_agentd   /usr/local/sbin/zabbix_agentd 
cp -Rf  zabbix_agentd   /usr/sbin/zabbix_agentd 
/etc/init.d/zabbix-agent  start
