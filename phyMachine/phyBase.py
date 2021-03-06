#!/usr/bin/env python
# -*- coding: utf-8 -*-
# API_Web:  https://www.zabbix.com/documentation/2.2/manual/api/reference

import sys,re,json,cPickle,urllib2
from time import mktime, strptime, strftime,localtime

import phyConfig as  zbconf
import getVipAndPhyip 



class MonitorError(Exception):
        pass

class MonitorAuthError(MonitorError):
        pass

class PhyBase(object):
	"""
	   the base level api
	   JSCONRPC API zabbix interface
	"""
	
	def __init__(self, areaid=1000, hostip="192.168.1.5"):
		" areaid  modify  when  you  create  areaHostIps.pk file "
		self.fpk = "%s/areaHostIps.pk" %(zbconf.os.path.dirname(zbconf.os.path.realpath(__file__)))
		cfg = zbconf.PhyConfig()
		self.areaid = areaid
		self.hostip = hostip
		# openstack db info
		self.osdbhost = cfg.get('lyosdbinfo', 'dbhost')
		self.osdbuser = cfg.get('lyosdbinfo', 'dbuser')
		self.osdbpass = cfg.get('lyosdbinfo', 'dbpass')
		self.osdbname = cfg.get('lyosdbinfo', 'dbname')
		self.osdbport = int(cfg.get('lyosdbinfo', 'dbport'))
		
		# openstack auth info
		self.osusername = cfg.get('lyopenstackinfo', 'osusername')
		self.ospassword = cfg.get('lyopenstackinfo', 'ospassword')
		self.ostenantname = cfg.get('lyopenstackinfo', 'ostenantname')
		self.osauthurl = cfg.get('lyopenstackinfo', 'osauthurl')
		
		#self.areaid = self.checkValidHost(hostip=self.hostip)
		if self.areaid == 1000:
			#self.url = cfg.zmsurl
			#self.user = cfg.zmsuser
			#self.passwd = cfg.zmspasswd

			self.url = cfg.zlyurl
			self.user = cfg.zlyuser
			self.passwd = cfg.zlypasswd
		elif self.areaid == 2000:
			self.url = cfg.zksurl
			self.user = cfg.zksuser
			self.passwd = cfg.zkspasswd
		elif self.areaid == 3000:
			self.url = cfg.zszurl
			self.user = cfg.zszuser
			self.passwd = cfg.zszpasswd
		elif self.areaid == 4000:
			self.url = cfg.zxyurl
			self.user = cfg.zxyuser
			self.passwd = cfg.zxypasswd
		self.header = {"Content-Type": "application/json"}
		self.authID = self.userLogin()

	def getHipFromVip(self, vip):
		'''
		get openstack computer ip from virtual ip
		@param vip string virtual ip addr
		'''
		# init VipAndIp Class
		vip_and_ip_instance = getVipAndPhyip.IpAndVip(
								user = self.osusername,
								password = self.ospassword,
                 				tenantName = self.ostenantname,
                 				url = self.osauthurl,
                 	   			dbhost = self.osdbhost,
                 	   			dbname = self.osdbname,
                 	   			dbuser = self.osdbuser,
                 	      		dbpass = self.osdbpass,
                 	      		dbport = self.osdbport)
		return vip_and_ip_instance.get_host_ip_from_vip(vip)
		

	def timestamp2Date(self,timeStamp):
		' 时间戳 转换为 日期'
		tarr = localtime(float(timeStamp))
		ret = strftime("%Y-%m-%d %H:%M:%S", tarr)
		return str(ret)

	def date2Timestamp(self, date):
		""" datetime  convert to  timestamp """
		date = str(date)
		ts = int(mktime(strptime(date, "%Y-%m-%d %H:%M:%S")))
		return ts
	
	def userLogin(self):
		''' user login auth '''
		data = json.dumps(
			{
			    "jsonrpc": "2.0",
			    "method": "user.login",
			    "params": {
				"user": self.user,
				"password": self.passwd 
				},
			    "id": 1
			    })
		request = urllib2.Request(self.url,data)

		for key in self.header:
			request.add_header(key,self.header[key])

		try:
			result = urllib2.urlopen(request, timeout=5)
		except urllib2.URLError:
			raise MonitorError("Network error: connect Monitor server failed!")
		else:
			response = json.loads(result.read())
			result.close()
                        try:
			        authID = response['result']
                        except KeyError:
                                raise MonitorAuthError(response['error']['data'])
			else:
			        return authID

	def getData(self,data, hostip=""):
		''' get json rpc data '''
		request = urllib2.Request(self.url,data)
		for key in self.header:
			request.add_header(key,self.header[key])
		try:
			result = urllib2.urlopen(request, timeout=5)
		except urllib2.URLError as e:
			if hasattr(e, 'reason'):
				raise Exception("connect  api server error!")
			elif hasattr(e, 'code'):
				print 'The server could not fulfill the request.'
			return  -1
		else:
			response = json.loads(result.read())
			result.close()
			return response


	def getAllHost(self):
		''' 
		Get all host ip 
		Linux servers  for physical machine groups
		Libvirt VMS    for virtual machine groups
		Switches	       for switches, Routers 
		'''
		data = json.dumps(
			{
			    "jsonrpc": "2.0",
			    "method": "host.get",
			    "params": {
				"output":["hostid","name","status","host", "groups"],
				"selectGroups": "extend",
				# "filter" : ['Zabbix server', 'Linux server', 'Meishang']
				},
			    "auth": self.authID,
			    "id": 1
			})
		res = self.getData(data)['result']
		if (res != 0) and (len(res) != 0):
			hostList = [[r['host'], r['groups'][0]['name']]  for r in res
					     if r['status'] == '0']
			# resDict = {'phy': [], 'vm': [], 'sw': []}
			phy, vm, sw= [], [], []
			hostDict = dict(hostList)
			for k, v in hostDict.items():
				if v in 'Linux servers':
					phy.append(k)
				elif v in 'Libvirt VMS':
					vm.append(k)
				elif v in 'Switches':
					vm.append(k)
				else:
					phy.append(k)
			hD = {'phy': phy, 'vm': vm, 'sw': sw}
			return  hD
		else:
			print "get hostip list  failed"
			return -1

	def getHostId(self,hostip):
		''' get host ip id '''
		data = json.dumps(
			{
			    "jsonrpc": "2.0",
			    "method": "host.get",
			    "params": {
				"output":["hostid","name","status","host"],
				"filter": {"host": [hostip]}
				},
			    "auth": self.authID,
			    "id": 1
			})
		
		try:
			res = self.getData(data)['result']
		except (TypeError, ValueError) :
			return -1
		
		if (res != 0) and (len(res) != 0):
			return str(([ hostid['hostid'] for hostid in res])[0])
		else:
			msg = "get hostid :%s failed" %(hostip)
			raise ValueError(msg)

	def getItemId(self,hostid, mkey):
		""" 	get monitor item id 
			hostid:  monitor host id
			 mkey : monitor key
		"""

		data = json.dumps(
			{
			    "jsonrpc": "2.0",
			    "method": "item.get",
			    "params": {
				#"output":["hostid","name","status","host"],
				"output": "itemid",
				"hostids": hostid,
				#"filter": {"host": [hostip]}
				"search": {
					"key_": mkey
				},
				"sortfield": "name"
				},
			    "auth": self.authID,
			    "id": 1
			})
		try:
			res = self.getData(data)['result']
		except TypeError:
			return  -1
		if (res != 0) and (len(res) != 0):
			#print res
			return res[0]['itemid']
		else:
			print "no such the monitorItem Key:%s" %mkey
			return -1

	def _checkExcludeKey(self, excludeKeyList, mkey):
		""" Check mkey  is  in my scope
		"""
		# excludeKey = ['hostname', 'uname', 'version']
		rlt = [0  for k in excludeKeyList if k in mkey ]
		if len(rlt)>0:
			return True
		else:
			return False

	def getLastValue(self,hostid, mkey):
		""" 	get last value of item id 
			hostid:  monitor host id
			 mkey : monitor key
		"""
		data = json.dumps(
			{
			    "jsonrpc": "2.0",
			    "method": "item.get",
			    "params": {
				"output": ["itemid","lastclock", "lastvalue"],
				"hostids": hostid,
				#"filter": {"host": [hostip]}
				"search": {
					"key_": mkey
				},
				"sortfield": "name"
				},
			    "auth": self.authID,
			    "id": 1
			})
		req = self.getData(data)
		
		if "error" in req:
			return req['error']
		
		#res = self.getData(data)['result']
		res = req['result']
		if (res != 0) and (len(res) != 0):
			resRlt = {'lastvalue': res[0]['lastvalue'],
					   'lastclock': int(res[0]['lastclock'])}
			excludeKeyList = ['hostname', 'uname', 'version'] 
			if self._checkExcludeKey(excludeKeyList, mkey):
				return resRlt
			else:
				return {"lastvalue": float("%.4f"%(float(res[0]['lastvalue']))),
				        'lastclock':int(res[0]['lastclock'])}
		else:
			if mkey.startswith('system.cpu.load'):
				return self.getLastValueE(hostid, mkey)
			elif mkey.startswith('net.if'):
				return self.getLastValueE(hostid, mkey)
			else:	
				msg = "no such  monitor key:%s value"%(mkey)
				return {"errmsg": msg, "errrlt": -1}
	
	def getLastValueE(self,hostid, mkey):
		""" 	get last value of item id 
			hostid:  monitor host id
			 mkey : monitor key
		"""
		if mkey.startswith('system.cpu.load'):
			mkey = mkey.replace('percpu', '')
		elif mkey.startswith('net.if'):
			mkey = mkey.replace('eth1', 'eth0')
			
		data = json.dumps(
			{
			    "jsonrpc": "2.0",
			    "method": "item.get",
			    "params": {
				"output": ["itemid","lastclock", "lastvalue"],
				"hostids": hostid,
				#"filter": {"host": [hostip]}
				"search": {
					"key_": mkey
				},
				"sortfield": "name"
				},
			    "auth": self.authID,
			    "id": 1
			})
		res2 = self.getData(data)['result']
		if (res2 != 0) and (len(res2) != 0):
			return {"lastvalue": float("%.4f"%(float(res2[0]['lastvalue']))),
				     'lastclock':int(res2[0]['lastclock'])}
		else:	
			msg =  "valueE no such  monitor key value:%s"%(mkey)
			return {"errmsg": msg, "errrlt": -1}
		
	def getMonitorKeyByHostid(self,hostid):
		""" 	get Monitor key by hostid
			hostid:  monitor host id
		"""
		data = json.dumps(
			{
			    "jsonrpc": "2.0",
			    "method": "item.get",
			    "params": {
				"output": ["itemid","lastclock", "lastvalue", 'key_'],
				"hostids": hostid,
				"sortfield": "name"
				},
			    "auth": self.authID,
			    "id": 1
			})
		req = self.getData(data)
		
		if "error" in req:
			return req['error']
		
		#res = self.getData(data)['result']
		res = req['result']
		if (res != 0) and (len(res) != 0):
			return [{'itemid':k['itemid'], 'key_': k['key_']} for k in res ]
		else:
			# print "get monitor key failed" 
			return {"errmsg": "get monitor key failed", "errrlt": -1}	
	
	def getPeriodValue(self,hostid, mkey, timefrom, timeuntil):
		""" 	get  Value for a period 
			hostid:  int  monitor host id
			mkey :  string monitor key
			timefrom:  int timestamp
			timetill:  int timestamp
		"""
		myItemId = self.getItemId(hostid, mkey)
		timeFrom = int(timefrom)
		timeUntil = int(timeuntil)
		# print timeFrom, timeUntil
		data = json.dumps(
			{
			    "jsonrpc": "2.0",
			    "method": "history.get",
			    "params": {
				"output": "extend",
				"history": 0,  ##0 - float, 1- log, 3- integer(default), 4- text
				"itemids": myItemId,
				"time_from": timeFrom,
				"time_till": timeUntil,
				"sortfield": "clock",
				"sortorder": "DESC"
				},
			    "auth": self.authID,
			    "id": 1
			})
		res = self.getData(data)['result']
		if (res != 0) and (len(res) != 0):
			return  self.listDictCompre(res)
		else:
			msg = "get period key :%s value error:"%mkey
			return {"errmsg": msg, "errrlt": -1}

	# get trends data 
	def getPeriodValue2(self,hostid, mkey, timefrom, timeuntil):
		""" 	get  Value for a period 
			hostid:  int  monitor host id
			mkey :  string monitor key
			timefrom:  int timestamp
			timetill:  int timestamp
		"""
		myItemId = self.getItemId(hostid, mkey)
		timeFrom = int(timefrom)
		timeUntil = int(timeuntil)
		
		excludeKeyList = ['cpu', 'pfree', 'rate', 'libvirt.vm.status[net',
						  'libvirt.vm.status[disk.root.free']
		
		if self._checkExcludeKey(excludeKeyList, mkey):
			methodh = 'trends.get'
			historyFlag = 0
		else:
			methodh = 'trends_uint.get'
			historyFlag =3
		#print methodh
		data = json.dumps(
			{
			    "jsonrpc": "2.0",
			    "method": methodh,
			    "params": {
				"output": "extend",
				"history": historyFlag,  ##0 - float, 1- log, 3- integer(default), 4- text
				"itemids": myItemId,
				"time_from": timeFrom,
				"time_till": timeUntil,
				"sortfield": "clock",
				"sortorder": "DESC"
				},
			    "auth": self.authID,
			    "id": 1
			})
		# print self.getData(data), methodh
		if "error" in  self.getData(data):
			raise ValueError(self.getData(data)['error'])
		res = self.getData(data)['result']
		if (res != 0) and (len(res) != 0):
			return  self.listDictCompre(res,historyFlag)
		else:
			msg = "get trends key :%s value error:"%mkey
			return {"errmsg": msg, "errrlt": -1}		
	
	def listDictCompre(self, myList, flag=0):
		""" find the value, clock value in dict,
			yield others from dict
		""" 
		myL=[]
		for itemD in myList:
			for k,v in itemD.items():
				if k not in ['value', 'clock', 'value_min',
							'value_max','value_avg']:
					del itemD[k]
				
				if k == 'value':
					itemD['value'] = float("%.4f"%(float(v)))
				elif k=='clock':
					itemD['clock'] = int(v) 
				elif k=='value_min':
					itemD[k] = int(v) if flag else float("%.4f"%(float(v)))
				elif k=='value_max':
					itemD[k] = int(v) if flag else float("%.4f"%(float(v)))
				elif k == 'value_avg':
					itemD[k] = int(v) if flag else float("%.4f"%(float(v)))
			myL.append(itemD)
		return myL
	
		
	def hostsPickle(self, the_list):
		""" write hostip to pickle file if you add new monitor ip ,
		    you must initiate it
		"""
		areaidtmp = 'areaid' + str(self.areaid)
		hostsDict = {areaidtmp:the_list}
		# print hostsDict
		try:
			fpk = open(self.fpk, "ab")
			cPickle.dump(hostsDict, fpk)
			#fpk.close()
		except IOError as err:
			print "open file failed:%s, %s"%(self.fpk, str(err))
		finally:
			if "fpk" in locals():
				fpk.close()
				
	def hostPickleE(self, the_list):
		""" another hostPickle with open file 
		  write hostip to pickle file  if you add new monitor ip
			you must run it
		"""
		areaidtmp = 'areaid' + str(self.areaid)
		hostsDict = {areaidtmp:the_list}
		try:
			with open(self.fpk, "ab") as fpk:
				cPickle.dump(hostsDict, fpk)
		except IOError as err:
			print "file error: %s"%(str(err))
		except cPickle.PickleError as perr:
			print "Pickling error: %s" %(str(perr))
				

	def read_records(self, filename):
		"""
			Decompress `filename`, unpickle records from it, and yield them.
		"""
		#if not os.path.exists(filename):
		#	sys.exit("not such  file :%s" %filename)
		try:
		
			with open(filename, "rb") as f:
				while True:
					try:
						yield cPickle.load(f)
					except EOFError:
						return
				f.close()
		except IOError:
			print "the data file: %s is missing!" %(filename)
			return 
	
	def read_records2(self, filename):
		""" when  I have  time , I'll write it again
		    Python Lingo
		"""
		pass 
	
	def checkValidHost(self, hostip=None):
		"check  monitor hostip valid or not "
		hostDictIter = self.read_records(self.fpk)
		pattern = r'\d{4}'
		re.compile(pattern)
		loopNum = 1 # 有4 个area , 所以要循环四次迭代
		forFlag = 0
		for hditem in hostDictIter:
			if forFlag == 1:
				break 
			for hareaid, hhost in hditem.items():
				hareaid = int(re.findall(pattern, hareaid)[0].strip())
				#print hareaid, hostip , hhost
				if hareaid == 1000 and (hostip in hhost):
					self.areaid = hareaid
					forFlag = 1
					break 
				elif hareaid == 2000 and (hostip in hhost):
					self.areaid = hareaid
					forFlag = 1
					break 
				elif hareaid == 3000 and (hostip in hhost):
					# print "go here #####"
					self.areaid = hareaid
					forFlag = 1
					break 
				elif hareaid == 4000 and (hostip in hhost):
					self.areaid = hareaid
					forFlag = 1
					break 
				else:
					#print "loopNum is: %d" %loopNum
					if loopNum > 4:
						sys.exit("no such monitor ip：%s"%(hostip))
			loopNum += 1
		return self.areaid

	def unitConvert(self, fnum):
		'unit nums to convert KB, MB, GB, TB'

		fnum = float(fnum)
		basenum=1024.0
		zunit = ['', 'KB', 'MB', 'GB']
		for u in zunit:
			if fnum < basenum and fnum > -basenum:
				return str('%.4f%s'%(fnum,u))
			fnum /=basenum
		return str('%.3f%s'%(fnum, 'TB'))
	
	def getHostGroupid(self, groupname='Linux servers'):
		'''
		Get hostGroup id
		@param groupname string
		'''
		data = json.dumps(
				{
				 	"jsonrpc": "2.0",
					 "method": "hostgroup.get",
					 "params": {
							"output": "extend",
							"filter": {
									"name": [
											groupname
											]
									}
							 },
				     "auth": self.authID,
			         "id": 1					 
				})
		if "error" in  self.getData(data):
			raise ValueError(self.getData(data)['error'])
		res = self.getData(data)['result']
		if (res != 0) and (len(res) != 0):
			out = {item: res[0][item] for item in res[0] if item in['name', 'groupid']}
			return  out
		else:
			msg = "get host group id:{} error, no groupname".format(groupname)
			return {"errmsg": msg, "errrlt": -1}		

	def getTemplateid(self, tempname='Template OS Linux'):
		'''
		Get TemplateId
		@param tempname, string template name
		'''
		data = json.dumps(
				{
				 "jsonrpc": "2.0",
				 "method": "template.get",
				 "params":{
					 "output": "extend",
					 "filter":{
							"host": [
								 tempname
								]
							}
						},
			    "auth": self.authID,
			    "id": 1				
				})
		if "error" in  self.getData(data):
			raise ValueError(self.getData(data)['error'])
		res = self.getData(data)['result']
		if (res != 0) and (len(res) != 0):
			out = {item: res[0][item] for item in res[0] if item in['name', 'templateid']}
			return  out
		else:
			msg = "get template id:{} error".format(tempname)
			return {"errmsg": msg, "errrlt": -1}

	def createVMMonitor(self, vip, hip, tpname=None):
		'''
		Create virtual monitor item
		@param vip string virtual ip addr
		@param hip string host ip addr
		@param tpname string template name
		'''
		try:
			templateid = self.getTemplateid(tpname)['templateid']
			groupid = self.getHostGroupid('Libvirt VMS')['groupid']
		except KeyError as ke:
			return {"errmsg": 'Create vm monitor error,'
				    'no template or hostgroup:{}'.format(ke),"errrlt": -1}
		macroValue = str(vip)
		# print groupid, templateid
		data = json.dumps(
			{
			    "jsonrpc": "2.0",
			    "method": "host.create",
			    "params": {
				    "host": vip,
				    "interfaces":[
						{
						  "type": 1,
						  "main": 1,
						  "useip": 1,
						   "ip": hip,
						   "dns": "",
						   "port": "10050"
		                }
					],
					"groups": [
							{
							  "groupid": groupid
							}
					],
					"templates": [
						{
						  "templateid": templateid
						}
					],
					"macros": [
						{
						  "macro": '{$HOSTIP}',
		                  "value": macroValue
						}
					],
				},
			    "auth": self.authID,
			    "id": 1
			})
		res = self.getData(data)['result']
		if (res != 0) and (len(res) != 0):
			return  res
		else:
			msg = "Create vm monitor  {} error".format(vip)
			return {"errmsg": msg, "errrlt": -1}

	def deleteVMMonitor(self, vip=None):
		'''
		Delete virtual monitor
		@param vip string virtual ip addr
		'''
		msg = " delete vm monitor  {} error".format(vip)		
		try:
			vhostid = self.getHostId(vip)
		except ValueError as err:
			return {"errmsg": str(err) + msg, "errrlt": -1}
		data = json.dumps(
				{
				 "jsonrpc": "2.0",
			    "method": "host.delete",
			    "params": [vhostid],
			    "auth": self.authID,
			    "id": 1
				})
		res = self.getData(data)['result']
		if (res != 0) and (len(res) != 0):
			return  res
		else:
			return {"errmsg": msg, "errrlt": -1}

	def __repr__(self):
		return '<PhyBase : %s>' %(getattr(self, 'url', 'unknown'))
	

	
