#!/usr/bin/env python
# coding: utf-8

from  phyBase import PhyBase

class PhyMetrics(PhyBase):
    ''' get physical machine & vm resources utilization
    '''

    def __init__(self, hostip=None): 
        super(PhyMetrics,self).__init__(hostip=hostip)
        self.hid = self.getHostId(hostip)
        # print 'init funcation hostip value', self.hostip
    

    def  getCpuSystemUtil(self):
        " get system cpu util info "
        cpusysutil = self.getLastValue(self.hid, 'system.cpu.util[,system]')
        return cpusysutil
    
    def getPeriodCpuSystemUtil(self,timeFrom,timeUntil):
        " get one period  cpu system  info"
        periodCpuSys = self.getPeriodValue(self.hid, 'system.cpu.util[,system]',
                                                        timeFrom, timeUntil)
        return periodCpuSys
        
    def getPeriodCpuIdleUtil(self,timeFrom, timeUntil):
        " get period  cpu  idle  util"
        periodCpuIdle = self.getPeriodValue(self.hid, 'system.cpu.util[,idle]',
                                                        timeFrom, timeUntil)
        return periodCpuIdle

    def getCpuUserUtil(self):
        " 获取用户占用cpu 信息 "
        cpuuserutil = self.getLastValue(self.hid, 'system.cpu.util[,user]')
        return cpuuserutil

    def getCpuIdleUtil(self):
        " get idle cpu info "
        cpuidleutil = self.getLastValue(self.hid, 'system.cpu.util[,idle]')
        return cpuidleutil

    def getCpuDiskIOUtil(self):
        " get disk io load info "
        cpudiskioutil = self.getLastValue(self.hid, 'system.cpu.util[,iowait]')
        return cpudiskioutil
    
    def getProcessLoad1min(self, ):
        " get process load in average 1 min "
        processload1min = self.getLastValue(self.hid, 'system.cpu.load[percpu,avg1]')
        return processload1min
    
    def getProcessLoad5min(self, ):
        " get process load in average 5 min"
        processload5min = self.getLastValue(self.hid, 'system.cpu.load[percpu,avg5]')
        return processload5min
    
    def getProcessLoad15min(self, ):
        " get process load in average 15 min"
        processload15min = self.getLastValue(self.hid, 'system.cpu.load[percpu,avg15]')
        return processload15min
    
    def getMonitorKeys(self):
        ' get monitor key by host id'
        rlt = self.getMonitorKeyByHostid(self.hid)
        mkeys = [v['key_'] for v in rlt]
        return mkeys
    
    def getValueByMonitorKey(self,  mkey=None):
        " get Value by Monitor Key"
        v = self.getLastValue(self.hid, mkey)
        return v
    
    def getTrendsValue(self, mkey, timeFrom, timeEnd):
        """get one time  periods values 
        @param mkey, monitor key
        @param timeFrom,  start timestamp
        @param timeEnd,  end timestamp
        """
        timeFrom = int(timeFrom)
        timeEnd = int(timeEnd)
        #print type(timeFrom), timeFrom, timeEnd
        if (timeEnd - timeFrom) < 10800:  
            # 3h = 10800 
            v = self.getPeriodValue(self.hid, mkey, timeFrom, timeEnd)
            return v
        else:
            #print "goes here!", mkey
            v = self.getPeriodValue2(self.hid, mkey, timeFrom, timeEnd)
            return v
    
    def getMonitorKeyDescription(self):
        """ description  the monitor key
        """
        ks = self.getMonitorKeys()
        kmap = { k: {'description':k} for k in ks}
        return kmap 
    
    def __repr__(self):
        #return ('<PhyMetrics  %s>') %(getattr(self,'cpusyskey', 'unknown'))
        return ('%s %r') %(self.__class__.__name__, self.__dict__)
       
    
