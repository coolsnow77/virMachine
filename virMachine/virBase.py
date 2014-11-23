# coding: utf-8
'''
Created on 2014年10月20日

@author: cuimingwen
'''

import sys,os,urllib2, json, datetime, time, virMachineConfig 

class VirBase(object):
    '''
      This is Ceilometer base Class
    '''


    def __init__(self, params=None, resource_id=None):
        '''
        Constructor
        '''
        filename ="%s/virMachineConfig.cfg" %( '.' if len(os.path.dirname(__file__))== 0 else os.path.dirname(__file__))
        ccInstance = virMachineConfig.VirMachineConfig(filename)
        self.curl = ccInstance.clyauthurl
        self.cmeter = ccInstance.clymeterurl
        self.cuser = ccInstance.clyusername
        self.cpasswd = ccInstance.clypasswd
        self.ctenant = ccInstance.clytenantname
        self.cheader = {'Content-Type': 'application/json', 
                       'Accept':'application/json',
                       'User-Agent':'python-keystoneclient'}
        self.authkey={"auth":{"passwordCredentials":
                              {"username":"admin","password":"incito"},
                              "tenantName":"admin"}}
        self.ctokenurl=self.curl + "/tokens"
        self.cmeterurl= self.cmeter + '/meters'
        self.cresourceurl = self.cmeter + '/resources'
        self.ctoken = self.getToken()
        self.cheader.update({'X-Auth-Token': self.ctoken})
        self.resource_id = resource_id
        # cut it below
        self.resourcesid =[]
        
    def getToken(self):
        ' get token id'
        params = json.dumps(self.authkey)
        req = urllib2.Request(self.ctokenurl, params, self.cheader )
        try:
            result = urllib2.urlopen(req)
        except urllib2.URLError as urlerr:
            #print "url_ %s error: %s" %(self.ctokenurl, str(urlerr))
            print "request  url  error!"
            #return -1
            sys.exit(-1)
        else:
            response = json.loads(result.read())
            result.close()
            token = response['access']['token']['id']
            return token
    
    def _getData(self, url, jdata=None):
        ' get  url response data  '
        myheader = self.cheader
        #print myheader
        if jdata:
            print jdata
            req = urllib2.Request(url, jdata)
        else:
            req = urllib2.Request(url)
        for key in myheader:
            req.add_header(key, myheader[key])
        
        try:
            result = urllib2.urlopen(req)
        except urllib2.URLError as urle:
            #print " urlerr %s err: %s" %(self.cmeterurl, str(urle))
            print "request  url error!"
            return -1
        else:
            response = json.loads(result.read())
            result.close()
            return response
        
    def getMeters(self):
        ''' get meters 
           Return all known meters, based on the data recorded so far
        '''
        meterData = self._getData(self.cmeterurl)
        return meterData
    
    def getResourceId(self):
        ''' get resources id 
            The unique identifier for the resource
        '''
        meteData = self.getMeters()
        rlt = set([ item['resource_id']  for item in meteData ])
        return rlt
    
    def getResIdAndMeter(self):
        ' get resourceid and  meter(ceilometer定义的监控项，诸如内存占用，网络IO，磁盘IO等等)'
        meteD = self.getMeters()
        rlt = [{'name': item['name'], 'resource_id': item['resource_id']} for item in meteD]
        return rlt
        
    def getMeterNameByResId(self, resid):
        ' get meter name from resid'
        meteD = self.getMeters()
        rlt = [ item['name'] for item in meteD if item['resource_id'] ==resid ]
        tmplist = ['network.outgoing.bytes.rate','network.incoming.bytes.rate',
                                                'memory.usage', 'disk.usage']
        rlt.extend(tmplist)
        return rlt
    
    def getMeterSampleByName(self, mkey=''):
        ' sample 是每个采集时间点上meter对应的值'
        
        urlsample= self.cmeterurl + '/' + mkey + '?q.field=resource_id&q.value=' + self.resource_id +'&limit=1' 
        #print urlsample
        try:
            rlt = [{'counter_name'  : item['counter_name'],
                     'timestamp'    : item['timestamp'],
                     'counter_volume':item['counter_volume'],
                     'counter_unit' : item['counter_unit']} for item in self._getData(urlsample)]
            if len(rlt) == 0:
                print "there is no monitor_item: %s in resource_id: %s"%(mkey, self.resource_id)
                return -1
            else:
                return rlt
        except TypeError as e:
            #print " Type Error: %s"%(str(e))
            print "no such monitor item!"
            return -1
        
    def getPeriodMeterSample(self, mkey=None, timeFrom=None, timeEnd=None):
        ''' get period meter Sample 
            mkey: metric
            timeFrom: 时间戳
            timeEnd： 时间戳
        '''
        # utc  datetime
        timeFrom = str(datetime.datetime.utcfromtimestamp(int(timeFrom))).replace(' ', 'T')
        # utc datetime
        timeEnd =  str(datetime.datetime.utcfromtimestamp(int(timeEnd))).replace(' ', 'T') 
        qjson = '''?q.field=resource_id&q.field=timestamp&q.field=timestamp&q.op=eq&q.op=gt&q.op=lt&q.value=%s&q.value=%s&q.value=%s
                ''' %(self.resource_id, timeFrom, timeEnd)
        urlsample = self.cmeterurl + '/' + mkey + qjson
        #print urlsample
        try:
            rlt = [{'counter_name'  : item['counter_name'],
                     'timestamp'    : item['timestamp'],
                     'counter_volume':item['counter_volume'],
                     'counter_unit' : item['counter_unit']} for item in self._getData(urlsample)]
            if len(rlt) == 0:
                print "there is no monitor_item: %s in resource_id: %s"%(mkey, self.resource_id)
                return -1
            else:
                return rlt
        except TypeError as e:
            print "Type error:%s"%(str(e))
            return -1
        except NameError as nerr:
            print " error: %s" %(str(nerr))
            return -1
        
    def getPeriodMeterStatistics(self, mkey=None, timeFrom=None, timeEnd=None, period=86400):
        ''' get period  meter statistics 
            mkey: metric
            timeFrom: 时间戳
            timeEnd： 时间戳
            period : 1 天
        '''
        tf = timeFrom
        te = timeEnd
        period = str(period)
        # utc  datetime
        timeFrom = str(datetime.datetime.utcfromtimestamp(int(timeFrom))).replace(' ', 'T')
        # utc datetime
        timeEnd =  str(datetime.datetime.utcfromtimestamp(int(timeEnd))).replace(' ', 'T') 
        
        if mkey in ['network.outgoing.bytes.rate','network.incoming.bytes.rate']:
            resID = VirOtherHandle().get_interUUID_by_uuid(self.resource_id)['interUUID']
            qjson = '''?q.field=resource_id&q.field=timestamp&q.field=timestamp&q.op=eq&q.op=gt&q.op=lt&q.value=%s&q.value=%s&q.value=%s&period=%s
                ''' %(resID, timeFrom, timeEnd, period)
        elif mkey == 'memory.usage':
            pm = VirOtherHandle().getPMem(self.resource_id, tf, te)
            return pm
        elif mkey == 'disk.usage':
            pd = VirOtherHandle().getPDisk(self.resource_id, tf, te)
            return pd
        else:
            qjson = '''?q.field=resource_id&q.field=timestamp&q.field=timestamp&q.op=eq&q.op=gt&q.op=lt&q.value=%s&q.value=%s&q.value=%s&period=%s
                ''' %(self.resource_id, timeFrom, timeEnd, period)
            
        urlsample = self.cmeterurl + '/' + mkey + '/statistics' + qjson
        #print urlsample
        try:
            rlt = [{'min': item['min'],
                     'max': item['max'],
                     'sum': item['sum'],
                     'avg' : item['avg'],
                     'unit': item['unit'],
                     'period_start': item['period_start'],
                     'period_end': item['period_end'],
                     'duration': item['duration']} for item in self._getData(urlsample)]
            if len(rlt) == 0:
                print "there is no monitor_item: %s in resource_id: %s"%(mkey, self.resource_id)
                return -1
            else:
                return rlt
        except TypeError as e:
            print "Type error:%s"%(str(e))
            return -1
        except NameError as nerr:
            print " error: %s" %(str(nerr))
            return -1        
        

    def getResources(self):
        ''' get resources 
            Retrieve definitions of all of the resources
        '''
        #print self.cresourceurl
        resourceData = self._getData(self.cresourceurl)
        return resourceData
    
    def getSingleResources(self, resourcesid):
        ' retrieve definitions of one resources '
        url = self.cresourceurl + '/' + resourcesid
        singleResData = self._getData(url)
        return singleResData['links']
    
    def getSingleMeter(self, resourcesid1):
        ' get single meter data'
        for item in self.getSingleResources(resourcesid1):
            iurl = item['href'] + '&limit=3'
            print item['rel'],"==>",  iurl
            
            mydict = self._getData(iurl)
            if isinstance(mydict, list):
                print "########" * 10
                #print mydict
                self.print_listE(mydict)
                print mydict[0]['counter_name'], mydict[0]['timestamp'], mydict[0]['counter_volume'], mydict[0]['counter_unit'],mydict[0]['resource_metadata']['display_name']
                print "########"  * 10
            else:
                print mydict
            #print mydict[0]['counter_name'], mydict[0]['timestamp'], mydict[0]['counter_volume'], mydict[0]['counter_uint'],mydict[0]['resource_metadata']['display_name']
    
    def print_list(self, the_list ):
        
        for item in the_list:
            if isinstance(item, dict):
                self.print_list(item)
            else:
                #print item , '==>' , the_list[item]
                if item == 'resource_id':
                    #print item , '==>' , the_list[item]
                    #print the_list[item]
                    self.resourcesid.append(str(the_list[item]))
                    
    def print_listE(self, the_list):
        for item in the_list:
            if isinstance(item, dict):
                self.print_listE(item)
            else:
                print item , "==>", the_list[item]        
        
    def __repr__(self):
        ' repr function instance '
        return self.curl

