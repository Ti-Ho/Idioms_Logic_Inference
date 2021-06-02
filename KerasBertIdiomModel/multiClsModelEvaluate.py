#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/6/2 9:40
# @Author : Tiho
# @File : multiClsModelEvaluate.py
# @Software: PyCharm

# 模型评估脚本
import json
import numpy as np
import pandas as pd
from keras.models import load_model
from keras_bert import get_custom_objects
from sklearn.metrics import classification_report

from multiClsModelTrain import token_dict, OurTokenizer

ifPool = 1  # 控制训练模型 1 - mean max pool; 0 - CLS
maxlen = 300
# 加载训练好的模型
if ifPool == 0:
    model = load_model("bert_model/multi_cls_bert.h5", custom_objects=get_custom_objects())
else:
    model = load_model("bert_model/multi_mmp_bert.h5", custom_objects=get_custom_objects())
tokenizer = OurTokenizer(token_dict)


# 对单句话进行预测
def predict_single_text(text, text2):
    # 利用BERT进行tokenize
    text = text[:maxlen//2]
    text2 = text2[:maxlen//2]
    x1, x2 = tokenizer.encode(first=text, second=text2)
    X1 = x1 + [0] * (maxlen - len(x1)) if len(x1) < maxlen else x1
    X2 = x2 + [0] * (maxlen - len(x2)) if len(x2) < maxlen else x2

    # 模型预测并输出预测结果
    predicted = model.predict([[X1], [X2]])
    y = np.argmax(predicted[0])
    return y


# 模型评估
def evaluate():
    test_df = pd.read_csv("corpus/IdiomData_test.csv").fillna(value="")
    true_y_list, pred_y_list = [], []
    for i in range(test_df.shape[0]):
        print("predict %d samples" % (i+1))
        idiom1, idiom2, explanation1, example1, explanation2, example2, label = test_df.iloc[i, :]
        if example1 == "无":
            sentence1 = explanation1
        else:
            sentence1 = explanation1 + str(example1)

        if example2 == "无":
            sentence2 = explanation2
        else:
            sentence2 = explanation2 + str(example2)
        pred_y = predict_single_text(sentence1, sentence2)
        true_y_list.append(label)
        pred_y_list.append(pred_y)

    return classification_report(true_y_list, pred_y_list, digits=4)


output_data = evaluate()
print("model evaluate result:\n")
print(output_data)
