#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/6/4 10:54
# @Author : Tiho
# @File : ModelPredict.py
# @Software: PyCharm
# 模型预测脚本

import json
import re
from multiClsModelTrain import token_dict, OurTokenizer
from keras.models import load_model
from keras_bert import get_custom_objects

maxlen = 300

# 加载训练好的模型
ifPool = 1  # 控制加载模型 1 - mean max pool; 0 - CLS
syn_or_ant = 0  # 控制加载并列关系还是转折关系模型 0 - 并列关系; 0 - 转折关系
model_type = 0  # 控制加载模型为 0 - 多分类 1 - 二分类

if model_type == 0:
    if ifPool == 0:
        model = load_model("bert_model/multi_cls_bert.h5", custom_objects=get_custom_objects())
        print('加载模型：multi_cls_bert.h5')
    else:
        model = load_model("bert_model/multi_mmp_bert.h5", custom_objects=get_custom_objects())
        print('加载模型：multi_mmp_bert.h5')
else:
    if syn_or_ant == 0:
        if ifPool == 0:
            model = load_model("bert_model/bi_syn_cls_bert.h5", custom_objects=get_custom_objects())
            print('加载模型：bi_syn_cls_bert.h5')
        else:
            model = load_model("bert_model/bi_syn_mmp_bert.h5", custom_objects=get_custom_objects())
            print('加载模型：bi_syn_mmp_bert.h5')
    else:
        if ifPool == 0:
            model = load_model("bert_model/bi_ant_cls_bert.h5", custom_objects=get_custom_objects())
            print('加载模型：bi_ant_cls_bert.h5')
        else:
            model = load_model("bert_model/bi_ant_mmp_bert.h5", custom_objects=get_custom_objects())
            print('加载模型：bi_ant_mmp_bert.h5')

tokenizer = OurTokenizer(token_dict)


# 获取两个成语的解释和举例
def getExplanationAndExample(idiom1, idiom2, idiomDict):
    print(idiom1 + " " + idiom2)
    dic1 = idiomDict.get(idiom1)
    dic2 = idiomDict.get(idiom2)
    if dic1 == None:  # 在idiomDict中查找 若没有 则跳过
        return None, None, 0, 0
    if dic2 == None:
        return 0, 0, None, None

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


idiomDict = {}
# 读取idiom.json中的数据 重构f
with open('corpus/idiom.json', 'r', encoding="utf-8") as f:
    lists = f.readlines()[0]
    preData = json.loads(lists)
    for data in preData:
        word = data["word"]
        idiomDict[word] = {}
        idiomDict[word]["explanation"] = data["explanation"]
        idiomDict[word]["example"] = data["example"]

while True:
    idiom1 = input("请输入第一个成语：")
    idiom2 = input("请输入第二个成语：")
    # 预测示例成语
    InputIdiom = [idiom1, idiom2]
    flag = 0
    # 获得成语的解释 举例
    explanation1, example1, explanation2, example2 = getExplanationAndExample(InputIdiom[0], InputIdiom[1], idiomDict)
    if explanation1 == None:
        print(InputIdiom[0] + "不是成语")
        flag = 1
    if explanation2 == None:
        print(InputIdiom[1] + "不是成语")
        flag = 1

    if flag == 1:
        continue

    text1 = explanation1 if example1 == "无" else explanation1 + example1
    text2 = explanation2 if example2 == "无" else explanation2 + example2
    text1 = text1[: maxlen // 2]
    text2 = text2[: maxlen // 2]
    x1, x2 = tokenizer.encode(first=text1, second=text2)

    X1 = x1 + [0] * (maxlen - len(x1)) if len(x1) < maxlen else x1
    X2 = x2 + [0] * (maxlen - len(x2)) if len(x2) < maxlen else x2

    # 模型预测并输出预测结果
    predicted = model.predict([[X1], [X2]])
    predicted = predicted.tolist()[0]
    print(predicted)

    if predicted[0] > predicted[1] and predicted[0] > predicted[2]:
        print("两成语无逻辑关系")
    elif predicted[1] > predicted[0] and predicted[1] > predicted[2]:
        print("两成语具有并列关系")
    else:
        print("两成语具有转折关系")

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")