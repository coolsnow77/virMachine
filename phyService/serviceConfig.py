#!/usr/bin/env python
# coding: utf-8

import os

class ServiceConfig(object):
	def __init__(self, configFileName=None):
		configFileName="%s/serviceConfig.cfg" %( '.' if len(os.path.dirname(__file__))== 0 else os.path.dirname(__file__))
		try:
			with open(configFileName) as fh:
				for line in fh:
					if line.startswith("#"):
						continue
					else:
						content = [ line.strip() for line in line.strip().split("=")]
						if len(content) == 2:
							setattr(self, content[0], content[1])
		except IOError as err:
			print "file error: %s"%(str(err))
			
			
if __name__ == '__main__':
	NC = ServiceConfig()
	if  hasattr(NC, "nlyurl"):
		print NC.nlyurl
	