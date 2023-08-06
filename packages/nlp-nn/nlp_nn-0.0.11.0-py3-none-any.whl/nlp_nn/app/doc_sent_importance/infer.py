# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
文本分类模型预测

Authors: fubo
Date: 2019/11/28 00:00:00
"""
import argparse
import json
import torch
import copy
from typing import List, Dict

from ...base.common import BerType, TokensSplitType
from ...base.abstract import AbstractInfer
from ...base.tokenizer import BertTokenizer
from ...base.model_dict import TagsDict
from ...base.model_data import DocPos
from ...app.doc_sent_importance.data_set import DocSentImportanceDataSet, DocSentImportanceSample
from ...app.doc_sent_importance.settings import DocSentImportanceExportedModelSettings
from ...base.metrics import Metric


class DocSentImportanceInfer(AbstractInfer):
    def __init__(self, model_path: str, model_config_file: str, gpu_idx: int = -1):
        super().__init__(model_path, model_config_file, gpu_idx)

    def load_model_config(self, model_config_file: str) -> DocSentImportanceExportedModelSettings:
        """
        读取配置文件
        :return:
        """
        try:
            settings = DocSentImportanceExportedModelSettings().parse_file(model_config_file)
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
                tags_file=self.model_path + "/" + self.settings.third_dict_dir + "/" + self.settings.class_label
            )
        ]

    def create_data_pipe(self) -> DocSentImportanceDataSet:
        """
        创建数据处理pipe
        :return:
        """
        return DocSentImportanceDataSet(
            tagger=self.taggers[0],
            tokenizer=self.tokenizer,
            max_sentence=self.settings.max_sentences
        )

    def inference(self, title: str, content: List[str]) -> List[Dict]:
        """
        短文本分类
        :param title:
        :param content:
        :return:

        分类结果详情
        [{"label_idx": 1, "label": "label1", "score": 0.85}, {{"label_idx": 0, "label": "label1", "score": 0.11}, ... ]

        term权重
        term_weights

        sentence权重
        sent_weights
        """
        sample = self.data_pipe.parse_sample(
            DocSentImportanceSample(
                title=title, content=content,
                labels=[DocPos(sec_pos=0, sent_pos=0, label=self.taggers[0].id2tag(0))]
            ).json()
        )
        scores = self.model(
            self.set_tensor_device(torch.LongTensor([sample["data"]]))
        )
        pos_mapping = sample["pos_mapping"]
        scores = self.set_tensor_cpu(torch.exp(scores))[0, :]
        values, indices = torch.max(scores, dim=1)
        results = [
            {
                "sec_pos": pos_mapping[pos]["sec_pos"] if pos < len(pos_mapping) else -1,
                "sent_pos": pos_mapping[pos]["sent_pos"] if pos < len(pos_mapping) else -1,
                "label": self.taggers[0].id2tag(idx=idx),
                "label_idx": idx,
                "score": score
            } for pos, (idx, score) in enumerate(zip(indices.tolist(), values.tolist()))
        ]
        return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("release_path", type=str, help="Release path of model")
    parser.add_argument("config_file", type=str, help="Config file")
    parser.add_argument("data_file", type=str, help="Data file")
    parser.add_argument("output_file", type=str, help="Output file")
    parser.add_argument("metric_file", type=str, help="Metric results")
    parser.add_argument("--gpu_idx", type=int, help="GPU idx [Default -1]", default=-1)
    args = parser.parse_args()
    infer = DocSentImportanceInfer(
        model_path=args.release_path, model_config_file=args.config_file, gpu_idx=args.gpu_idx
    )
    fp_data = open(args.data_file, "r")
    fp_output = open(args.output_file, "w")
    y_true = []
    y_pred = []
    while True:
        line = fp_data.readline().strip("\r\n")
        if len(line) == 0:
            break
        parsed_data = infer.data_pipe.parse_sample(line=line)
        data = DocSentImportanceSample.parse_raw(line)
        y_true_out = list(map(infer.taggers[0].id2tag, parsed_data["label"]))
        scores = infer.inference(title=data.title, content=data.content)
        y_pred_out = []
        for score in scores:
            if score["sec_pos"] == -1:
                break
            y_pred_out.append(score["label"])

        y_true_out = y_true_out[:len(y_pred_out)]
        y_pred.append(copy.deepcopy(y_pred_out))
        y_true.append(copy.deepcopy(y_true_out))
        fp_output.write(
            json.dumps(y_true_out, ensure_ascii=False) + "\t" + json.dumps(y_pred_out, ensure_ascii=False) + "\n"
        )
        fp_output.flush()
    fp_data.close()
    fp_output.close()
    Metric.ClassifySeqLabelZeroOneEvaluate.report_to_file(y_true=y_true, y_pred=y_pred, metrics_file=args.metric_file)


if __name__ == '__main__':
    main()