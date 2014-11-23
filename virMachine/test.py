# coding: utf-8
'''
Created on 2014年11月4日

@author: cuimingwen
'''
import unittest
from virGlanceUtil import *
from virNovaUtil import *

class TestBase(unittest.TestCase):
    '''
    classdocs
    '''
    def setUp(self):
        self.g = VirGlanceUtil(resource_id='f57e4f9f-6524-48d7-bd7b-8677085344d2')
        self.n = VirNovaUtil(resource_id='572e2069-1d61-4e0a-9a7d-fc9e726c22cb')
    
    def tearDown(self):
        pass

class VirGlanceUtilTest(TestBase):
    def setUp(self):
        super(VirGlanceUtilTest, self).setUp()
    
    def tearDown(self):
        pass
    
    def testgetGlanceImageExists(self):
        rlt = self.g.getGlanceImageExists()
        self.assertEqual(rlt[0]['counter_name'], 'image')
    
    def testgetCommonService(self):
        rlt = self.g.getCommonService('image.serve')
        self.assertEqual(rlt[0]['counter_name'], 'image.serve', "Test image serve failed")
    
    def testgetGlanceImageDelete(self):
        rlt = self.g.getGlanceImageDelete()
        if rlt == -1:
            self.assertEqual(rlt, -1, "Test image delete failed")
        else:
            self.assertEqual(rlt[0]['counter_name'], 'image.delete', "Test image delete failed")
    
    def testgetGlanceImageServe(self):
        rlt = self.g.getGlanceImageServe()[0]['counter_name']
        self.assertEqual(rlt, "image.serve", "Test image serve failed")
        
    def testgetGlanceImageDownload(self):
        rlt = self.g.getGlanceImageDownload()
        self.assertEqual(rlt[0]['counter_name'],"image.download", "Test image download failed")
    
    def testgetGlanceImageSize(self):
        rlt = self.g.getGlanceImageSize()
        #self.assertEqual(rlt[0]['counter_name'], 'image.size', "Test image size failed")
        self.assertTrue(isinstance(rlt, list), "Test image size failed")
    
    
        
class VirNovaUtilTest(TestBase):
    def setUp(self):
        super(VirNovaUtilTest, self).setUp()
    
    def tearDown(self):
        pass
    
    def testgetAllMeters(self):
        rlt = self.n.getAllMeters()
        self.assertTrue(isinstance(rlt, list), "Test getAllMeters failed")
    
    def testgetDiskReadBytes(self):
        rlt = self.n.getDiskReadBytes()
        self.assertTrue(isinstance(rlt, list), "Test get disk Read bytes failed")
        
    def testgetCpuUsedTime(self):
        rlt = self.n.getCpuUsedTime()
        self.assertTrue(isinstance(rlt, list), "Test getCpuUsedTime failed")
            
    def testgetDiskReadBytesRate(self):
        rlt = self.n.getDiskReadBytesRate()
        self.assertTrue(isinstance(rlt, list), "Test getDiskReadBytesRate failed")
                
    def testgetNetworkInBytesRate(self):
        rlt = self.n.getNetworkInBytesRate()
        self.assertTrue(isinstance(rlt, list), "Test getNetworkInBytesRate failed")
                
    def testgetDiskRootSize(self):
        rlt = self.n.getDiskRootSize()
        self.assertTrue(isinstance(rlt, list), "Test getDiskRootSize failed")
            
    def testgetCpuUtil(self):
        rlt = self.n.getCpuUtil()
        self.assertTrue(isinstance(rlt, list), "Test getCpuUtil failed")
                
    def testgetMemory(self):
        rlt = self.n.getMemory()
        self.assertTrue(isinstance(rlt, dict), "Test getMemory failed")
           
    def testgetMemoryUsage(self):
        rlt = self.n.getMemoryUsage()
        self.assertTrue(isinstance(rlt, dict), "Test getMemoryUsage failed")  
              
    def testgetDiskReadRequestsRate(self):
        rlt = self.n.getDiskReadRequestsRate()
        self.assertTrue(isinstance(rlt, list), "Test get disk Read request rate failed")
                
    def testgetDaysSample(self):
        " get Days sample"
        rlt= self.n.getDaysSample(mkey='disk.read.requests.rate', days=1)
        self.assertTrue(isinstance(rlt, list), "Test one day sample failed")
        
    def testgetTrendsData(self):
        " get trends data"
        rlt = self.n.getTrendsData(mkey='network.outgoing.bytes.rate', timeFrom=1416326400, timeEnd=1416467700, days=1)
        self.assertTrue(isinstance(rlt, list), "Test getTrends data failed")
    
        
if __name__ == '__main__':
    unittest.main()
        