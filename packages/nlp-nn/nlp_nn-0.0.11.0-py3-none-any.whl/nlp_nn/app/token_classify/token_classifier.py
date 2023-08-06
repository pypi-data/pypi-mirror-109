# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2020 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
序列标注模型

Authors: fubo01
Date: 2020/03/11 00:00:00
"""

import json
import os
import logging
from typing import List

import torch
import torch.jit
from torch.utils.data import Dataset

from ...base.abstract import AbstractModelApp, AbstractModel
from ...base.layer import BertEmbeddingLayer, LinearLayer, CRFLayer
from ...base.common import BerType, ModelState, TokensSplitType
from ...base.common import DeviceSettings
from ...base.model_dict import TagsDict, AbstractTagger
from ...base.tokenizer import BertTokenizer, AbstractTokenizer

from ...app.token_classify.data_set import TokenClassifyDataSet
from ...app.token_classify.settings import TokenClassifyModelSettings, TokenClassifyCoachSettings
from ...app.token_classify.settings import TokenClassifyExportedModelSettings


class TokenClassifyModel(AbstractModel):

    def __init__(
            self,
            token_class_count: int,
            bert_type=BerType.LITE_BERT_TINY,
            dropout_prob: float = 0.3,
            max_tokens: int = 20
    ):
        """
        :param dropout_prob: dropout概率
        :param max_tokens: 最大token长度
        """
        super().__init__()
        self.max_tokens = max_tokens
        # bert embedding layer
        self.bert_embedding_layer = BertEmbeddingLayer(bert_type=bert_type)

        # drop out layer
        self.drop_out_layer = torch.nn.Dropout(p=dropout_prob)

        # entity classifier
        self.token_linear_layer = LinearLayer(
            n_input_dim=self.bert_embedding_layer.hidden_size,
            n_output_dim=token_class_count
        )

        # # CRF Layer
        # self.crf_layer = CRFLayer(num_tags=token_class_count)

    def get_dummy_input(self):
        """
        获取dummy数据
        :return:
        """
        x = torch.LongTensor([[0] * self.max_tokens])
        return x

    # def loss_function(self, x: torch.Tensor, tags: torch.LongTensor) -> torch.FloatTensor:
    #     """
    #     计算loss
    #     :param x:
    #     :param tags:
    #     :return:
    #     """
    #     return self.crf_layer(self.forward(x), tags)

    def forward(self, x):
        """
        forward 计算
        :param x:
        :return:
        """
        res = self.bert_embedding_layer(x)
        x_token, _ = res[0], res[1]
        x_token = self.token_linear_layer(self.drop_out_layer(x_token))
        x_token = torch.log_softmax(x_token, dim=2)
        return x_token


