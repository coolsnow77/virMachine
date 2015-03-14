#!/usr/bin/env python
# coding: utf-8

from ZabbixAPI.phyCpuUtil import PhyCpuUtil
from ZabbixAPI.phySystemStatus import PhySystemStatus

class ICSMAPI(object):
    """ ICAMAPI """ 
    def __init__(self, hostip='10.66.49.19',): #areaid=1000):
        """areaid 1000 眉山
            areaid 2000 襄阳
            areaid 3000 昆山
            已经废弃不用区域id 了.
        """
        self.hostip = hostip
        #self.areaid = areaid
        self.instancePhyCpuUtil = PhyCpuUtil(hostip = self.hostip)
                                             #areaid = self.areaid) #easy error point
        self.instancePhySystemStat = PhySystemStatus(hostip=self.hostip)
                                                    # areaid= self.areaid)
    
    def getCpuSysUtil(self):
        " 获取物理机cpu系统使用率 "
        return self.instancePhyCpuUtil.getCpuSystemUtil()
    
    def getPhyCpuAllUtil(self):
        " 获取所有cpu 使用率的信息"
        return [{'cpusystem':self.instancePhyCpuUtil.getCpuSystemUtil()},
                {'cpuuser':self.instancePhyCpuUtil.getCpuUserUtil()},
                {'cpuidle': self.instancePhyCpuUtil.getCpuIdleUtil()},
                {'cpudiskio': self.instancePhyCpuUtil.getCpuDiskIOUtil()},
                {'cpuprocessload1min': self.instancePhyCpuUtil.getProcessLoad1min()},
                {'cpuprocessload5min': self.instancePhyCpuUtil.getProcessLoad5min()},
                {'cpuprocessload15min': self.instancePhyCpuUtil.getProcessLoad15min()}]
    
    def getPhyCpuMethodUti(self, cpumethod):
        " 根据cpu 方法获取相应的cpu 使用率"
        tmpMethod = 'self.instancePhyCpuUtil.' + cpumethod + '()'
        #print tmpMethod (ctrl +3 comment)
        return eval(tmpMethod)
    
    def getPhySystemInfo(self,systemmethod ):
        " 根据system stats 方法获取 相应系统信息"
        sysM = 'self.instancePhySystemStat.' + systemmethod + '()'
        return eval(sysM)
    
    def getPhyOther(self, ):
        " may  be  write a little"
        pass
    
    
if __name__ =='__main__':
    t = ICSMAPI(hostip = '10.66.49.19',) #areaid=1000)
    print t.getCpuSysUtil()
    print t.getPhyCpuAllUtil()
    print t.getPhyCpuMethodUti("getProcessLoad5min")
    print t.getPhySystemInfo("getPhySystemLocaltime")
