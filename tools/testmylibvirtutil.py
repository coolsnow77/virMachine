# coding: utf-8
import unittest
import mylibvirtutil


class TestVirtMetrics(unittest.TestCase):

    def setUp(self):
        self.ip = '10.66.32.67'
        self.inst = mylibvirtutil.VirtMetrics()
        self.inst.init_memory_period()

    def tearDown(self):
        self.inst = None

    def testGetMemoryTotal(self):
        rlt = self.inst.get_memory_total(self.ip)
        self.assertTrue(isinstance(rlt, long),
                        "test get_memory_total() failed")

    def testGetMemoryAvailable(self):
        rlt = self.inst.get_memory_available(self.ip)
        self.assertTrue(isinstance(rlt, long),
                        "Test get_memory_available failed")

    def testGetCpuUtil(self):
        rlt = self.inst.get_cpu_util(self.ip)
        self.assertTrue(isinstance(rlt, float),
                        "test get_cpu_util failed")

    def testGetNetIn(self):
        rlt = self.inst.get_net_in(self.ip)
        self.assertTrue(isinstance(rlt, float),
                        "test get_net_in failed")

    def testGetNetOut(self):
        rlt = self.inst.get_net_out(self.ip)
        self.assertTrue(isinstance(rlt, float),
                        "test get_net_out failed")

    def testGetNetTotal(self):
        rlt = self.inst.get_net_total(self.ip)
        self.assertTrue(isinstance(rlt, float),
                        "test get_net_total failed")

    def testGetDiskRootFree(self):
        rlt = self.inst.get_disk_root_free(self.ip)
        self.assertTrue(isinstance(rlt, int),
                        "test get_disk_root_free failed")

    def testGetDiskRootPfree(self):
        rlt = self.inst.get_disk_root_pfree(self.ip)
        self.assertTrue(isinstance(rlt, float),
                        "test get_disk_root_pfree failed")

    def testGetDiskRootTotal(self):
        rlt = self.inst.get_disk_root_total(self.ip)
        self.assertTrue(isinstance(rlt, long),
                        "test get_disk_root_total failed")

    def testGetDiskRootUsed(self):
        rlt = self.inst.get_disk_root_used(self.ip)
        self.assertTrue(isinstance(rlt, int),
                        "test get_disk_root_used failed")

    def testGetDiskReadBytesRate(self):
        rlt = self.inst.get_disk_read_bytes_rate(self.ip)
        self.assertTrue(isinstance(rlt, float),
                        "test get_disk_read_bytes_rate failed")

    def testGetDiskWriteBytesRate(self):
        rlt = self.inst.get_disk_write_bytes_rate(self.ip)
        self.assertTrue(isinstance(rlt, float),
                        "test get_disk_write_bytes_rate() failed")

if __name__ == '__main__':
    unittest.main()
