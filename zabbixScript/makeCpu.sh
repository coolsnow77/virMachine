#!/bin/bash



gcc  -o  vCpu  vCpu.c  -lvirt


# 3个必须参数和1个可选参数，分别是虚拟机名称vpsName,警告值warning(百分比值),危急值critical(百分比值)和检查间隔interval(秒)
./vCpu  instance-0000000c  1 4  5
