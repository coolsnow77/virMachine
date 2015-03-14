# coding: utf-8
'''
Created on 2014年10月20日

@author: cuimingwen
'''

import time
import datetime
from virBase import VirBase, VirOtherHandle


class VirNovaUtil(VirBase):
    '''
    classdocs
    '''


    def __init__(self, resource_id=None):
        '''
        Constructor
        '''
        super(VirNovaUtil,self).__init__(resource_id=resource_id)
        self.resource_id = resource_id
        self._ovirMem = VirOtherHandle()
    
    def getCpuUsedTime(self, mkey='cpu'):
        ' CPU time used'
        rlt = self.getMeterSampleByName(mkey=mkey)
        return rlt        
    
    def getVcpus(self, mkey='vcpus'):
        ' Number of VCPUs'
        rlt = self.getMeterSampleByName(mkey=mkey)
        return rlt
        
    def getCpuUtil(self, mkey='cpu_util'):
        ' Average CPU utilisation'
        rlt = self.getMeterSampleByName(mkey=mkey)
        return rlt 
    
    def getPeriodCpuUtil(self, mkey='cpu_util', timestampFrom=None, timestampEnd=None):
        ' get period cpu util'
        prlt = self.getPeriodMeterSample(mkey= mkey, timeFrom=timestampFrom, timeEnd=timestampEnd)
        return prlt
    
    def getMemory(self, mkey='memory'):
        ''' Volume of RAM allocated in KB
        @param  rss: unused memory  KB
        '''
        
        #rlt = self.getMeterSampleByName(mkey=mkey)
        #return rlt
        rlt = self._ovirMem
        mRes = rlt.get_memory_by_uuid(self.resource_id)
        return mRes

    def getMemoryUsage(self, mkey='memory.usage'):
        ' Volume of RAM used in MB'
        #rlt = self.getMeterSampleByName(mkey=mkey)
        #return rlt
        m = self.getMemory()
        if m is None:
            print "there is no monitor_item:%s"%mkey
            return -1
        #intTime= m['timestamp']
        #mT = float(m['memTotal'])
        #mR = m['memRss']
        #mUsage = float("%.4f"%(mR/mT * 100))
        #utcStrT = datetime.datetime.utcfromtimestamp(intTime)
        #utcSTR = str(utcStrT).replace(' ', 'T')   
        #return [{'timestamp':utcSTR, 'counter_name': u'memory.usage', 
        #        'counter_unit':u'%', 'counter_volume':mUsage}]  
        return {'unusage': m['memRss'], 'timestamp':m['timestamp'],
                  'total': m['memTotal']}   
                 
    def getDiskReadBytes(self, mkey='disk.read.bytes'):
        ' Volume of reads in B per device (cumulative)'
        rlt = self.getMeterSampleByName(mkey=mkey)
        return rlt
    
    def getDiskReadBytesRate(self, mkey='disk.read.bytes.rate'):
        ' Average rate of reads in B per second per device (gauge)'
        rlt = self.getMeterSampleByName(mkey=mkey)
        return rlt
        
    def getDiskReadRequests(self, mkey='disk.read.requests'):
        ' Number of read requests'
        
    def getDiskReadRequestsRate(self, mkey='disk.read.requests.rate'):
        ' Average rate of read requests per second'
        rlt = self.getMeterSampleByName(mkey=mkey)
        return rlt        
    
    def getDiskWriteBytes(self, mkey='disk.write.bytes'):
        'Volume of writes in B'
        rlt = self.getMeterSampleByName(mkey=mkey)
        return rlt
    
    def getDiskWriteBytesRate(self, mkey='disk.write.bytes.rate'):
        ' Average volume of writes in B per second'
        rlt = self.getMeterSampleByName(mkey=mkey)
        return rlt
    
    def getDiskWriteRequests(self, mkey='disk.write.requests'):
        ' Number of write requests'
        rlt = self.getMeterSampleByName(mkey=mkey)
        return rlt
            
    def getDiskWriteRequestsRate(self, mkey='disk.write.requests.rate'):
        ' Average rate of write requests per second'
        rlt = self.getMeterSampleByName(mkey=mkey)
        return rlt        
        
    def getNetworkInBytes(self, mkey='network.incoming.bytes'):
        'Number of incoming bytes on a VM network interface'
        rlt = self.getMeterSampleByName(mkey=mkey)
        return rlt
    
    def getNetworkInBytesRate(self):
        ' network.incoming.bytes.rate  type:(g), unit: B/s'
        #rlt = self.getMeterSampleByName(mkey=mkey)
        #return rlt
        resID = self._ovirMem.get_interUUID_by_uuid(self.resource_id)['interUUID']
        virNetObj = VirNetworkBandHandle(resID)
        rlt = virNetObj.getNetworkInBytesRate()
        return rlt        
    
    
    def getNetworkOutBytes(self, mkey='network.outgoing.bytes'):
        'Number of outgoing bytes on a VM network interface'
        rlt = self.getMeterSampleByName(mkey=mkey)
        return rlt
    
    def getNetworkOutBytesRate(self):
        ''' Average rate per sec of outgoing bytes on a VM network interface
            type:(g)  unit: B/s
        '''
        resID = self._ovirMem.get_interUUID_by_uuid(self.resource_id)['interUUID']
        virNetObj = VirNetworkBandHandle(resID)
        rlt = virNetObj.getNetworkOutBytesRate()
        return rlt
        
    def getDiskRootSize(self, mkey='disk.root.size'):
        ' Size of root disk in bytes'
        rlt = self.getMeterSampleByName(mkey=mkey)
        return rlt 
        #=======================================================================
        # rlt = self._ovirMem
        # mRes = rlt.get_disk_by_uuid(self.resource_id)
        # return mRes   
        # 
        #=======================================================================
    #cut it
    def getDiskUsage2(self, mkey='disk.ephemeral.size'):
        ' disk  root  usage '
        rlt = self.getMeterSampleByName(mkey = mkey)
        return rlt
    
    def getDiskUsage(self):
        ' get disk usage '
        rlt = self._ovirMem
        dRlt = rlt.get_disk_by_uuid(self.resource_id)
        return dRlt
        
    
    def getInstance(self, mkey='instance'):
        ' Existence of instance, 云主机存在时间'
        rlt = self.getMeterSampleByName(mkey=mkey)
        return rlt 
    
    def getDaysSample(self,timeFrom=None, timeEnd=None,  
                                  mkey=None, days=1):
        """  get defined days sample  meter 
            @param timeFrom,  start timestamp
            @param timeEnd, end timestamp
            @param mkey, monitor key
            @param days,  date periods
        """

        if (timeFrom is not None) and (timeEnd is not None):
            mysubstract = (int(timeEnd) - int(timeFrom))
            if mysubstract >86400:
                period = 86400
            elif mysubstract < 0:
                timeFrom = timeEnd
                timeEnd = timeFrom
                period = abs(mysubstract) / 3
            else:
                period = abs(mysubstract) / 3
            prlt = self.getPeriodMeterStatistics(mkey=mkey, timeFrom=timeFrom, 
                                                 timeEnd=timeEnd, period=period)
            return prlt        
        
        period=86400
        te = int(time.time())
        days = int(days)
        if days == 1:
            tf = (int(time.time()) - days*24*60*60)
            period = 21600
        elif days == 7:
            tf = (int(time.time()) - days*24*60*60)
        elif days == 15:
            tf = (int(time.time()) - days*24*60*60)
        elif days == 30:
            tf = (int(time.time()) - days*24*60*60)
        elif days == 365:
            tf = (int(time.time()) - days*24*60*60)
        else:
            tf = (int(time.time()) - 1*24*60*60)
            
        prlt = self.getPeriodMeterStatistics(mkey=mkey, timeFrom=tf, 
                                            timeEnd=te, period=period)
        return prlt
    
    
    def getTrendsData(self,timeFrom=None, timeEnd=None, mkey=None, days=1):
        """ get history  data  by  date 
             @param mkey,  monitor key
             @param days,  default days for one day
             @param timeFrom, start timestamp
             @param timeEnd, end timestamp 
        """
        dataV = self.getDaysSample(timeFrom, timeEnd, mkey, days)
        return dataV
    
    def getInstanceCore(self, mkey='instance:core1'):
        'Existence of instance <type> (openstack types)'
        rlt = self.getMeterSampleByName(mkey=mkey)
        return rlt         

    def getAllMeters(self):
        'get all meters  '
        rlt = self.getResIdAndMeter()
        return rlt  
    
    def getValueByKey(self, mkey=None):
        """ get sample  from  monitor key 
            @param mkey, moitor key item
        """
        if mkey == 'network.outgoing.bytes.rate':
            Rlt = self.getNetworkOutBytesRate()
        elif mkey == 'network.incoming.bytes.rate':
            Rlt = self.getNetworkInBytesRate()
        elif mkey == 'memory.usage':
            Rlt = self.getMemoryUsage()
        elif mkey == 'disk.usage':
            Rlt = self.getDiskUsage()
        else:
            Rlt = self.getMeterSampleByName(mkey=mkey)
        return Rlt   
    
         
