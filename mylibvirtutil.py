# coding: utf-8
'''
Created on 2014年12月2日

@author: cuimingwen
'''
#  install   package as  followed
#  pip install  xmltodict
#  apt-get  -y  install  libguestfs-tools
#  sudo  vim  /etc/sudoer  ,  last line  add "zabbix ALL=NOPASSWD:ALL"
import sys

from time import sleep
from subprocess import Popen, PIPE

try:
    import libvirt
except ImportError:
    lib_e = sys.exc_info()[1]
    raise ImportError(lib_e)
finally:
    try:
        import xmltodict
    except ImportError:
        xml_e = sys.exc_info()[1]
        if str(xml_e).count("No module named"):
            raise ValueError(xml_e)


# The root of all libvirt errors.
class libvirtError(Exception):
    def __init__(self, defmsg):
        err = None
        if err is None:
            msg = defmsg
        else:
            msg = err[2]

        Exception.__init__(self, msg)

        self.err = err


class VirtIPHost(object):
    """ Get VM ip address and  hostname
    """
    def __init__(self, params=None):
        self.__ips = self.__get_ip_and_hostname()

    def __get_ip_and_hostname(self):
        ip_dict = {}
        try:
            cmd = 'ls /var/lib/nova/networks/nova*.conf'
            fp = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
            outputs = [item.strip() for item in fp.stdout.readlines()]
            for ip_file in outputs:
                file_cmd = '/bin/cat ' + ip_file
                ip_fd = Popen(file_cmd, shell=True, stdout=PIPE, stderr=PIPE)
                file_outputs = [item.strip() for item in
                                ip_fd.stdout.readlines()]
                if len(file_outputs) < 1:
                    continue
                for cont in file_outputs:
                    cont_list = cont.split(',')
                    ip_dict['ip_' + cont_list[2]] = {'mac': cont_list[0],
                                                     'ip': cont_list[2]}
            return ip_dict
        except Exception as e:
            raise libvirtError(str(e))

    @property
    def get_ips(self):
        return self.__ips


