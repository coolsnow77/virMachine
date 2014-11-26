#!/usr/bin/env python
"""
	zabbix  url
	zabbix web user
	zabbix web passwd
"""
#===============================================================================
# zurl="http://10.66.49.8/zabbix/api_jsonrpc.php"
# zuser="admin"
# zpasswd="zabbix"
#===============================================================================

import os

class PhyConfig(object):
    def __init__(self, configFileName=None):
        if configFileName:
            fh = open(configFileName)
        else:
            fh = open("%s/PhyConfig.cfg" %(os.path.dirname(os.path.realpath(__file__))))
            for line in fh:
                if line.startswith("#"):
                    continue
                else:
                    content = [ line.strip() for line in line.strip().split("=")]
                    if len(content) == 2:
                        setattr(self, content[0], content[1])
            
    
if __name__ == '__main__':
    ZC = PhyConfig()
    print ZC.zmsurl, ZC.zmsuser, ZC.zmspasswd
