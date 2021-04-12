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


def getPageUrl(page, url):
    urll = url[0:-5]
    urlr = url[-5:]
    return urll + urlr if page == 1 else urll + "_" + str(page) + urlr

def delChars(sentence):
    sentence = re.sub(r'^(\d+)*(\.)*(\()*(\))*(（)*(）)*(、)*', "", sentence)
    sentence = sentence.strip()
    return sentence

def getSubPageData(baseurl):
    datalist = []
    # 获取页数
    html = askURL(baseurl)
    soup = BeautifulSoup(html, "html.parser")
    bottom = soup.select("#div_main_left > div")[1]
    # print(bottom)
    bottom = str(bottom)
    pages = re.findall(findPage, bottom)[0]
    # print(page)

    # 解析每一页的数据
    for page in range(1, int(pages) + 1):
        url = getPageUrl(page, baseurl)
        subPageHtml = askURL(url)
        subPageSoup = BeautifulSoup(subPageHtml, "html.parser")
        t_list = subPageSoup.select("#all > div")
        for item in t_list:
            if item.em is None or item.a is None:
                continue
            # 成语
            cy = []
            cy.append(item.em.text)
            for cyi in item.find_all("a"):
                cy.append(cyi.text)
            print(cy)
            # 造句
            sentence = item.text
            sentence = delChars(sentence)
            print(sentence)
            print("---------------------------------------")
            if len(cy) == 1:
                continue
            # TODO 多成语处理成双成语
            

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
    baseurl = "https://zaojv.com/9669285.html"
    # baseurl = "https://zaojv.com/6589307.html"  # 单页例子
    # baseurl = "https://zaojv.com/7562039.html"
    # 爬取子页面数据
    datalist = getSubPageData(baseurl)
    print("----------------------------子页数据爬取完毕----------------------------")
