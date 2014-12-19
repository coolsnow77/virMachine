#!/bin/bash
# login zabbix to get one month pic 


if  [ -d zabbixpng ];then
	rm  -r  zabbixpng/*
fi



# login arg 
cook="/tmp/cookie"
url="http://10.66.49.8/zabbix"
dt=`date +%Y%m`
width=600
height=200
stime=${dt}01000000
period=2592000
ip=1

echo $stime

exit 

zlogin(){
	curl -c $cook -b $cook -d "request=&name=admin&password=zabbix&autologin=1&enter=Sign+in"  $url/index.php
}

getpic(){
	curl -b $cook -F "graphid=$id" -F "period=$period" -F "stime=$stime" -F "width=$width" -F "height=$height" $url/chart2.php >./zabbixpng/$ip.png
}

graphid=(`mysql -uroot -p'qazwsxedc123!'  -s -e "select  graphid from zabbix.graphs  where name='CPU utilization'"`)


# login 
zlogin

for((i=0;i<${#graphid[@]};i++))
do
	echo  $i, ${graphid[$i]}
	ip=`mysql  -p'qazwsxedc123!'  -s  -e "use zabbix; select host from hosts where \
	hostid in (select hostid from items where itemid in (select itemid from graphs_items where graphid=${graphid[$i]})) ;" `
	
	# get pic 
	id=${graphid[$i]}
	getpic
done
