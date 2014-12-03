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
import ConfigParser

class PhyConfig2(object):
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
            

class PhyConfig(object):
    def __init__(self, configFileName=None):
        conf = ConfigParser.ConfigParser()
        if configFileName is None:
            conf.read("{0}/PhyConfig.cfg".format(os.path.dirname\
												(os.path.realpath(__file__))))
        else:
            conf.read("{0}/".format(os.path.dirname\
									(os.path.realpath(__file__)))+configFileName)
        #print conf.sections()
        self.conf = conf
        for sect in conf.sections():
            dv = dict(conf.items(sect))
            for k, v in dv.items():
                setattr(self, k, v)

    def get(self, section, key):
        return self.conf.get(section, key)	
        

        
if __name__ == '__main__':
    ZC = PhyConfig()
    print ZC.zmsurl, ZC.zmsuser, ZC.zmspasswd
    tt = PhyConfig('PhyConfig.cfg')
    print  tt.zmsurl, tt.zmsuser, repr(tt.zxyurl)

    tt3 = PhyConfig()
    print tt3.get('zmeishancfg', 'zmsurl')
