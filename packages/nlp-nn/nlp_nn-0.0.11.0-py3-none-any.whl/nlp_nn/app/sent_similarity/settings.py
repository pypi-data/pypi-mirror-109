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


class SentSimilarityModelSettings(ModelSettings):
    """ 模型配置 """

    # sentence向量维度
    sent_encode_dim: int = 0

    # Dropout prob
    drop_out_prob: float = 0.5

    # 最大tokens长度
    max_tokens: int = 0


class SentSimilarityCoachSettings(CoachSettings):
    """ 训练参数配置 """
    pass


class SentSimilarityExportedModelSettings(ExportModelSettings):
    """ Query相似模型导出模型配置 """

    # 最大tokens长度
    max_tokens: int = 0