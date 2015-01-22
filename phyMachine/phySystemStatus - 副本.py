#!/usr/bin/env python
# coding: utf-8
# cut  this  class never used 

from phyBase import PhyBase

class PhySystemStatus(PhyBase):
    """ get physical server system uptime,
        disk, memory info
    """
    
    def __init__(self,hostip=None):
        super(PhySystemStatus, self).__init__( hostip=hostip)
        self.hid = self.getHostId(hostip)
        
    def getPhyTotalRootDiskSize(self):
        " get physical disk  / total size  "
        diskrootsize = self.getLastValue(self.hid, 'vfs.fs.size[/,total]')
        return diskrootsize
    
    def getPhyTotalDataDiskSize(self):
        " get physical disk /bakdata total size"
        diskbakdatasize = self.getLastValue(self.hid, 'vfs.fs.size[/bakdata,total]')
        return diskbakdatasize
    
    
    def getPhyAvailableRootDiskSize(self):
        " get / available  disk  size "
        diskrootavailsize = self.getLastValue(self.hid, 'vfs.fs.size[/,free]')
        return diskrootavailsize
    
    def getPhyAvailRootDiskPercent(self):
        "available /  disk  percentage"
        pfreedisk = self.getLastValue(self.hid, 'vfs.fs.size[/,pfree]')
        return pfreedisk
    
    def getPhyAvailDataDiskPercent(self):
        " available /bakdata disk percentage"
        pfreedata = self.getLastValue(self.hid, 'vfs.fs.size[/bakdata,pfree]')
        return pfreedata
    
    def getPhyTotalMemory(self):
        " system  total memory"
        summemory = self.getLastValue(self.hid, 'vm.memory.size[total]')
        return summemory
    
    def getPhyAvailMemory(self):
        " system  available memory"
        freememory = self.getLastValue(self.hid, 'vm.memory.size[available]')
        return freememory
    
    def getPhySystemUptime(self):
        " system  runtime  without  restart "
        uptimeStamp = self.getLastValue(self.hid, 'system.uptime')
        return uptimeStamp
    
    def getPhySystemLocaltime(self):
        " 获取系统当前时间 "
        syslocaltime = self.getLastValue(self.hid, 'system.localtime')
        return syslocaltime
    
    def getPhySystemLoggedInUser(self):
        " 获取系统当前登陆用户数目"
        loggeduser = self.getLastValue(self.hid, 'system.users.num')
        return loggeduser
    
    def getPhySystemMaxOFile(self):
        " 获取系统当前最大打开文件数"
        mofile = self.getLastValue(self.hid, 'kernel.maxfiles')
        return mofile
    
    def getPhySystemMaxProcesses(self):
        " 获取系统当前最大进程数限制"
        mprocess = self.getLastValue(self.hid, 'kernel.maxproc')
        return mprocess
    
    def getPhyAllHosts(self):
        " get all host ip address "
        hosts = self.getAllHost()
        return hosts
    
    def getPhyNetworkIn(self):
        " get network inbound  byte"
        ntIn = self.getLastValue(self.hid, 'net.if.in[eth1,]')
        return ntIn
    
    def getPhyNetworkOut(self):
        "get network outbound byte"
        ntOut = self.getLastValue(self.hid, 'net.if.out[eth1,]')
        return ntOut
    
    def getPhyNetworkTotal(self):
        "get network total  bandwidth bytes"
        ntTotal = self.getLastValue(self.hid, 'net.if.total[eth1,]')
        return ntTotal
    
    def getPhyAgentPing(self):
        " get agent ping "
        agentP = self.getLastValue(self.hid, 'agent.ping')
        return agentP
    
    def getPhyMd5Passwd(self):
        " get md5 passwd "
        md5P = self.getLastValue(self.hid, 'vfs.file.cksum[/etc/passwd]')
        return md5P
    
    def getPhyMySQLBeginOper(self):
        " MySQL begin operations per second"
        myBeOp = self.getLastValue(self.hid, 'mysql.status[Com_begin]')
        return myBeOp
    
    def getPhyMySQLBytesReceive(self):
        " MySQL bytes received per second"
        mByteRec = self.getLastValue(self.hid, 'mysql.status[Bytes_received]')
        return mByteRec
    
    def getPhyMySQLBytesSent(self):
        " MySQL bytes sent per second"
        mSent = self.getLastValue(self.hid, 'mysql.status[Bytes_sent]')
        return mSent
    
    def getPhyMySQLCommit(self):
        " MySQL commit operations per second"
        mCommit = self.getLastValue(self.hid, 'mysql.status[Com_commit]')
        return mCommit
    
    def getPhyMySQLDelete(self):
        " MySQL delete operations per second"
        mDel = self.getLastValue(self.hid, 'mysql.status[Com_delete]')
        return mDel
    
    def getPhyMySQLInsert(self):
        " MySQL insert operations per second"
        mInsert = self.getLastValue(self.hid, 'mysql.status[Com_insert]')
        return mInsert
    
    def getPhyMySQLSelect(self):
        " MySQL select operations per second"
        mSelect = self.getLastValue(self.hid, 'mysql.status[Com_select]')
        return mSelect
    
    def getPhyMySQLSlowQuery(self):
        " MySQL slow queries"
        mSlowQuery = self.getLastValue(self.hid, 'mysql.status[Slow_queries]')
        return mSlowQuery
    
    def getPhyMySQLUpdate(self):
        " MySQL update operations per second"
        mUpdate = self.getLastValue(self.hid, 'mysql.status[Com_update]')
        return mUpdate
    
    def getPhyMySQLStatus(self):
        " MySQL status"
        mStatus = self.getLastValue(self.hid, 'mysql.ping')
        return mStatus
    
    def getPhyMySQLUptime(self):
        " MySQL uptime"
        mUptime = self.getLastValue(self.hid, 'mysql.status[Uptime]')
        return mUptime
    
    def getPhyMySQLVersion(self):
        " MySQL version"
        mVersion = self.getLastValue(self.hid, 'mysql.version')
        return mVersion
    
    def getPhyMySQLRollback(self):
        " MySQL rollback operations per second"
        mRollBack = self.getLastValue(self.hid, 'mysql.status[Com_rollback]')
        return mRollBack
    
    def getPhyCommonStatus(self, mkey):
        " get physical common service "
        cs = self.getLastValue(self.hid, mkey)
        return cs
    
    
    def getMonitorExtendDefine(self):
        " other  self define methods  "
        pass
    
    def __repr__(self):
        ' repr  function '
        return ('%s %r') %(self.__class__.__name__, self.__dict__)
    
