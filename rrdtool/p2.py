#!/usr/bin/env python

import ConfigParser

conf = ConfigParser.ConfigParser()

conf.read('/etc/nova/nova.conf')

state_path = conf.get('DEFAULT', 'state_path')


if state_path.endswith('/'):
    tmp = state_path + 'instances'
else:
    tmp = state_path +'/instances'



print tmp

file='/var/lib/nova/instances/0732732b-fcca-4558-b77b-44d440eb5208/console.log'
with open(file) as fh:
    rlt = fh.read().split('\n')
    for i in rlt:
        if "ci-info" in i:
            print i
