# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
模型层管理

Authors: fubo
Date: 2019/11/28 00:00:00
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import torch
import transformers
from typing import Optional
from ..base.common import BerType
from ..base.utils import Utils


class EmbeddingLayer(torch.nn.Module):
    """
    Embedding lookup table层
    """
    def __init__(self, vocab_size, dim):
        super().__init__()
        self.layer = torch.nn.Embedding(vocab_size, dim)
        torch.nn.init.uniform_(self.layer.weight)

    def forward(self, x: torch.LongTensor) -> torch.Tensor:
        """
        :param x:
        :return:
        """
        return self.layer(x)


class BertEmbeddingLayer(torch.nn.Module):
    """
    Bert embedding 层
    """
    def __init__(self, bert_type=BerType.LITE_BERT_TINY):
        super().__init__()
        self.layer = transformers.AutoModel.from_pretrained(Utils.download_model(bert_type=bert_type))

        self.hidden_size = self.layer.config.hidden_size

    def forward(self, x: torch.LongTensor, mask: torch.LongTensor = None) -> torch.Tensor:
        """
        向后计算
        :param x:
        :param mask:
        :return:
        """
        return self.layer(x) if mask is None else self.layer(x, attention_mask=mask)


class LinearLayer(torch.nn.Module):
    """
    全连接层
    """
    def __init__(self, n_input_dim, n_output_dim, with_bias=False):
        super().__init__()
        self.linear_layer = torch.nn.Linear(
            in_features=n_input_dim,
            out_features=n_output_dim,
            bias=with_bias
        )
        torch.nn.init.xavier_uniform_(self.linear_layer.weight)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        向后计算
        :param x:
        :return:
        """
        return self.linear_layer(x)


class AttentionCoverageLayer(torch.nn.Module):
    """
    向量attention聚合
    N * S * D -> N * 1 * D
    """
    def __init__(self, n_dim: int):
        super().__init__()
        self.attention_vector = torch.nn.Parameter(torch.randn((n_dim, 1)))

    def forward(self, x: torch.LongTensor, mask: torch.LongTensor = None) -> torch.Tensor:
        """
        :param x: (batch_size * Length * EncodingDim)
        :param mask: (batch_size * Length)
        :return: (batch_size * EncodingDim)
        """
        if mask is None:
            mask = torch.ones(x.shape[:-1])
        mask = torch.unsqueeze(mask, dim=2)
        scores = torch.softmax(mask * torch.matmul(x, self.attention_vector), dim=1)
        return torch.squeeze(torch.matmul(torch.transpose(scores, dim0=2, dim1=1), x), dim=1)


class BertSentEncodeAvePoolingLayer(torch.nn.Module):
    """
    基于bert average pooling句编码layer
    """
    def __init__(self, sent_encode_dim, bert_type=BerType.LITE_BERT_TINY):
        """
        :param sent_encode_dim:
        :param bert_type:
        """
        super().__init__()
        # Embedding映射层##########
        self.embedding_layer = BertEmbeddingLayer(bert_type=bert_type)
        embedding_dim = self.embedding_layer.hidden_size

        # Encode linear layer
        self.linear_layer = LinearLayer(embedding_dim, sent_encode_dim)

    def forward(self, x: torch.LongTensor, mask: torch.LongTensor = None) -> torch.Tensor:
        """
        :param x:
        :param mask:
        :return:
        """
        return self.linear_layer(self.embedding_layer(x, mask=mask)[1])


class BertSentEncodeTermLevelLayer(torch.nn.Module):
    """
    基于bert layer，term粒度
    """
    def __init__(self, bert_type=BerType.LITE_BERT_TINY):
        """
        :param bert_type:
        """
        super().__init__()
        # Embedding映射层##########
        self.embedding_layer = BertEmbeddingLayer(bert_type=bert_type)

    def forward(self, x: torch.LongTensor, mask: torch.LongTensor = None) -> torch.Tensor:
        """
        :param x:
        :return:
        """
        return self.embedding_layer(x, mask=mask)[0]


class BertDocSentLevelEncodeLayer(torch.nn.Module):
    """
    文档分句编码 Hierarchical Attention Networks
    """
    def __init__(
            self,
            sent_encode_dim: int, transformer_head_count: int,
            max_tokens: int = 20, max_sentences: int = 10,
            bert_type=BerType.LITE_BERT_TINY
    ):
        """
        文档分句编码
        :param sent_encode_dim:
        :param transformer_head_count:
        :param max_tokens:
        :param max_sentences:
        :param bert_type:
        """
        super().__init__()
        self.max_tokens = max_tokens
        self.max_sentences = max_sentences
        self.sent_encode_dim = sent_encode_dim

        # sent encoding layer
        self.sent_encoding_layer = BertSentEncodeAvePoolingLayer(
            sent_encode_dim=sent_encode_dim,
            bert_type=bert_type
        )

        # transformer layer
        self.transformer_layer = torch.nn.TransformerEncoderLayer(
            d_model=self.sent_encode_dim,
            nhead=transformer_head_count
        )

    def forward(self, x: torch.LongTensor, mask: torch.LongTensor = None) -> (
            torch.Tensor, torch.Tensor, torch.Tensor
    ):
        """
        计算doc encoding
        :param x: (batch_size * sent_size * token_size) 每篇文档表示成为多句。段落用[unused1] token分割
        :param mask: 掩码 (batch_size * sent_size * token_size)
        :return:
        doc encoding (batch_size * doc_encoding_dim)
        token level attention (batch_size * sent_size * token_size)
        sent level attention (batch_size * sent_size)
        """
        shape_input = x.shape
        term_mask = None
        sent_mask = None
        if mask is not None:
            term_mask = torch.flatten(mask, start_dim=0, end_dim=1)
            sent_mask = (torch.sum(term_mask, dim=1, dtype=float) > 0).reshape(shape_input[:2])

        # sentence level encode
        term_x = torch.flatten(x, start_dim=0, end_dim=1)
        sents = self.sent_encoding_layer(term_x, mask=term_mask)

        sents = sents.reshape(list(shape_input[:2]) + [self.sent_encode_dim])
        # sents = self.transformer_layer(sents, src_mask=sent_mask)
        sents = self.transformer_layer(sents)

        return sents


class BertDocEncodeLayer(torch.nn.Module):
    """
    文档编码 Hierarchical Attention Networks
    """
    def __init__(
            self,
            sent_encode_dim: int, doc_encode_dim: int,
            transformer_head_count: int,
            max_tokens: int = 20, max_sentences: int = 10,
            bert_type=BerType.LITE_BERT_TINY
    ):
        super().__init__()
        self.doc_encode_dim = doc_encode_dim

        # doc sent encoding layer
        self.doc_sent_encoding_layer = BertDocSentLevelEncodeLayer(
            sent_encode_dim=sent_encode_dim, transformer_head_count=transformer_head_count,
            max_tokens=max_tokens, max_sentences=max_sentences,
            bert_type=bert_type
        )

        # converge layer
        self.sent_converge_layer = AttentionCoverageLayer(n_dim=sent_encode_dim)
        self.doc_linear_layer = LinearLayer(sent_encode_dim, self.doc_encode_dim)

    def forward(self, x: torch.LongTensor, mask: torch.LongTensor = None) -> (
            torch.Tensor, torch.Tensor, torch.Tensor
    ):
        """
        计算doc encoding
        :param x: (batch_size * sent_size * token_size) 每篇文档表示成为多句。段落用[unused1] token分割
        :param mask: 掩码 (batch_size * sent_size * token_size)
        :return:
        doc encoding (batch_size * doc_encoding_dim)
        token level attention (batch_size * sent_size * token_size)
        sent level attention (batch_size * sent_size)
        """
        shape_input = x.shape
        sent_mask = None
        if mask is not None:
            sent_mask = (
                    torch.sum(torch.flatten(mask, start_dim=0, end_dim=1), dim=1, dtype=float) > 0
            ).reshape(shape_input[:2])

        # sentence level encode
        sents = self.doc_sent_encoding_layer(x, mask=mask)

        # 计算sent mask
        doc = self.sent_converge_layer(sents, mask=sent_mask)
        doc = self.doc_linear_layer(doc)
        return doc


class CRFLayer(torch.nn.Module):
    """Conditional random field.
    This module implements a conditional random field [LMP01]_. The forward computation
    of this class computes the log likelihood of the given sequence of tags and
    emission score tensor. This class also has `~CRFLayer.decode` method which finds
    the best tag sequence given an emission score tensor using `Viterbi algorithm`_.
    Args:
        num_tags: Number of tags.
        batch_first: Whether the first dimension corresponds to the size of a minibatch.
    Attributes:
        start_transitions (`~torch.nn.Parameter`): Start transition score tensor of size
            ``(num_tags,)``.
        end_transitions (`~torch.nn.Parameter`): End transition score tensor of size
            ``(num_tags,)``.
        transitions (`~torch.nn.Parameter`): Transition score tensor of size
            ``(num_tags, num_tags)``.
    .. [LMP01] Lafferty, J., McCallum, A., Pereira, F. (2001).
       "Conditional random fields: Probabilistic models for segmenting and
       labeling sequence data". *Proc. 18th International Conf. on Machine
       Learning*. Morgan Kaufmann. pp. 282–289.
    .. _Viterbi algorithm: https://en.wikipedia.org/wiki/Viterbi_algorithm
    """

    def __init__(self, num_tags: int) -> None:
        if num_tags <= 0:
            raise ValueError(f'invalid number of tags: {num_tags}')
        super().__init__()
        self.num_tags = num_tags
        self.start_transitions = torch.nn.Parameter(torch.empty(num_tags))
        self.end_transitions = torch.nn.Parameter(torch.empty(num_tags))
        self.transitions = torch.nn.Parameter(torch.empty(num_tags, num_tags))

        torch.nn.init.uniform_(self.start_transitions, -0.1, 0.1)
        torch.nn.init.uniform_(self.end_transitions, -0.1, 0.1)
        torch.nn.init.uniform_(self.transitions, -0.1, 0.1)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(num_tags={self.num_tags})'

    def forward(
            self,
            emissions: torch.Tensor, tags: torch.LongTensor, mask: Optional[torch.ByteTensor] = None,
            reduction: str = 'sum',
    ) -> torch.Tensor:
        """Compute the conditional log likelihood of a sequence of tags given emission scores.
        Args:
            emissions (`~torch.Tensor`): Emission score tensor of size
                ``(batch_size, seq_length, num_tags)`` .
            tags (`~torch.LongTensor`): Sequence of tags tensor of size
                ``(batch_size, seq_length)`` .
            mask (`~torch.ByteTensor`): Mask tensor of size ``(batch_size, seq_length)`` .
            reduction: Specifies  the reduction to apply to the output:
                ``none|sum|mean|token_mean``. ``none``: no reduction will be applied.
                ``sum``: the output will be summed over batches. ``mean``: the output will be
                averaged over batches. ``token_mean``: the output will be averaged over tokens.
        Returns:
            `~torch.Tensor`: The log likelihood. This will have size ``(batch_size,)`` if
            reduction is ``none``, ``()`` otherwise.
        """
        # self._validate(emissions, tags=tags, mask=mask)
        if reduction not in ('none', 'sum', 'mean', 'token_mean'):
            raise ValueError(f'invalid reduction: {reduction}')
        if mask is None:
            mask = torch.ones_like(tags, dtype=torch.uint8)

        emissions = emissions.transpose(0, 1)
        tags = tags.transpose(0, 1)
        mask = mask.transpose(0, 1)

        numerator = self.__compute_score(emissions, tags, mask)
        denominator = self.__compute_normalizer(emissions, mask)
        llh = -1 * (numerator - denominator)

        if reduction == 'none':
            return llh
        if reduction == 'sum':
            return llh.sum()
        if reduction == 'mean':
            return llh.mean()
        assert reduction == 'token_mean'
        return llh.sum() / mask.float().sum()

    def __compute_score(
            self,
            emissions: torch.Tensor, tags: torch.LongTensor, mask: torch.ByteTensor
    ) -> torch.Tensor:
        # emissions: (seq_length, batch_size, num_tags)
        # tags: (seq_length, batch_size)
        # mask: (seq_length, batch_size)
        # assert emissions.dim() == 3 and tags.dim() == 2
        # assert emissions.shape[:2] == tags.shape
        # assert emissions.size(2) == self.num_tags
        # assert mask.shape == tags.shape
        # assert mask[0].all()

        seq_length, batch_size = tags.shape
        mask = mask.float()

        # Start transition score and first emission
        # shape: (batch_size,)
        score = self.start_transitions[tags[0]]
        score += emissions[0, torch.arange(batch_size), tags[0]]

        for i in range(1, seq_length):
            score += self.transitions[tags[i - 1], tags[i]] * mask[i]
            score += emissions[i, torch.arange(batch_size), tags[i]] * mask[i]

        seq_ends = mask.long().sum(dim=0) - 1
        last_tags = tags[seq_ends, torch.arange(batch_size)]
        score += self.end_transitions[last_tags]
        return score

    def __compute_normalizer(self, emissions: torch.Tensor, mask: torch.ByteTensor) -> torch.Tensor:
        # emissions: (seq_length, batch_size, num_tags)
        # mask: (seq_length, batch_size)
        # assert emissions.dim() == 3 and mask.dim() == 2
        # assert emissions.shape[:2] == mask.shape
        # assert emissions.size(2) == self.num_tags
        # assert mask[0].all()

        seq_length = emissions.size(0)
        score = self.start_transitions + emissions[0]

        for i in range(1, seq_length):
            broadcast_score = score.unsqueeze(2)
            broadcast_emissions = emissions[i].unsqueeze(1)
            next_score = broadcast_score + self.transitions + broadcast_emissions
            next_score = torch.logsumexp(next_score, dim=1)
            score = torch.where(mask[i].unsqueeze(1), next_score, score)

        score += self.end_transitions
        return torch.logsumexp(score, dim=1)


class CrossLayer(torch.nn.Module):
    """
    Cross layer part in Cross and Deep Network
    The ops in this module is x_0 * x_l^T * w_l + x_l + b_l for each layer l, and x_0 is the init input of this module
    """

    def __init__(self, input_feature_num, cross_layer):
        """
        :param input_feature_num: total num of input_feature, including of the embedding feature and dense feature
        :param cross_layer: the number of layer in this module expect of init op
        """
        super().__init__()
        self.cross_layer = cross_layer + 1  # add the first calculate
        weight_w = []
        weight_b = []
        batch_norm = []
        for i in range(self.cross_layer):
            weight_w.append(torch.nn.Parameter(torch.nn.init.normal_(torch.empty(input_feature_num))))
            weight_b.append(torch.nn.Parameter(torch.nn.init.normal_(torch.empty(input_feature_num))))
            batch_norm.append(torch.nn.BatchNorm1d(input_feature_num, affine=False))
        self.weight_w = torch.nn.ParameterList(weight_w)
        self.weight_b = torch.nn.ParameterList(weight_b)
        self.batch_norm = torch.nn.ModuleList(batch_norm)

    def forward(self, x):
        """
        向后计算
        :param x:
        :return:
        """
        output = x
        x = x.reshape(x.shape[0], -1, 1)
        for i in range(self.cross_layer):
            output = torch.matmul(torch.bmm(x, torch.transpose(output.reshape(output.shape[0], -1, 1), 1, 2)),
                                  self.weight_w[i]) + self.weight_b[i] + output
            output = self.batch_norm[i](output)
        return output
