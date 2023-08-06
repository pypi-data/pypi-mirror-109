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
import copy
from typing import Dict
import torch

from ...base.abstract import AbstractDataSet, AbstractTagger, AbstractTokenizer
from ...base.model_data import SentClassifySample


class SentMultiClassifyDataSet(AbstractDataSet):
    """
    Tagging 数据格式
    {"query": "", "intent_label": "", "entity_labels": [{"label": "", "pos":1, "len": 3}, ...]}
    """

    def __init__(
            self,
            tag_label: AbstractTagger,
            tokenizer: AbstractTokenizer
    ):
        super().__init__()
        self.__tag_label = tag_label
        self.__tokenizer = tokenizer

    def get_tag_label_size(self):
        """
        获取entity label的数量
        :return:
        """
        return self.__tag_label.get_size()

    def parse_sample(self, line: str) -> Dict:
        """
        解析json格式的sample数据
        {"queries": ["query"], "labels": ["label1", "label2", ...]}
        :param line:
        :return:
        """
        output = {
            "data": [],
            "tag_label": [self.__tag_label.tag2id(self.__tag_label.padding_tag)] * self.__tag_label.get_size()
        }

        sample = SentClassifySample.parse_raw(line)
        output["data"] = copy.deepcopy(self.__tokenizer.tokenize(sample.queries[0]).padding_tokens)
        for index, tag in enumerate(sample.labels):
            tag_idx = self.__tag_label.tag2id(tag)
            output["tag_label"][tag_idx] = 1

        return output

    def __getitem__(self, index):
        return self.data[index]["data"], self.data[index]["tag_label"]

    def __len__(self):
        return len(self.data)

    @staticmethod
    def collate_fn(batch):
        """
        数据封装
        :param batch: 数据batch
        :return:
        """
        data, tag_label = zip(*batch)
        return torch.LongTensor(data), torch.LongTensor(tag_label)