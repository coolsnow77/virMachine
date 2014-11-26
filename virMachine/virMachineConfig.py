#!/usr/bin/env python
# coding: utf-8

import os

class VirMachineConfig(object):
	def __init__(self, configFileName=None):
		#configFileName="%s/virMachineConfig.cfg" %( '.' if len(os.path.dirname(__file__))== 0 else os.path.dirname(__file__))
		configFileName = "%s/virMachineConfig.cfg"%(os.path.dirname(os.path.realpath(__file__)))
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
	CC = VirMachineConfig()
	if  hasattr(CC, "clyauthurl"):
		print CC.clyusername, CC.clypasswd, CC.clyauthurl, CC.clytenantname, CC.clymeterurl
	