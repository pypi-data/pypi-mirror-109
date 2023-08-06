# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2020 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
数据集定义

Authors: fubo01
Date: 2020/03/11 00:00:00
"""
import logging
import copy
from typing import Dict
import torch

from ...base.abstract import AbstractDataSet, AbstractTokenizer
from ...base.model_data import SentClassifySample


class SentSimilarityDataSet(AbstractDataSet):
    """
    文本相关性计算数据集管理
    {"queries": ["pivot", "positive", "negative"], "labels": []}
    """

    def __init__(self, tokenizer: AbstractTokenizer):
        super().__init__()
        self.__tokenizer = tokenizer

    def parse_sample(self, line: str) -> Dict:
        """
        解析样本数据
        :param line:
        :return:
        """

        sample = SentClassifySample.parse_raw(line)
        if len(sample.queries) != 3:
            logging.warning("Not enough queries %s" % line)
            return {}

        pivot_tokens = self.__tokenizer.tokenize(sample.queries[0])
        positive_tokens = self.__tokenizer.tokenize(sample.queries[1])
        negative_tokens = self.__tokenizer.tokenize(sample.queries[2])
        output = {
            "pivot": copy.deepcopy(pivot_tokens.padding_tokens),
            "positive": copy.deepcopy(positive_tokens.padding_tokens),
            "negative": copy.deepcopy(negative_tokens.padding_tokens)
        }
        return output

    def __getitem__(self, index):
        return self.data[index]["pivot"], self.data[index]["positive"], self.data[index]["negative"]

    def __len__(self):
        return len(self.data)

    @staticmethod
    def collate_fn(batch):
        """
        数据封装
        :param batch: 数据batch
        :return:
        """
        pivot, positive, negative = zip(*batch)
        return torch.LongTensor(pivot), torch.LongTensor(positive), torch.LongTensor(negative)