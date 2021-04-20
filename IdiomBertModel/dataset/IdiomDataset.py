#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/19 19:49
# @Author : Tiho
# @File : IdiomDataset.py
# @Software: PyCharm
import configparser

from torch.utils.data import Dataset
import pandas as pd
import tqdm
import json
import torch
from sklearn.utils import shuffle


class IdiomDataset(Dataset):
    def __init__(self, corpus_path, word2idx, max_seq_len):
        self.word2idx = word2idx
        # define max length
        self.max_seq_len = max_seq_len
        # directory of corpus d
        self.corpus_path = corpus_path
        # define special symbols
        self.pad_index = 0
        self.unk_index = 1
        self.cls_index = 2
        self.sep_index = 3
        self.mask_index = 4
        self.num_index = 5

        # 加载语料
        file = pd.read_csv(self.corpus_path)
        self.lines = file.values
        self.lines = shuffle(self.lines)
        self.corpus_lines = len(self.lines)

    def __len__(self):
        return self.corpus_lines

    def __getitem__(self, item):
        sentence1, sentence2, label = self.get_text_and_label(item)
        # print(sentence1)
        # print(sentence2)
        # print(label)
        text_input1 = self.tokenize_char(sentence1)
        text_input2 = self.tokenize_char(sentence2)

        # 添加#CLS#和#SEP#特殊token
        text_input1 = [self.cls_index] + text_input1 + [self.sep_index]
        text_input2 = text_input2 + [self.sep_index]
        text_input = text_input1 + text_input2
        # 如果序列的长度超过self.max_seq_len限定的长度, 则截断
        text_input = text_input[:self.max_seq_len]

        output = {"text_input": torch.tensor(text_input),
                  "label": torch.tensor([label])}
        return output

    def get_text_and_label(self, item):
        # 获取文本和标记
        idiom1, idiom2, explanation1, example1, explanation2, example2, label = [i for i in self.lines[item]]
        if explanation1 == "无":
            explanation1 = ""
        if example1 == "无":
            example1 = ""
        if explanation2 == "无":
            explanation2 = ""
        if example2 == "无":
            example2 = ""
        # print(idiom1)
        # print(idiom2)
        sentence1 = explanation1 + example1
        sentence2= explanation2 + example2
        return sentence1, sentence2, label

    def tokenize_char(self, segments):
        return [self.word2idx.get(char, self.unk_index) for char in segments]

if __name__ == "__main__":
    config_ = configparser.ConfigParser()
    config_.read("../config/idiom_model_config.ini")
    config = config_["DEFAULT"]
    vocab_size = int(config["vocab_size"])
    # 加载字典
    word2idx = {}
    with open("../corpus/bert_word2idx_extend.json", "r", encoding="utf-8") as f:
        word2idx = json.load(f)
    # 声明训练数据集, 按照pytorch的要求定义数据集class
    train_dataset = IdiomDataset(corpus_path="../corpus/IdiomData_train.csv",
                               word2idx=word2idx,
                               max_seq_len=300,
                               )
    print(train_dataset)
    print(train_dataset[0])
