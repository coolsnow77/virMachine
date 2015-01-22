# coding: utf-8
'''
Created on 2014年11月5日

@author: cuimingwen
'''
import unittest
from serviceStatus import *

class TestBase(unittest.TestCase):
    '''
    classdocs
    '''
    def setUp(self):
        self.s = ServiceStatus(hostip="10.66.32.18")
    
    def tearDown(self):
        pass

class ServiceStatusTest(TestBase):
    def setUp(self):
        super(ServiceStatusTest, self).setUp()
    
    def testgetMonitorService(self):
        rlt = self.s.getMonitorService()
        self.assertTrue(isinstance(rlt, list), "Test getMonitorService error")
    
    def testgetAllHosts(self):
        rlt = self.s.getMonitorService()
        self.assertTrue(isinstance(rlt, list), "Test getAllHosts error")
    
    def testgetHttpStatus(self):
        rlt = self.s.getHttpStatus()
        self.assertTrue(isinstance(rlt, dict), "Test getHttpStatus error")
    
    def testgetCommonServiceStatus(self):
        rlt = self.s.getCommonServiceStatus('PING')
        self.assertTrue(isinstance(rlt, dict), "test getCommonServiceStatus('PING') error")
    
    def testgetCurrentLoadStatus(self):
        rlt = self.s.getCurrentLoadStatus()
        self.assertTrue(isinstance(rlt, dict), "Test getCurrentLoadStatus  error")
    
    def testgetCurrentUserStatus(self):
        rlt = self.s.getCurrentUserStatus()
        self.assertTrue(isinstance(rlt, dict), "Test getCurrentUserStatus error")
    
    def testgetMondodbStatus(self):
        rlt = self.s.getMondodbStatus()
        self.assertTrue(isinstance(rlt, dict), "Test getMondodbStatus error")
    
    def testgetNovaNetworkStatus(self):
        rlt = self.s.getNovaNetworkStatus()
        self.assertTrue(isinstance(rlt, dict), "Test getNovaNetworkStatus error")
    
    def testgetPingStatus(self):
        rlt = self.s.getPingStatus()
        self.assertTrue(isinstance(rlt, dict), "Test getPingStatus error")
        
    def testGetServiceStatusByKey(self):
        rlt = self.s.getServiceStatusByKey('LY_novaNetwork')
        self.assertTrue(isinstance(rlt, dict), "Test get  service  status by key failed")
        
if __name__ =='__main__':
    unittest.main()
        