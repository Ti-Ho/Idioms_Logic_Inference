#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/11 18:04
# @Author : Tiho
# @File : dataCrawl.py
# @Software: PyCharm

"""
用于爬取多成语造句数据
主要爬取主页面中的子页面URL
通过调用subPageCrawl.py中的方法来获取目标数据
"""

import re
import urllib.error
import urllib.request
from bs4 import BeautifulSoup
import time
import random
from DataCrawler.subPageCrawl import getSubPageData
import pandas as pd

findLink = re.compile(r'<a href="/(.*?)"')


# 爬取网页
def getData(baseurl):
    all_set = set()
    for i in range(1, 29):
        url = baseurl + ("wordcy" if i == 1 else "wordcy_" + str(i)) + ".html"
        html = askURL(url)
        # 解析数据
        soup = BeautifulSoup(html, "html.parser")
        firstItem = True
        for cyIndex, item in enumerate(soup.find_all(class_="dotline")):
            print("****正在爬取第{}页, 第{}个成语的数据****".format(str(i), str(cyIndex + 1)))
            datalist = []
            item = str(item)
            link = re.findall(findLink, item)[0]
            subPageUrl = baseurl + link  # 获取到子页面url
            # print(subPageUrl)
            subPageData = getSubPageData(subPageUrl)  # 获取子页面数据
            for subdata_i in subPageData:  # 去重
                if len(subdata_i[0]) < 4 or len(subdata_i[1]) < 4:  # 去除成语长度小于4的脏数据
                    continue
                strcat1 = {subdata_i[0] + subdata_i[1]}
                strcat2 = {subdata_i[1] + subdata_i[0]}
                # print(strcat1)
                # print(strcat2)
                if all_set & strcat1 == set() and all_set & strcat2 == set():
                    all_set = all_set | strcat1
                    datalist.append(subdata_i)
            # print(subPageData)
            saveData(datalist, i, firstItem)
            firstItem = False
        time.sleep(random.randint(0, 3))


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


# 保存数据
def saveData(datalist, i, IsFirst):
    if len(datalist) == 0:
        return
    data = pd.DataFrame(datalist)
    savepath = "MyData/Data_" + str(i) + ".csv"
    data.to_csv(savepath, mode='a', index=False, header=['idiom1', 'idiom2', 'sentence'] if IsFirst else None)


if __name__ == "__main__":
    start = time.time()
    baseurl = "https://zaojv.com/"
    # 爬取数据
    getData(baseurl)

    end = time.time()
    print('Running time: %s Seconds' % (end - start))
    # 保存数据
    # savepath = "CrawledData.xls"
    # saveData(datalist, savepath)
    print("----------------------------数据爬取完毕----------------------------")
