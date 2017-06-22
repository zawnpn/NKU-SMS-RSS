#!/usr/bin/python3
# -*- coding: <utf-8> -*-

from function.rss import *
from function.mail import *
from traceback import format_tb
from config.config import *


# 构造邮件发送信息
def make_message(table, local):
    updates = get_update(table, local)
    message = "Hello, NKU-SMS has new update!\n\n"
    for update in updates:
        if update:
            update.reverse()
            for item in update:
                if not re.compile('http://').findall(item[0]):
                    message += "[Title]%s \n[Link] http://sms.nankai.edu.cn%s \n\n" % (item[1], item[0])
                else:
                    message += "[Title]%s \n[Link] %s \n\n" % (item[1], item[0])
    return message


# 发送邮件
def send_mail(table, local):
    message = make_message(table, local)
    with open(ReceiverPath, 'r') as f:
        receivers = f.readlines()
        receivers = [receivers[2*i+1][:-1] for i in range(int(len(receivers)/2))]
        print(receivers)
    sends(receivers, message)


if __name__ == '__main__':
    try:
        if test_net():
            table = get_content_table()
            local = get_local_latest()
            if not is_updated(table, local):
                update_xml(table, local)
                update_latest(table)
                send_mail(table, local)
                print("Successfully Updated!")
            else:
                print("Already Updated!")
        else:
            print("Failed to connect the website!")
    except Exception as exc:
        print(format_tb(exc.__traceback__)[0])
