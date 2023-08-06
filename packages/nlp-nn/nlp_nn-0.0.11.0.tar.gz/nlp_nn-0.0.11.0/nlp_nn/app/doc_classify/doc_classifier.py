# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2020 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
篇章文本分类模型

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
from ...base.layer import BertDocEncodeLayer, LinearLayer
from ...base.common import BerType, ModelState, DeviceSettings, TokensSplitType
from ...base.model_dict import TagsDict, AbstractTagger
from ...base.tokenizer import BertTokenizer, AbstractTokenizer

from ...app.doc_classify.data_set import DocClassifyDataSet
from ...app.doc_classify.settings import DocClassifyCoachSettings, DocClassifyModelSettings
from ...app.doc_classify.settings import DocClassifyExportedModelSettings


class DocClassifyModel(AbstractModel):
    def __init__(
            self,
            sent_encode_dim: int, doc_encode_dim: int, transformer_head_count: int,
            class_count: int, dropout_prob: float,
            max_tokens: int = 20, max_sentences: int = 10,
            bert_type: BerType = BerType.LITE_BERT_TINY
    ):
        """
        HAN Model from "Hierarchical Attention Networks for Document Classification"
        :param sent_encode_dim: 句向量维度
        :param class_count: 类别数量
        :param dropout_prob: dropout概率
        :param max_tokens: 最大token长度
        :param max_sentences: 每个段落最大sentence数量
        """
        super().__init__()
        self.max_sentences, self.max_tokens = max_sentences, max_tokens

        # doc level layer
        self.doc_encode_layer = BertDocEncodeLayer(
            sent_encode_dim=sent_encode_dim, doc_encode_dim=doc_encode_dim,
            transformer_head_count=transformer_head_count,
            max_tokens=max_tokens, max_sentences=max_sentences, bert_type=bert_type
        )

        # drop out layer
        self.drop_out_layer = torch.nn.Dropout(p=dropout_prob)

        # classify layer
        self.classify_layer = LinearLayer(n_input_dim=doc_encode_dim, n_output_dim=class_count, with_bias=False)

    def get_dummy_input(self):
        """
        获取dummy数据
        :return:
        """
        return torch.randint(0, 1, [1, self.max_sentences, self.max_tokens])

    def forward(self, x: torch.LongTensor, mask: torch.LongTensor = None):
        """
        forward 计算
        :param x: (batch_size, segment_size, sentence_size, token_size)
        :param mask:
        :return:
        """
        x = self.doc_encode_layer(x, mask=mask)
        x = self.drop_out_layer(x)
        x = self.classify_layer(x)
        x = torch.log_softmax(x, dim=1)
        return x


class DocClassify(AbstractModelApp):
    """ 篇章文本分类 """

    def __init__(
            self, device_settings: DeviceSettings,
            coach_settings: DocClassifyCoachSettings = DocClassifyCoachSettings(),
            model_settings: DocClassifyModelSettings = DocClassifyModelSettings(),
            export_settings: DocClassifyExportedModelSettings = DocClassifyExportedModelSettings()
    ):
        super().__init__(device_settings, coach_settings, model_settings, export_settings)
        self.device_settings = device_settings
        self.model_settings = model_settings
        self.coach_settings = coach_settings
        self.export_settings = export_settings
        self.labeler = AbstractTagger()
        self.tokenizer = AbstractTokenizer()

    def load_third_dict(self) -> bool:
        # 加载类别词典
        self.labeler = TagsDict(tags_file=self.coach_settings.dict_dir + "/" + self.coach_settings.class_label)
        self.model_settings.class_count = self.labeler.get_size()

        # 加载分词
        self.tokenizer = BertTokenizer(
            max_sent_len=self.model_settings.max_tokens,
            split_type=TokensSplitType(value=self.model_settings.split_type_id),
            bert_type=BerType(value=self.model_settings.bert_type_id)
        )
        return True

    def define_data_pipe(self) -> Dataset:
        """ 创建数据集计算pipe """
        return DocClassifyDataSet(
            labels=self.labeler, tokenizer=self.tokenizer,
            max_sentence=self.model_settings.max_sentences
        )

    def define_model(self) -> bool:
        """
        定义模型
        :return: bool
        """
        self.model = DocClassifyModel(
            sent_encode_dim=self.model_settings.sent_encode_dim,
            doc_encode_dim=self.model_settings.doc_encode_dim,
            transformer_head_count=self.model_settings.transformer_head_count,
            max_tokens=self.model_settings.max_tokens,
            max_sentences=self.model_settings.max_sentences,
            class_count=self.model_settings.class_count,
            dropout_prob=self.model_settings.drop_out_prob,
            bert_type=BerType(value=self.model_settings.bert_type_id)
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
        self.coach_settings = DocClassifyCoachSettings.parse_obj(config_data["coach_settings"])
        self.model_settings = DocClassifyModelSettings.parse_obj(config_data["model_settings"])

        # 加载模型文件
        model_file = model_path_ckpt + "/" + self.coach_settings.model_file
        if self.define_model() is False:
            logging.error("Failed to define doc_classify_model")
            return False
        try:
            self.model.load_state_dict(
                torch.load(
                    model_file,
                    map_location=torch.device('cuda:%d' % self.device_settings.gpu_idx if self.use_cuda else "cpu")
                )
            )
        except Exception as exp:
            logging.error("load doc_classify_model params failed %s" % exp)
            return False

        return True

    def create_loss_optimizer(self) -> bool:
        """
        创建loss function和optimizer
        :return: bool
        """
        self.loss_func = torch.nn.NLLLoss()
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
        y, x, mask = params[0], params[1], params[2]
        y_ = self.model(x, mask)
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
        export_model_settings = DocClassifyExportedModelSettings(
            model_config_file="config.json",
            model_file="model.pt",
            third_dict_dir="dict",
            class_label=self.coach_settings.class_label,
            max_tokens=self.model_settings.max_tokens,
            max_sentences=self.model_settings.max_sentences,
            bert_type_id=self.model_settings.bert_type_id,
            split_type_id=self.model_settings.split_type_id
        )
        dict_path = model_path_script + "/" + export_model_settings.third_dict_dir
        model_file = model_path_script + "/" + export_model_settings.model_file
        config_file = model_path_script + "/" + export_model_settings.model_config_file
        try:
            with open(config_file, "w") as fp:
                fp.write(export_model_settings.json())
        except Exception as ex:
            logging.error("Failed to save doc_classify_model.config %s" % ex)
            return False

        # 打包第三方词典
        os.system("mkdir %s" % dict_path)
        os.system("cp -rf %s %s/" % (self.coach_settings.dict_dir + "/" + self.coach_settings.class_label, dict_path))

        # 生成torch script模型文件
        try:
            self.model.eval()
            dummy_input = self.model.get_dummy_input()
            torch.jit.trace(self.model, dummy_input).save(model_file)
        except Exception as ex:
            logging.error("Failed to export doc_classify_model %s" % ex)
            return False
