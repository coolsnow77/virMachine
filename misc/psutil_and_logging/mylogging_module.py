# coding: utf-8
'''
Created on 2015年3月19日

@author: Administrator
'''

import logging
import string
import sys
import traceback

console = logging.StreamHandler()
console.setLevel(logging.ERROR)
formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
console.setFormatter(formatter)

logging.basicConfig(level=logging.DEBUG,
                    filename='log.txt',
                    filemode='ab',
                    format=('%(asctime)s %(filename)s'
                    ' %(lineno)s %(levelname)s %(message)s'))



log = logging.getLogger("mylogging")
log.addHandler(console)

class MyLogging(object):
    '''
    classdocs
    '''


    def __init__(self, params=None):
        '''
        Constructor
        '''
        self.gList = list(tuple(string.letters))[:5]
        
    
    def  f(self):
        print self.gList
        self.gList[5]
        log.info("-----glist[5] %s" % self.gList[5])
        return self.g()
    
    def g(self):
        log.info("-----g")
        return self.h()
    
    def h(self):
        log.info("info h")
        del self.gList[5]
        return self.i()
    
    def i(self):
        log.info("---i fun")
        self.gList.append("i")
        print self.gList[7]

if __name__ == "__main__":
    log.debug("Information debug calling f()")
    t = MyLogging()
    try:
        t.f()
    except IndexError as ex:
        print "Sorry---------------"
        ty, tv, tb = sys.exc_info()
        log.error("Exception-----")
        log.critical("object info: %s" %ex)
        log.critical("Error type:{0}, information:{1}".format(ty, tv))
        log.critical("".join(traceback.format_tb(tb)))