# -*- coding: utf-8 -*- 

import sys
import re
import ConfigParser
import MySQLdb
import json

from  subprocess  import  Popen, PIPE


def _cmd(command):
    if sys.platform == 'win32':
        close_fds = False
    else:
        close_fds = True
    process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE,
                    close_fds=close_fds)
    (stdout, stderr) = process.communicate()
    if stderr:
        print command
        #import pdb;pdb.set_trace()
        raise ExternalCommandError(stderr.strip())
    if process.returncode != 0:
        errmsg = "Return code from '%s' was %s." % ( 
            command, process.returncode)
        raise ExternalCommandError(errmsg)
    return stdout



def parseConsoleLog():

    conf = ConfigParser.ConfigParser()
    
    conf.read('/etc/nova/nova.conf')
    
    state_path = conf.get('DEFAULT', 'state_path')
    
    if state_path.endswith('/'):
        tmp = state_path + 'instances/'
    else:
        tmp = state_path +'/instances/'
    return tmp

def getIpMacFromMySQL():
    conn = MySQLdb.connect(host='10.66.32.18', user='root', passwd='incito', db='nova', charset='utf8')
    cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    sql = """select network_info  from  instance_info_caches where  instance_uuid='529f78e3-1290-4294-92c7-aebf76fc4c8a'"""
    result = cursor.execute(sql)
    rlt = cursor.fetchall()
    return rlt

if __name__ =='__main__':
    logfile =  parseConsoleLog()
    domainids = _cmd('virsh list').split()[4:][::3]
    instance_uuid_list = list()
    print domainids
    for did in domainids:
        instance_com = 'virsh dominfo ' + did
        print instance_com
        ins_uuid = _cmd(instance_com).split()
        instance_uuid_list.append(ins_uuid[5].strip())
    print instance_uuid_list
    for xuid in instance_uuid_list:
        colog = logfile +  xuid
        print colog
