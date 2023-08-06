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
from typing import Dict, List
import torch

from ...base.abstract import AbstractDataSet, AbstractTagger, AbstractTokenizer
from ...base.model_data import DocSentImportanceSample
from ...base.utils import Utils


class DocSentImportanceDataSet(AbstractDataSet):
    """
    篇章句级别重要程度问题数据格式
    {"title": "", "content": [""], "labels": [{"sec_pos": 0, "sent_pos":1}, ]}
    """

    def __init__(self, tagger: AbstractTagger, tokenizer: AbstractTokenizer, max_sentence: int):
        super().__init__()
        self.__tagger = tagger
        self.__tokenizer = tokenizer
        self.__max_sentence = max_sentence

    def get_label_size(self):
        """
        获取label的数量
        :return:
        """
        return self.__tagger.get_size()

    def parse_sample(self, line: str) -> Dict:
        """
        解析json格式的sample数据
        :param line:
        :return:
        """
        output = {"data": [], "mask": [], "label": -1, "pos_mapping": []}
        sample = DocSentImportanceSample.parse_raw(line)
        if len(sample.labels) < 1:
            logging.warning("Error labels %s" % line)
            return {}

        data = []
        mask = []
        labels = []
        pos_mapping: List[Dict] = []
        dict_pos = {("%d_%d" % (elem.sec_pos, elem.sent_pos)): elem.label for elem in sample.labels}
        all_content = []

        if sample.title != "":
            all_content = [sample.title]
        all_content = all_content + sample.content

        for sec_pos, sec in enumerate(all_content):
            for sent_pos, sent in enumerate(Utils.split_sentence(section=sec)):
                tk_output = self.__tokenizer.tokenize(sent)
                data.append(copy.deepcopy(tk_output.padding_tokens))
                mask.append(copy.deepcopy(tk_output.mask))
                labels.append(self.__tagger.tag2id(dict_pos.get("%d_%d" % (sec_pos, sent_pos), "")))
                pos_mapping.append({"sec_pos": sec_pos, "sent_pos": sent_pos}.copy())

        padding_tokens_result = self.__tokenizer.tokenize("")
        data_size = len(data)
        if data_size <= self.__max_sentence:
            data = data + [padding_tokens_result.padding_tokens] * (self.__max_sentence - data_size)
            mask = mask + [padding_tokens_result.padding_tokens] * (self.__max_sentence - data_size)
            labels = labels + [0] * (self.__max_sentence - data_size)
        else:
            data = data[:self.__max_sentence]
            mask = mask[:self.__max_sentence]
            labels = labels[:self.__max_sentence]

        output["data"] = copy.deepcopy(data)
        output["mask"] = copy.deepcopy(mask)
        output["label"] = copy.deepcopy(labels)
        output["pos_mapping"] = copy.deepcopy(pos_mapping)

        return output

    def __getitem__(self, index):
        if self.data[index] is None:
            self.data[index] = self.parse_sample(self.raw_data[index]).copy()

        return self.data[index]["label"], self.data[index]["data"], self.data[index]["mask"]

    def __len__(self):
        return len(self.data)

    @staticmethod
    def collate_fn(batch):
        """
        数据封装
        :param batch: 数据batch
        :return:
        """
        label, data, mask = zip(*batch)
        return torch.LongTensor(list(label)), torch.LongTensor(data), torch.LongTensor(mask)