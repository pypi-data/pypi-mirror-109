# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2020 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
配置文件

Authors: fubo01
Date: 2020/03/11 00:00:00
"""
from ...base.common import CoachSettings, ModelSettings, ExportModelSettings


class DocClassifyModelSettings(ModelSettings):
    """ 篇章文本分类模型配置 """

    # sentence向量维度
    sent_encode_dim: int = 0

    # doc向量维度
    doc_encode_dim: int = 0

    # transformer 头的数量
    transformer_head_count: int = 1

    # 类别数量
    class_count: int = 0

    # Dropout prob
    drop_out_prob: float = 0.5

    # 最大tokens长度
    max_tokens: int = 50

    # 最大句子数量
    max_sentences: int = 15


class DocClassifyCoachSettings(CoachSettings):
    """ 篇章文本分类训练参数配置 """

    # 分类类别词典
    class_label: str = ""


class DocClassifyExportedModelSettings(ExportModelSettings):
    """ 篇章文本分类模型导出模型配置 """

    # 分类类别词典
    class_label: str = ""

    # 最大tokens长度
    max_tokens: int = 0

    # 最大句子数量
    max_sentences: int = 10