class VirtMetrics(object):
    '''
      Get vm cpu， mem， disk， bandwidth util from
      libvirt.
    '''

    def __init__(self, params=None):
        '''
            Init  libvirtConn
        '''
        self.interval = 3.0
        self.conn = self.__get_libvirt_connection()

    def __get_libvirt_connection(self):
        " get libvirt connection"
        conn = libvirt.openReadOnly(None)
        if conn is None:
            return -1
        else:
            return conn

    def __get_list_domain_id(self):
        if self.conn == -1:
            return -1
        else:
            list_domid = self.conn.listDomainsID()
            return list_domid

    def init_memory_period(self):
        " Init  memory  period "
        domid_list = self.__get_list_domain_id()
        if len(domid_list) < 1:
            raise libvirtError("not instance run ")
        for did in domid_list:
            cmd = "virsh  dommemstat {0} --period 1000".format(did)
            fp = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
            outputs = [item.strip() for item in fp.stdout.readlines()]
            # print outputs
        return None

    def get_libvirt_path(self):
        " path is vda, vnet0, or mac "
        libv_path = {}
        for domid in self.__get_list_domain_id():
            myDom = self.conn.lookupByID(domid)
            uuidStr = myDom.UUIDString()
            xmlStr = myDom.XMLDesc()
            rlt = dict(xmltodict.parse(xmlStr)['domain'])
            com_d = dict(rlt['devices']['interface'])
            # disk path  validate     
            if isinstance(rlt['devices']['disk'], list):
                for i in rlt['devices']['disk']:
                    if '@file' in dict(i).get('source', 0):
                        dPath = dict(i)['target']['@dev']
                        break
                    else:
                        dPath = dict(i)['target']['@dev'] 
            else:
                dPath = dict(rlt['devices']['disk'])['target']['@dev']
            # dPath = dict(rlt['devices']['disk'])['target']['@dev']
            interPath = com_d['target']['@dev']
            interfaceRef = com_d['filterref']['@filter']
            macstring = com_d['mac']['@address']
            # print "mac string:", macstring
            libv_path['domid_' + str(domid)] = {'uuidstr': uuidStr,
                                                'diskPath': dPath,
                                                'interfacePath': interPath,
                                                'interRef': interfaceRef,
                                                'macstr': macstring}

        return libv_path

    def __get_domain_mac_by_ip(self, ip=None):
        " get  domain mac  by ip address "
        ip_instance = VirtIPHost()
        for pi in ip_instance.get_ips:
            if ("ip_"+str(ip)) == pi:
                mac_str = ip_instance.get_ips[pi]['mac']
                break
            else:
                # print "mac address not exist"
                mac_str = None
                continue

        return mac_str

    def __get_domain_id_by_mac(self, mac=None):
        " get domain id  by  mac  address "
        if mac is None:
            return None

        domid = self.get_libvirt_path()
        for did in domid:
            if mac == domid[did]['macstr']:
                tmp_did = int(did.split('_')[-1])
                break
            else:
                tmp_did = None
                continue

        return tmp_did

    def __get_domain_id_by_ip(self, ip=None):
        macstr = self.__get_domain_mac_by_ip(ip)
        domid = self.__get_domain_id_by_mac(macstr)
        return domid

    def __get_disk_info(self, domid):
        try:
            cmd = 'sudo virt-df -d `virsh domuuid %d`' % (domid)
            df = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
            outputs = df.stdout.readlines()
            # print outputs
            list_disk = outputs[2].strip().split()
            d0 = int(list_disk[0]) * 1000
            d1 = int(list_disk[1]) * 1000
            d2 = int(list_disk[2]) * 1000
            d3 = float('%.4f' % (float(d1)/float(d0)))
            disk_dict = {'total': d0,
                         'used': d1,
                         'available': d2,
                         'userpercent': d3}
            return disk_dict
        except Exception as e:
            raise ValueError(str(e))

    # cut it
    def get_disk2(self, ip=None):
        " Get disk info from virt-df"
        dom_id = self.__get_domain_id_by_ip(ip)
        if dom_id is None:
            raise libvirtError("domain id or ip not exist")
        d_info = self.__get_disk_info(dom_id)
        return d_info

    def __get_disk_info2(self, ip=None):
        " Get  disk  from  libvirt"
        dom_id = self.__get_domain_id_by_ip(ip)
        if dom_id is None:
            raise libvirtError("domain id or ip not exist")
        vir_domain = self.conn.lookupByID(dom_id)
        dkey = 'domid_' + str(dom_id)
        dp = self.get_libvirt_path()[dkey]['diskPath']
        disk_info = vir_domain.blockInfo(dp)
        return disk_info

    def __get_disk_rw_bytes_info(self, ip=None):
        " Get disk  read  / write Bytes rate "
        interval = self.interval
        dom_id = self.__get_domain_id_by_ip(ip)
        if dom_id is None:
            raise libvirtError("domain id or ip not exist")
        vir_domain = self.conn.lookupByID(dom_id)
        dkey = 'domid_' + str(dom_id)
        dp = self.get_libvirt_path()[dkey]['diskPath']
        disk_rw_info1 = vir_domain.blockStatsFlags(dp)
        sleep(interval)
        disk_rw_info2 = vir_domain.blockStatsFlags(dp)
        disk_rw_info = self.__union_dict(interval,
                                         disk_rw_info2,
                                         disk_rw_info1)
        return disk_rw_info

    def __get_mem_info(self, ip=None):
        " get memory info"
        dom_id = self.__get_domain_id_by_ip(ip)
        if dom_id is None:
            raise libvirtError("domain id or ip not exist")
        vir_domain = self.conn.lookupByID(dom_id)
        mem_info = vir_domain.memoryStats()
        return mem_info

    def __get_net_info(self, ip=None):
        " Get  network information"
        interval = self.interval
        dom_id = self.__get_domain_id_by_ip(ip)
        if dom_id is None:
            raise libvirtError("domain id or ip not exist")
        mydom = self.conn.lookupByID(dom_id)
        nkey = 'domid_' + str(dom_id)
        np = self.get_libvirt_path()[nkey]['interfacePath']
        net_info1 = {'rx_bytes': mydom.interfaceStats(np)[0],
                     'tx_bytes': mydom.interfaceStats(np)[4]}
        sleep(interval)

        net_info2 = {'rx_bytes': float(mydom.interfaceStats(np)[0]),
                     'tx_bytes': float(mydom.interfaceStats(np)[4])}
        net_info = self.__union_dict(interval, net_info2, net_info1)
        return net_info

    def __get_cpu_info(self, ip=None):
        " cpu info "
        interval = self.interval
        dom_id = self.__get_domain_id_by_ip(ip)
        if dom_id is None:
            raise libvirtError("domain id or ip not exist")
        mydom = self.conn.lookupByID(dom_id)
        cpu_info1 = {k: v/float(1000000000) for k,
                     v in mydom.getCPUStats(1)[0].items()}
        sleep(interval)
        cpu_info2 = {k: v/float(1000000000) for k,
                     v in mydom.getCPUStats(1)[0].items()}
        cpu_info = self.__union_dict(interval, cpu_info1, cpu_info2)
        return cpu_info

    def __union_dict(self, interval, *mobjs):
        " Dict  union (subtract )"
        _keys = set(sum([mobj.keys() for mobj in mobjs], []))
        _total = {}
        for _key in _keys:
            _klist = [mobj.get(_key, 0) for mobj in mobjs]
            _total[_key] = abs(sum([v if k != 1 else -v for k, v
                                    in enumerate(_klist)]))/interval
        return _total

    def get_memory_total(self, ip=None):
        " total memory"
        m_info = self.__get_mem_info(ip)
        return (m_info.get('actual', 0)) * 1000

    def get_memory_available(self, ip=None):
        " available memory"
        m_info = self.__get_mem_info(ip)
        return (m_info.get('unused', 0)) * 1000

    def get_cpu_util(self, ip=None):
        " cpu utilizaiton 0.4%"
        cpu_info = self.__get_cpu_info(ip)
        ret = float('{:.4f}'.format(cpu_info.get('cpu_time', 0) * 100))
        return ret

    def get_net_in(self, ip):
        " network-in, download"
        net_info = self.__get_net_info(ip)
        ret = float('{:.4f}'.format(net_info.get('rx_bytes', 0)))
        return ret

    def get_net_out(self, ip):
        " network-out, upload"
        net_info = self.__get_net_info(ip)
        ret = float('{:.4f}'.format(net_info.get('tx_bytes', 0)))
        return ret

    def get_net_total(self, ip):
        " network total"
        total = self.get_net_in(ip) + self.get_net_out(ip)
        net_t = float('{:.4f}'.format(total))
        return net_t

    def get_disk_root_free(self, ip=None):
        " disk root free"
        dom_id = self.__get_domain_id_by_ip(ip)
        if dom_id is None:
            raise libvirtError("domain id or ip not exist")
        disk_free = self.__get_disk_info(dom_id)
        return disk_free.get('available', 0)

    def get_disk_root_pfree(self, ip=None):
        " disk root free percentage "
        dom_id = self.__get_domain_id_by_ip(ip)
        if dom_id is None:
            raise libvirtError("domain id or ip not exist")
        disk_pfree = self.__get_disk_info(dom_id)
        rlt = 1 - disk_pfree.get('userpercent', 0)
        return rlt

    def get_disk_root_total(self, ip=None):
        " disk root total size, capacity "
        disk_info = self.__get_disk_info2(ip)
        return disk_info[0]

    def get_disk_root_used(self, ip=None):
        " disk root used size "
        dom_id = self.__get_domain_id_by_ip(ip)
        if dom_id is None:
            raise libvirtError("domain id or ip not exist")
        disk_pfree = self.__get_disk_info(dom_id)
        return disk_pfree.get('used', 0)

    def get_disk_read_bytes_rate(self, ip=None):
        " disk read bytes rate "
        disk_rw_b = self.__get_disk_rw_bytes_info(ip)
        ret = float('{:.4f}'.format(disk_rw_b.get('rd_bytes', 0)))
        return ret

    def get_disk_write_bytes_rate(self, ip=None):
        " disk write bytes rate "
        disk_rw_b = self.__get_disk_rw_bytes_info(ip)
        ret = float('{:.4f}'.format(disk_rw_b.get('wr_bytes', 0)))
        return ret

    def __del__(self):
        " close libvirt connection"
        try:
            self.conn.close()
        except ValueError:
            raise libvirtError("close libvirt connection failed")

    def __repr2__(self):
        return self.__class__

if __name__ == '__main__':
    #fh = open("/tmp/vim1.log", "wb")
    #print sys.argv[0], sys.argv[1], sys.argv[2]
    #fh.write("%s-%s-%s" %(sys.argv[0], sys.argv[1], sys.argv[2]))
    #fh.close()
    if len(sys.argv) < 3:
        raise libvirtError("Not enough  arguments, argv >=3")
    else:
        command, ip = sys.argv[1], sys.argv[2]
        # print command, ip
        tt = VirtIPHost()
        # print tt.get_ips
        t = VirtMetrics()
        t.init_memory_period()
        # print t.get_cpu_util()
        # print t.get_libvirt_path()
        # print dir(t)
        tmp_com = 'get_' + str(command).replace('.', '_')
        # print tmp_com
        if tmp_com in dir(t):
            # com_str = 't.' + str(tmp_com) + '(' + str(ip) + ')'
            com_str = ''.join(['t.', str(tmp_com), '("', ip, '")'])
            print eval(com_str)
