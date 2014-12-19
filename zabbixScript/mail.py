#!/usr/bin/env python
#coding: utf-8



import smtplib,datetime,mimetypes,time,os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import Encoders
from email.MIMEBase import MIMEBase


import os

image_path="/tmp/zabbix-graph/" 
#Stime=os.popen('date +%Y%m%d%H%M%S').read().rstrip() 
Stime=os.popen('date +%Y%m%d').read().rstrip()+str('000000') 
graphid=1137


def _getgraph(graphid): 

	zabbix_url="http://10.66.49.8/zabbix" 
	zabbix_user="admin" 
	zabbix_pass="zabbix" 
 
	cookie="/tmp/cookie" 
	
	#Period=3600 
	Period=86400
	#Width=1222 
	Width=900

        os.popen("""curl -c '%s' -b '%s' -d "request=&name=%s&password=%s&autologin=1&enter=Sign+in" '%s'/index.php""" %\
	 	(cookie,cookie,zabbix_user,zabbix_pass,zabbix_url)) 
        os.popen("""curl -b '%s' -F "graphid=%d" -F "period=%d" -F "stime='%s'" -F "width=%d" '%s'/chart2.php > '%s''%s''.png'""" %\
		 (cookie,graphid,Period,Stime,Width,zabbix_url,image_path,Stime)) 
        image_name = '%s.png' % Stime 
        return image_name 
 
print _getgraph(graphid)

def send_mail():
	print "send_mail start#################################"

	"mail  from sender"
	sender  = 'mwcui@isoftstone.com'

	"mail receiver"
	receiver = ['mwcui@isoftstone.com', 'cuimingwen001@126.com','cuimingwen@incito.com.cn']

	smtpserver = 'smtp.isoftstone.com'
	username = 'mwcui'
	password = 'fykh+wa8'
	netpic = image_path+ _getgraph(graphid)

	""" attachment file """
	listfile=['/tmp/33.log', '5228775.jpg','bk-api-ref.pdf', 'mail22.py', 'mail_p2.tar.gz', netpic]

	"""
		1) Content-Type: multipart/mixed
		它表明这封Email邮件中包含各种格式的MIME实体但没有具体给出每个实体的类型。
		2) Content-Type: multipart/alternative
		如果同一封Email邮件既以文本格式又以HTML格式发送，那么要使用Content-Type: multipart/alternative。这两种邮件格式实际上是显示同样的内容但是具有不同的编码。
		3) Content-Type: multipart/related
		用于在同一封邮件中发送HTML文本和图像或者是其他类似类型。
		邮件主体的编码：
		主要是包括quoted-printable与base64两种类型的编码。Base64和Quoted-Printable都属于MIME（多用途部分、多媒体电子邮件和 WWW 超文本）的一种编码标准，用于传送诸如图形、声音和传真等非文本数据）。
	"""
	
	# 构造MIMEMultipart对象做为根容器
	msgRoot = MIMEMultipart()

	""" 根容器属性设置 """
	msgRoot['Subject'] = 'ISSM MonitorZ_' +  str(datetime.date.today()) 
	msgRoot['From'] = sender
	msgRoot['To'] = ';'.join(receiver)
	msgRoot['date']=time.strftime('%a, %d %b %Y %H:%M:%S %z') 


	

	""" mail body content """
	mail_body = "This is mail body test"
	body = MIMEText(mail_body)

	""" message content html """
	html = """
		<html>
			<head>ISS_Monitor</head>
			<body>
			<p>您好，测试运维监控邮件<br>
			  Test_ISS_Monitor
			</p>
			</body>
		</html>
	"""
	htm = MIMEText(html,'html', 'utf-8')

	text ="This is mail content plain"
	tex = MIMEText(text, 'plain', 'utf-8')
	
	

	""" attachment2 """

	# 构造MIMEBase对象做为文件附件内容并附加到根容器
	for f in listfile:
		print "start  attach  file: ", f

		""" validate the file exist """
		path = os.path.join('', f)
		if not os.path.isfile(path):
			print "file:%s not exist!" % f
			continue
	
		fp = open(f, 'rb')
		attfile = MIMEBase('application', 'octet-stream')
		#attfile.set_payload(open(f, 'rb').read())
		attfile.set_payload(fp.read())
		fp.close()
		Encoders.encode_base64(attfile)
		attfile.add_header('Content-Disposition', 'attachment; filename='+f)
		msgRoot.attach(attfile)

	# attach  mail body content 
	msgRoot.attach(body)

	# 发送文本
	msgRoot.attach(tex)  
	# 发送html 
	msgRoot.attach(htm)
	


	"""
		smtp sendmail start
	"""
	try:
		smtp=smtplib.SMTP()
		smtp.connect(smtpserver)
		""" smtp  ssl  add """
		smtp.ehlo()
		smtp.starttls()
		smtp.ehlo()
		#smtp.set_debuglevel(1)   #debug option
		""" smtp ssl  end """
		
		smtp.login(username, password)
		smtp.sendmail(sender, receiver, msgRoot.as_string())
		smtp.quit()
		return True
	except Exception, e:
		print str(e)
		return False
	
if __name__ == '__main__':
	if send_mail():
		print "Send mail success!"
	else:
		print "Send mail Fail!"	
