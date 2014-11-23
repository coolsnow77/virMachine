#!/usr/bin/env  python

import MySQLdb


class  mMySQL(object):
    """
    """
    def __init__(self):
        try:
            self.conn = MySQLdb.connect(host='10.66.32.18',user='root',
         			passwd='incito',db='mylibvirt', charset='utf8')
            self.cursor = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        except MySQLdb.Error as  e:
            print "Mysql Error: %d, %s" %(e.args[0],  e.args[1])

    def getTable(self):
        sql = '''select  *  from  libvirtMem limit  1'''
        self.cursor.execute(sql)
        list = self.cursor.fetchall()
        return list

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

    def writeDiskinfo(self,uuid, times, capacity, myusage):
        sql = ''' insert into libvirtDisk (`uuidstring`, `timestamp`, `capacity`,`usage`)
			values('%s', %d, %d, %d)'''%(uuid, times, capacity,myusage)
        print sql
        rlt = self.cursor.execute(sql)
        self.conn.commit()
        if rlt !=1:
            print "write disk Failed!"
            return -1
        else:
            print "write disk OK!"
            return True

    def writeInterfaceinfo(self,uuid, times, outp, inputs):
        sql = ''' insert into libvirtBandW (uuidstring, timestamp, outputBandW,
		inputBandW) values('%s', %d, %d, %d)'''%(uuid, times, outp,inputs)
        print sql
        rlt = self.cursor.execute(sql)
        self.conn.commit()
        if rlt !=1:
            print "write interface bandwidth Failed!"
            return -1
        else:
            print "write interface bandwidth OK!"
            return True
        
    def writeParameters(self, myuuid, interUUID, vInterfacePath,vDiskPath):
        sql = ''' insert into libvirtParameter (uuidstring, interUUID, 
               vInterfacePath,vDiskPath) values('%s','%s','%s','%s')'''%(
               myuuid, interUUID,vInterfacePath, vDiskPath)
        print sql
        rlt = self.cursor.execute(sql)
        self.conn.commit()
        if rlt !=1:
            print "write  parameters  Failed!"
            return -1
        else:
            print "write parameters  OK!"
            return True        



    def __del__(self):
        self.cursor.close()
        self.conn.close()


if  __name__ == '__main__':
    t = mMySQL()
    #rlt = t.writeMeminfo("11111", 111111, 22,33,44)
    #print "result:",  rlt
    print t.getTable()
    #t.writeInterfaceinfo("11111", 11111, 1111,1111)
    #t.writeDiskinfo("1111",1111,2222,22222)
