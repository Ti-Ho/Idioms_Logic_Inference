#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/11 19:14
# @Author : Tiho
# @File : subPageCrawl.py
# @Software: PyCharm

"""
从子页面中爬取含有多个成语的造句
"""

import re
import urllib.error
import urllib.request
from bs4 import BeautifulSoup

findPage = re.compile(r'第 1/(.*?) 页')

def getSubPageData(baseurl):
    datalist = []
    # 获取页数
    html = askURL(baseurl)
    soup = BeautifulSoup(html, "html.parser")
    bottom = soup.select("#div_main_left > div")[1]
    # print(bottom)

    bottom = str(bottom)
    page = re.findall(findPage, bottom)[0]
    print(page)
    return datalist

# 得到指定URL的网页内容
def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html

if __name__ == "__main__":
    baseurl = "https://zaojv.com/4420198.html"
    # 爬取子页面数据
    datalist = getSubPageData(baseurl)
    print("----------------------------数据爬取完毕----------------------------")