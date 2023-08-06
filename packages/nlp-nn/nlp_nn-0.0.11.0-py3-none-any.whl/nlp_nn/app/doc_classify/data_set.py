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
from ...base.model_data import DocClassifySample
from ...base.utils import Utils


class DocClassifyDataSet(AbstractDataSet):
    """
    篇章文本分类问题数据格式
    {"title": "", "content": [""], "labels": [""]}
    """

    def __init__(self, labels: AbstractTagger, tokenizer: AbstractTokenizer, max_sentence: int):
        super().__init__()
        self.__labels = labels
        self.__tokenizer = tokenizer
        self.__max_sentence = max_sentence

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
        output = {"data": [], "mask": [], "label": -1}
        sample = DocClassifySample.parse_raw(line)
        if len(sample.labels) < 1:
            logging.warning("Error labels %s" % line)
            return {}

        label_idx = self.__labels.tag2id(sample.labels[0])
        if label_idx < 0:
            logging.warning("Error format of line %s" % line)
            return {}

        data = []
        mask = []
        all_content = []

        if sample.title != "":
            all_content.append(sample.title)
        all_content = all_content + sample.content

        for sec in all_content:
            for sent in Utils.split_sentence(section=sec):
                if len(sent) == 0:
                    continue
                tk_output = self.__tokenizer.tokenize(sent)
                data.append(copy.deepcopy(tk_output.padding_tokens))
                mask.append(copy.deepcopy(tk_output.mask))

            # 添加段落分隔符
            sec_tokens = self.__tokenizer.tokenize("")
            sec_tokens.padding_tokens[0] = self.__tokenizer.section_segment_idx
            sec_tokens.mask[0] = 1
            data.append(copy.deepcopy(sec_tokens.padding_tokens))
            mask.append(copy.deepcopy(sec_tokens.mask))

        padding_tokens_result = self.__tokenizer.tokenize("")
        data_size = len(data)
        if data_size <= self.__max_sentence:
            data = data + [padding_tokens_result.padding_tokens] * (self.__max_sentence - data_size)
            mask = mask + [padding_tokens_result.padding_tokens] * (self.__max_sentence - data_size)
        else:
            data = data[:self.__max_sentence]
            mask = mask[:self.__max_sentence]

        output["data"] = copy.deepcopy(data)
        output["mask"] = copy.deepcopy(mask)
        output["label"] = label_idx

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