if __name__ == '__main__':
    #t= PhySystemStatus(hostip='10.66.49.8')
    #print t.getPhyMySQLStatus(), t.getPhyMySQLUptime(), t.getPhyMySQLSelect()
    #t = PhySystemStatus(hostip='192.168.43.203')
    t = PhySystemStatus(hostip='10.66.49.19')
    #print t.getPhyNetworkIn(), t.getPhyNetworkOut(), t.getPhyNetworkTotal()
    
    #t = PhySystemStatus(hostip='10.66.49.17')
    #t = PhySystemStatus(hostip='192.168.43.203')
    print t.getPhyAllHosts()
    print t.getPhyTotalRootDiskSize()
    print t.getPhyAvailableRootDiskSize()
    print t.getPhyAvailRootDiskPercent()
    print t.getPhyAvailDataDiskPercent()
    print t.getPhyTotalMemory()
    print t.getPhyAvailMemory()
    print t.getPhySystemUptime()
    print t.getPhySystemLocaltime()
    print t.getPhySystemLoggedInUser()
    print t.getPhySystemMaxOFile()
    print t.getPhySystemMaxProcesses()
    print t.getPhyNetworkTotal()
    print t.getPhyNetworkIn()
    print t.getPhyNetworkOut()
    print t.getPhyAgentPing()
    print t.getPhyMd5Passwd()
    
    
#===============================================================================
#     hhhhoo=[u'10.66.49.8', u'10.66.49.17', u'10.66.49.18'] #, u'10.66.49.19', u'10.66.49.20', u'10.66.49.21', u'10.66.49.22', u'10.66.49.23', u'10.66.49.24', u'10.66.49.25', u'10.66.49.26', u'10.66.49.33', u'10.66.49.34', u'10.66.49.35', u'10.66.49.36', u'10.66.49.37', u'10.66.49.38', u'10.66.49.65', u'10.66.49.66', u'10.66.49.67', u'10.66.49.68', u'10.66.49.69', u'10.66.49.70', u'10.66.49.71', u'10.66.49.72', u'10.66.49.73', u'10.66.49.74', u'10.66.49.75', u'10.66.49.76', u'10.66.49.77', u'10.66.49.78', u'10.66.49.79', u'10.66.49.80', u'10.66.49.81', u'10.66.49.82', u'10.66.49.83', u'10.66.49.84', u'10.66.49.85', u'10.66.49.86', u'10.66.49.87', u'10.66.49.88', u'10.66.49.129', u'10.66.49.130', u'10.66.49.131', u'10.66.49.132', u'10.66.49.133', u'10.66.49.134', u'10.66.49.135', u'10.66.49.136', u'10.66.49.137', u'10.66.49.138', u'10.66.49.139', u'10.66.49.140', u'10.66.49.141', u'10.66.49.142', u'10.66.49.143', u'10.66.49.144', u'10.66.49.145', u'10.66.49.146', u'10.66.49.147', u'10.66.49.148', u'10.66.49.149', u'10.66.49.150', u'10.66.49.151', u'10.66.49.152', u'10.66.49.153', u'10.66.49.154', u'10.66.49.155', u'10.66.49.156', u'10.66.49.157', u'10.66.49.158', u'10.66.49.159', u'10.66.49.160', u'10.66.49.161', u'10.66.49.162', u'10.66.49.163', u'10.66.49.164', u'10.66.49.165', u'10.66.49.166', u'10.66.49.167', u'10.66.49.168', u'10.66.49.169', u'10.66.49.170', u'10.66.49.171', u'10.66.49.172', u'10.66.49.173', u'10.66.49.174', u'10.66.49.175', u'10.66.49.176', u'58.211.121.114', u'172.18.10.194', u'172.18.10.161', u'172.18.10.193', u'172.18.10.135', u'172.18.10.132', u'172.18.10.130', u'172.18.10.131', u'172.18.10.134', u'221.233.60.163', u'61.155.215.91', u'172.18.10.129', u'10.66.49.2', u'10.66.49.8', u'172.18.10.133', u'172.18.10.136']
# 
#     for h in hhhhoo:
#         if h.startswith("10.66.49"):
#             " shift +Tab (left), Tab(Right)"
#             t = PhySystemStatus(hostip=h)
#             print h, (t.getPhyTotalRootDiskSize(),t.getPhyAvailRootDiskPercent(),t.getPhyNetworkIn(),
#                       t.getPhyAgentPing(), t.getPhyMd5Passwd())
#                     #t.getPhyTotalDataDiskSize(), t.getPhyAvailDataDiskPercent())
#===============================================================================

     

