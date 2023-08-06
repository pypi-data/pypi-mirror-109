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

from ...base.abstract import AbstractDataSet, AbstractTagger, AbstractTokenizer
from ...base.model_data import SentClassifySample


class SentClassifyDataSet(AbstractDataSet):
    """
    文本分类问题数据格式
    {"queries": [""], "labels": [""]}
    """

    def __init__(self, labels: AbstractTagger, tokenizer: AbstractTokenizer):
        super().__init__()
        self.__labels = labels
        self.__tokenizer = tokenizer

    def get_label_size(self):
        """
        获取label的数量
        :return:
        """
        return self.__labels.get_size()

    def parse_sample(self, line: str) -> Dict:
        """
        解析json格式的sample数据
        :param line:
        :return:
        """
        output = {"data": [], "label": -1}
        sample = SentClassifySample.parse_raw(line)
        if len(sample.labels) < 1:
            logging.warning("Error labels %s" % line)
            return {}
        if len(sample.queries) < 1:
            logging.warning("Error queries %s" % line)
            return {}

        label_idx = self.__labels.tag2id(sample.labels[0])
        tokens = self.__tokenizer.tokenize(sample.queries[0])

        if sample.queries[0] == "" or len(tokens.padding_tokens) == 0:
            logging.warning("Error format of line %s" % line)
            return {}

        if label_idx < 0:
            logging.warning("Error format of line %s" % line)
            return {}

        output["data"] = copy.deepcopy(tokens.padding_tokens)
        output["label"] = label_idx
        return output

    def __getitem__(self, index):
        return self.data[index]["label"], self.data[index]["data"]

    def __len__(self):
        return len(self.data)

    @staticmethod
    def collate_fn(batch):
        """
        数据封装
        :param batch: 数据batch
        :return:
        """
        label, data = zip(*batch)
        return torch.LongTensor(list(label)), torch.LongTensor(data)