class VirOtherHandle(object):
    def __init__(self):
        from IaaSMonitor.virMachineExtension import mysqlLibvirt
        self.mInstance = mysqlLibvirt.LibvirtDB()
    
    def get_memory_by_uuid(self, resourceid):
        virMeminfo = self.mInstance.getMemoryByUUID(resourceid)
        return virMeminfo
    
    def get_disk_by_uuid(self, resourceid):
        diskInfo = self.mInstance.getDiskByUUID(resourceid)
        return diskInfo
    
    def get_interface_by_uuid(self, resid):
        interInfo = self.mInstance.getInterfaceByUUID(resid)
        return interInfo
    
    def get_interUUID_by_uuid(self, uuid):
        interUID = self.mInstance.getInterUUIDByUUID(uuid)
        return interUID
    
    def getPMem(self,uuid, tf, te):
        pm = self.mInstance.getPeriodMemory(uuid, tf, te)
        return pm
    
    def getPDisk(self, uuid, tf, te):
        pd = self.mInstance.getPeriodDisk(uuid, tf, te)
        return pd
        
        

if __name__ =='__main__':
    t = VirBase()
    f = VirOtherHandle()
    print f.getPMem('572e2069-1d61-4e0a-9a7d-fc9e726c22cb', 1416326400,1416467700 )
    print f.getPDisk('572e2069-1d61-4e0a-9a7d-fc9e726c22cb', 1416326400, 1416467700)
    #print t.ctoken
    print "####" * 8
    #print t.getMeters()
    t.print_list(t.getResources())
    print "########"  * 6
    #print t.resourcesid
    #print t.getMeters()
    print t.getResourceId()
    print t.getResIdAndMeter()
    print t.getMeterNameByResId('572e2069-1d61-4e0a-9a7d-fc9e726c22cb')
    #t.print_listE(t.getMeters())
    print t.getSingleResources('572e2069-1d61-4e0a-9a7d-fc9e726c22cb')
    #t.print_listE(t.getSingleResources('572e2069-1d61-4e0a-9a7d-fc9e726c22cb'))
    #print t.getSingleMeter('572e2069-1d61-4e0a-9a7d-fc9e726c22cb')
            