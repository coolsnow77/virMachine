#!/usr/bin/env python
import libvirt
import pprint

import sys
print  sys.path
conn = libvirt.openReadOnly(None)

p = conn.lookupByName('instance-0000000c')

pprint.pprint(dir(p))


for id in conn.listDomainsID():
    dom = conn.lookupByID(id)
    infos = dom.info()
    print "ID = %d" %id
    print 'Name =  %s' % dom.name()
    print 'State = %d' % infos[0]
    print 'Max Memory = %d' % infos[1]
    print 'Number of virt CPUs = %d' % infos[3]
    print 'CPU Time (in ns) = %d' % infos[2]
    print ' '
