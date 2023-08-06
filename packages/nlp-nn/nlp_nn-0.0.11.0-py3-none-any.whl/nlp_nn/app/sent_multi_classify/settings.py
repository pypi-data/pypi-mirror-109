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


class SentMultiClassifyModelSettings(ModelSettings):
    """ Tagging模型配置 """

    # tag 类别数量
    tags_count: int = 0

    # Dropout prob
    drop_out_prob: float = 0.5

    # 最大tokens长度
    max_tokens: int = 0


class SentMultiClassifyCoachSettings(CoachSettings):
    """ Tagging训练参数配置 """

    # tag词典文件
    tag_label_dic: str = ""


class SentMultiClassifyExportedModelSettings(ExportModelSettings):
    """ Tagging模型导出模型配置 """

    # tag词典文件
    tag_label_dic: str = ""

    # 最大tokens长度
    max_tokens: int = 0
