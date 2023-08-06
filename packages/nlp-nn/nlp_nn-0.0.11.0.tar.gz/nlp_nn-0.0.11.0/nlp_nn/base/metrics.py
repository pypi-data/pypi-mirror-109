# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
评估指标

Authors: fubo
Date: 2019/11/28 00:00:00
"""

from typing import List, Dict
from pydantic import BaseModel
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score, roc_curve, auc
from sklearn.metrics import hamming_loss, jaccard_score
import numpy
from seqeval import metrics as seqeval_metrics
from ..base.common import Const


class Metric(object):
    class ClassifyEvaluate(object):
        class Result(BaseModel):
            # 标签
            label: str
            # 标签分数
            score: float

        @staticmethod
        def evaluate(y_true: List[str], y_pred: List[List[Result]]) -> Dict:
            """
            计算单类别分类评估(整体Accuracy，混淆矩阵，单类别(Precision, Recall, F-Score, AUC, ROC))
            :param y_true:
            :param y_pred:
            :return:
            """
            labels = list(set(y_true))
            y_true_label_idx = [labels.index(data) for data in y_true]
            y_pred = [sorted(data, key=lambda elem: elem.score, reverse=True) for data in y_pred]
            y_pred_label = [data[0].label for data in y_pred]
            y_pred_label_idx = [labels.index(data[0].label) for data in y_pred]

            # 计算accuracy
            accuracy = accuracy_score(y_true=y_true_label_idx, y_pred=y_pred_label_idx)

            # 计算混淆矩阵
            conf_matrix = confusion_matrix(y_true=y_true, y_pred=y_pred_label, labels=labels)

            # 计算每个类别的RPF
            rpf = [
                (
                    precision_score(
                        y_true=y_true_label_idx, y_pred=y_pred_label_idx, average="macro", labels=[i]
                    ),
                    recall_score(
                        y_true=y_true_label_idx, y_pred=y_pred_label_idx, average="macro", labels=[i]
                    ),
                    f1_score(
                        y_true=y_true_label_idx, y_pred=y_pred_label_idx, average="macro", labels=[i]
                    ),
                ) for i in range(len(labels))
            ]

            # 计算每个类别的AUC和ROC
            auc_values = []
            roc_values = []
            for i in range(len(labels)):
                fpr, tpr, thresholds = roc_curve(
                    y_true=list(map(lambda x: 1 if x == i else 0, y_true_label_idx)),
                    y_score=[list(filter(lambda x: x.label == labels[i], elem))[0].score for elem in y_pred]
                )
                auc_values.append(auc(fpr, tpr))
                roc_values.append((fpr, tpr, thresholds))

            # 计算每个类别的ROC
            return {
                "accuracy": accuracy,
                "confusion_matrix": conf_matrix,
                "rpf": rpf,
                "auc": auc_values,
                "roc": roc_values,
                "labels": labels
            }

        @staticmethod
        def report_to_file(y_true: List[str], y_pred: List[List[Result]], metrics_file: str):
            """
            评估结果写入文件
            :param y_true:
            :param y_pred:
            :param metrics_file:
            :return:
            """
            fp = open(metrics_file, "w")
            if "" in y_true:
                fp.close()
                return
            result = Metric.ClassifyEvaluate.evaluate(y_true=y_true, y_pred=y_pred)
            fp.write("Accuracy: %f\n" % result["accuracy"])

            fp.write("===============Confusion Matrix========================\n")
            fp.write("\t".join(result["labels"]) + "\n")
            for row in result["confusion_matrix"]:
                fp.write("\t".join(list(map(str, row))) + "\n")
            fp.write("===============RPF AUC in all labels========================\n")
            for index, label in enumerate(result["labels"]):
                fp.write("Label %s Precision %f\n" % (label, result["rpf"][index][0]))
                fp.write("Label %s Recall %f\n" % (label, result["rpf"][index][1]))
                fp.write("Label %s F1-Score %f\n" % (label, result["rpf"][index][2]))
                fp.write("Label %s AUC %f\n" % (label, result["auc"][index]))
            fp.close()

    class ClassifyMultiEvaluate(object):

        @staticmethod
        def evaluate(y_true: List[List[str]], y_pred: List[List[str]]) -> Dict:
            """
            计算评估分数
            :param y_true:
            :param y_pred:
            :return:
            """
            metric = {
                "instance_accuracy": 0.0,
                "ave_hamming_loss": 0.0,
                "max_hamming_loss": 0.0,
                "min_jaccard_score": 0.0,
                "ave_jaccard_score": 0.0
            }
            labels = set()
            for label_list in y_true + y_pred:
                for label in label_list:
                    labels.add(label)
            labels = list(labels)

            y_true_matrix = numpy.zeros([len(y_true), len(labels)], dtype="int32").tolist()
            y_pred_matrix = numpy.zeros([len(y_true), len(labels)], dtype="int32").tolist()
            for i, vec in enumerate(y_true_matrix):
                for j, data in enumerate(vec):
                    label = labels[j]
                    if label in y_true[i]:
                        y_true_matrix[i][j] = 1
                    if label in y_pred[i]:
                        y_pred_matrix[i][j] = 1

            hamming_losses = []
            jaccard_scores = []
            correct_count = 0
            for pair in zip(y_true_matrix, y_pred_matrix):
                if sum(pair[0]) == 0 and sum(pair[1]) == 0:
                    hamming_losses.append(0.0)
                    jaccard_scores.append(1.0)
                    correct_count = correct_count + 1
                    continue
                hamming_losses.append(hamming_loss(pair[0], pair[1]))
                jaccard_scores.append(jaccard_score(pair[0], pair[1]))
                if pair[0] == pair[1]:
                    correct_count = correct_count + 1
            metric["max_hamming_loss"] = max(hamming_losses)
            metric["ave_hamming_loss"] = 1.0 * sum(hamming_losses) / (len(hamming_losses) + Const.MIN_POSITIVE_NUMBER)
            metric["min_jaccard_score"] = min(jaccard_scores)
            metric["ave_jaccard_score"] = 1.0 * sum(jaccard_scores) / len(jaccard_scores)
            metric["instance_accuracy"] = 1.0 * correct_count / len(hamming_losses)
            return metric

        @staticmethod
        def report_to_file(y_true: List[List[str]], y_pred: List[List[str]], metrics_file: str):
            """
            评估结果写入metrics文件中
            :param y_true:
            :param y_pred:
            :param metrics_file:
            :return:
            """
            fp = open(metrics_file, "w")
            if "" in y_true:
                fp.close()
                return
            result = Metric.ClassifyMultiEvaluate.evaluate(y_true=y_true, y_pred=y_pred)
            fp.write("Instance Accuracy: %f\n" % result["instance_accuracy"])

            fp.write("===============Hamming Loss========================\n")
            fp.write("Max Hamming Loss: %f\n" % result["max_hamming_loss"])
            fp.write("Average Hamming Loss: %f\n" % result["ave_hamming_loss"])
            fp.write("===============Jaccard Score========================\n")
            fp.write("Min Jaccard Score: %f\n" % result["min_jaccard_score"])
            fp.write("Average Jaccard Score: %f\n" % result["ave_jaccard_score"])

            fp.close()

    class ClassifySeqLabelEvaluate(object):
        """
        序列标注评估 BOIES标注体系
        """
        @staticmethod
        def evaluate(y_true: List[List[str]], y_pred: List[List[str]]) -> Dict:
            """
            计算评估分数
            :param y_true:
            :param y_pred:
            :return:
            """
            return {
                "accuracy": seqeval_metrics.accuracy_score(y_true=y_true, y_pred=y_pred),
                "precision": seqeval_metrics.precision_score(y_true=y_true, y_pred=y_pred),
                "recall": seqeval_metrics.recall_score(y_true=y_true, y_pred=y_pred),
                "f1_score": seqeval_metrics.f1_score(y_true=y_true, y_pred=y_pred),
                "report": seqeval_metrics.classification_report(y_true=y_true, y_pred=y_pred),
                "performance": seqeval_metrics.performance_measure(y_true=y_true, y_pred=y_pred)
            }

        @staticmethod
        def report_to_file(y_true: List[List[str]], y_pred: List[List[str]], metrics_file: str):
            """
            评估结果写入metrics文件中
            :param y_true:
            :param y_pred:
            :param metrics_file:
            :return:
            """
            fp = open(metrics_file, "w")
            if "" in y_true:
                fp.close()
                return
            result = Metric.ClassifySeqLabelEvaluate.evaluate(y_true=y_true, y_pred=y_pred)
            fp.write("Accuracy: %f\n" % result["accuracy"])
            fp.write("Precision: %f\n" % result["precision"])
            fp.write("Recall: %f\n" % result["recall"])
            fp.write("F1 Score: %f\n" % result["f1_score"])
            fp.write("===============Confusion Matrix========================\n")
            fp.write("%d\t%d\n" % (result["performance"]["TP"], result["performance"]["FP"]))
            fp.write("%d\t%d\n" % (result["performance"]["FN"], result["performance"]["TN"]))

            fp.write("===============Sequence Report========================\n")
            fp.write(result["report"])
            fp.close()

    class ClassifySeqLabelZeroOneEvaluate(object):
        """
        序列标注评估 0/1标注体系
        """
        @staticmethod
        def evaluate(y_true: List[List[str]], y_pred: List[List[str]]) -> Dict:
            """
            计算评估分数
            :param y_true:
            :param y_pred:
            :return:
            """
            metric = {
                "instance_accuracy": 0.0,
                "ave_accuracy": 0.0,
                "ave_precision": 0.0,
                "ave_recall": 0.0,
                "confusion_matrix": []
            }
            correct_count = 0
            accuracies = []
            precisions = []
            recalls = []
            f1_scores = []
            y_true_flatten = []
            y_pred_flatten = []
            for pair in zip(y_true, y_pred):
                y_true_labels = pair[0]
                y_pred_labels = pair[1]
                y_true_flatten = y_true_flatten + y_true_labels
                y_pred_flatten = y_pred_flatten + y_pred_labels
                if y_true_labels == y_pred_labels:
                    correct_count = correct_count + 1
                accuracies.append(accuracy_score(y_true_labels, y_pred_labels))
                precisions.append(precision_score(y_true_labels, y_pred_labels, pos_label='1'))
                recalls.append(recall_score(y_true_labels, y_pred_labels, pos_label='1'))
                f1_scores.append(f1_score(y_true_labels, y_pred_labels, pos_label='1'))
            metric["instance_accuracy"] = 1.0 * correct_count / len(y_true)
            metric["ave_accuracy"] = 1.0 * sum(accuracies) / len(y_true)
            metric["ave_precision"] = 1.0 * sum(precisions) / len(y_true)
            metric["ave_recall"] = 1.0 * sum(recalls) / len(y_true)
            metric["ave_f1_score"] = 1.0 * sum(f1_scores) / len(y_true)
            tn, fp, fn, tp = confusion_matrix(y_true_flatten, y_pred_flatten, labels=["1", "0"]).ravel()
            metric["confusion_matrix"] = [tn, fp, fn, tp]
            return metric

        @staticmethod
        def report_to_file(y_true: List[List[str]], y_pred: List[List[str]], metrics_file: str):
            """
            评估结果写入metrics文件中
            :param y_true:
            :param y_pred:
            :param metrics_file:
            :return:
            """
            fp = open(metrics_file, "w")
            if "" in y_true:
                fp.close()
                return
            result = Metric.ClassifySeqLabelZeroOneEvaluate.evaluate(y_true=y_true, y_pred=y_pred)
            fp.write("Instance Accuracy: %f\n" % result["instance_accuracy"])
            fp.write("Average Accuracy: %f\n" % result["ave_accuracy"])
            fp.write("Average Precision: %f\n" % result["ave_precision"])
            fp.write("Average Recall: %f\n" % result["ave_recall"])
            fp.write("Average F1-Score: %f\n" % result["ave_f1_score"])
            fp.write("===============Confusion Matrix========================\n")
            fp.write("%d\t%d\n" % (result["confusion_matrix"][3], result["confusion_matrix"][1]))
            fp.write("%d\t%d\n" % (result["confusion_matrix"][2], result["confusion_matrix"][0]))

            fp.close()

    class SentTokensClassifyEvaluate(object):
        """
        分类序列标注评估
        """
        class Result(BaseModel):
            # 标签
            label: str
            # 标签分数
            score: float

        @staticmethod
        def evaluate(
                y_true_sent: List[str], y_pred_sent: List[List[Result]],
                y_true_tokens: List[List[str]], y_pred_tokens: List[List[str]]

        ) -> (Dict, Dict):
            y_pred_value = [
                [
                    Metric.ClassifyEvaluate.Result(label=elem.label, score=elem.score) for elem in value
                ] for value in y_pred_sent
            ]
            sent_metric = Metric.ClassifyEvaluate.evaluate(y_true=y_true_sent, y_pred=y_pred_value)
            tokens_metric = Metric.ClassifySeqLabelEvaluate.evaluate(y_true=y_true_tokens, y_pred=y_pred_tokens)
            return sent_metric, tokens_metric

        @staticmethod
        def report_to_file(
                y_true_sent: List[str], y_pred_sent: List[List[Result]],
                y_true_tokens: List[List[str]], y_pred_tokens: List[List[str]],
                metrics_file: str
        ):
            fp = open(metrics_file, "w")
            if "" in y_true_tokens:
                fp.close()
                return
            sent_metric, tokens_metric = Metric.SentTokensClassifyEvaluate.evaluate(
                y_true_sent=y_true_sent, y_pred_sent=y_pred_sent,
                y_true_tokens=y_true_tokens, y_pred_tokens=y_pred_tokens
            )
            fp.write("===============Sent Classify Evaluation========================\n")
            fp.write("Accuracy: %f\n" % sent_metric["accuracy"])

            fp.write("===============Confusion Matrix========================\n")
            fp.write("\t".join(sent_metric["labels"]) + "\n")
            for row in sent_metric["confusion_matrix"]:
                fp.write("\t".join(list(map(str, row))) + "\n")
            fp.write("===============RPF AUC in all labels========================\n")
            for index, label in enumerate(sent_metric["labels"]):
                fp.write("Label %s Precision %f\n" % (label, sent_metric["rpf"][index][0]))
                fp.write("Label %s Recall %f\n" % (label, sent_metric["rpf"][index][1]))
                fp.write("Label %s F1-Score %f\n" % (label, sent_metric["rpf"][index][2]))
                fp.write("Label %s AUC %f\n" % (label, sent_metric["auc"][index]))

            fp.write("================================================================\n")
            fp.write("===============Token Classify Evaluation========================\n")
            fp.write("Accuracy: %f\n" % tokens_metric["accuracy"])
            fp.write("Precision: %f\n" % tokens_metric["precision"])
            fp.write("Recall: %f\n" % tokens_metric["recall"])
            fp.write("F1 Score: %f\n" % tokens_metric["f1_score"])
            fp.write("===============Confusion Matrix========================\n")
            fp.write("%d\t%d\n" % (tokens_metric["performance"]["TP"], tokens_metric["performance"]["FP"]))
            fp.write("%d\t%d\n" % (tokens_metric["performance"]["FN"], tokens_metric["performance"]["TN"]))

            fp.write("===============Sequence Report========================\n")
            fp.write(tokens_metric["report"])
            fp.close()



