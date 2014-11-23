#!/bin/bash

virsh   dominfo  instance-0000000c



 virsh  domblklist  2 
 virsh  domblklist  4
 virsh  domblkinfo  2  vda
 virsh  domblkinfo  4  vda
 virsh   dommemstat  2
 virsh   domiflist   2
virsh   domifstat    2  vnet0




  virsh  version
  virsh version
  virsh nodememstats
  free
  virsh nodecpustats
  virsh  nodecpustats  --cpu  0
  virsh nodecpustats -percent
  virsh nodecpustats  --percent
  #top
  virsh nodecpustats  --percent
  virsh  list --all
  vir net-info  default
  virsh  net-info  default
  virsh  dominfo  BaseMachine
  virsh dominfo
  virsh dominfo 2
  virsh  vcpucount 2
  virsh dommemstat 2
  virsh  domiflist 2