if __name__ == '__main__':
    #t = PhyMetrics(hostip='10.66.49.19', areaid=1000)
    #t = PhyMetrics(hostip='10.66.49.19')
    #hhhhoo=[u'10.66.49.17', u'10.66.49.18', u'10.66.49.19', u'10.66.49.20', u'10.66.49.21', u'10.66.49.22', u'10.66.49.23', u'10.66.49.24', u'10.66.49.25', u'10.66.49.26', u'10.66.49.33', u'10.66.49.34', u'10.66.49.35', u'10.66.49.36', u'10.66.49.37', u'10.66.49.38', u'10.66.49.65', u'10.66.49.66', u'10.66.49.67', u'10.66.49.68', u'10.66.49.69', u'10.66.49.70', u'10.66.49.71', u'10.66.49.72', u'10.66.49.73', u'10.66.49.74', u'10.66.49.75', u'10.66.49.76', u'10.66.49.77', u'10.66.49.78', u'10.66.49.79', u'10.66.49.80', u'10.66.49.81', u'10.66.49.82', u'10.66.49.83', u'10.66.49.84', u'10.66.49.85', u'10.66.49.86', u'10.66.49.87', u'10.66.49.88', u'10.66.49.129', u'10.66.49.130', u'10.66.49.131', u'10.66.49.132', u'10.66.49.133', u'10.66.49.134', u'10.66.49.135', u'10.66.49.136', u'10.66.49.137', u'10.66.49.138', u'10.66.49.139', u'10.66.49.140', u'10.66.49.141', u'10.66.49.142', u'10.66.49.143', u'10.66.49.144', u'10.66.49.145', u'10.66.49.146', u'10.66.49.147', u'10.66.49.148', u'10.66.49.149', u'10.66.49.150', u'10.66.49.151', u'10.66.49.152', u'10.66.49.153', u'10.66.49.154', u'10.66.49.155', u'10.66.49.156', u'10.66.49.157', u'10.66.49.158', u'10.66.49.159', u'10.66.49.160', u'10.66.49.161', u'10.66.49.162', u'10.66.49.163', u'10.66.49.164', u'10.66.49.165', u'10.66.49.166', u'10.66.49.167', u'10.66.49.168', u'10.66.49.169', u'10.66.49.170', u'10.66.49.171', u'10.66.49.172', u'10.66.49.173', u'10.66.49.174', u'10.66.49.175', u'10.66.49.176', u'58.211.121.114', u'172.18.10.194', u'172.18.10.161', u'172.18.10.193', u'172.18.10.135', u'172.18.10.132', u'172.18.10.130', u'172.18.10.131', u'172.18.10.134', u'221.233.60.163', u'61.155.215.91', u'172.18.10.129', u'10.66.49.2', u'10.66.49.8', u'172.18.10.133', u'172.18.10.136']
    #
    #for h in hhhhoo:
    #    if h.startswith("10.66.49"):
    #        t=PhyMetrics(hostip=h)
    #        print h, t.getProcessLoad15min()
    t = PhyMetrics(hostip='10.66.32.19')
    print(t.getMonitorKeyDescription())
    import sys; sys.exit("over......")
    t = PhyMetrics(hostip='10.66.49.176')
    #t = PhyMetrics(hostip='192.168.43.203')
    import datetime, time,sys
    t1 = t.date2Timestamp("2014-11-19 16:00:00")
    t2 = int(time.time())
    print t1, t2
    #sys.exit(1)
    #print t.getPeriodCpuSystemUtil(t1, t2)
    #print t.getPeriodCpuIdleUtil(t.date2Timestamp("2014-10-15 01:00:00"), t.date2Timestamp("2014-10-15 17:00:00"))
    print t.getProcessLoad1min()
    print t.getProcessLoad5min()
    print t.getProcessLoad15min()
    for memethod in dir(t):
        if memethod.startswith("getCpu"):
            t11  = "t."+ str(memethod) + "()"
            print str(memethod), eval(t11)
    print t.getMonitorKeys()
    for k in t.getMonitorKeys():
        print k
        # print t.getValueByMonirotKey(k)
        # print t.getTrendsValue(k['key_'], t1, t2)
