# coding: utf-8
'''
Created on 2014年10月20日

@author: cuimingwen
'''

import os
import sys
import json
import urllib2

import serviceConfig

class MonitorError(Exception):
    pass

class ServiceBase(object):
    '''
     this is nagio base api 
    '''


    def __init__(self, hostip="10.66.32.21"):
        '''
        Constructor
        '''
        #filename ="%s/serviceConfig.cfg" %( '.' if len(os.path.dirname(__file__))== 0 else os.path.dirname(__file__))
        filename = "%s/serviceConfig.cfg"%(os.path.dirname(os.path.realpath(__file__)))
        ncInstance = serviceConfig.ServiceConfig(filename)
        self.url = ncInstance.nlyurl
        self.header = {'Content-Type': 'application/json', 
                       'Accept':'application/json'}
        self.hostip = hostip
        self.nHost=self.url + "/host"
        self.hService= self.url + '/service'
        self.hObjects = self.url + '/objects'
        #print self.url
    
    def urlRequest(self, url):
        "url  request"
        request = urllib2.Request(url)

        for  key in self.header:
            request.add_header(key,self.header[key])
        
        try:
            result=urllib2.urlopen(request, timeout=5)
        except urllib2.URLError :
            raise MonitorError("connect monitor server error")
        else:
            response = json.loads(result.read())
            result.close()
            return response
   
    def getAllHost(self):
        rlt = self.urlRequest(self.hObjects)
        if rlt['success']:
            return rlt['content'].keys()
        else:
            return -1
    
    def getHostData(self):
        ' get Host info '
        hostUrl = self.nHost +'/' + self.hostip
        hostRlt = self.urlRequest(hostUrl)
        try:
            if hostRlt['success']:
                hostInfoList = {'host_name': hostRlt['content']['host_name'],
                                 'last_check': hostRlt['content']['last_check'],
                                 'plugin_output': hostRlt['content']['plugin_output'],
                                 'services':hostRlt['content']['services']}
                #print "####",hostInfoList,"#####"
                return hostInfoList
            else:
                # print hostRlt['content']
                return hostRlt['content']
        except TypeError as err:
            raise MonitorError("get service host data error!")
    
    def getServiceData(self):
        ' get service data '
        serviceUrl = self.hService +'/' + self.hostip
        servRlt = self.urlRequest(serviceUrl)
        try:
            if servRlt['success']:
                #self.printDict(servRlt['content'])
                #print servRlt['content']
                return {k:{"current_state":v['current_state'],
                            "plugin_output":v['plugin_output']} 
                        for k, v in servRlt['content'].items()}
            else:
                return servRlt['content']
        except TypeError as e:
            raise MonitorError("get service data error!")
        
    def printDict(self, mydict):
        try:
            for k, v in mydict.items():
                print k, "==>", {"current_state": v['current_state'],
                                     'plugin_output': v['plugin_output']}

        except KeyError as kerr:
            print "error: %s" %(str(kerr))
            return -1

if __name__ == '__main__':
    nInstance = ServiceBase(hostip="10.66.32.21")
    print nInstance.getHostData()
    print nInstance.getServiceData()
