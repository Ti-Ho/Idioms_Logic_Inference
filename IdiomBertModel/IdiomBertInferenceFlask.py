#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/5/5 14:38
# @Author : Tiho
# @File : IdiomBertInferenceFlask.py
# @Software: PyCharm

# 解决跨域
from flask_cors import CORS
from flask import Flask, request, jsonify
from IdiomBertModel.dataset.InferenceDataset import InferenceDataset
from IdiomBertModel.models.bert_idiom_model import *
from IdiomBertModel.models.bert_idiom_binary_model import *
import numpy as np
import configparser
import os
import json
import re

app = Flask(__name__)
CORS(app, supports_credentials=True)


# 成语推断类
class IdiomLogicAnalysis:
    def __init__(self, max_seq_len,
                 with_cuda=True,  # 是否使用GPU, 如未找到GPU, 则自动切换CPU
                 ):
        config_ = configparser.ConfigParser()
        config_.read("./config/idiom_model_config.ini")
        self.config = config_["DEFAULT"]
        self.vocab_size = int(self.config["vocab_size"])
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
        # 初始化模型
        # 1.【多分类】【CLS】
        # 初始化BERT情感分析模型
        self.cls_bert_model = Bert_Idiom_Analysis(config=bertconfig)
        # 将模型发送到计算设备(GPU或CPU)
        self.cls_bert_model.to(self.device)
        # 开去evaluation模型, 关闭模型内部的dropout层
        self.cls_bert_model.eval()
        # 2.【多分类】【mean max pool】
        self.pool_bert_model = Bert_Idiom_Analysis(config=bertconfig)
        self.pool_bert_model.to(self.device)
        self.pool_bert_model.eval()
        # 3. 【二分类】【CLS】【并列关系判断】
        self.bicls_bert_model = Bert_Idiom_Analysis_v2(config=bertconfig)
        self.bicls_bert_model.to(self.device)
        self.bicls_bert_model.eval()
        # 4. 【二分类】【mean max pool】【并列关系判断】
        self.bipool_bert_model = Bert_Idiom_Analysis_v2(config=bertconfig)
        self.bipool_bert_model.to(self.device)
        self.bipool_bert_model.eval()
        # 5. 【二分类】【CLS】【转折关系判断】
        self.bicls_bert_model2 = Bert_Idiom_Analysis_v2(config=bertconfig)
        self.bicls_bert_model2.to(self.device)
        self.bicls_bert_model2.eval()
        # 6. 【二分类】【mean max pool】【转折关系判断】
        self.bipool_bert_model2 = Bert_Idiom_Analysis_v2(config=bertconfig)
        self.bipool_bert_model2.to(self.device)
        self.bipool_bert_model2.eval()

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
        self.load_model(self.cls_bert_model, dir_path=self.config["multi_cls_state_dict_dir"])
        self.load_model(self.pool_bert_model, dir_path=self.config["multi_pool_state_dict_dir"])
        self.load_model(self.bicls_bert_model, dir_path=self.config["bi_cls_state_dict_dir"])
        self.load_model(self.bipool_bert_model, dir_path=self.config["bi_pool_state_dict_dir"])
        self.load_model(self.bicls_bert_model2, dir_path=self.config["bi_cls_state_dict_dir2"])
        self.load_model(self.bipool_bert_model2, dir_path=self.config["bi_pool_state_dict_dir2"])

    # 位置编码
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

    # 加载模型
    def load_model(self, model, dir_path="../output"):
        checkpoint_dir = self.find_most_recent_state_dict(dir_path)
        checkpoint = torch.load(checkpoint_dir)
        model.load_state_dict(checkpoint["model_state_dict"], strict=True)
        torch.cuda.empty_cache()
        model.to(self.device)
        print("{} loaded!".format(checkpoint_dir))

    # 模型推断
    def __call__(self, idiom1msg, idiom2msg, model_type, ifPool):
        """
        :param idiom1msg:
        :param idiom2msg:
        :param batch_size:
        :return:
        """
        max_seq_len = len(idiom1msg) + len(idiom2msg)
        # 预处理, 获取batch
        texts_tokens, positional_enc = \
            self.process_batch([[idiom1msg, idiom2msg]], max_seq_len=max_seq_len)
        # 准备positional encoding
        positional_enc = torch.unsqueeze(positional_enc, dim=0).to(self.device)

        # 数据按mini batch切片过正向, 这里为了可视化所以吧batch size设为1
        texts_tokens = texts_tokens.to(self.device)
        if model_type == 0:  # 多分类
            if ifPool:  # mean max pool
                predictions = self.pool_bert_model.forward(text_input=texts_tokens, positional_enc=positional_enc,
                                                           ifPool=ifPool)
            else:  # cls
                predictions = self.cls_bert_model.forward(text_input=texts_tokens, positional_enc=positional_enc,
                                                          ifPool=ifPool)
            return predictions.detach().cpu().numpy().reshape(-1).tolist()
        else:  # 二分类
            if ifPool:  # mean max pool
                p1 = self.bipool_bert_model.forward(text_input=texts_tokens, positional_enc=positional_enc,
                                                    ifPool=ifPool)
                p2 = self.bipool_bert_model2.forward(text_input=texts_tokens, positional_enc=positional_enc,
                                                     ifPool=ifPool)
                predictions = [p1.detach().cpu().reshape(-1).tolist()[0], p2.detach().cpu().reshape(-1).tolist()[0]]
            else:  # cls
                p1 = self.bicls_bert_model.forward(text_input=texts_tokens, positional_enc=positional_enc,
                                                   ifPool=ifPool)
                p2 = self.bicls_bert_model2.forward(text_input=texts_tokens, positional_enc=positional_enc,
                                                    ifPool=ifPool)
                predictions = [p1.detach().cpu().reshape(-1).tolist()[0], p2.detach().cpu().reshape(-1).tolist()[0]]
            return predictions

    # 寻找模型加载文件
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
                ifPool: True使用mean max pool;False使用CLS向量
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

        predictions = model(explanation1 if example1 == "无" else explanation1 + example1,
                            explanation2 if example2 == "无" else explanation2 + example2,
                            model_type=model_type,
                            ifPool=ifPool)

        return jsonify({
            "status": 0,
            "predictions": predictions,
        })


if __name__ == "__main__":
    print("######加载模型中######")
    model = IdiomLogicAnalysis(max_seq_len=300)
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
