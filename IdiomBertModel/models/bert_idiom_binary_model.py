#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/29 22:06
# @Author : Tiho
# @File : bert_idiom_binary_model.py
# @Software: PyCharm

"""
二分类成语推断模型
"""

from models.bert_model import *


class Bert_Idiom_Analysis_v2(nn.Module):
    def __init__(self, config):
        super(Bert_Idiom_Analysis_v2, self).__init__()
        self.bert = BertModel(config)
        self.final_dense = nn.Linear(config.hidden_size, 1)     # 将分为两个类    0/1
        self.activation = nn.Sigmoid()                          # 使用Sigmoid激活函数
        # 增加mean max pool的层
        self.dense = nn.Linear(config.hidden_size * 2, config.hidden_size)

    def compute_loss(self, predictions, labels):
        # 将预测和标记的维度展平, 防止出现维度不一致
        predictions = predictions.view(-1)
        labels = labels.float().view(-1)
        epsilon = 1e-8
        # 交叉熵
        loss = \
            - labels * torch.log(predictions + epsilon) - \
            (torch.tensor(1.0) - labels) * torch.log(torch.tensor(1.0) - predictions + epsilon)
        # 求均值, 并返回可以反传的loss
        # loss为一个实数
        loss = torch.mean(loss)
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
        # sequence_output的维度是[batch_size, seq_len, embed_dim]
        if ifPool:                                                          # ifPool = True : 使用mean max pool
            avg_pooled = sequence_output.mean(1)
            max_pooled = torch.max(sequence_output, dim=1)
            pooled = torch.cat((avg_pooled, max_pooled[0]), dim=1)
            pooled = self.dense(pooled)
            # 下面是[batch_size, hidden_dim] 到 [batch_size, 1]的映射
            # 在这里要解决的是二分类问题
            predictions = self.final_dense(pooled)
        else:                                                               # ifPool = False: 截取#CLS#标签所对应的一条向量也就是时间序列维度(seq_len)的第0条
            first_token_tensor = sequence_output[:, 0]
            # 下面是[batch_size, hidden_dim] 到 [batch_size, 1]的映射
            # 在这里要解决的是二分类问题
            predictions = self.final_dense(first_token_tensor)

        predictions = self.activation(predictions)
        if labels is not None:
            # 计算loss
            loss = self.compute_loss(predictions, labels)
            return predictions, loss
        else:
            return predictions

"""
# 单元测试
import random
def compute_loss(predictions, labels):
    # 将预测和标记的维度展平, 防止出现维度不一致
    predictions = predictions.view(-1)
    labels = labels.float().view(-1)
    epsilon = 1e-8
    # 交叉熵
    loss = - labels * torch.log(predictions + epsilon) - (torch.tensor(1.0) - labels) * torch.log(torch.tensor(1.0) - predictions + epsilon)
    # 求均值, 并返回可以反传的loss
    # loss为一个实数
    loss = torch.mean(loss)
    return loss

if __name__ == "__main__":
    predictions = torch.rand(16, 1)
    label = torch.randint(0, 2, size=(16,))
    print(predictions)
    print(label)
    loss = compute_loss(predictions, label)
    print(loss)
"""