class VirNetworkBandHandle(VirBase):
    def __init__(self, resource_id=None):
        '''
        Constructor
        '''
        super(VirNetworkBandHandle,self).__init__(resource_id=resource_id)
        self.resource_id = resource_id    
    
    def getNetworkOutBytesRate(self, mkey='network.outgoing.bytes.rate'):
        ''' Average rate per sec of outgoing bytes on a VM network interface
            type:(g)  unit: B/s
        '''
        rlt = self.getMeterSampleByName(mkey=mkey)
        return rlt
    
    def getNetworkInBytesRate(self, mkey='network.incoming.bytes.rate'):
        ' network.incoming.bytes.rate  type:(g), unit: B/s'
        rlt = self.getMeterSampleByName(mkey=mkey)
        return rlt
        
        
if __name__ =='__main__':
    from time import mktime, strptime
    def dt2ts(date):
        ts = int(mktime(strptime(date, "%Y-%m-%d %H:%M:%S")))
        return ts
        
    import sys, pprint
    t = VirNovaUtil(resource_id='572e2069-1d61-4e0a-9a7d-fc9e726c22cb')
    #t = VirNovaUtil(resource_id='nova-instance-instance-00000001-fa163ede05c5')
    #t = VirNovaUtil(resource_id='nova-instance-instance-0000000c-fa163e2d3e17')
    print t.getNetworkOutBytesRate()
    print t.getNetworkInBytesRate()
    #sys.exit(0)
    #pprint.pprint( t.getAllMeters())
    #sys.exit(0)
    print t.getDiskReadBytes()
    print t.getCpuUsedTime()
    print "cpu util", t.getCpuUtil()
    #pprint.pprint( t.getAllMeters())
    print t.getDiskReadBytesRate()
    print t.getNetworkInBytesRate()
    print "disk size", t.getDiskRootSize()
    print "disk usage", t.getDiskUsage()
    print "cpu util, ", t.getCpuUtil()
    print "memory:", t.getMemory()
    print "mem_usage:", t.getMemoryUsage() # some trouble problem 
    print t.getVcpus()
    print t.getInstance()
    print t.getInstanceCore()
    print t.getDiskReadRequestsRate()
    #print t.getDiskWriteRequestsRate()
    #print t.getNetworkInBytes()
    #print t.getNetworkInBytesRate()
    #print t.getNetworkOutBytes()
    #print t.getNetworkOutBytesRate()
    print "***********"  * 10
    #import datetime, time
    tf =dt2ts('2014-11-19  00:00:00')
    #tf = 1413275644
    #te = 1414049753
    te = dt2ts('2014-11-20  15:15:00')
    
    print tf, te
    #myInsta = MetersAggregate('572e2069-1d61-4e0a-9a7d-fc9e726c22cb')
    #print myInsta.allKeys
    #print t.getPeriodCpuUtil(timestampFrom=tf, timestampEnd=te)
    meterKs = t.getMeterNameByResId('572e2069-1d61-4e0a-9a7d-fc9e726c22cb')
    #print t.getDaysSample('cpu_util', 1)
    #print t.getDaysSample('disk.read.requests.rate', 1)
    print meterKs
    for k in meterKs:
        print k
        print t.getValueByKey(k)
        print t.getTrendsData(mkey=k, timeFrom = tf, timeEnd = te, days=1)

    
        
        