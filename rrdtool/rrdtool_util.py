#!usr/bin/env python
# -*- coding: utf-8 -*-

"""
RRDTOOL graph util
"""
import os
import time
import re
import psutil
import rrdtool
from datetime import datetime
from operator import itemgetter


class RRDTOOLBASE(object):
    '''
    RRDTOOLBASE create  graph
    '''
    def __init__(self, monitor_list=[], png_file='rrdtest.png'):
        '''
        Constructor
        @param monitor_list list  monitor
        @param png_file string graph file
        '''
        self.png_file = png_file
        self.monitor_list = monitor_list

    def escapeColons(self, data):
        return re.sub(':', '\:', data)
 
    def tab_numbers(self, num=13):
        '''
        Spawn  tab  numbers  
        @param num int , tab numbers
        '''
        tstr='\\t' * num
        return tstr
    
    def datetime_now_string(self, dt_format='%Y-%m-%d %H:%M:%S'):
        dt = datetime.now()
        res = dt.strftime(dt_format)
        if dt_format == '%Y-%m-%d':
            res = res + ' 00:00:00'
        rlt = str(res).replace(':', '\:')
        return rlt

    def get_zero_clock_datetime(self):
        '''
        Get 0 clock  datetime string
        '''
        dt = datetime.now()
        ymd = dt.strftime('%Y%m%d')
        ymdhms = ymd + '000000'
        return ymdhms

    def datetime_to_timestamp(self, dt_str):
        '''
        Datetime to timestamp
        @param dt_str  string  datetime
        '''
        timeArray = time.strptime(dt_str, '%Y%m%d%H%M%S')
        rlt = str(int(time.mktime(timeArray)))
        return rlt

    def timestamp_to_datetime(self, timestamp):
        '''
        Timestamp  to  datetime
        @param timestamp  float timestamp
        '''
        tarr = time.localtime(float(timestamp))
        ret = time.strftime("%Y-%m-%d %H:%M:%S", tarr)
        rlt = str(ret).replace(':', '\:')
	return rlt

    def sort_trends_list(self, mylist, order_key=''):
        '''
        Sort  the trends  result list
        @param mylist: my trends data  list with dict 
        @param order_key:  the ordered  key 
        '''
        rlt = sorted(mylist, key=itemgetter(order_key))
        return rlt

    # XXX 
    def _rrdtool_create_rrddb(self): 
        ''' 
        Create rrdtool db
        '''
        for monitor_item in self.monitor_list:
            rrd_file = monitor_item + '.rrd'
            rrdb = rrdtool.create(rrd_file, '--step', '300',
                                  '--start', '1422432014',
                                  'DS:%s:GAUGE:3600:U:U' % (monitor_item),
                                  #'DS:output:GAUGE:120:U:U',
                                  'RRA:LAST:0.5:1:9000',
                                  'RRA:AVERAGE:0.1:288:797',
                                  'RRA:MAX:0.5:288:797',
                                  'RRA:MIN:0.5:288:797')
            if rrdb:
                return {'message': str(rrdtool.error()), 'code': -1}
            else:
                return {'message': "create rrddb: %s  OK!" % (monitor_item),
                        'code':  0 }
     
    # insert data  to rrd db
    def rrdtool_insert2(self):
        for keys in psutil.network_io_counters(pernic=True):
            if keys == 'eth0':
                sent=psutil.network_io_counters(pernic=True)[keys][0]
                recv=psutil.network_io_counters(pernic=True)[keys][1]
                #up=rrdtool.updatev('rest.rrd','N:%d:%d' % (sent,recv))
                up=rrdtool.updatev(self.rrd_file, 'N:%d:%d' % (recv,sent))
                # print up
                print "sent: %f recv: %f" % (sent, recv)

    # insert date to rrd db improved
    # XXX 
    def _rrdtool_insert(self, monitor_item, timestamp, value):
        '''
        Update  rrd db 
        @param monitor_item monitor item  in monitor_list
        @param timestamp  int timestamp
        @param value  the value under the timestamp
        '''
        rrd_file = monitor_item + '.rrd'
        rlt = rrdtool.updatev(rrd_file, '%d:%d' %(timestamp, value))
        if 'return_value' not in rlt:
            return {'message': 'rrdtool  insert db error', 'code': -1}
        return {'message': 'rrdtool update db OK!', 'code': 0}
         
    # rrdtool  draw  graph
    # XXX 
    def _rrdtool_draw(self, start=None, end=None, title='服务器流量统计(1天)',
                      vtitle='流量', xgrid='2', height='200', 
                      width='700', description='cpu util', alarm='10000000'):
        '''
        Draw with  rrdtool

        @param start:  int start timestamp
        @param end:  int end timestamp
        @param title: horizontal title
        @param vtitle: vertical  title
        @param xgrid: x-cordinate axis scale
        @param description string description  information for legend
        @param alarm string alarm  thresold 
        @rtype None
        '''

        # spawn  graph  strings
        i = 0
        defstr , cdefstr =  '', ''
        for  mm in self.monitor_list:
             print mm
             cdeftag = 'mycdef' + str(i)
             i = i + 1
             rrfile = mm + '.rrd'
             defstr = defstr + 'DEF:{0}={1}:{2}:LAST,'.format(mm, rrfile, mm)
             cdefstr = cdefstr + '''CDEF:{mycdef}={ds},COMMENT: '\\n','''.format(mycdef=cdeftag, ds=mm)
             #tmpstr =  '''LINE1:memoryTotal#0000FF:memoryTotalutil,'''
             #cdefstr = cdefstr + '''
             #       'GPRINT:{mycdef}:LAST:当前\: \%6.2lf \%S,'
             #       'GPRINT:{mycdef}:MIN:最小\: \%6.2lf \%S,'
             #       'GPRINT:{mycdef}:AVERAGE:平均\: \%6.2lf \%S,'
             #       'GPRINT:{mycdef}:MAX:最大\: \%6.2lf \%S,'
             #       '''.format(mycdef=cdeftag, ds=mm, desc=mm)
        defstr = defstr.strip(',')
        #cdefstr = cdefstr + tmpstr
        cdefstr = cdefstr.strip(',')
        print "defstr:", defstr, "cdefstr:", cdefstr
        # return  

        if start is None:
            startT = self.datetime_to_timestamp(self.get_zero_clock_datetime())
            fstart = self.datetime_now_string('%Y-%m-%d')
        else:
            startT = str(start)
            fstart = self.timestamp_to_datetime(startT)

        if end is None:
            endT = 'N'
            toend = self.datetime_now_string()
        else:
            endT = str(end)
            toend = self.timestamp_to_datetime(endT) 

        try:
            #import pdb;pdb.set_trace()
            rrdtool.graph(self.png_file, '--start', startT,
                    '--end',  endT,
                    '--title', title,
                    '--vertical-label', vtitle,
                    '-N',
                    '-E',
                    '--disable-rrdtool-tag',
                    '--watermark', 'incito_cloud',
                    '--x-grid', ('MINUTE:10:HOUR:1:HOUR:'
                                '{0}:0:%H:%M').format(xgrid),
                    '--height',  height,
                    '--width',   width,
                    defstr,
                    #'DEF:{0}={1}:{2}:LAST'.format(self.ds,
                    #                                 self.rrd_file,
                    #                                 self.ds),
                    'COMMENT: %sFrom %s to %s\\n' % (self.tab_numbers(5),
                                                     fstart, toend),
                    'COMMENT:   \\n',
                     cdefstr,
                    #'CDEF:mycdef0=memoryTotal',
                    #'COMMENT: \\n', 
                    'LINE1:memoryTotal#0000FF:memoryTotalutil',
                    'GPRINT:mycdef0:LAST:当前\: %6.2lf %S',
                    'GPRINT:mycdef0:MIN:最小\: %6.2lf %S',
                    'GPRINT:mycdef0:AVERAGE:平均\: %6.2lf %S',
                    'GPRINT:mycdef0:MAX:最大\: %6.2lf %S',
                    'COMMENT: \\n',

                    #'CDEF:mycdef0=%s' % (mm),
                    #'COMMENT:\\n',
                    #'LINE1:{0}#0000FF:{1}'.format(mm, description),
                    #'GPRINT:mycdef0:LAST:当前\: %6.2lf %S',
                    #'GPRINT:mycdef0:MIN:最小\: %6.2lf %S',
                    #'GPRINT:mycdef0:AVERAGE:平均\: %6.2lf %S',
                    #'GPRINT:mycdef0:MAX:最大\: %6.2lf %S',
                    #'COMMENT:  \\n',
                    'HRULE:10000000#ff0000:Alarm',
                    'COMMENT:> %s ' % (alarm),
                   
                    #""" 
                    #'DEF:input=%s:input:LAST' % ( self.rrd_file),
                    #'DEF:output=%s:output:LAST' % ( self.rrd_file),
                    #'COMMENT: %sFrom %s to %s\\n' % (self.tab_numbers(5),
                    #                                 fstart, toend),
                    #'COMMENT:   \\n',
                    #'CDEF:bytes_in=input',
                    #'CDEF:bytes_out=output',
                    #'CDEF:bytes_total=input,output,+',
                    #'COMMENT:\\n',
                    #'LINE1:input#0000FF:In  traffic',
                    #'GPRINT:bytes_in:LAST:当前\: %6.2lf %Sbps',
                    #'GPRINT:bytes_in:MIN:最小\: %6.2lf %Sbps',
                    #'GPRINT:bytes_in:AVERAGE:平均\: %6.2lf %Sbps',
                    #'GPRINT:bytes_in:MAX:最大\: %6.2lf %Sbps',
                    #'COMMENT:  \\n',
                    #'AREA:output#00FF00:Out traffic',
                    #'GPRINT:bytes_out:LAST:当前\: %6.2lf %Sbps',
                    #'GPRINT:bytes_out:MIN:最小\: %6.2lf %Sbps',
                    #'GPRINT:bytes_out:AVERAGE:平均\: %6.2lf %Sbps',
                    #'GPRINT:bytes_out:MAX:最大\: %6.2lf %Sbps',
                    #'COMMENT:  \\n',
                    #'LINE3:bytes_total#FF8833:Total traffic',
                    #'COMMENT:  \\n',
                    #'HRULE:200000#ff0000:Alarm',
                    #'COMMENT:> 10M ',
                    #"""
                    'COMMENT:\\n',
                    'COMMENT:%sLast update\: %s\\n'%(self.tab_numbers(),
                                                   self.datetime_now_string()),
                    'COMMENT:%sAuthor\: cloudteam@incito.com.cn\\n' %(
                                                         self.tab_numbers()),
                     )
        except ValueError as err:
            return {'message': str(err), 'code': -1}

    def __del__(self):
        try:
            for fn in self.monitor_list:
                filename = fn + '.rrd'
                print filename
                os.remove(filename)
        except Exception as err:
            print  err
            return {'message': str(err), 'code': -1}


if  __name__ == '__main__':
    import mema
    t = RRDTOOLBASE(monitor_list=['memoryTotal'], png_file='mem.png', )
    rlt = t.sort_trends_list(mema.memory_list, 'clock')
    start = rlt[0].get('clock', None)
    end = rlt[-1].get('clock', None)
    t._rrdtool_create_rrddb()
    for v in rlt:
        timestamp = v['clock']
        value = v['value_avg']
        t._rrdtool_insert('memoryTotal', timestamp, value)
    # t._rrdtool_draw()
    print t._rrdtool_draw(start, end, title='服务器内存统计',
                      vtitle='memory', xgrid='2', height='200', 
                      width='700', description='memory util', alarm='10000000')
