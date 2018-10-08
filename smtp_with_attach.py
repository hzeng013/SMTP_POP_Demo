#!/usr/bin/env python3


'带附件发送'

__author__ = 'Neil Zeng'


import smtplib

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase


from_addr = input('From:')
password = input('Password:')  #填入授权码, 而不是邮箱登陆密码

to_addr = input('To:')

smtp_server = 'smtp.qq.com' #使用QQ邮箱发送


def _format_addr(s):
	name, addr = parseaddr(s)
	return formataddr((Header(name, 'utf-8').encode(), addr))

#邮件对象
msg = MIMEMultipart()
msg['From'] = _format_addr('Python爱好者<%s>' % from_addr)
msg['To'] = _format_addr('管理员 <%s>' % to_addr)
msg['Subject'] = Header('来自SMTP的问候....', 'utf-8').encode()

#邮件正文
msg.attach(MIMEText('I am Neil Zeng, send by Python with attachment...', 'plain', 'utf-8'))


#添加一个MIMEBase，从本地读取一个图片
with open('test.png', 'rb') as f:
	#设置附件的MINE和文件名，这里是PNG类型:
	mime = MIMEBase('image', 'png', filename = 'test.png')

	#加上必要的头信息:
	mime.add_header('Content-Disposition', 'attachment', filename='test.png')
	mime.add_header('Content-ID', '<0>')
	mime.add_header('X-Attachment-Id', '0')   
	 # 把附件的内容读进来:
	mime.set_payload(f.read())
	# 用Base64编码:
	encoders.encode_base64(mime)
	# 添加到MIMEMultipart:
	msg.attach(mime)

server = smtplib.SMTP()
server.set_debuglevel(1)
server.connect(smtp_server)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
