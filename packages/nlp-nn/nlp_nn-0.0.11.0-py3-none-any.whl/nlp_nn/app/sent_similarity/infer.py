# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
文本相似度计算模型预测

Authors: fubo
Date: 2019/11/28 00:00:00
"""
import argparse
import torch
import json
from typing import List
from copy import deepcopy

from ...base.abstract import AbstractInfer
from ...base.common import BerType, TokensSplitType
from ...base.tokenizer import BertTokenizer
from ...base.model_dict import TagsDict
from ...base.metrics import Metric
from ...app.sent_similarity.settings import SentSimilarityExportedModelSettings
from ...app.sent_similarity.data_set import SentSimilarityDataSet, SentClassifySample


class SentSimilarityInfer(AbstractInfer):
    def __init__(self, model_path: str, model_config_file: str, gpu_idx: int = -1):
        super().__init__(model_path, model_config_file, gpu_idx)
        self.set_model_device()

    def load_model_config(self, model_config_file: str) -> SentSimilarityExportedModelSettings:
        """
        读取配置文件
        :return:
        """

        try:
            settings = SentSimilarityExportedModelSettings().parse_file(model_config_file)
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
            TagsDict(tags_file=self.model_path + "/" + self.settings.third_dict_dir + "/" + self.settings.class_label)
        ]

    def create_data_pipe(self) -> SentSimilarityDataSet:
        """
        创建数据处理pipe
        :return:
        """
        return SentSimilarityDataSet(
            tokenizer=self.tokenizer
        )

    def inference(self, query: str) -> (str, torch.FloatTensor, torch.FloatTensor):
        """
        短文本分类
        :param query:
        :param label:
        :return:

        分类结果详情
        [{"label_idx": 1, "label": "label1", "score": 0.85}, {{"label_idx": 0, "label": "label1", "score": 0.11}, ... ]

        term权重
        term_weights
        """
        sample = self.data_pipe.parse_sample(
            SentClassifySample(queries=[query], labels=[self.taggers[0].id2tag(0)]).json()
        )
        scores, term_weights = self.model(self.set_tensor_device(torch.LongTensor([sample["data"]])))
        scores = self.set_tensor_cpu(torch.exp(scores))[0, :]
        term_weights = self.set_tensor_cpu(term_weights)[0, :]

        # 最大概率label
        label = self.taggers[0].id2tag(int(torch.argmax(scores)))
        return label, scores, term_weights


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("release_path", type=str, help="Release path of model")
    parser.add_argument("config_file", type=str, help="Config file")
    parser.add_argument("data_file", type=str, help="Data file")
    parser.add_argument("output_file", type=str, help="Output file")
    parser.add_argument("metric_file", type=str, help="Metric results")
    parser.add_argument("--gpu_idx", type=int, help="GPU idx [Default -1]", default=-1)
    args = parser.parse_args()
    infer = SentSimilarityInfer(model_path=args.release_path, model_config_file=args.config_file, gpu_idx=args.gpu_idx)
    fp_data = open(args.data_file, "r")
    fp_output = open(args.output_file, "w")
    y_true = []
    y_pred = []
    while True:
        line = fp_data.readline().strip("\r\n")
        if len(line) == 0:
            break
        data = SentClassifySample.parse_raw(line)
        y_true.append(data.labels[0])
        label, scores, term_weights = infer.inference(data.queries[0])
        pred_scores = []
        for index, score in enumerate(scores.tolist()):
            pred_scores.append(Metric.ClassifyEvaluate.Result(label=infer.taggers[0].id2tag(index), score=score))
        y_pred.append(deepcopy(pred_scores))
        pred_scores_out = [elem.dict() for elem in pred_scores]
        fp_output.write(data.labels[0] + "\t" + json.dumps(pred_scores_out, ensure_ascii=False) + "\n")
        fp_output.flush()
    fp_data.close()
    fp_output.close()
    Metric.ClassifyEvaluate.report_to_file(y_true=y_true, y_pred=y_pred, metrics_file=args.metric_file)


if __name__ == '__main__':
    main()

