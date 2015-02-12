# -*- coding: utf-8 -*-


import ConfigParser
import sys
from  subprocess  import  Popen, PIPE
import re
class VirtIPHost(object):
    """
    Get virtual ip address and mac address
    @rtype dict  e.g. {"ip_10.66.32.136": 
                          {"ip": '10.66.32.136",
                           "mac": "f2:2e:ef:ff:ff:ff"}
                      }
    """
    def __init__(self):
        self._nova_conf = '/etc/nova/nova.conf'
        self.__ips = self._get_vip_and_mac()


    def _cmd(self, command):
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
            raise libvirtError(stderr.strip())
        if process.returncode != 0:
            errmsg = "Return code from '%s' was %s." % ( 
                command, process.returncode)
            raise libvirtError(errmsg)
        return stdout   

    def _get_domain_ids(self):
        domain_ids = self._cmd('virsh list').split()[4:][::3]
        return domain_ids

    def _get_instance_id(self):
        instance_uuid_list = list()
        for did in self._get_domain_ids():
            dominfo_com = 'virsh dominfo ' + did
            rlt = self._cmd(dominfo_com).split()
            instance_uuid_list.append(rlt[5].strip())
        return instance_uuid_list

    def _spawn_console_log_list(self):
        cons_log = 'console.log'
        conf = ConfigParser.ConfigParser()
        conf.read(self._nova_conf)
        state_path = conf.get('DEFAULT', 'state_path')
        if state_path.endswith('/'):
            console_log = state_path + 'instances/'
        else:
            console_log = state_path + '/instances/'
        inst_uid_list = self._get_instance_id()
        return [console_log+item+'/' + cons_log  for item in inst_uid_list]

    def _get_vip_and_mac(self):
        """
        Get virtual and  mac address
        """
        ip_mac = dict()
        try:
            # pass
            con_log_list = self._spawn_console_log_list()
            for logfile in con_log_list:
                with open(logfile) as fh:
                    rlt = fh.read().split('\n')
                    for line in rlt:
                        if "ci-info" in line:
                            rlt =  re.findall(r'((\d+.){3}\d+)(\s+\|\s+(\d+.){3}\d+\s+\|\s+)((\w{2}:){5}\w{2})', line)
                            if rlt:
                                ip_mac['ip_'+rlt[0][0]]={"ip": rlt[0][0], "mac": rlt[0][4]}
                                break
            return ip_mac
        except Exception as e:
            raise ValueError(str(e))

    @property
    def get_ips(self):
        return self.__ips

if __name__ == '__main__':
   t = VirtIPHost()
   print t.get_ips
