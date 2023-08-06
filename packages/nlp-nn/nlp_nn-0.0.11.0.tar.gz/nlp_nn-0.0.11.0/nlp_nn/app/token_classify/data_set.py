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
from ...base.model_data import TokenLabel, TokenClassifySample, Tokens


class TokenClassifyDataSet(AbstractDataSet):
    """
    序列标注模型 数据格式
    {"query": "", "token_labels": [{"label": "", "pos":1, "length": 3}, ...]}
    """

    def __init__(
            self,
            token_label: AbstractTagger,
            token_inner_label: AbstractTagger,
            tokenizer: AbstractTokenizer
    ):
        super().__init__()
        self.__token_label = token_label
        self.__token_inner_label = token_inner_label
        self.__tokenizer = tokenizer

    def get_token_label_size(self):
        """
        获取序列标注模型 label的数量
        :return:
        """
        return self.__token_label.get_size()

    def get_token_inner_label_size(self):
        """
        获取序列标注模型 inner label的数量
        :return:
        """
        return self.__token_inner_label.get_size()

    def token_label_to_inner_token_label(self, tokens: Tokens, token_label: TokenLabel) -> (int, List[str]):
        """
        样本的token label转换为内部训练的token label
        :param token_length: token长度
        :param token_label: token的外部标签
        :return: pos, labels
        """
        entity_pos = token_label.pos
        entity_label = token_label.label
        entity_poses = [entity_pos + entity_offset for entity_offset in range(token_label.length)]
        pos = tokens.pos_mapping.index(entity_pos) if entity_pos in tokens.pos_mapping else -1
        if pos == -1:
            return -1, []

        labels = []
        for i, _ in enumerate(tokens.pos_mapping):
            if tokens.pos_mapping[i] in entity_poses:
                labels.append(entity_label)

        if len(labels) == 1:
            return pos, ["S-" + labels[0]]

        if len(labels) > 1:
            tokens_label_head = ["B-" + labels[0]]
            tokens_label_tail = ["E-" + labels[-1]]
            tokens_label_body = ["I-" + entity_label] * (len(labels) - 2)
            return pos, tokens_label_head + tokens_label_body + tokens_label_tail

        return pos, []

    def token_label_inner_to_token_label(self, tokens: Tokens, inner_labels: List[str]) -> List[TokenLabel]:
        """
        样本的内部训练的token label转换为token label
        :param tokens: token序列
        :param inner_labels: token的内部标签序列
        :return:
        """
        output: List[TokenLabel] = []
        labels = []
        term_idx = []
        tmp_labels = []
        tmp_term_idx = []
        for index, inner_label in enumerate(inner_labels):
            elem = inner_label.split("-")
            if len(elem) == 1:
                label = elem[0]
            else:
                label = elem[1]

            if label == "O":
                if len(tmp_labels) > 0:
                    labels.append(copy.deepcopy(tmp_labels))
                    term_idx.append(copy.deepcopy(tmp_term_idx))

                tmp_labels = []
                tmp_term_idx = []
                continue

            tmp_labels.append(inner_label)
            tmp_term_idx.append(index)

        if len(tmp_labels) > 0:
            labels.append(copy.deepcopy(tmp_labels))
            term_idx.append(copy.deepcopy(tmp_term_idx))

        for index, (tmp_labels, tmp_term_idx) in enumerate(zip(labels, term_idx)):
            label = tmp_labels[0].split("-")[1]
            length_tmp = len(tmp_labels)
            if length_tmp == 1:
                tmp_labels_template = ["S-" + label]
            else:
                tmp_labels_template = ["B-" + label] + ["I-" + label] * (length_tmp - 2) + ["E-" + label]

            # 标签序列是否匹配
            if tmp_labels_template != tmp_labels:
                continue
            entity_idx = list(set([tokens.pos_mapping[idx] for idx in tmp_term_idx]))
            entity_idx = sorted(entity_idx)
            text = [tokens.simple_terms[idx] for idx in entity_idx]
            output.append(TokenLabel(label=label, pos=min(entity_idx), length=len(entity_idx), text=" ".join(text)))

        return output

    def parse_sample(self, line: str) -> Dict:
        """
        解析json格式的sample数据
        :param line:
        :return:
        """
        output = {"data": [], "token_label": []}
        sample = TokenClassifySample.parse_raw(line)

        tokens = self.__tokenizer.tokenize(sample.query)
        output["data"] = copy.deepcopy(tokens.padding_tokens)
        output["token_label"] = ["O"] * self.__tokenizer.max_length

        for token_label in sample.token_labels:
            pos, labels = self.token_label_to_inner_token_label(tokens=tokens, token_label=token_label)
            if pos == -1:
                continue
            output["token_label"][pos: pos + len(labels)] = labels

        output["token_label"] = list(map(self.__token_inner_label.tag2id, output["token_label"]))

        return output

    def __getitem__(self, index):
        return self.data[index]["data"], self.data[index]["token_label"]

    def __len__(self):
        return len(self.data)

    @staticmethod
    def collate_fn(batch):
        """
        数据封装
        :param batch: 数据batch
        :return:
        """
        data, token_label = zip(*batch)
        return torch.LongTensor(data), torch.LongTensor(list(token_label))

