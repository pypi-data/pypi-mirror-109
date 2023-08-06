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


class TokenClassifyModelSettings(ModelSettings):
    """ 序列标注模型配置 """

    # token 类别数量
    token_class_count: int = 0

    # Dropout prob
    drop_out_prob: float = 0.5

    # 最大tokens长度
    max_tokens: int = 0


class TokenClassifyCoachSettings(CoachSettings):
    """ 序列标注模型训练参数配置 """

    # 内部部序列标注模型词典文件
    token_class_label_inner_dic: str = ""

    # 外部序列标注模型词典文件
    token_class_label_dic: str = ""

    # O标签loss权重
    o_label_loss_weight: float = 0.05


class TokenClassifyExportedModelSettings(ExportModelSettings):
    """ 序列标注模型导出模型配置 """

    # 内部部序列标注模型词典文件
    token_label_inner_dic: str = ""

    # 外部序列标注模型词典文件
    token_label_dic: str = ""

    # 最大tokens长度
    max_tokens: int = 0