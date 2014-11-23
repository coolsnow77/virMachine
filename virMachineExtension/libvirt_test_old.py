#!/usr/bin/env  python
# coding: utf-8
# python-libvirt   installed

import libvirt

import sys

def createConnection():
    "  connection "    
    conn = libvirt.openReadOnly(None)
    if conn == None:
        print "Failed to open connection to QEMu/KVM"
        sys.exit(1)
    else:
        print "connection is created successfully!"
        return conn


def closeConnection(conn):
    print " close  conn"
    try:
        conn.close()
    except:
        print "Failed to close the connection"
    else:
        print "Connection is closed"
        return 1

def getMACAddress(conn):
    print  " get mac  address" 
    try:
        rlt = libvirt.virInterface(conn)
    except:
        print  "vir interface  error"
    else:
        mac = rlt.MACString()
        return mac
        


def getDomInfoByName(conn, name):
    print "get domain info by name "
    try:
        #myDom = conn.lookupByName(name)
        myDom = conn.lookupByUUIDString(name)
    except:
        print 'Failed to find the domain with name"%s"'%name
        return 1
    else:
        #print dir(myDom)
        #print help(myDom)
        print myDom.vcpus()
	print myDom.memoryParameters()
        #print myDom.memoryPeek()
        #print myDom.listInterfaces()
        #print myDom.listNetworks()
        print "uuid: %s" % myDom.UUIDString()
	print "interfaceStat: rx bytes, rx drop pack, tx bytes,  tx pack " , myDom.interfaceStats('vnet0')
        #print "block stats: %s" %myDom.blockStats()
        print "cpu  stats: %s" %myDom.getCPUStats('CPU0')
        print "Dom id: %d name: %s" %(myDom.ID(), myDom.name())
        print "Dom  state: %s" %myDom.state(0)
        print "Dom info: %s" % myDom.info()
        print "Memory: %d MB" %(myDom.maxMemory()/1024)
        print "memory status: %s" %myDom.memoryStats()
        print "vCPUs: %s" % myDom.maxVcpus()

def getDomInfoByID(conn, id):
    print " get domain info by ID "
    try:
        myDom = conn.lookupByID(id)
    except:
        print "Failed to find the domain with ID, %d" %id
        return 1
    else:
        print "Domain id is %d; Name is %s" %(myDom.ID(), myDom.name())

if  __name__ == '__main__':
    #name1 = 'instance-0000000c'
    name1 = '572e2069-1d61-4e0a-9a7d-fc9e726c22cb'
    id = 2
    print " get domain info via libvirt python API "
    conn = createConnection()
    getDomInfoByName(conn, name1)
    getDomInfoByID(conn, id)
    closeConnection(conn)
    
    print  "****"* 7
    #print getMACAddress(createConnection)
    print  "****"* 7
