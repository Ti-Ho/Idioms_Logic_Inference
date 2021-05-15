#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/24 9:40
# @Author : Tiho
# @File : IdiomBertInference.py
# @Software: PyCharm

"""
BERT模型推断 多分类
输入：InputIdiom [[成语1,成语2], ..., [], []]
输出：多分类各自的概率
"""

from dataset.InferenceDataset import InferenceDataset
from models.bert_idiom_model import *
import numpy as np
import configparser
import os
import json
import re


class IdiomLogicAnalysis:
    def __init__(self, max_seq_len,
                 batch_size,
                 with_cuda=True,  # 是否使用GPU, 如未找到GPU, 则自动切换CPU
                 ifPool=True
                 ):
        config_ = configparser.ConfigParser()
        config_.read("./config/idiom_model_config.ini")
        self.config = config_["DEFAULT"]
        self.vocab_size = int(self.config["vocab_size"])
        self.batch_size = batch_size
        self.ifPool = ifPool
        # 加载字典
        with open(self.config["word2idx_path"], "r", encoding="utf-8") as f:
            self.word2idx = json.load(f)
        # 判断是否有可用GPU
        cuda_condition = torch.cuda.is_available() and with_cuda
        self.device = torch.device("cuda:0" if cuda_condition else "cpu")
        # 允许的最大序列长度
        self.max_seq_len = max_seq_len
        # 定义模型超参数
        bertconfig = BertConfig(vocab_size=self.vocab_size)
        # 初始化BERT情感分析模型
        self.bert_model = Bert_Idiom_Analysis(config=bertconfig)
        # 将模型发送到计算设备(GPU或CPU)
        self.bert_model.to(self.device)
        # 开去evaluation模型, 关闭模型内部的dropout层
        self.bert_model.eval()

        # 初始化位置编码
        self.hidden_dim = bertconfig.hidden_size
        self.positional_enc = self.init_positional_encoding()
        # 扩展位置编码的维度, 留出batch维度,
        # 即positional_enc: [batch_size, embedding_dimension]
        self.positional_enc = torch.unsqueeze(self.positional_enc, dim=0)

        # 初始化预处理器
        self.process_batch = InferenceDataset(hidden_dim=bertconfig.hidden_size,
                                              max_positions=max_seq_len,
                                              word2idx=self.word2idx)
        # 加载BERT预训练模型
        self.load_model(self.bert_model, dir_path=self.config["multi_pool_state_dict_dir" if ifPool else "multi_cls_state_dict_dir"])

    def init_positional_encoding(self):
        position_enc = np.array([
            [pos / np.power(10000, 2 * i / self.hidden_dim) for i in range(self.hidden_dim)]
            if pos != 0 else np.zeros(self.hidden_dim) for pos in range(self.max_seq_len)])

        position_enc[1:, 0::2] = np.sin(position_enc[1:, 0::2])  # dim 2i
        position_enc[1:, 1::2] = np.cos(position_enc[1:, 1::2])  # dim 2i+1
        denominator = np.sqrt(np.sum(position_enc ** 2, axis=1, keepdims=True))
        # 归一化
        position_enc = position_enc / (denominator + 1e-8)
        position_enc = torch.from_numpy(position_enc).type(torch.FloatTensor)
        return position_enc

    def load_model(self, model, dir_path="../output"):
        checkpoint_dir = self.find_most_recent_state_dict(dir_path)
        checkpoint = torch.load(checkpoint_dir)
        model.load_state_dict(checkpoint["model_state_dict"], strict=True)
        torch.cuda.empty_cache()
        model.to(self.device)
        print("{} loaded!".format(checkpoint_dir))

    def __call__(self, text_list, batch_size=1):
        """
        :param text_list:
        :param batch_size: 为了注意力矩阵的可视化, batch_size只能为1, 即单句
        :return:
        """
        max_seq_len = max([len(text[0]) + len(text[1]) for text in text_list])
        # 预处理, 获取batch
        texts_tokens, positional_enc = \
            self.process_batch(text_list, max_seq_len=max_seq_len)
        # 准备positional encoding
        positional_enc = torch.unsqueeze(positional_enc, dim=0).to(self.device)

        # 正向
        n_batches = math.ceil(len(texts_tokens) / batch_size)

        # 数据按mini batch切片过正向, 这里为了可视化所以吧batch size设为1
        for i in range(n_batches):
            start = i * batch_size
            end = start + batch_size
            # 切片
            texts_tokens_ = texts_tokens[start: end].to(self.device)

            predictions = self.bert_model.forward(text_input=texts_tokens_,
                                                  positional_enc=positional_enc,
                                                  ifPool=self.ifPool
                                                  )

            self.multiClsIdiomInference(predictions)

    # 根据预测结果输出信息
    def multiClsIdiomInference(self, predictions):
        print(predictions)

    def sentiment_print_func(self, text, pred, threshold):
        print(text)
        if pred >= threshold:
            print("正样本, 输出值{:.2f}".format(pred))
        else:
            print("负样本, 输出值{:.2f}".format(pred))
        print("----------")

    def find_most_recent_state_dict(self, dir_path):
        """
        :param dir_path: 存储所有模型文件的目录
        :return: 返回最新的模型文件路径, 按模型名称最后一位数进行排序
        """
        dic_lis = [i for i in os.listdir(dir_path)]
        if len(dic_lis) == 0:
            raise FileNotFoundError("can not find any state dict in {}!".format(dir_path))
        dic_lis = [i for i in dic_lis if "model" in i]
        dic_lis = sorted(dic_lis, key=lambda k: int(k.split(".")[-1]))
        return dir_path + "/" + dic_lis[-1]


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


if __name__ == '__main__':
    # mean max pool 多分类推断
    # model = IdiomLogicAnalysis(max_seq_len=300, batch_size=1, ifPool=True)
    # Cls 多分类推断
    model = IdiomLogicAnalysis(max_seq_len=300, batch_size=1, ifPool=False)
    InputIdiom = [
        # ["墨守成规", "安于现状"], # 1
        # ["报仇雪恨", "饮恨吞声"], # 2
        # ["饱食终日", "饥肠辘辘"], # 2
        # ["浑浑噩噩", "懒懒散散"], # 1
        # ["好吃懒做", "衣来伸手,饭来张口"], # 1
        # ["白纸黑字","口说无凭"],  # 2
        ["胸有成竹", "十拿九稳"],  # 1
        # ["报仇雪恨", "曲意奉迎"],   # 2
        # ["络绎不绝", "比肩接踵"]  # 1
    ]

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

    # 获得成语的解释 举例
    textList = []
    for idiom_i in InputIdiom:
        explanation1, example1, explanation2, example2 = getExplanationAndExample(idiom_i[0], idiom_i[1], idiomDict)
        if explanation1 == None:
            print(idiom_i[0] + "不是成语")
            continue

        if explanation2 == None:
            print(idiom_i[1] + "不是成语")
            continue

        textList.append([explanation1 if example1 == "无" else explanation1 + example1,
                         explanation2 if example2 == "无" else explanation2 + example2])
    # print(textList)
    model(textList)
