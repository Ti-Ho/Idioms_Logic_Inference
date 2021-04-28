#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/24 9:54
# @Author : Tiho
# @File : InferenceDataset.py
# @Software: PyCharm

"""
语料加载与tokenize处理
用于【多分类】的Bert【模型推断】 IdiomBertInference
数据(text_list)中的字段:成语1解释+举例, 成语2解释+举例 ('+'表示连接)
"""

import warnings
import torch
import numpy as np


class InferenceDataset():
    def __init__(self, hidden_dim, word2idx, max_positions):
        """
        :param hidden_dim: 模型hidden维度
        :param word2idx: 字典, for tokenizing
        :param max_positions: 最大positions的长度, 用来初始化sinosoid positional encoding
        """
        self.max_positions = max_positions + 3
        self.hidden_dim = hidden_dim
        self.word2idx = word2idx
        self.pad_index = 0
        self.unk_index = 1
        self.cls_index = 2
        self.sep_index = 3
        self.mask_index = 4
        self.num_index = 5
        self.positional_encoding = self.init_positional_encoding()

    def init_positional_encoding(self):
        # 初始化 sinosoid
        position_enc = np.array([
            [pos / np.power(10000, 2 * i / self.hidden_dim) for i in range(self.hidden_dim)]
            if pos != 0 else np.zeros(self.hidden_dim) for pos in range(self.max_positions)])

        position_enc[1:, 0::2] = np.sin(position_enc[1:, 0::2])  # dim 2i
        position_enc[1:, 1::2] = np.cos(position_enc[1:, 1::2])  # dim 2i+1
        denominator = np.sqrt(np.sum(position_enc ** 2, axis=1, keepdims=True))
        position_enc = position_enc / (denominator + 1e-8)
        return position_enc

    def tokenize(self, text_or_label, dict):
        # tokenize a sentence, return a list of tokens sequence
        return [dict.get(i, self.unk_index) for i in text_or_label]

    def __call__(self, text_list, max_seq_len):
        """
        预处理
        :param text_list: 输入格式为[[成语1解释+举例, 成语2解释+举例], [], ..., []]
        :param max_seq_len:
        :return: 文本的token, 位置编码
        """
        text_list_len = [len(text[0]) + len(text[1]) for text in text_list]
        # 判断输入文本长度是否合规, 是否小于等于
        if max(text_list_len) > max_seq_len:
            warnings.warn(
                "maximum length of input texts exceeds \"max_seq_len\"! exceeded length will be cut off! 输入的最大文本长度大于指定最大长度, 多余的部分将会被剪切!")

        batch_max_seq_len = max_seq_len + 3
        # tokenize
        texts_tokens = [[self.tokenize(text[0], self.word2idx), self.tokenize(text[1], self.word2idx)] for text in
                        text_list]
        # add cls, sep
        texts_tokens = [[self.cls_index] + text[0] + [self.sep_index] + text[1] + [self.sep_index] for text in
                        texts_tokens]
        # print(texts_tokens)
        # padding
        texts_tokens = [torch.tensor(i) for i in texts_tokens]
        texts_tokens = torch.nn.utils.rnn.pad_sequence(texts_tokens, batch_first=True)
        positional_enc = \
            torch.from_numpy(self.positional_encoding[:batch_max_seq_len]).type(torch.FloatTensor)
        return texts_tokens, positional_enc


"""
# 单元测试
import json
if __name__ == "__main__":
    text_list = [['墨守战国时墨翟善于守城；成规现成的或久已通行的规则、方法。指思想保守，守着老规矩不肯改变。墨守成规，不敢勇于创造也决然是和客观事物的发展规律不能相容的。', '对目前的情况习惯了，不愿改变。'],
                 ['雪洗刷掉。报冤仇，除仇恨。滥官害民贱徒，把我全家诛戮，今日正好报仇雪恨！', '饮恨强忍怨恨；吞声哭泣而不敢出声。形容忍恨含悲，不敢表露。'],
                 ['终日整天。整天吃饱饭，不动脑筋，不干什么正经事。人如果饱食终日，无所用心，那是最没有出息的。', '饥肠饥饿的肚子；辘辘车行声。肚子饿得咕咕直响。形容十分饥饿。这时已错了传膳的时刻，都是天色微明吃的早饭，至此无不饥肠辘辘。']]
    # 加载字典
    word2idx = {}
    with open("../corpus/bert_word2idx_extend.json", "r", encoding="utf-8") as f:
        word2idx = json.load(f)

    dataSet = InferenceDataset(384, word2idx, 300)
    dataSet(text_list, 300)
"""
