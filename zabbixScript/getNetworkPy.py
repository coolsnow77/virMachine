#!/usr/bin/env python
# coding: utf-8

import MySQLdb
import time, datetime

USER='zabbix'
PASS='qazwsxedc123!'
HOST='10.66.49.8'
DB='zabbix'
CHARSET = 'utf8'
xlsfilename = 'meishan.xlsx'
IPSTR='172.18.10.129|172.18.10.130|172.18.10.131|172.18.10.132|\
            172.18.10.133|172.18.10.134|172.18.10.135|172.18.10.136|172.18.10.161'
valueList=['流量流入(max)(Mbps)', '流量流入(avg)(Kbps)','流量流入(min)(Kbps)',
           '流量流出(max)(Mbps)','流量流出(avg)(Kbps)','流量流出(min)(Kbps)']

class GetNetwork(object):
    ''' 获取网络流量数据并写入Excel
        获取每个月25口或者0口交换机流量(流入，流出)带宽的最大值，最小值，平均值
    '''
    def __init__(self):
        self.conn = MySQLdb.connect(user=USER,passwd=PASS,host=HOST,db=DB, charset=CHARSET)
        self.cursor = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        self.ipstr = IPSTR
        self.__getItems()
    
    def __getItems(self):
        ''' 获取 items值'''
        ipList = self.ipstr.split('|')
        items={}
        for ip in ipList:
            ip=ip.strip()
            sql = '''select  itemid , name  from items where hostid in (select hostid  from  hosts  where  name='%s') and name REGEXP '[^1|^2](0|1|25)$' ''' % (ip)
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            
            # print data
            # {'172.18.10.161':({'interface1':2222},{'interface2':3333})}
            ''' items'''
            if ip == '172.18.10.161':
                dd = [d for d in data if d['name'].endswith('0')]
                # print dd
                items[ip] = {'interface0':(dd[0]['itemid'], dd[1]['itemid'])}
            else:
                d2 = [d for d in data if d['name'].endswith('25')]
                items[ip] = {'interface25':(d2[0]['itemid'], d2[1]['itemid'])}
                
        return items
    
    def getBandwidth(self):
        ''' 获取带宽值'''
        
        '''获取一个月的第一天和当前天'''
        ts_first = datetime.date(datetime.date.today().year,datetime.date.today().month,1)
        timestart = int(time.mktime(ts_first.timetuple()))
        timeend = int(time.time())
        banddict = {}
        
        itemids = self.__getItems()
        
        for ip in itemids:
            # print ip, itemids[ip]
            for interface in itemids[ip]:
                # print ip, interface, itemids[ip][interface]
                bandwidth = []
                for item in itemids[ip][interface]:
                    # print ip, interface, item
                    sql = '''select min(value), avg(value), max(value) from zabbix.history
                       where  itemid= '%s' and clock>='%s' and
                      clock<='%s' ''' %(item, timestart, timeend)
                    # print sql
                    self.cursor.execute(sql)
                    dataBandwidth = self.cursor.fetchall()
                    # print ip, interface, item, dataBandwidth
                    bandwidth.append(dataBandwidth)
                    # first inBand, second outBand
                banddict[str(ip)+'|' + str(interface)] = bandwidth
        # print banddict
        return banddict
            
        
    
        
    def write2Excel(self):
        ipList = [ ip.strip() for ip in IPSTR.split('|')]
        mydict = self.getBandwidth()
        
        try:
            import xlsxwriter
            workbook = xlsxwriter.Workbook(xlsfilename)
            worksheet = workbook.add_worksheet()
                
            # write first column
            worksheet.write(0,0,"主机".decode('utf-8'))
                
            
            i = 1
            for value in valueList:
                worksheet.write(0,i,value.decode('utf-8'))
                i +=1
            i=1
            for ip,vvv in mydict.items():
                # print ip, vvv
                m=1
                for value in vvv :
                    
                    # print ip, value
                    if m==1:
                        j = 1
                    else:
                        j = 4
                    # '''
                    for v in value:
                        
                        # print i,m,j
                        print ip, v['max(value)'], v['avg(value)'], v['min(value)']
                        worksheet.write(i,j,round(float(v['max(value)'])/(1024*1024),3))
                        #worksheet.write(i,j,v['max(value)'])
                        j += 1
                        worksheet.write(i,j,round(float(v['avg(value)'])/1024,3))
                        # worksheet.write(i,j,v['avg(value)'])
                        j +=1
                        worksheet.write(i,j,round(float(v['min(value)'])/1024,3))
                        #worksheet.write(i,j,v['min(value)'])
                        j +=1 
                    m +=1
                worksheet.write(i,0,ip)
                i += 1
                
      
        except Exception,e:
            print e
    
        
    def __del__(self):
        '''关闭数据库连接'''
        self.conn.close()
        self.cursor.close()
    
if __name__ == '__main__':
    D = GetNetwork()
    print D.write2Excel()