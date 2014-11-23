#!/usr/bin/env python

from  subprocess import Popen, PIPE

class GetVirDiskPar(object):
    def __init__(self):
        pass
    
    def get_disk_partion(self, domid):
        " "
        try:
            cmd='sudo  virt-df  -d  `virsh  domuuid %d`'%domid
            df = Popen(cmd, shell=True, stdout=PIPE, stderr = PIPE)
            outputs = df.stdout.readlines()
            return outputs[2].strip().split()
        except  Exception as e:
            return -1



if __name__== '__main__':
    t = GetVirDiskPar()
    print t.get_disk_partion(5)
