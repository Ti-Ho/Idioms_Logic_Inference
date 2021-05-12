#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/5/11 22:25
# @Author : Tiho
# @File : synonymAntonymDataCrawl.py
# @Software: PyCharm

"""
用于爬取近义词反义词数据
"""
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from urllib import parse
from selenium.webdriver.support import expected_conditions as EC
import json
import pandas as pd

def getsoup(url):
    try:
        # 关闭弹窗
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1']")
        brower = webdriver.Chrome(options=chrome_options)

        brower.get(url)
        wait = WebDriverWait(brower, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'main')))
        soup = BeautifulSoup(brower.page_source, 'html.parser')
        brower.close()
        return soup
    except Exception as e:
        print('获取详情页失败：{}'.format(e))
        # 清除 cookie
        brower.delete_all_cookies()
        return None

def getidiom(idiom):
    """
    获取idiom成语的近义词和反义词
    :param idiom: 输入成语
    :return: synIdiomList  近义词成语的list
             antoIdiomList 反义词成语的list
    """
    base_url = r'https://hanyu.baidu.com'
    url = base_url + '/s?wd=' + parse.quote(idiom)
    # 获取成语网页的soup
    soup = getsoup(url)
    if soup is None:
        # 再试一次
        soup = getsoup(url)
        if soup is None:
            return [], []
    # 获取近义成语
    text = soup.findAll(id='synonym')
    synIdiomList = []
    if text:
        synText = text[0].find_all("a")
        for idiom_i in synText:
            synIdiomList.append(idiom_i.string)

    # 获取反义成语
    text = soup.findAll(id='antonym')
    antoIdiomList = []
    if text:
        antoText = text[0].find_all("a")
        for idiom_i in antoText:
            antoIdiomList.append(idiom_i.string)

    return synIdiomList, antoIdiomList


def getExplanationAndExample(idiom1, idiom2):
    dic1 = idiomDict.get(idiom1)
    dic2 = idiomDict.get(idiom2)
    if dic1 == None or dic2 == None:  # 在idiomDict中查找 若没有 则跳过
        return (None, None, None, None)
    example1 = dic1['example']
    example2 = dic2['example']
    example1 = re.sub('(～)+', idiom1, example1)  # 使用正则表达式 将成语加入到造句中
    example2 = re.sub('(～)+', idiom2, example2)
    example1 = re.sub('(★.*)+', "", example1)  # 使用正则表达式 去除造句来源
    example2 = re.sub('(★.*)+', "", example2)
    example1 = re.sub('(（.*)+', "", example1)
    example2 = re.sub('(（.*)+', "", example2)
    explanation1 = dic1['explanation']
    explanation2 = dic2['explanation']
    return explanation1, example1, explanation2, example2

# 保存数据
def saveData(datalist, IsFirst):
    if len(datalist) == 0:
        return
    myDf = pd.DataFrame(datalist)
    savepath = "SynAntIdiomData.csv"
    myDf.to_csv(savepath, mode='a', index=False, header=['idiom1', 'idiom2', 'explanation1', 'example1', 'explanation2', 'example2', 'label'] if IsFirst else None)

if __name__ == '__main__':
    start = time.time()
    # 构建成语字典
    idiomDict = {}
    allIdioms = []
    # 读取idiom.json中的数据 重构
    with open('idiom.json', 'r', encoding="utf-8") as f:
        lists = f.readlines()[0]
        preData = json.loads(lists)
        for data in preData:
            word = data["word"]
            allIdioms.append(word)
            idiomDict[word] = {}
            idiomDict[word]["explanation"] = data["explanation"]
            idiomDict[word]["example"] = data["example"]

    # 用于去重
    all_set = set()
    # 保存时是否添加header
    flag = True
    cnt = 0
    tot = len(allIdioms)
    for i, idiom_item in enumerate(allIdioms):
        # 输出进度
        print("爬取第{}条成语的数据,总共{}条".format(i + 1, tot))
        # 爬取数据
        allData = []
        synIdiomList, antoIdiomList = getidiom(idiom_item)
        # 处理近义词
        for synItem in synIdiomList:
            if idiomDict.get(synItem) is not None:
                # 去重
                strcat1 = {idiom_item + synItem}
                strcat2 = {synItem + idiom_item}
                dic1 = idiomDict.get(idiom_item)
                dic2 = idiomDict.get(synItem)
                if all_set & strcat1 == set() and all_set & strcat2 == set():
                    all_set = all_set | strcat1
                    explanation1, example1, explanation2, example2 = getExplanationAndExample(idiom_item, synItem)
                    allData.append([idiom_item, synItem, explanation1, example1, explanation2, example2, 1])
        # 处理反义词
        for antoItem in antoIdiomList:
            if idiomDict.get(antoItem) is not None:
                # 去重
                strcat1 = {idiom_item + antoItem}
                strcat2 = {antoItem + idiom_item}
                dic1 = idiomDict.get(idiom_item)
                dic2 = idiomDict.get(antoItem)
                if all_set & strcat1 == set() and all_set & strcat2 == set():
                    all_set = all_set | strcat1
                    explanation1, example1, explanation2, example2 = getExplanationAndExample(idiom_item, antoItem)
                    allData.append([idiom_item, antoItem, explanation1, example1, explanation2, example2, 2])
        # print('-------------------')
        # print(allData)
        # print('-------------------')
        # 保存数据
        saveData(allData, flag)
        flag = False

    end = time.time()
    print('Running time: %s Seconds' % (end - start))
    print("----------------------------数据爬取完毕----------------------------")
