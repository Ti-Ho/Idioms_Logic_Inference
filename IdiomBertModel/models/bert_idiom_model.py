#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/19 20:11
# @Author : Tiho
# @File : bert_idiom_model.py
# @Software: PyCharm

"""
多分类成语推断模型
"""

from IdiomBertModel.models.bert_model import *


class Bert_Idiom_Analysis(nn.Module):
    def __init__(self, config):
        super(Bert_Idiom_Analysis, self).__init__()
        self.bert = BertModel(config)
        self.final_dense = nn.Linear(config.hidden_size, 3)  # 将分为三个类 0/1/2
        self.activation = nn.Softmax(dim=1)                  # 使用Softmax激活函数
        # 增加mean max pool的层
        self.dense = nn.Linear(config.hidden_size * 2, config.hidden_size)

    def compute_loss(self, predictions, labels):
        criterion = nn.CrossEntropyLoss()
        loss = criterion(predictions, labels)
        return loss

    def forward(self, text_input, positional_enc, labels=None, ifPool=True):
        """
        :param text_input: 文本输入
        :param positional_enc: 位置编码
        :param labels: 标签
        :param ifPool:  ifPool = True 使用Mean Max Pool
                        ifPool = False 截取#CLS#标签所对应的向量
        :return: 预测predictions 损失loss
        """
        encoded_layers, _ = self.bert(text_input, positional_enc, output_all_encoded_layers=True)
        sequence_output = encoded_layers[2]
        # predictions_ = []
        # sequence_output的维度是[batch_size, seq_len, embed_dim]
        if ifPool:                                                          # ifPool = True : 使用mean max pool
            avg_pooled = sequence_output.mean(1)
            max_pooled = torch.max(sequence_output, dim=1)
            pooled = torch.cat((avg_pooled, max_pooled[0]), dim=1)
            pooled = self.dense(pooled)
            # 下面是[batch_size, hidden_dim] 到 [batch_size, 3]的映射
            # 在这里要解决的是多分类问题
            predictions_ = self.final_dense(pooled)
        else:                                                               # ifPool = False: 截取#CLS#标签所对应的一条向量 也就是时间序列维度(seq_len)的第0条
            first_token_tensor = sequence_output[:, 0]
            # 下面是[batch_size, hidden_dim] 到 [batch_size, 3]的映射
            # 在这里要解决的是多分类问题
            predictions_ = self.final_dense(first_token_tensor)



        # print("shape = {}".format(predictions_.shape))  输出：shape = torch.Size([24, 3])
        # 用softmax函数做激活
        predictions = self.activation(predictions_)
        if labels is not None:
            # 计算loss
            loss = self.compute_loss(predictions_, labels)
            return predictions, loss
        else:
            return predictions


"""
# 单元测试
import random
def compute_loss(predictions, labels):
    criterion = nn.CrossEntropyLoss()
    loss = criterion(predictions, labels)
    return loss

if __name__ == "__main__":
    predictions = torch.randn(16, 3)
    label = torch.randint(0, 3, size=(16,))
    print(predictions)
    print(label)
    loss = compute_loss(predictions, label)
    print(loss)
"""