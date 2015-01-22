# coding: utf-8
'''
Created on 2014��11��4��

@author: cuimingwen
'''
import unittest
from phyCpuUtil import  *
from phySystemStatus import *


class TestBase(unittest.TestCase):
    '''
    classdocs
    '''
    def setUp(self):
        self.cpu = PhyCpuUtil(hostip='10.66.32.19')
        self.mysys = PhySystemStatus(hostip='10.66.32.19')
        
    def tearDown(self):
        pass

class PhyCpuUtilTest(TestBase):
    def setUp(self):
        super(PhyCpuUtilTest, self).setUp()
    
    def testgetProcessLoad1min(self):
        rlt = self.cpu.getProcessLoad1min()
        self.assertTrue(isinstance(rlt, dict), "Test getProcessLoad1min() error")

    def testgetValueByMonitorKey(self):
        rlt = self.cpu.getValueByMonitorKey('agent.ping')
        self.assertTrue(isinstance(rlt, dict), "Test getValueByMonitorKey() error")
    
    def testcreate_vm_monitor(self, vip=None, tpname='Template Libvirt VM Status'):
        "create  virtual ip address monitor"
        " before test , you must set vip value"
        vip = '10.66.32.69'
        rlt = self.cpu.create_vm_monitor(vip, 'Template Libvirt VM Status')
        self.assertTrue(isinstance(rlt, map),  "Test create_vm_monitor error")
        
    def testdelete_vm_monitor(self, vip=None):
        """
        Delete virtual monitor
        """
        vip = '10.66.32.69'
        rlt = self.cpu.delete_vm_monitor(vip)
        self.assertTrue(isinstance(rlt, map), "Test delete vm monitor error")

    def testGetMonitorKeys(self):
        rlt = self.cpu.getMonitorKeys()
        self.assertTrue(isinstance(rlt, list), "Test getMonitorKeys error!")
    
    def testgetProcessLoad5min(self):
        rlt = self.cpu.getProcessLoad5min()
        self.assertTrue(isinstance(rlt, dict), "test getProcessLoad5min error")
    
    def testgetProcessLoad15min(self):
        rlt = self.cpu.getProcessLoad15min()
        self.assertTrue(isinstance(rlt, dict), "Test getProcessLoad15min failed")
    
    def testgetCpuDiskIOUtil(self):
        rlt = self.cpu.getCpuDiskIOUtil()
        self.assertTrue(isinstance(rlt, dict), "test getCpuDiskIOUtil failed")
    
    def testgetCpuIdleUtil(self):
        rlt = self.cpu.getCpuIdleUtil()
        self.assertTrue(isinstance(rlt, dict), "Test getCpuIdleUtil failed")
    
    def testgetCpuSystemUtil(self):
        rlt = self.cpu.getCpuSystemUtil()
        self.assertTrue(isinstance(rlt, dict), "Test getCpuSystemUtil failed")
    
    def testgetCpuUserUtil(self):
        rlt = self.cpu.getCpuUserUtil()
        self.assertTrue(isinstance(rlt, dict), "Test getCpuUserUtil failed")
    
    def testgetPeriodCpuSystemUtil(self):
        rlt = self.cpu.getPeriodCpuSystemUtil(1415120400, 1415158002)
        self.assertTrue(isinstance(rlt, list), "Test getPeriodCpuSystemUtil failed")
        
        

class PhySystemStatusTest(TestBase):
    #def setUp(self):
        #super(PhySystemStatus, self).setUp()
        #self.mysys = PhySystemStatus(hostip='10.66.49.19')
    
    def testgetPhyTotalRootDiskSize(self):
        rlt = self.mysys.getPhyTotalRootDiskSize()
        self.assertTrue(isinstance(rlt, dict), "Test getPhyTotalRootDiskSize error")
    
    def testgetPhyAvailableRootDiskSize(self):
        rlt = self.mysys.getPhyAvailableRootDiskSize()
        self.assertTrue(isinstance(rlt, dict), "Test getPhyAvailableRootDiskSize error")
    
    def testgetPhyAvailRootDiskPercent(self):
        rlt = self.mysys.getPhyAvailRootDiskPercent()
        self.assertTrue(rlt['lastvalue']<100, "Test getPhyAvailRootDiskPercent error")
    
    def testgetPhyAvailDataDiskPercent(self):
        rlt = self.mysys.getPhyAvailDataDiskPercent()
        self.assertTrue(isinstance(rlt, dict), "test getPhyAvailDataDiskPercent error")
        
    def testgetPhyTotalMemory(self):
        rlt = self.mysys.getPhyTotalMemory()
        self.assertTrue(isinstance(rlt, dict), "Test getPhyTotalMemory error")
        
    def testgetPhyAvailMemory(self):
        rlt = self.mysys.getPhyAvailMemory()
        self.assertTrue(isinstance(rlt, dict), "Test getPhyAvailMemory error")
        
    def testgetPhySystemUptime(self):
        rlt = self.mysys.getPhySystemUptime()
        self.assertTrue(isinstance(rlt, dict), "Test getPhySystemUptime error")
        
    def testgetPhySystemLocaltime(self):
        rlt = self.mysys.getPhySystemLocaltime()
        self.assertTrue(isinstance(rlt, dict), "Test getPhySystemLocaltime error")
        
    def testgetPhySystemLoggedInUser(self):
        rlt = self.mysys.getPhySystemLoggedInUser()
        self.assertTrue(isinstance(rlt, dict), "Test getPhySystemLoggedInUser error")
        
    def testgetPhySystemMaxOFile(self):
        rlt = self.mysys.getPhySystemMaxOFile()
        self.assertTrue(isinstance(rlt, dict), "Test getPhySystemMaxOFile error")
        
    def testgetPhyNetworkTotal(self):
        rlt = self.mysys.getPhyNetworkTotal()
        self.assertTrue(isinstance(rlt, dict), "Test getPhyNetworkTotal error")
    
    def testgetPhyNetworkOut(self):
        rlt = self.mysys.getPhyNetworkOut()
        self.assertTrue(isinstance(rlt, dict), "Test getPhyNetworkOut error")
        
    def testgetPhyNetworkIn(self):
        rlt = self.mysys.getPhyNetworkIn()
        self.assertTrue(isinstance(rlt, dict), "Test getPhyNetworkIn error")
    
    def testgetPhyAgentPing(self):
        rlt = self.mysys.getPhyAgentPing()
        self.assertTrue(rlt['lastvalue'] ==1.0, "Test getPhyAgentPing error")
    
    def testgetPhyCommonStatus(self):
        rlt = self.mysys.getPhyCommonStatus('mysql.version')
        self.assertTrue(isinstance(rlt, dict), " Test getPhyCommonStatus error")
        
        

if __name__ == '__main__':
    unittest.main()
