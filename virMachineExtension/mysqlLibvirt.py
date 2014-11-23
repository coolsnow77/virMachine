#!/usr/bin/env  python

import time
import MySQLdb


class  LibvirtDB(object):
    """
    """
    def __init__(self):
        try:
            from IaaSMonitor.virMachine.virMachineConfig import VirMachineConfig
            tI = VirMachineConfig()
            hh = tI.dbhost
            hu = tI.dbuser
            hp = tI.dbpass
            hdb = tI.dbname
            #print hh, hu, hp, hdb
            self.conn = MySQLdb.connect(host=hh,user=hu,
         			passwd=hp,db=hdb, charset='utf8')
            self.cursor = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        except MySQLdb.Error as  e:
            print "Mysql Error: %d, %s" %(e.args[0],  e.args[1])
            
        self.cur_timestamp = (int(time.time())-3600)

    def getTable(self):
        sql = '''select  *  from  libvirtMem order by timestamp desc limit 1'''
        self.cursor.execute(sql)
        mlist = self.cursor.fetchall()
        return mlist
    
     #cut it
    def writeMeminfo(self, uuid, times, mtotal, mswap, mrss):
        sql = """ insert  into  libvirtMem (uuidstring, timestamp, memTotal, 
                    memSwap, memRss) values ('%s', %d, %d, %d, %d)"""%(
			uuid, times, mtotal, mswap, mrss)
        print sql
        rlt = self.cursor.execute(sql)
        self.conn.commit()
        if  rlt !=1:
            print "write Mem  Failed"
            return -1
        else:
            print  "Write  mem  OK"
            return True
        
    def getResultBySQL(self, sqlStatement, flag=0):
        try:
            self.cursor.execute(sqlStatement)
            rlt = self.cursor.fetchall()
            self.conn.commit()
            if flag==1:
                tmp = rlt
            else:
                tmp = rlt[0]
        except Exception as e:
            print "error:", str(e)
            return  -1
        except TypeError as e:
            return -1
        else:
            return tmp
    
    def getMemoryByUUID(self, uuid):
        " get virtual meminfo  from uuid"
        sql = """ select memTotal, timestamp, memSwap, 
                    memRss from libvirtMem where  uuidstring='%s' 
                   and timestamp > %d  order by timestamp desc  
                   limit 1 """ %(uuid, self.cur_timestamp)
        rlt = self.getResultBySQL(sql)
        return rlt
    
    def getPeriodMemory(self, uuid, tf, te):
        """ get period memory info
            @param tf,  start timestamp
            @param te, end timestamp
        """
        
        sql = """ select memTotal, timestamp, memSwap, 
                memRss from libvirtMem where  uuidstring='%s' 
      and timestamp >= %d  and timestamp<= %d""" %(uuid, tf, te)
        #print sql
        rlt = self.getResultBySQL(sql, flag=1)
        return rlt
        
    
    def getDiskByUUID(self, uuid):
        """ get disk  Total size and usage  size by uuid
           @param uuid, resource_id 
        """
        
        sql = '''select `usage`,timestamp, capacity from libvirtDisk where 
            uuidstring='%s' and timestamp > %d order by timestamp desc  
            limit 1'''%(uuid, self.cur_timestamp) 
        rlt = self.getResultBySQL(sql)
        return rlt
    
    def getPeriodDisk(self, uuid, tf, te):
        sql = '''select `usage`,timestamp, capacity from libvirtDisk where 
            uuidstring='%s' and timestamp >= %d  and timestamp<=%d 
            '''%(uuid, tf, te) 
        rlt = self.getResultBySQL(sql, flag=1)
        return rlt
            
    #cut it, deprecated , not use it
    def getInterfaceByUUID(self, uuid):
        " get bandwidth  flow bytes  by  uuid"
        sql = ''' select outputBandW,timestamp, inputBandW from libvirtBandW 
        where uuidstring='%s' order by timestamp desc  limit 2'''%uuid 
        #rlt = self.getResultBySQL(sql)
        self.cursor.execute(sql)
        rlt = self.cursor.fetchall()
        self.conn.commit()
        outtmp = rlt[0]['outputBandW'] - rlt[1]['outputBandW']
        inputtmp = rlt[0]['inputBandW'] - rlt[1]['inputBandW']
        rltTMP = {'timestamp': rlt[0]['timestamp'],
                  'outputBandW':outtmp,
                  'inputBandW': inputtmp}
        return rltTMP  
    
    def getInterUUIDByUUID(self, uuid):
        " get interfaceUUID"
        date1 = time.localtime(float(self.cur_timestamp))
        dateObj = time.strftime("%Y-%m-%d %H:%M:%S", date1)
        #print type(dateObj), dateObj
        sql2 = ''' select interUUID from libvirtParameter where 
                uuidstring='%s' and timestamp > '%s' 
                limit 1 '''%(uuid, dateObj)

        sql = ''' select interUUID from libvirtParameter where 
                uuidstring='%s' limit 1 '''%(uuid)
        #print sql
        rlt = self.getResultBySQL(sql)
        return rlt
    
    def getDiskUsage(self, uuid):
        " get disk usage"
        sql = ''' select `usage`, `capacity` from libvirtDisk where
              uuidstring='%s' limit 1'''%(uuid)
        rlt = self.getResultBySQL(sql)
        return  rlt

    def __del__(self):
        self.cursor.close()
        self.conn.close()


if  __name__ == '__main__':
    t = LibvirtDB()
    #rlt = t.writeMeminfo("11111", 111111, 22,33,44)
    #print "result:",  rlt
    #print t.getTable()
    print t.getMemoryByUUID('572e2069-1d61-4e0a-9a7d-fc9e726c22cb')
    print t.getDiskByUUID('572e2069-1d61-4e0a-9a7d-fc9e726c22cb')
    #print t.getInterfaceByUUID('572e2069-1d61-4e0a-9a7d-fc9e726c22cb')
    print t.getInterUUIDByUUID('572e2069-1d61-4e0a-9a7d-fc9e726c22cb')
    print t.getDiskUsage('572e2069-1d61-4e0a-9a7d-fc9e726c22cb')
    print t.getPeriodDisk('572e2069-1d61-4e0a-9a7d-fc9e726c22cb', 1416326400, 1416467700)
    print t.getPeriodMemory('572e2069-1d61-4e0a-9a7d-fc9e726c22cb', 1416326400, 1416467700)
