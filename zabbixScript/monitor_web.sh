#!/bin/bash
# desc: monitor web server

# $1 --- url  http://10.66.49.8/zabbix/index.php
usage(){
   echo "usage: $0 url"
   echo "example: $0 http://10.66.49.8/zabbix/index.php"
}
if [ $# -ne 1 ];then
	usage
else
	url_status=$(curl -o /dev/null -s -m 10 --connect-timeout 10 -w %{http_code} $1)
        if [ $url_status -eq 200 ]; then
                 echo "OK - $1"
                 exit 0
        else
              echo "Cirtical - $1"
              exit 2
        fi
fi
