'''
Created on 2015-03-19 09:35

@author: Administrator
'''

import logging
import logging.config

logging.config.fileConfig("logging.conf")

LOG = logging.getLogger("mysite")

LOG.debug("debug message")
LOG.info("info message")
LOG.warn("warn message")
LOG.error("error message")
LOG.critical("critical message")

logHello = logging.getLogger("hello")
logHello.info("Hello world!")

#===============================================================================
# for  _ in xrange(2000000):
#     try:
#         gList = [x for x in xrange(5)]
#         print gList[6]
#     except IndexError as ex:
#         LOG.error("ex %s" %ex, exc_info=True)
#===============================================================================

import os
print os.stat("test.log")