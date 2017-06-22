#!/usr/bin/python3
# -*- coding: <utf-8> -*-

from config.config import *
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import time
from traceback import format_tb
import sys
sys.path.append("..")


# 编码发件人信息
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


# 登录邮件
def login():
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.set_debuglevel(1)
    server.login(From, pwd)
    return server


# 发送邮件
def send(receiver, message, server):
    from_addr = From
    to_addr = receiver
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['Subject'] = Header('News Update of NKU SMS', 'utf-8').encode()
    msg['From'] = _format_addr('NKU-SMS<%s>' % from_addr)
    msg['To'] = _format_addr('Receiver<%s>' % to_addr)
    server.sendmail(from_addr, [to_addr], msg.as_string())


# 发送多个邮件
def sends(receivers, message):
    server = login()
    for receiver in receivers:
        print("send to %s" % receiver)
        try:
            send(receiver, message, server)
        except Exception as exc:
            print(format_tb(exc.__traceback__)[0])
        time.sleep(8)
    server.quit()
