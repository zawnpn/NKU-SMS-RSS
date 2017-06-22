#!/usr/bin/python3
# -*- coding: <utf-8> -*-

import os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 主页地址
url = 'http://sms.nankai.edu.cn'
# 分页链接
links = [
    '/5547/list.htm',   # 学院新闻
    '/5536/list.htm',   # 本科生教育
    '/5537/list.htm',   # 研究生教育
    '/5538/list.htm',   # 科研动态
    '/5540/list.htm',   # 学生工作
    '/5539/list.htm',   # 公共数学
]
# 本地更新保存地址
latest_file_path = os.path.join(base_dir, 'config/latest')
# xml文件保存地址
rss_path = os.path.join(base_dir, 'rss/')
rss_files = ['xyxw.xml', 'bksjy.xml', 'yjsjy.xml', 'kydt.xml', 'xsgz.xml', 'ggsx.xml']
rss_files = [rss_path + i for i in rss_files]

# 管理员邮箱地址
From = ''
# 管理员邮箱密码
pwd = ''
# 邮箱SMTP地址
smtp_server = ''
# 邮箱端口
port = ''
# 收件人信息文件地址
ReceiverPath = os.path.join(base_dir, 'config/receivers')
