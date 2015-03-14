#!/bin/bash

apt-get  -y  install dpkg-dev
cd  ubuntu
#sudo dpkg-scanpackages ubuntu /dev/null |gzip >ubuntu/Packages.gz
sudo dpkg-scanpackages . /dev/null |gzip >Packages.gz
