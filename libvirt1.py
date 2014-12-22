#!/usr/bin/env python

import libvirt
import sys
import xmltodict
import pprint

conn = libvirt.openReadOnly(None)

dom = conn.lookupByID(210)

#print dom.XMLDesc()




xmlStr = dom.XMLDesc()

print xmlStr

rlt =  dict(xmltodict.parse(xmlStr)['domain'])

#print rlt
#print dict(rlt['devices']['disk'])['target']['@dev']
#print dict(rlt['devices']['disk'])
print rlt['devices']['disk']
print "*" * 30

if isinstance(rlt['devices']['disk'], list):
    for i in rlt['devices']['disk']:
        if '@file' in dict(i).get('source', 0):
            print dict(i)['target']['@dev']
            break
        else:
            print dict(i)['target']['@dev'] 
else:
    print dict(rlt['devices']['disk'])['target']['@dev']

#sys.exit(0)
#print "#" * 37
#print dict(rlt['devices']['disk'][0])
#print dict(rlt['devices']['disk'][0])['target']['@dev']
#print "*" * 30
#print dict(rlt['devices']['disk'][1])['target']['@dev']
#
#sys.exit(0)
print dict(rlt['devices']['interface'])['target']['@dev']
print dict(rlt['devices']['interface'])['source']['@bridge']
print dict(rlt['devices']['interface'])['filterref']['@filter']
print dict(rlt['devices']['interface'])['mac']['@address']

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