class TokenClassify(AbstractModelApp):
    """ 序列标注 """

    def __init__(
            self, device_settings: DeviceSettings,
            coach_settings: TokenClassifyCoachSettings = TokenClassifyCoachSettings(),
            model_settings: TokenClassifyModelSettings = TokenClassifyModelSettings(),
            export_settings: TokenClassifyExportedModelSettings = TokenClassifyExportedModelSettings()
    ):
        super().__init__(device_settings, coach_settings, model_settings, export_settings)
        self.device_settings = device_settings
        self.model_settings = model_settings
        self.coach_settings = coach_settings
        self.export_settings = export_settings
        self.token_labeler = AbstractTagger()
        self.token_inner_labeler = AbstractTagger()
        self.tokenizer = AbstractTokenizer()

    def load_third_dict(self) -> bool:

        # 加载外部序列标注类别词典
        self.token_labeler = TagsDict(
            tags_file=self.coach_settings.dict_dir + "/" + self.coach_settings.token_class_label_dic
        )

        # 加载内部序列标注类别词典
        self.token_inner_labeler = TagsDict(
            tags_file=self.coach_settings.dict_dir + "/" + self.coach_settings.token_class_label_inner_dic
        )
        self.model_settings.token_class_count = self.token_inner_labeler.get_size()

        # 加载分词
        self.tokenizer = BertTokenizer(
            max_sent_len=self.model_settings.max_tokens,
            split_type=TokensSplitType(value=self.model_settings.split_type_id),
            bert_type=BerType(value=self.model_settings.bert_type_id)
        )
        return True

    def define_data_pipe(self) -> Dataset:
        """ 创建数据集计算pipe """
        return TokenClassifyDataSet(
            token_label=self.token_labeler,
            token_inner_label=self.token_inner_labeler,
            tokenizer=self.tokenizer
        )

    def define_model(self) -> bool:
        """
        定义模型
        :return: bool
        """
        self.model = TokenClassifyModel(
            token_class_count=self.model_settings.token_class_count,
            bert_type=BerType(value=self.model_settings.bert_type_id),
            dropout_prob=self.model_settings.drop_out_prob,
            max_tokens=self.model_settings.max_tokens
        )
        return True

    def load_model_ckpt(self, model_path_ckpt) -> bool:
        """
        加载ckpt模型
        :param model_path_ckpt:
        :return:
        """
        # 模型配置文件
        config_file = model_path_ckpt + "/" + self.coach_settings.model_conf_file
        with open(config_file, "r") as fp:
            config_data = json.load(fp)
        self.coach_settings = TokenClassifyCoachSettings.parse_obj(config_data["coach_settings"])
        self.model_settings = TokenClassifyModelSettings.parse_obj(config_data["model_settings"])

        # 加载模型文件
        model_file = model_path_ckpt + "/" + self.coach_settings.model_file
        if self.define_model() is False:
            logging.error("Failed to define token_similarity_model")
            return False
        try:
            self.model.load_state_dict(torch.load(model_file, map_location=torch.device("cpu")))
        except Exception as exp:
            logging.error("load token_similarity_model params failed %s" % exp)
            return False

        return True

    def create_loss_optimizer(self) -> bool:
        """
        创建loss function和optimizer
        :return: bool
        """
        self.loss_func = torch.nn.NLLLoss(
            weight=self.set_tensor_gpu(
                torch.FloatTensor(
                    [self.coach_settings.o_label_loss_weight] + [1] * (self.model_settings.token_class_count - 1)
                )
            )
        )
        self.optimizer = torch.optim.Adam(
            self.get_model_params(),
            lr=self.coach_settings.lr, weight_decay=self.coach_settings.lr_weight_decay
        )
        return True

    def stop_criteria(self) -> (bool, int):
        """
        停止训练条件，如果不重载，则默认训练最长次数
        :return: bool, int
        """
        return False, -1

    def show_network_tf(self) -> bool:
        """
        在tensor board上画出network
        不实现函数则不画出网络图
        :return: bool
        """
        self.set_model_state(ModelState.INFERENCE)
        dummy_input = self.set_tensor_gpu(self.model.get_dummy_input())
        self.tb_logger.add_graph(self.model, dummy_input)
        self.set_model_state(ModelState.TRAIN)
        return True

    def batch_forward(self, params: List[torch.Tensor]):
        """
        一个batch forward计算
        :return:
        """
        x, y = params[0], params[1]
        y_ = self.model(x)
        y_ = torch.transpose(y_, dim0=2, dim1=1)
        return self.loss_func(y_, y)

    def release_model(self, model_path_ckpt: str, model_path_script: str) -> bool:
        """
        发布模型（TorchScript模型）
        :param model_path_ckpt ckpt的模型文件夹
        :param model_path_script torch script模型文件夹
        :return:
        """
        os.system("rm -rf %s" % model_path_script)
        os.system("mkdir -p %s" % model_path_script)

        # 生成模型配置清单
        export_model_settings = TokenClassifyExportedModelSettings(
            model_config_file="config.json",
            model_file="model.pt",
            third_dict_dir="dict",
            token_label_inner_dic=self.coach_settings.token_class_label_inner_dic,
            token_label_dic=self.coach_settings.token_class_label_dic,
            max_tokens=self.model_settings.max_tokens,
            split_type_id=self.model_settings.split_type_id,
            bert_type_id=self.model_settings.bert_type_id
        )
        dict_path = model_path_script + "/" + export_model_settings.third_dict_dir
        model_file = model_path_script + "/" + export_model_settings.model_file
        config_file = model_path_script + "/" + export_model_settings.model_config_file
        try:
            with open(config_file, "w") as fp:
                fp.write(export_model_settings.json())
        except Exception as ex:
            logging.error("Failed to save token_classify_model.config %s" % ex)
            return False

        # 打包第三方词典
        os.system("mkdir %s" % dict_path)
        os.system(
            "cp -rf %s %s/" % (
                self.coach_settings.dict_dir + "/" + self.coach_settings.token_class_label_dic, dict_path
            )
        )
        os.system(
            "cp -rf %s %s/" % (
                self.coach_settings.dict_dir + "/" + self.coach_settings.token_class_label_inner_dic, dict_path
            )
        )

        # 生成torch script模型文件
        try:
            self.model.eval()
            dummy_input = self.model.get_dummy_input()
            torch.jit.trace(self.model, dummy_input).save(model_file)
        except Exception as ex:
            logging.error("Failed to export token_classify_model %s" % ex)
            return False
