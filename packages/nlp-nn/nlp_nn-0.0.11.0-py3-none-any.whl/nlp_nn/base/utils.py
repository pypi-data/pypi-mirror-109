# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2020 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
Utils

Authors: fubo
Date: 2020/03/11 00:00:00
"""
import os
import requests
import hashlib
import tarfile
import torch

from typing import List
from pydantic import BaseModel
from argparse import ArgumentParser, Namespace

from ..base.common import BerType


class Utils(object):
    """ 常用工具 """

    @staticmethod
    def data_sign_sha512(data):
        """
        data 签名
        :param data:
        :return:
        """
        sha512 = hashlib.sha512()
        sha512.update(data.encode("utf-8"))
        return sha512.hexdigest()

    @staticmethod
    def data_sign_md5(data):
        """
        data 签名
        :param data:
        :return:
        """
        md5 = hashlib.md5()
        md5.update(data.encode("utf-8"))
        return md5.hexdigest()

    @staticmethod
    def reciprocal_log_nature_sum(num: int, values: torch.LongTensor) -> float:
        """
        自然数迭代的log倒数和
        num: 序列数量 batch * num
        """
        return float(torch.sum(values / torch.log2(torch.linspace(1, num, steps=num) + 2), dim=0))

    @staticmethod
    def download_model(bert_type: BerType = BerType.LITE_BERT_TINY) -> str:
        """
        下载部署model
        :param bert_type:
        :return:
        """
        base_url = "https://transformer-models.fwh.bcebos.com"
        base_model_path = os.path.expanduser("~/.nlp_nn_cache")

        model_name = ""
        if bert_type == BerType.LITE_BERT_SMALL:
            model_name = "voidful_albert_chinese_small"

        if bert_type == BerType.LITE_BERT_TINY:
            model_name = "voidful_albert_chinese_tiny"

        if bert_type == BerType.LITE_BERT_LARGE:
            model_name = "voidful_albert_chinese_large"

        if bert_type == BerType.LITE_BERT_XLARGE:
            model_name = "voidful_albert_chinese_xlarge"

        if bert_type == BerType.LITE_BERT_XXLARGE:
            model_name = "voidful_albert_chinese_xxlarge"

        if bert_type == BerType.BASE_BERT:
            model_name = "bert-base-chinese"

        if bert_type == BerType.LITE_BERT_BASE_EN:
            model_name = "albert-base-v2"

        if model_name == "":
            return ""

        if not os.path.exists(base_model_path):
            os.mkdir(base_model_path)

        gz_model_name = model_name + ".tar.gz"
        if os.path.exists(base_model_path + os.sep + model_name):
            return base_model_path + os.sep + model_name

        if os.path.exists(base_model_path + os.sep + gz_model_name):
            os.system("rm -rf " + base_model_path + os.sep + gz_model_name)

        try:
            r = requests.get(url=base_url + "/" + gz_model_name)
            with open(base_model_path + os.sep + gz_model_name, "wb") as fp:
                fp.write(r.content)

            with tarfile.open(base_model_path + os.sep + gz_model_name) as tar:
                for name in tar.getnames():
                    tar.extract(name, path=base_model_path)
            os.system("rm -rf " + base_model_path + os.sep + gz_model_name)
        except Exception as exp:
            raise exp
        return base_model_path + os.sep + model_name

    @staticmethod
    def split_sentence(section: str) -> List[str]:
        """
        分句
        :param section:
        :return:
        """
        section = section.strip("\r\n\t").strip(" ")
        for sign in ["。", "！", "？", "?", ";", "；"]:
            section = section.replace(sign, sign + "\n")
        return section.strip("\n").split("\n")

    @staticmethod
    def tokens_to_sentence(tokens: List[str], is_ch: bool = True) -> str:
        """
        token转sentence
        :param tokens:
        :param is_ch:
        :return:
        """
        if is_ch is True:
            terms = []
            for token in tokens:
                if "##" in token and token.index("##") == 0:
                    terms[-1] = terms[-1] + token.strip("#")
                else:
                    terms.append(token)
            return " ".join(terms)
        terms = []
        for token in tokens:
            if "▁" in token and token.index("▁") == 0:
                terms.append(token.strip("▁"))
            else:
                terms[-1] = terms[-1] + token.strip("▁")
        return " ".join(terms)

    @staticmethod
    def create_cmd_params(params: List[BaseModel]) -> Namespace:
        """
        参数结构体转参数命令行
        :param params:
        :return:
        """
        parser = ArgumentParser()
        if len(params) == 0:
            return parser.parse_args()

        for settings in params:
            for name in settings.__dict__:
                if "_" in name and name.index("_") == 0:
                    continue
                parser.add_argument(
                    "--" + name,
                    type=type(settings.__dict__[name]),
                    help="%s [default: %s]" % (" ".join(name.split("_")),settings.__dict__[name]),
                    default=settings.__dict__[name],
                    required=False
                )
        return parser.parse_args()

    @staticmethod
    def viterbi_decode(
            num_tags: int,
            start_transitions: torch.FloatTensor, transitions: torch.FloatTensor, end_transitions: torch.FloatTensor,
            emissions: torch.FloatTensor, mask: torch.ByteTensor = None
    ) -> List[List[int]]:
        """

        :param num_tags: 标签类别数量
        :param start_transitions: 
        :param transitions:
        :param end_transitions:
        :param emissions:
        :param mask:
        :return:
        """
        # emissions: (seq_length, batch_size, num_tags)
        # mask: (seq_length, batch_size)
        if mask is None:
            mask = emissions.new_ones(emissions.shape[:2], dtype=torch.uint8)
        emissions = emissions.transpose(0, 1)
        mask = mask.transpose(0, 1)

        assert emissions.dim() == 3 and mask.dim() == 2
        assert emissions.shape[:2] == mask.shape
        assert emissions.size(2) == num_tags
        assert mask[0].all()

        seq_length, batch_size = mask.shape

        # Start transition and first emission
        # shape: (batch_size, num_tags)
        score = start_transitions + emissions[0]
        history = []

        # score is a tensor of size (batch_size, num_tags) where for every batch,
        # value at column j stores the score of the best tag sequence so far that ends
        # with tag j
        # history saves where the best tags candidate transitioned from; this is used
        # when we trace back the best tag sequence

        # Viterbi algorithm recursive case: we compute the score of the best tag sequence
        # for every possible next tag
        for i in range(1, seq_length):
            # Broadcast viterbi score for every possible next tag
            # shape: (batch_size, num_tags, 1)
            broadcast_score = score.unsqueeze(2)

            # Broadcast emission score for every possible current tag
            # shape: (batch_size, 1, num_tags)
            broadcast_emission = emissions[i].unsqueeze(1)

            # Compute the score tensor of size (batch_size, num_tags, num_tags) where
            # for each sample, entry at row i and column j stores the score of the best
            # tag sequence so far that ends with transitioning from tag i to tag j and emitting
            # shape: (batch_size, num_tags, num_tags)
            next_score = broadcast_score + transitions + broadcast_emission

            # Find the maximum score over all possible current tag
            # shape: (batch_size, num_tags)
            next_score, indices = next_score.max(dim=1)

            # Set score to the next score if this timestep is valid (mask == 1)
            # and save the index that produces the next score
            # shape: (batch_size, num_tags)
            score = torch.where(mask[i].unsqueeze(1), next_score, score)
            history.append(indices)

        # End transition score
        # shape: (batch_size, num_tags)
        score += end_transitions

        # Now, compute the best path for each sample

        # shape: (batch_size,)
        seq_ends = mask.long().sum(dim=0) - 1
        best_tags_list = []

        for idx in range(batch_size):
            # Find the tag which maximizes the score at the last timestep; this is our best tag
            # for the last timestep
            _, best_last_tag = score[idx].max(dim=0)
            best_tags = [best_last_tag.item()]

            # We trace back where the best last tag comes from, append that to our best tag
            # sequence, and trace it back again, and so on
            for hist in reversed(history[:seq_ends[idx]]):
                best_last_tag = hist[idx][best_tags[-1]]
                best_tags.append(best_last_tag.item())

            # Reverse the order because we start from the last timestep
            best_tags.reverse()
            best_tags_list.append(best_tags)

        return best_tags_list
