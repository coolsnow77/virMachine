#!usr/bin/env python
# -*- coding: utf-8 -*-

import rrdtool
import time
import psutil
from datetime import datetime


startTime = str(int(time.time()))

def getZeroClockDatetime():
    dt = datetime.now()
    ymd = dt.strftime('%Y%m%d')
    ymdhms = ymd + '000000'
    return ymdhms

def datetime2timestamp(dt_str):
    timeArray = time.strptime(dt_str, '%Y%m%d%H%M%S')
    rlt = str(int(time.mktime(timeArray)))
    return rlt
 

'''
rrdb = rrdtool.create('rest.rrd', '--step', '300',
                      '--start', '1422432014',
                      'DS:input:GAUGE:120:U:U',
                      'DS:output:GAUGE:120:U:U',
                      'RRA:LAST:0.5:1:9000',
                      'RRA:AVERAGE:0.1:288:797',
                      'RRA:MAX:0.5:288:797',
                      'RRA:MIN:0.5:288:797')
if rrdb:
    print rrdtool.error()

'''
#time.sleep(5)

# 插入数据
 
for keys in psutil.network_io_counters(pernic=True):
    if keys == 'eth3':
        sent=psutil.network_io_counters(pernic=True)[keys][0]
        recv=psutil.network_io_counters(pernic=True)[keys][1]
        #up=rrdtool.updatev('rest.rrd','N:%d:%d' % (sent,recv))
        up=rrdtool.updatev('rest.rrd','N:%d:%d' % (recv,sent))
        print up
        print "sent: %f recv: %f" % (sent, recv)
 


def tabNum(num=13):
    tstr='\\t' * num
    return tstr

def dtNowString(dt_format='%Y-%m-%d %H:%M:%S'):
    dt = datetime.now()
    res = dt.strftime(dt_format)
    if dt_format == '%Y-%m-%d':
        res = res + ' 00:00:00'
    rlt = str(res).replace(':', '\:')
    return rlt

###根据rrd绘图
 
#rrdtool.graph('rest.png','--start', '1422432014',
startT = datetime2timestamp(getZeroClockDatetime())

rrdtool.graph('rest.png','--start', startT,
        '--title','服务器流量统计(1天)',
        '--vertical-label','流量',
        '-N',
        '-E',
        '--disable-rrdtool-tag',
        '--watermark', 'incito_cloud',
        #'--x-grid', 'MINUTE:10:HOUR:1:HOUR:2:0:%H:%M',
        '--x-grid', 'MINUTE:30:HOUR:1:HOUR:2:0:%b-%d %H:%M',
        #'--x-grid', 'MINUTE:10:HOUR:1:MINUTE:30:0:%H:%M',
        #'--x-grid', 'MINUTE:10:HOUR:1:MINUTE:30:0:%X',
        '--height', '200',
        '--width',  '700',
        'DEF:input=rest.rrd:input:LAST',
        'DEF:output=rest.rrd:output:LAST',
        #'CDEF:bytes_in=input,8,*',
        'COMMENT: %sFrom %s to %s\\n' % (tabNum(5), dtNowString('%Y-%m-%d'), dtNowString()),
        'COMMENT:   \\n',
        'CDEF:bytes_in=input',
        #'CDEF:bytes_out=output,8,*',
        'CDEF:bytes_out=output',
        'CDEF:bytes_total=input,output,+',
        'COMMENT:\\n',
        'LINE1:input#0000FF:In  traffic',
        #'GPRINT:bytes_in:LAST:Last in traffic\: %6.2lf %Sbps',
        'GPRINT:bytes_in:LAST:当前\: %6.2lf %Sbps',
        'GPRINT:bytes_in:MIN:最小\: %6.2lf %Sbps',
        'GPRINT:bytes_in:AVERAGE:平均\: %6.2lf %Sbps',
        'GPRINT:bytes_in:MAX:最大\: %6.2lf %Sbps',
        'COMMENT:  \\n',
        'AREA:output#00FF00:Out traffic',
        'GPRINT:bytes_out:LAST:当前\: %6.2lf %Sbps',
        'GPRINT:bytes_out:MIN:最小\: %6.2lf %Sbps',
        'GPRINT:bytes_out:AVERAGE:平均\: %6.2lf %Sbps',
        'GPRINT:bytes_out:MAX:最大\: %6.2lf %Sbps',
        'COMMENT:  \\n',
        'LINE3:bytes_total#FF8833:Total traffic',
        'COMMENT:  \\n',
        'HRULE:200000#ff0000:Alarm',
        'COMMENT:> 10M ',
        'COMMENT:\\n',
        'COMMENT:%sLast update\: %s\\n'%(tabNum(),dtNowString()),
        'COMMENT:%sAuthor\: cuimingwen@incito.com.cn\\n' %(tabNum()),
         )

print '*' * 50