def main():
	import pprint
	#hip = "192.168.43.204"
	hip = "10.66.32.19"
	#Z = PhyBase(hostip="10.66.49.19")
	Z = PhyBase(hostip=hip)
	print Z
	pprint.pprint(Z.getTemplateid())
	print Z.getHostGroupid()
	#print Z.createVMMonitor('10.66.32.69', '10.66.32.20', 'Template Libvirt VM Status')
	#print Z.deleteVMMonitor('10.66.32.69')
	# pprint.pprint(Z.getAllHost())
	sys.exit("over")
	#rlt = Z.getAllHost()
	########Z.hostsPickle(rlt) # write to pickle file if you need not to add  new host , never run it 
	#print Z.checkValidHost("10.66.49.19")
	#print Z.checkValidHost(hostip="192.168.1.15") #  output content host
	#print Z.areaid
	#print rlt
	hid = Z.getHostId(hip)
	#hid = Z.getHostId(rlt[0])
	if hid:
		#print "hostip : %s,  hid : %s"%(rlt[0], hid)
		print "hostip ： %s, hid: %s" %(hip, hid)
	else:
		print "hid not exits"

	print "itemid #####################"
	#mkey='vm.memory.size[available]'
	#mkey='system.cpu.util[,system]'
	#mkey = 'system.cpu.load[percpu,avg5]'
	mkey ='vfs.fs.size[/,total]'
	print "cpu system available item id: %s" %(Z.getItemId(hid,mkey))
	print Z.getLastValue(hid, mkey)
	#print Z.getPeriodValue(hid, mkey, "2014-10-15 01:00:00", "2014-10-15 17:00:00")
	print Z.getPeriodValue2(hid, mkey, 1415548800, 1415808000)
	print Z.getMonitorKeyByHostid(hid)

if __name__ == "__main__":
	main()
