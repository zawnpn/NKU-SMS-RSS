#!/usr/bin/python3
# -*- coding: <utf-8> -*-

from config.config import *
import requests
import re
import xml.etree.ElementTree as ET
from traceback import format_tb
import sys
sys.path.append("..")


# 测试网络是否可用, 并判断是否是502页面
def test_net():
    try:
        conn = requests.get(url)
        content = conn.text
        if content.find('502 Bad Gateway') != -1:
            return False
        return True
    except:
        return False


# 获取页面下的分页数量
def get_list_page(page):
        result_re = re.compile('<span class="pages">页码：.*?<em class="all_pages">(.+?)</em></span>',  re.S)
        result = result_re.findall(page)
        return result


# 获取页面上的名称，超链接和时间内容
def get_content(page):
    result_re = re.compile("<li><a href='(.+?)' target='_blank' title='(.+?)'>.+?</a><span>(.+?)</span></li>", re.S)
    result = result_re.findall(page)
    return result


# 将获取到的分页数放到一个表里
def get_list_page_table():
    table = []
    for link in links:
        try:
            conn = requests.get(url + link)
            content = conn.text
            table.extend(get_list_page(content))
        except Exception as exc:
            print(format_tb(exc.__traceback__)[0])
    return table


# 将首页获取到的内容放到一个表里
def get_content_table():
    table = []
    for link in links:
        try:
            conn = requests.get(url + link)
            content = conn.text
            table.append(get_content(content))
        except Exception as exc:
            print(format_tb(exc.__traceback__)[0])
    return table


# 将所有分页获取到的内容放到一个表里
def get_whole_content_table():
    pages = get_list_page_table()
    i = 0
    table = []
    for link in links:
        for page_num in range(int(pages[i])+1):
            try:
                if page_num == 0:
                    conn = requests.get(url + link)
                else:
                    conn = requests.get(url+link[:-4]+str(page_num)+'.htm')
                content = conn.text
                table.append(get_content(content))
            except Exception as exc:
                print(format_tb(exc.__traceback__)[0])
        i += 1
    return table


# 获取网页上最新的内容
def get_now_latest(table):
    now_latests = [c[0][0] for c in table]
    return now_latests


# 获得本地上最新的内容
def get_local_latest():
    with open(latest_file_path, 'r') as local_latest:
        local_latests = local_latest.readlines()
    return local_latests


# 判断是否有更新
def is_updated(table, local):
    now_latests = get_now_latest(table)
    local_latests = local
    for i in range(len(now_latests)):
        if (now_latests[i].strip() + '\n') != local_latests[i]:
            return False
    return True


# 获得具体的更新
def get_update(table, local):
    result = []
    length = len(table)
    for i in range(length):
        l = []
        c = table[i]
        j = 0
        max_length = len(c)
        while (j < max_length) and (c[j][0]+'\n' != local[i]):
            l.append(c[j])
            j = j + 1
        l.reverse()
        result.append(l)
    return result


# 新建一个elem节点:
def create_elem(title, link, date):
    element_item = ET.Element('item')
    element_title = ET.Element('title')
    element_link = ET.Element('link')
    element_description = ET.Element('description')
    element_date = ET.Element('date')
    element_title.text = title
    element_link.text = link
    element_description.text = title
    element_date.text = date
    element_item.insert(0, element_date)
    element_item.insert(0, element_description)
    element_item.insert(0, element_link)
    element_item.insert(0, element_title)
    return element_item


# 更新XML文件
def update_xml(table, local):
    length = len(rss_files)
    update = get_update(table, local)
    for i in range(length):
        tree = ET.parse(rss_files[i])
        root = tree.getroot()
        channel = root.getchildren()[0]
        if update[i]:
            for item in update[i]:
                if not re.compile('http://').findall(item[0]):
                    channel.insert(3, create_elem(item[1], url + item[0], item[2]))
                else:
                    channel.insert(3, create_elem(item[1], item[0], item[2]))
        tree.write(rss_files[i])


# 更新latest文件
def update_latest(table):
    with open(latest_file_path, 'w') as f:
        latest = get_now_latest(table)
        for l in latest:
            f.write(l+'\n')
