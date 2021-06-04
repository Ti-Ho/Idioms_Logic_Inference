#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/6/4 12:41
# @Author : Tiho
# @File : IdiomBertFlask.py
# @Software: PyCharm

# 解决跨域
from flask_cors import CORS
from flask import Flask, request, jsonify
import json
import numpy as np
import re
from multiClsModelTrain import token_dict, OurTokenizer
from keras.models import load_model
from keras_bert import get_custom_objects
import os
import configparser
import json

maxlen = 300
app = Flask(__name__)
CORS(app, supports_credentials=True)

# 加载训练好的模型
ifPool = 0      # 控制加载模型 1 - mean max pool; 0 - CLS
syn_or_ant = 0  # 控制加载并列关系还是转折关系模型 0 - 并列关系; 0 - 转折关系
model_type = 1  # 控制加载模型为 0 - 多分类 1 - 二分类

tokenizer = OurTokenizer(token_dict)
# 获取两个成语的解释和举例
def getExplanationAndExample(idiom1, idiom2, idiomDict):
    # print(idiom1 + " " + idiom2)
    dic1 = idiomDict.get(idiom1)
    dic2 = idiomDict.get(idiom2)
    if dic1 is None:  # 在idiomDict中查找 若没有 则跳过
        return None, None, 0, 0
    if dic2 is None:
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

@app.route("/get_res", methods=["POST"])
def idiom_api():
    """
    后端接口:POST请求
    POST请求数据:idiom1: 成语1
                idiom2: 成语2
                model_type: 0->多分类模型 1->二分类模型
                ifPool: 1 使用mean max pool; 0 使用CLS向量
    返回数据: 二分类: p1是并列关系的概率, p2是转折关系的概率
             多分类: p0无逻辑关系的概率, p1是并列关系的概率, p2是转折关系的概率
    """
    if request.method == "POST":
        idiom1 = request.form["idiom1"]
        idiom2 = request.form["idiom2"]
        model_type = int(request.form["model_type"])
        ifPool = int(request.form["ifPool"])
        print("{} {} {} {}".format(idiom1, idiom2, model_type, ifPool))
        # 获取两个成语的解释与造句
        explanation1, example1, explanation2, example2 = getExplanationAndExample(idiom1, idiom2, idiomDict)
        if explanation1 is None:
            print(idiom1 + "不是成语")
            return jsonify({"status": 1})
        if explanation2 is None:
            print(idiom2 + "不是成语")
            return jsonify({"status": 2})

        text1 = explanation1 if example1 == "无" else explanation1 + example1
        text2 = explanation2 if example2 == "无" else explanation2 + example2
        text1 = text1[: maxlen // 2]
        text2 = text2[: maxlen // 2]
        x1, x2 = tokenizer.encode(first=text1, second=text2)

        X1 = x1 + [0] * (maxlen - len(x1)) if len(x1) < maxlen else x1
        X2 = x2 + [0] * (maxlen - len(x2)) if len(x2) < maxlen else x2

        # 模型预测并输出预测结果
        if model_type == 0:
            if ifPool == 0:
                predictions = multi_cls_model.predict([[X1], [X2]])
            else:
                predictions = multi_pool_model.predict([[X1], [X2]])
        else:
            if syn_or_ant == 0:
                if ifPool == 0:
                    predictions = bi_syn_cls_model.predict([[X1], [X2]])
                else:
                    predictions = bi_syn_pool_model.predict([[X1], [X2]])
            else:
                if ifPool == 0:
                    predictions = bi_ant_cls_model.predict([[X1], [X2]])
                else:
                    predictions = bi_ant_pool_model.predict([[X1], [X2]])

        return jsonify({
            "status": 0,
            "predictions": predictions,
            "explanation1": explanation1,
            "example1": example1,
            "explanation2": explanation2,
            "example2": example2
        })


if __name__ == '__main__':
    print("######加载模型中######")
    multi_cls_model = load_model("bert_model/multi_cls_bert.h5", custom_objects=get_custom_objects())
    multi_pool_model = load_model("bert_model/multi_mmp_bert.h5", custom_objects=get_custom_objects())
    bi_syn_cls_model = load_model("bert_model/bi_syn_cls_bert.h5", custom_objects=get_custom_objects())
    bi_syn_pool_model = load_model("bert_model/bi_syn_mmp_bert.h5", custom_objects=get_custom_objects())
    bi_ant_cls_model = load_model("bert_model/bi_ant_cls_bert.h5", custom_objects=get_custom_objects())
    bi_ant_pool_model = load_model("bert_model/bi_ant_mmp_bert.h5", custom_objects=get_custom_objects())
    print("######加载模型完毕######")

    print("######加载新华字典数据集######")
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
    print("######加载完毕######")

    app.run()