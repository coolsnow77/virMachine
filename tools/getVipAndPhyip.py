#!/usr/bin/env python
# coding: utf-8
# Get all instance ip address and determine virtual
# ip on which  hostip 

import os
from subprocess import Popen, PIPE
import MySQLdb


class IpAndVip(object):
    """
    Get all virtual ip on computer node,
    determine vip  on which  computer node
    """
    mcmd = r'nova  hypervisor-list'

    def __init__(self, cmd=mcmd, user='admin', password='incito',
                 tenantName='admin', url='http://controller:35357/v2.0',
                 dbhost='10.66.32.18', dbname='nova', dbuser='root',
                 dbpass='incito', dbport=3306):
        self.setEnv(user, password, tenantName, url)
        self.cmd = cmd
        # MySQLdb parameters
        self.odbhost = dbhost
        self.odbname = dbname
        self.odbuser = dbuser
        self.odbpass = dbpass
        self.odbport = dbport
        self.mysqlconn = self.get_mysql_connection()
        self.mysqlcursor = self.mysqlconn.cursor(cursorclass=
                                                 MySQLdb.cursors.DictCursor)

    def setEnv(self, user, password, tenantName, url):
        os.environ['OS_USERNAME'] = user
        os.environ['OS_PASSWORD'] = password
        os.environ['OS_TENANT_NAME'] = tenantName
        os.environ['OS_AUTH_URL'] = url
        return True

    def get_mysql_connection(self):
        ' Get mysql connection'
        try:
            conn = MySQLdb.connect(host=self.odbhost, user=self.odbuser,
                                   passwd=self.odbpass, port=self.odbport,
                                   db=self.odbname, charset='utf8')
        except MySQLdb.Error as e:
            raise ValueError({'message': str(e), 'code': -1})
            # return {'message': str(e), 'code': -1}
        else:
            return conn

    def getResult(self, cmd=None):
        if cmd is None:
            cmd = self.cmd
        fp = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        outputs = [item.strip() for item in fp.stdout.readlines()]
        if len(outputs) < 1:
            raise ValueError({"message": "command failed", "code": -1})
        return outputs

    def handleResult(self, cmd=None):
        if cmd is None:
            cmd = self.cmd
        res = self.getResult(cmd)
        tmp = [item for item in res if '+' not in item]
        return tmp

    def getHyperId(self):
        ' cut  the function never used'
        rlt = self.handleResult()
        # print rlt
        hIdList = [[vv.strip() for vv in v.split('|') if vv.strip() not in
                    ['', 'ID']][0] for v in rlt]
        return hIdList

    def getHypervisorId(self):
        rlt = self.handleResult()
        rrlt = [[vv.strip() for vv in v.split('|') if vv.strip() not in ['']
                 ] for v in rlt][1:]
        rrrlt = {item[0]: {"ID": item[0], 'Hypervisor_Hostname': item[1]}
                 for item in rrlt}
        return rrrlt

    def getNetworkIds(self):
        netCmd = r'nova network-list'
        rlt = self.handleResult(netCmd)
        # print rlt
        netids = [[vv.strip() for vv in v.split('|') if vv.strip() not in [
                   '', 'ID', 'Label', 'Cidr']] for v in rlt]
        nnetids = [item[0] for item in netids if len(item) > 0]
        return nnetids

    def get_networkid_and_gateway(self):
        netid = self.getNetworkIds()
        rltList = dict()
        for nid in netid:
            vipcmd = r'nova network-show ' + nid
            rlt = self.handleResult(vipcmd)
            rrlt = [[vv.strip() for vv in v.split('|') if vv.strip() not in [
                     '', 'ID']] for v in rlt]
            rrrlt = [item for item in rrlt if
                     'dhcp_start' in item or 'gateway' in item]
            rltList.update({nid: rrrlt})
        return rltList

    def get_host_ip(self):
        hypervisor_ids = self.getHypervisorId()
        hyper_dict = dict()
        for k, v in hypervisor_ids.items():
            # host_ip_cmd = "nova  hypervisor-show " + k + \
            #              " |  grep  host_ip  | sed  's/ //g'"
            host_ip_cmd = 'nova hypervisor-show ' + k
            rlt = self.getResult(host_ip_cmd)
            host_ip = [item for item in rlt if 'host_ip' in item][0]
            v.update({"host_ip": self.truncatestr(host_ip)})
            hyper_dict.update({k: v})
        return hyper_dict

    def truncatestr(self, strs):
        rlt = strs.split('|')
        out = [item.strip() for item in rlt if item.strip() not in ['']][1]
        return out

    def get_virtual_ip_on_host(self):
        ' Cut the function '
        vip_dict = dict()
        for _, v in self.getVip().items():
            vipstart = v[0][1]
            vipend = v[1][1]
            # loop  dhcp  start and end for get virtual ip all
            ips = self.get_ip_suffix(vipstart)['ip_suffix']
            ipe = self.get_ip_suffix(vipend)['ip_suffix']
            for ips in range(int(ips), int(ipe)+1):
                ips = str(ips)
                vcmd = r'nova fixed-ip-get ' + \
                       self.get_ip_suffix(vipstart)['ip_pre3fix'] + ips
                # print vcmd
                rlt = self.handleResult(vcmd)
                rrlt = [[vv.strip() for vv in v.split('|') if vv.strip() not in
                         ''] for v in rlt]
                # print vipstart, vipend
                if rrlt[1][3] == '-':
                    continue
                vip_dict.update({rrlt[1][0] + '_'+rrlt[1][3]:
                                 {"address": rrlt[1][0],
                                  "cidr": rrlt[1][1],
                                  "vhostname": rrlt[1][2],
                                  "hostname": rrlt[1][3]
                                  }})
        return vip_dict

    def get_virtual_ip_on_host_new(self):
        vip_dict = dict()
        fixed_ip_list = self.get_fixed_ip()
        for ips in fixed_ip_list:
            vcmd = r'nova fixed-ip-get ' + ips
            # print vcmd
            rlt = self.handleResult(vcmd)
            rrlt = [[vv.strip() for vv in v.split('|') if vv.strip() not in
                     ''] for v in rlt]
            # print vipstart, vipend
            if rrlt[1][3] == '-':
                continue
            vip_dict.update({rrlt[1][0] + '_'+rrlt[1][3]:
                             {"address": rrlt[1][0],
                              "cidr": rrlt[1][1],
                              "vhostname": rrlt[1][2],
                              "hostname": rrlt[1][3]
                              }
                             }
                            )
        return vip_dict

    def get_fixed_ip(self):
        ' Get fixed ip from mysqldb nova.fixed_ips'
        sql = ('select  address , allocated  from  fixed_ips where '
               'allocated=1 ;')
        self.mysqlcursor.execute(sql)
        rlt = self.mysqlcursor.fetchall()
        rrlt = [item['address'] for item in rlt]
        return rrlt

    def get_ip_suffix(self, ip=None):
        if ip is None:
            return None
        ip_suffix = ip.split('.')[-1]
        ip_pre3fix = '.'.join(ip.split('.')[:3]) + '.'
        return {'ip_suffix': ip_suffix,
                'ip_pre3fix': ip_pre3fix}

    def get_vip_and_hostip(self):
        rlta = self.get_host_ip()
        rltb = self.get_virtual_ip_on_host_new()
        vdict = dict()
        for k in rltb:
            for _, vv in rlta.items():
                if k.split('_')[-1] in vv['Hypervisor_Hostname']:
                    vdict.update({k: vv['host_ip']})
        return vdict

    def get_host_ip_from_vip(self, vip):
        '''
        Get hostip from  virtual ip
        @parameter vip string virtual ip address
        return hostip string, hostip address
        '''
        data = self.get_vip_and_hostip()
        hostip = [data[hip] for hip in data if vip in hip][0]
        return hostip

    def __del__(self):
        try:
            self.mysqlcursor.close()
            self.mysqlconn.close()
        except:
            pass

if __name__ == '__main__':
    import pprint
    t = IpAndVip()
    # t =IpAndVip(dbhost='192.168.188.200', dbpass='123456', password='123456')
    print "fixed ip is:"
    pprint.pprint(t.get_fixed_ip())
    print "*" * 80
    print "hypervisor_host_info :"
    pprint.pprint(t.get_host_ip())
    print "*" * 80
    # print t.get_virtual_ip_on_host()
    # print t.get_virtual_ip_on_host_new()
    # print "*" *  150
    print "virtual_ip, hostname， host_ip"
    # pprint.pprint(t.get_vip_and_hostip())
    print t.get_host_ip_from_vip('10.66.32.67')
