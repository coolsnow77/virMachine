# coding: utf-8
'''
Created on 2014年10月20日

@author: cuimingwen
'''
from serviceBase import ServiceBase

class ServiceStatus(ServiceBase):
    '''
      this is physical  machine  monitor service status api 
    '''


    def __init__(self, hostip=None):
        '''
        Constructor
        '''
        super(ServiceStatus, self).__init__(hostip=hostip)
        self.hostip = hostip
        if hostip is None:
            self.hostip = 'localhost'
        self.hostData = self.getHostData()
        
    
    def getMonitorService(self):
        ' 获取当前主机的监控服务项目'
        return self.hostData['services']

    def getAllHosts(self):
        rlt = self.getAllHost()
        return rlt    
        
    def getWebStatus(self, mkey='incitoWeb'):
        ' get InctioWebStatus'
        incitoWebStat = self.hostData
        try:
            if  mkey in incitoWebStat['services']:
                rlt = self.getServiceData()
                return {'current_state': rlt[mkey]['current_state'], 
                        'plugin_output': self.uto8(rlt[mkey]['plugin_output'])}
            else:
                print "no such  monitor service: %s" %mkey
                return -1
        except KeyError as err:
            print "keyerror: %s"%(str(err))
            return -1
    
    def uto8(self, myunicode):
        ' unicode 2 utf8 string'
        try:
            str1 = myunicode.encode('utf-8')
            #print str1
            return str1
        except :
            print "unicode convert error"
            return -1
            
    def getMondodbStatus(self, mkey='mongodb'):
        ' get Mondodb status '
        mongoStat = self.hostData
        try:
            if  self.checkKeyValid(mongoStat['services'], mkey=mkey):
                rlt = self.getServiceData()
                rltKey=self.checkKeyValid(rlt, mkey, flag=1)
                return rlt[rltKey]
            else:
                print "no such  monitor service: %s" %mkey
                return -1
        except KeyError as err:
            print "keyerror: %s"%(str(err))
            return -1        
        
    
    def getPingStatus(self, mkey='PING'):
        ' get host ping status '
        pingStat = self.hostData
        try:
            if  mkey in pingStat['services']:
                rlt = self.getServiceData()
                return rlt[mkey]
            else:
                print "no such  monitor service: %s" %mkey
                return -1
        except KeyError as err:
            print "keyerror: %s"%(str(err))
            return -1
        
        
    
    def getNovaNetworkStatus(self, mkey='novaNetwork'):
        ' get Nova network status'
        novaNetworkStat = self.hostData
        try:
            if  self.checkKeyValid(novaNetworkStat['services'], mkey=mkey):
                rlt = self.getServiceData()
                rltKey=self.checkKeyValid(rlt, mkey, flag=1)
                return rlt[rltKey]
            else:
                print "no such  monitor service: %s" %mkey
                return -1
        except KeyError as err:
            print "keyerror: %s"%(str(err))
            return -1        
        
    
    def getMemcacheStatus(self, mkey='memcached'):
        ' get memcache status '
        memcacheStat = self.hostData
        try:
            if  self.checkKeyValid(memcacheStat['services'], mkey=mkey):
                rlt = self.getServiceData()
                rltKey=self.checkKeyValid(rlt, mkey, flag=1)
                return rlt[rltKey]
            else:
                print "no such  monitor service: %s" %mkey
                return -1
        except KeyError as err:
            print "keyerror: %s"%(str(err))
            return -1        
        
    
    def getSSHStatus(self, mkey='SSH'):
        ' get SSH Status'
        sshStat = self.hostData
        try:
            if  mkey in sshStat['services']:
                rlt = self.getServiceData()
                return rlt[mkey]
            else:
                print "no such  monitor service: %s" %mkey
                return -1
        except KeyError as err:
            print "keyerror: %s"%(str(err))
            return -1        
    
    def getHttpStatus(self, mkey='HTTP'):
        ' get HTTP Status'
        httpStat = self.hostData
        try:
            if  mkey in httpStat['services']:
                rlt = self.getServiceData()
                return rlt[mkey]
            else:
                print "no such  monitor service: %s" %mkey
                return -1
        except KeyError as err:
            print "keyerror: %s"%(str(err))
            return -1
    
    def getCurrentUserStatus(self, mkey='Current Users'):
        ' get current user numbers '
        cUserStat = self.hostData
        try:
            if  mkey in cUserStat['services']:
                rlt = self.getServiceData()
                return rlt[mkey]
            else:
                print "no such  monitor service: %s" %mkey
                return -1
        except KeyError as err:
            print "keyerror: %s"%(str(err))
            return -1
        
    def getSmtpStatus(self, mkey='smtp'):
        ' smtp status'
        smtpStat = self.hostData
        try:
            if  self.checkKeyValid(smtpStat['services'], mkey=mkey):
                rlt = self.getServiceData()
                rltKey=self.checkKeyValid(rlt, mkey, flag=1)
                return rlt[rltKey]
            else:
                print "no such  monitor service: %s" %mkey
                return -1
        except KeyError as err:
            print "keyerror: %s"%(str(err))
            return -1       
    
    def getPop3Status(self, mkey='pop3'):
        ' pop3 status '
        pop3Stat = self.hostData
        try:
            if  self.checkKeyValid(pop3Stat['services'], mkey=mkey):
                rlt = self.getServiceData()
                rltKey=self.checkKeyValid(rlt, mkey, flag=1)
                return rlt[rltKey]
            else:
                print "no such  monitor service: %s" %mkey
                return -1
        except KeyError as err:
            print "keyerror: %s"%(str(err))
            return -1       
    
    def getCurrentLoadStatus(self, mkey='Current_load'):
        ' get current load info'
        cLoadStat = self.hostData
        try:
            if  mkey in cLoadStat['services']:
                rlt = self.getServiceData()
                return rlt[mkey]
            else:
                print "no such  monitor service: %s" %mkey
                return -1
        except KeyError as err:
            print "keyerror: %s"%(str(err))
            return -1
    
    def getRootPartionStatus(self, mkey='Root Partition'):
        ' get root partion size '
        rootPartionStat = self.hostData
        try:
            if  mkey in rootPartionStat['services']:
                rlt = self.getServiceData()
                return rlt[mkey]
            else:
                print "no such  monitor service: %s" %mkey
                return -1
        except KeyError as err:
            print "keyerror: %s"%(str(err))
            return -1
    
    def checkKeyValid(self,myList, mkey=None, flag=None):
        ' check  key valid' 
        try:
            for item in myList:
                if item.find(mkey) != -1:
                    if flag:
                        return item
                    else:
                        return True
                else:
                    continue
        except Exception as e:
            print "error: %s"%(str(e))
            return  False


    def getCommonServiceStatus(self, mkey=None):
        ' common service status '
        comStat = self.hostData
        try:
            if  self.checkKeyValid(comStat['services'], mkey=mkey):
                rlt = self.getServiceData()
                rltKey=self.checkKeyValid(rlt, mkey, flag=1)
                return rlt[rltKey]
            else:
                print "no such  monitor service: %s" %mkey
                return -1
        except KeyError as err:
            print "keyerror: %s"%(str(err))
            return -1   
    
    def getServiceStatusByKey(self, mkey=None):
        '''
          get service status  by  service name
          @param string mkey,  service name
        '''
        comStat = self.hostData
        try:
            if  self.checkKeyValid(comStat['services'], mkey=mkey):
                rlt = self.getServiceData()
                rltKey=self.checkKeyValid(rlt, mkey, flag=1)
                if rlt[rltKey]['current_state'] == '0':
                    rlt[rltKey]['current_state'] = 'OK'
                else:
                    rlt[rltKey]['current_state'] = 'Critical'
                return rlt[rltKey]
            else:
                print "no such  monitor service: %s" %mkey
                return -1
        except KeyError as err:
            print "keyerror: %s"%(str(err))
            return -1                 
    
    def getUserDefinedStatus(self, mkey="Other"):
        ' the future plugin'
        pass
    
    def __repr__(self):
        ''
        return '<classname:' + self.__class__.__name__ +'>'
    
if __name__ == '__main__':
    t = ServiceStatus(hostip="10.66.32.18")
    print t
    print t.getMonitorService()
    print t.getWebStatus()
    print t.getMondodbStatus()
    print t.getHttpStatus()
    print t.getCommonServiceStatus('PING')
    print t.getCommonServiceStatus('Root Partition')
    for memethod in dir(t):
        if memethod.startswith("get"):
            t1  = "t."+ str(memethod) + "()"
            print str(memethod), eval(t1)  
            
    print "*" * 70        
    for k in t.getMonitorService():
        #print k
        print k, t.getServiceStatusByKey(k)  
