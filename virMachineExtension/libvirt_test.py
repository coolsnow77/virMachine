#!/usr/bin/env  python
# coding: utf-8
# python-libvirt   installed

import sys
import time
import libvirt
import xmltodict
import getDiskPar


class MyLibvirt(object):
    """ my libvirt  utils """
    
    
    def __init__(self):
        self.conn = self.get_connection()
        self.mytimeStamp = int(time.time())
        self.diskObj = getDiskPar.GetVirDiskPar()
    
    def get_connection(self):
        " get connection "
        conn = libvirt.openReadOnly(None)
        if conn is None:
            print "Failed to open connection to QEMU libvirt"
            return -1
        else:
            return conn
    
    def get_alive_status(self):
        if self.conn == -1:
            return -1
        else:
            return self.conn.isAlive()
    

    
    def get_list_domain_id(self):
        if self.conn == -1:
            return -1
        else:
            domIDs = self.conn.listDomainsID()
            return domIDs
        
    def get_memory(self):
        mList = []
        dList = self.get_list_domain_id()
        for domID in dList:
            myDomain = self.conn.lookupByID(domID)
            uuidStr = myDomain.UUIDString()
            meminfo = myDomain.memoryStats()
            mList.append({'uuidString':uuidStr, 'memory':meminfo,
                          'lasttime':self.mytimeStamp})
        return mList
    
    def get_disk_info2(self):
        diskInfo = []
        dI = self.get_list_domain_id()
        for did in dI:
            myDom = self.conn.lookupByID(did)
            uuidStr = myDom.UUIDString()
            diskRlt = self.get_path_by_name(uuidStr)
            if diskRlt != -1:
                dP = diskRlt['diskPath']
                diskStat = myDom.blockInfo(dP)
                #interfaceStat = myDom.interfaceStats(iPath)
                diskInfo.append({'uuidString':uuidStr, 'disk':{'Capacity':diskStat[0],
                                'usage':diskStat[2]},'lasttime': self.mytimeStamp})
        return diskInfo
    
    def get_disk_info(self):
        diskInfo = []
        dI = self.get_list_domain_id()
        for did in dI:
            myDom = self.conn.lookupByID(did)
            uuidStr = myDom.UUIDString()
            diskRlt = self.diskObj.get_disk_partion(did)
            if diskRlt != -1:
                diskInfo.append({'uuidString':uuidStr, 'disk':{'Capacity':int(diskRlt[0]),
                                'usage':int(diskRlt[1])},'lasttime': self.mytimeStamp})
        return diskInfo
  
    
    def get_interface_bandwidth(self):
        interfaceInfo=[]
        dI = self.get_list_domain_id()
        for did in dI:
            myDom = self.conn.lookupByID(did)
            uuidStr = myDom.UUIDString()
            interfaceRlt = self.get_path_by_name(uuidStr)
            if  interfaceRlt != -1:
                intP = interfaceRlt['interfacePath']
                interStat = myDom.interfaceStats(intP)
                interfaceInfo.append({'uuidString':uuidStr, 'interface':{'inputBandW':interStat[0],
                                'outputBandW':interStat[4]},'lasttime': self.mytimeStamp})
        return interfaceInfo   
    
    def get_path_by_name(self, uuidStr):
        for d in self.get_disk_path():
            if uuidStr in d:
                return d[uuidStr]
        return -1
                    
    def get_disk_path(self):
        diskL = []
        for d in self.get_list_domain_id():
            myDom = self.conn.lookupByID(d)
            uuidStr = myDom.UUIDString()
            xmlStr = myDom.XMLDesc()
            rlt = dict(xmltodict.parse(xmlStr)['domain'])
            dPath = dict(rlt['devices']['disk'])['target']['@dev']
            interPath=dict(rlt['devices']['interface'])['target']['@dev']
            interfaceRef=dict(rlt['devices']['interface'])['filterref']['@filter']
            diskL.append({uuidStr:{'diskPath':dPath, 'interfacePath':interPath}, 
                          'interRef':interfaceRef})
        result = diskL
        return result
                    
    def __del__(self):
        " close connection "
        try:
            self.conn.close()
        except ValueError:
            print "close connection failed"        

if  __name__ == '__main__':
    t = MyLibvirt()
    print t.get_memory()
    print t.get_disk_info()
    print t.get_disk_info2()
    print t.get_disk_path()
    print t.get_interface_bandwidth()
