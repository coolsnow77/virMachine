#!/bin/bash
 sudo  apt-get  install  python-setuptools
  sudo  easy_install  pip
  sudo  pip  install  pika

 #  vim  /etc/rsyslog.d/50-default.conf  #cron

sudo  service  rsyslog restart 


sudo  service  cron  restart  

# echo  cron  path  
#　PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin 
