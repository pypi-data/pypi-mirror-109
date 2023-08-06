# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
实体识别模型预测

Authors: fubo
Date: 2019/11/28 00:00:00
"""
import json
from typing import List
import argparse
import torch
from copy import deepcopy

from ...base.abstract import AbstractInfer
from ...base.common import BerType, TokensSplitType
from ...base.tokenizer import BertTokenizer
from ...base.model_dict import TagsDict
from ...base.metrics import Metric
from ...app.token_classify.settings import TokenClassifyExportedModelSettings
from ...app.token_classify.data_set import TokenClassifyDataSet, TokenClassifySample


class TokenClassifyInfer(AbstractInfer):
    def __init__(self, model_path: str, model_config_file: str, gpu_idx: int = -1):
        super().__init__(model_path, model_config_file, gpu_idx)
        self.set_model_device()

    def load_model_config(self, model_config_file: str) -> TokenClassifyExportedModelSettings:
        """
        读取配置文件
        :return:
        """
        try:
            settings = TokenClassifyExportedModelSettings().parse_file(model_config_file)
        except Exception as exp:
            raise FileNotFoundError(exp)
        return settings.copy()

    def create_tokenizer(self) -> BertTokenizer:
        """
        创建tokenizer
        :return:
        """
        return BertTokenizer(
            max_sent_len=self.settings.max_tokens,
            split_type=TokensSplitType(value=self.settings.split_type_id),
            bert_type=BerType(value=self.settings.bert_type_id)
        )

    def load_taggers(self) -> List[TagsDict]:
        """
        读取第三方词典
        :return:
        """

        return [
            TagsDict(
                tags_file=self.model_path + "/" + self.settings.third_dict_dir + "/" + self.settings.token_label_dic
            ),
            TagsDict(
                tags_file=self.model_path + "/" + self.settings.third_dict_dir + "/" + self.settings.token_label_inner_dic
            )
        ]

    def create_data_pipe(self) -> TokenClassifyDataSet:
        """
        创建数据处理pipe
        :return:
        """
        return TokenClassifyDataSet(
            token_label=self.taggers[0],
            token_inner_label=self.taggers[1],
            tokenizer=self.tokenizer
        )

    def inference(self, query: str) -> (List[dict], List[str], torch.FloatTensor):
        """
        短文本分类
        :param query:
        :return:

        分类结果详情
        [{"label_idx": 1, "label": "label1", "score": 0.85}, {{"label_idx": 0, "label": "label1", "score": 0.11}, ... ]

        term权重
        term_weights

        sentence权重
        sent_weights
        """
        sample = self.data_pipe.parse_sample(
            TokenClassifySample(query=query, token_labels=[]).json()
        )
        tokens = self.tokenizer.tokenize(query=query)
        scores = self.model(self.set_tensor_device(torch.LongTensor([sample["data"]])))
        scores = self.set_tensor_cpu(torch.exp(scores))
        token_labels_idx = torch.argmax(scores, dim=2)[0]
        inner_labels = [self.taggers[1].id2tag(label_idx) for label_idx in token_labels_idx]
        labels = self.data_pipe.token_label_inner_to_token_label(
            tokens=tokens,
            inner_labels=inner_labels
        )
        labels = [label.dict() for label in labels]
        return labels, inner_labels, scores


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("release_path", type=str, help="Release path of model")
    parser.add_argument("config_file", type=str, help="Config file")
    parser.add_argument("data_file", type=str, help="Data file")
    parser.add_argument("output_file", type=str, help="Output file")
    parser.add_argument("metric_file", type=str, help="Metric results")
    parser.add_argument("--gpu_idx", type=int, help="GPU idx [Default -1]", default=-1)
    args = parser.parse_args()
    infer = TokenClassifyInfer(model_path=args.release_path, model_config_file=args.config_file, gpu_idx=args.gpu_idx)
    fp_data = open(args.data_file, "r")
    fp_output = open(args.output_file, "w")
    y_true = []
    y_pred = []
    while True:
        line = fp_data.readline().strip("\r\n")
        if len(line) == 0:
            break
        data = TokenClassifySample.parse_raw(line)
        length = len(infer.tokenizer.tokenize(data.query).tokens)
        y_true_sample_idx = infer.data_pipe.parse_sample(line)["token_label"][:length]
        y_true_sample = list(map(infer.taggers[1].id2tag, y_true_sample_idx))
        y_true.append(deepcopy(y_true_sample))
        _, inner_labels, _ = infer.inference(query=data.query)
        y_pred_sample = inner_labels[:length]
        y_pred.append(deepcopy(y_pred_sample))
        y_true_out = json.dumps(y_true_sample, ensure_ascii=False)
        y_pred_out = json.dumps(y_pred_sample, ensure_ascii=False)

        fp_output.write(y_true_out + "\t" + y_pred_out + "\n")
        fp_output.flush()
    fp_data.close()
    fp_output.close()
    Metric.ClassifySeqLabelEvaluate.report_to_file(y_true=y_true, y_pred=y_pred, metrics_file=args.metric_file)


if __name__ == '__main__':
    main()
