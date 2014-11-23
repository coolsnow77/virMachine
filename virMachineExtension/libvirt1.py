#!/usr/bin/env python

import libvirt
import sys
import xmltodict
import pprint

conn = libvirt.openReadOnly(None)

dom = conn.lookupByID(4)

#print dom.XMLDesc()




xmlStr = dom.XMLDesc()

print xmlStr

rlt =  dict(xmltodict.parse(xmlStr)['domain'])

print rlt
print dict(rlt['devices']['disk'])['target']['@dev']
print dict(rlt['devices']['interface'])['target']['@dev']
print dict(rlt['devices']['interface'])['filterref']['@filter']

sys.exit(0)
print "##" *  10

for   i,v  in rlt.items():
    if  i == "devices":
        #print i, "=>", v
        if isinstance(v, dict):
            for k,vv  in v.items():
                print k, "===>", vv

    else:
        print "___________"
        

#pprint.pprint(rlt)

print   "##########"  * 5

for i , v  in rlt.items():
    print i, "===>", v

sys.exit(1)
import xml.sax
import xml.sax.handler

class XMLHandler(xml.sax.handler.ContentHandler):  
    def __init__(self):  
        self.buffer = ""                    
        self.mapping = {}                  
  
    def startElement(self, name, attributes):  
        self.buffer = ""                    
  
    def characters(self, data):  
        self.buffer += data                      
  
    def endElement(self, name):  
        self.mapping[name] = self.buffer           
  
    def getDict(self):  
        return self.mapping  


xh = XMLHandler()
xmlStr = dom.XMLDesc()
xml.sax.parseString(xmlStr, xh)

ret = xh.getDict()

import pprint
print pprint.pprint(ret)



print  "*" * 30
