#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/6/1 16:08
# @Author : Tiho
# @File : multiClsModelTrain.py
# @Software: PyCharm

import codecs
import pandas as pd
import numpy as np
from keras_bert import load_trained_model_from_checkpoint, Tokenizer
from keras.layers import *
from keras.models import Model
from keras.optimizers import Adam
import tensorflow as tf
# 建议长度<=510
maxlen = 300
BATCH_SIZE = 1
config_path = './chinese_L-12_H-768_A-12/bert_config.json'
checkpoint_path = './chinese_L-12_H-768_A-12/bert_model.ckpt'
dict_path = './chinese_L-12_H-768_A-12/vocab.txt'

ifPool = 0      # 控制训练模型 1 - mean max pool; 0 - CLS
syn_or_ant = 0  # 控制训练并列关系还是转折关系模型 0 - 并列关系; 0 - 转折关系

token_dict = {}
with codecs.open(dict_path, 'r', 'utf-8') as reader:
    for line in reader:
        token = line.strip()
        token_dict[token] = len(token_dict)


class OurTokenizer(Tokenizer):
    def _tokenize(self, text):
        R = []
        for c in text:
            if c in self._token_dict:
                R.append(c)
            else:
                R.append('[UNK]')   # 剩余的字符是[UNK]
        return R


tokenizer = OurTokenizer(token_dict)

def seq_padding(X, padding=0):
    L = [len(x) for x in X]
    ML = max(L)
    return np.array([
        np.concatenate([x, [padding] * (ML - len(x))]) if len(x) < ML else x for x in X
    ])

class DataGenerator:

    def __init__(self, data, batch_size=BATCH_SIZE):
        self.data = data
        self.batch_size = batch_size
        self.steps = len(self.data) // self.batch_size
        if len(self.data) % self.batch_size != 0:
            self.steps += 1

    def __len__(self):
        return self.steps

    def __iter__(self):
        while True:
            idxs = list(range(len(self.data)))
            np.random.shuffle(idxs)
            X1, X2, Y = [], [], []
            for i in idxs:
                d = self.data[i]
                text = d[0][:maxlen//2]
                text2 = d[1][:maxlen//2]
                x1, x2 = tokenizer.encode(first=text, second=text2)
                y = d[2]
                X1.append(x1)
                X2.append(x2)
                Y.append(y)
                if len(X1) == self.batch_size or i == idxs[-1]:
                    X1 = seq_padding(X1)
                    X2 = seq_padding(X2)
                    Y = seq_padding(Y)
                    yield [X1, X2], Y
                    [X1, X2, Y] = [], [], []


# 构建模型
def create_cls_model():
    bert_model = load_trained_model_from_checkpoint(config_path, checkpoint_path, seq_len=None)

    for layer in bert_model.layers:
        layer.trainable = True

    x1_in = Input(shape=(None,))
    x2_in = Input(shape=(None,))

    x = bert_model([x1_in, x2_in])
    cls_layer = Lambda(lambda x: x[:, 0])(x)    # 取出[CLS]对应的向量用来做分类
    p = Dense(1, activation='sigmoid')(cls_layer)     # 多分类

    model = Model([x1_in, x2_in], p)
    model.compile(
        loss='categorical_crossentropy',
        optimizer=Adam(1e-5),   # 用足够小的学习率
        metrics=['accuracy']
    )
    # model.summary()

    return model

def myMean(x):
    return tf.reduce_mean(x, axis=1)
def myMax(x):
    return tf.reduce_max(x, axis=1)

def create_mmp_model():
    bert_model = load_trained_model_from_checkpoint(config_path, checkpoint_path, seq_len=None)

    for layer in bert_model.layers:
        layer.trainable = True

    x1_in = Input(shape=(None,))
    x2_in = Input(shape=(None,))

    x = bert_model([x1_in, x2_in])
    mean_pool = Lambda(myMean)(x)
    max_pool = Lambda(myMax)(x)
    pool = concatenate([mean_pool, max_pool], axis=1)
    tmp = Dense(int(mean_pool.shape[1]))(pool)
    p = Dense(1, activation="sigmoid")(tmp)
    model = Model([x1_in, x2_in], p)
    model.compile(
        loss='categorical_crossentropy',
        optimizer=Adam(1e-5),  # 用足够小的学习率
        metrics=['accuracy']
    )
    # model.summary()

    return model


if __name__ == '__main__':
    # 数据处理, 读取训练集和测试集
    print("begin data processing...")
    if syn_or_ant == 0:
        train_df = pd.read_csv("corpus/BinaryClsData1/BiIdiomData_train.csv").fillna(value="")
        test_df = pd.read_csv("corpus/BinaryClsData1/BiIdiomData_test.csv").fillna(value="")
    else:
        train_df = pd.read_csv("corpus/BinaryClsData2/BiIdiomData_train.csv").fillna(value="")
        test_df = pd.read_csv("corpus/BinaryClsData2/BiIdiomData_test.csv").fillna(value="")

    labels = [0, 1]

    train_data = []
    test_data = []
    for i in range(train_df.shape[0]):
        idiom1, idiom2, explanation1, example1, explanation2, example2, label = train_df.iloc[i, :]
        if example1 == "无":
            sentence1 = explanation1
        else:
            sentence1 = explanation1 + str(example1)

        if example2 == "无":
            sentence2 = explanation2
        else:
            sentence2 = explanation2 + str(example2)
        label_id = [0] * len(labels)
        for j, _ in enumerate(labels):
            if _ == label:
                label_id[j] = 1
        train_data.append((sentence1, sentence2, label_id))

    for i in range(test_df.shape[0]):
        idiom1, idiom2, explanation1, example1, explanation2, example2, label = test_df.iloc[i, :]
        if example1 == "无":
            sentence1 = explanation1
        else:
            sentence1 = explanation1 + str(example1)

        if example2 == "无":
            sentence2 = explanation2
        else:
            sentence2 = explanation2 + str(example2)
        label_id = [0] * len(labels)
        for j, _ in enumerate(labels):
            if _ == label:
                label_id[j] = 1
        test_data.append((sentence1, sentence2, label_id))

    print("finish data processing!")

    # 模型训练
    if ifPool == 0:      # 1. 训练输出层为cls的模型
        model = create_cls_model()
    else:                # 2. 训练输出层为mean max pool的模型
        model = create_mmp_model()
    train_D = DataGenerator(train_data)
    test_D = DataGenerator(test_data)

    print("begin model training...")
    history = model.fit_generator(
        train_D.__iter__(),
        steps_per_epoch=len(train_D),
        epochs=2,
        validation_data=test_D.__iter__(),
        validation_steps=len(test_D)
    )

    print("finish model training!")

    # 模型保存
    if syn_or_ant == 0:
        if ifPool == 0:
            model.save('bert_model/bi_syn_cls_bert.h5')
        else:
            model.save('bert_model/bi_syn_mmp_bert.h5')
    else:
        if ifPool == 0:
            model.save('bert_model/bi_ant_cls_bert.h5')
        else:
            model.save('bert_model/bi_ant_mmp_bert.h5')
    print("Model saved!")

    result = model.evaluate_generator(test_D.__iter__(), steps=len(test_D))
    print("模型评估结果:", result)