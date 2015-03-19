'''
@author: Administrator
'''

import psutil
from psutil import AccessDenied

class Psutil_Class(object):
    '''
    classdocs
    '''


    def __init__(self, params=None):
        '''
        Constructor
        '''
        pass
    
    def hello(self):
        return "Hello"

    def get_cpu_time(self):
        cputime = psutil.cpu_times()
        for _ in xrange(4):
            print psutil.cpu_percent(interval=1)
        print psutil.cpu_count(logical=False) 
        return cputime

    def get_memory(self):
        mem = psutil.virtual_memory()
        mem_used = psutil.virtmem_usage()
        print mem, mem_used

    def get_disk(self):
        disk_io = psutil.disk_io_counters()
        disk_par = psutil.disk_partitions()
        disk_  =psutil.disk_usage('c:\\')
        print disk_io
        print disk_par
        print disk_

    def get_net(self):
        net_io = psutil.net_io_counters()
        print net_io

    def get_users(self):
        user = psutil.users()
        return user
    
    def get_pids(self):
        pids = psutil.pids()
        print pids
        for pid in pids:
            p=psutil.Process(pid)
            try:
                print pid , '\t', p.name(), '\t\t\t', p.cpu_times(), '\t\t\t', p.memory_info()
            except AccessDenied:
                pass
        print psutil.test() #ps aux

if __name__ == "__main__":
    p = Psutil_Class()
    print p.hello()
    print p.get_cpu_time()
    print p.get_memory()
    print "disk------------------------"
    print p.get_disk()
    print p.get_net()
    print p.get_users()
    p.get_pids()