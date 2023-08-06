# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
query序列化

Authors: fubo
Date: 2019/11/28 00:00:00
"""
import copy
from typing import List

import transformers
from .abstract import AbstractTokenizer
from .common import BerType, TokensSplitType
from .utils import Utils
from .model_data import Tokens


class BertTokenizer(AbstractTokenizer):
    """
    Bert token化
    """

    def __init__(self, max_sent_len: int, split_type: TokensSplitType, bert_type=BerType.LITE_BERT_TINY):
        """
        bert分词
        :param max_sent_len:
        :param bert_type:
        :param split_type: 分词方式
        """
        super().__init__(max_sent_len)
        self.__split_type = split_type
        self.__is_auto_tokenizer = False

        self.__tokenizer = None

        if bert_type in [BerType.LITE_BERT_BASE_EN, BerType.BASE_BERT]:
            self.__tokenizer = transformers.AutoTokenizer.from_pretrained(
                Utils.download_model(bert_type=bert_type)
            )
            self.__is_auto_tokenizer = True
        else:
            self.__tokenizer = transformers.BertTokenizer.from_pretrained(
                Utils.download_model(bert_type=bert_type)
            )
            self.__is_auto_tokenizer = False
        self.padding_idx = self.__tokenizer.pad_token_id
        self.padding = self.__tokenizer.pad_token
        self.section_segment_idx = self.__tokenizer.sep_token_id
        self.section_segment = self.__tokenizer.sep_token

    def convert_ids_to_tokens(self, ids: List[int]) -> List[str]:
        """
        id转化token
        """
        return self.__tokenizer.convert_ids_to_tokens(ids=ids)

    def __term_level_split(self, tokens: Tokens) -> Tokens:
        """
        词语粒度分割, 粒度过粗的需要使用bert进行再次切分
        :param tokens:
        :return:
        """
        terms = [term for term in tokens.query.strip(" ").split(" ")]
        tokens.simple_terms = copy.deepcopy(terms)
        pos = 0
        for index, term in enumerate(terms):
            if self.__is_auto_tokenizer is True:
                bert_terms = self.__tokenizer.tokenize(term, add_special_tokens=False)
            else:
                bert_terms = self.__tokenizer.tokenize(term)
            term_tokens = self.__tokenizer.convert_tokens_to_ids(bert_terms)
            tokens.tokens = tokens.tokens + copy.deepcopy(term_tokens)
            tokens.bert_terms = tokens.bert_terms + copy.deepcopy(bert_terms)
            for i in range(len(term_tokens)):
                pos = pos + 1
                tokens.pos_mapping.append(index)
        return tokens

    def __natural_split(self, tokens: Tokens) -> Tokens:
        """
        直接使用bert分割
        :param tokens:
        :return:
        """
        if self.__is_auto_tokenizer is True:
            bert_terms = self.__tokenizer.tokenize(tokens.query, add_special_tokens=False)
        else:
            bert_terms = self.__tokenizer.tokenize(tokens.query)
        tokens.simple_terms = copy.deepcopy(bert_terms)
        tokens.bert_terms = copy.deepcopy(bert_terms)
        tokens.tokens = copy.deepcopy(self.__tokenizer.convert_tokens_to_ids(bert_terms))
        tokens.pos_mapping = [index for index, _ in enumerate(tokens.tokens)]
        return tokens

    def __char_split(self, tokens: Tokens) -> Tokens:
        """
        直接char粒度分割
        :param tokens:
        :return:
        """
        terms = list(tokens.query)
        tokens.simple_terms = copy.deepcopy(terms)
        tokens.bert_terms = copy.deepcopy(terms)
        tokens.tokens = copy.deepcopy(self.__tokenizer.convert_tokens_to_ids(terms))
        tokens.pos_mapping = [index for index, _ in enumerate(tokens.tokens)]
        return tokens

    def tokenize(self, query: str) -> Tokens:
        """
        query序列化
        :param query:
        :return:
        """
        output_tokens = Tokens(query=query, tokens=[], padding_tokens=[], mask=[1] * self.max_length)
        if self.__tokenizer is None:
            return output_tokens

        if self.__split_type == TokensSplitType.CHAR_TYPE:
            output_tokens = self.__char_split(tokens=output_tokens)

        if self.__split_type == TokensSplitType.BERT_TYPE:
            output_tokens = self.__natural_split(tokens=output_tokens)

        if self.__split_type == TokensSplitType.MIX_TYPE:
            output_tokens = self.__term_level_split(tokens=output_tokens)

        if self.max_length == 0:
            return output_tokens

        if len(output_tokens.tokens) < self.max_length:
            token_size_gap = self.max_length - len(output_tokens.tokens)
            output_tokens.padding_tokens = output_tokens.tokens + [self.padding_idx] * token_size_gap
            output_tokens.mask[len(output_tokens.tokens):] = [0] * token_size_gap
            output_tokens.pos_mapping = output_tokens.pos_mapping + [-1] * token_size_gap
        else:
            output_tokens.padding_tokens = copy.deepcopy(output_tokens.tokens[:self.max_length])
            output_tokens.pos_mapping = copy.deepcopy(output_tokens.pos_mapping[:self.max_length])
        return output_tokens
