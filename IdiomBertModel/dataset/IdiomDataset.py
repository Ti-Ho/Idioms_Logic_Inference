#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/19 19:49
# @Author : Tiho
# @File : IdiomDataset.py
# @Software: PyCharm

from torch.utils.data import Dataset
import tqdm
import json
import torch
import random
import numpy as np
from sklearn.utils import shuffle
import re


class IdiomDataset(Dataset):
    def __init__(self, corpus_path, word2idx, max_seq_len, data_regularization=False):
        self.data_regularization = data_regularization
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
        with open(corpus_path, "r", encoding="utf-8") as f:
            # 将数据集全部加载到内存
            self.lines = [eval(line) for line in tqdm.tqdm(f, desc="Loading Dataset")]
            # 打乱顺序
            self.lines = shuffle(self.lines)
            # 获取数据长度(条数)
            self.corpus_lines = len(self.lines)
