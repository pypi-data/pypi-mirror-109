# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com), lhy<lhy_in_blcu@126.com
@description: 
"""

import sys
from collections import defaultdict


class TextRankGraph:
    """textrank图算法"""

    def __init__(self):
        """init, no params"""
        self.graph = defaultdict(list)
        self.d = 0.85  # d是阻尼系数，一般设置为0.85
        self.min_diff = 1e-5  # 设定收敛阈值

    def add_edge(self, start, end, weight):
        """
        添加节点之间的边
        :param start:
        :param end:
        :param weight:
        :return:
        """
        self.graph[start].append((start, end, weight))
        self.graph[end].append((end, start, weight))

    def rank(self):
        """
        节点排序
        :return:
        """
        # 默认初始化权重
        weight_deafault = 1.0 / (len(self.graph) or 1.0)
        # nodeweight_dict, 存储节点的权重
        nodeweight_dict = defaultdict(float)
        # outsum，存储节点的出度权重
        outsum_node_dict = defaultdict(float)
        # 根据图中的边，更新节点权重
        for node, out_edge in self.graph.items():
            # 是 [('是', '全国', 1), ('是', '调查', 1), ('是', '失业率', 1), ('是', '城镇', 1)]
            nodeweight_dict[node] = weight_deafault
            outsum_node_dict[node] = sum((edge[2] for edge in out_edge), 0.0)
        # 初始状态下的textrank重要性权重
        sorted_keys = sorted(self.graph.keys())
        # 设定迭代次数，
        step_dict = [0]
        for step in range(1, 1000):
            for node in sorted_keys:
                s = 0
                # 计算公式：(edge_weight/outsum_node_dict[edge_node])*node_weight[edge_node]
                for e in self.graph[node]:
                    s += e[2] / outsum_node_dict[e[1]] * nodeweight_dict[e[1]]
                # 计算公式：(1-d) + d*s
                nodeweight_dict[node] = (1 - self.d) + self.d * s
            step_dict.append(sum(nodeweight_dict.values()))

            if abs(step_dict[step] - step_dict[step - 1]) <= self.min_diff:
                break

        # 利用Z-score进行权重归一化，也称为离差标准化，是对原始数据的线性变换，使结果值映射到[0 - 1]之间。
        # 先设定最大值与最小值均为系统存储的最大值和最小值
        min_rank = sys.float_info.min
        max_rank = sys.float_info.max
        for w in nodeweight_dict.values():
            if w < min_rank:
                min_rank = w
            if w > max_rank:
                max_rank = w

        for n, w in nodeweight_dict.items():
            nodeweight_dict[n] = (w - min_rank / 10.0) / (max_rank - min_rank / 10.0)

        return nodeweight_dict


class TextKeyword:
    """
    基于textrank图算法的关键词提取
    """

    def __init__(self):
        """init, no params"""
        self.candi_pos = ['n', 'v']  # 名词，动词
        self.stop_pos = ['t', 'Tg']  # 时间词，时素词
        self.span = 5

    def extract_keywords(self, word_list, num_keywords=10):
        """
        提取关键词
        :param word_list: list
        :param num_keywords: top n
        :return:
        """
        g = TextRankGraph()
        cm = defaultdict(int)
        for i, word in enumerate(word_list):
            if word[1][0] in self.candi_pos and len(word[0]) > 1:
                for j in range(i + 1, i + self.span):
                    if j >= len(word_list):
                        break
                    if word_list[j][1][0] not in self.candi_pos or word_list[j][1] in self.stop_pos or len(
                            word_list[j][0]) < 2:
                        continue
                    pair = tuple((word[0], word_list[j][0]))
                    cm[pair] += 1

        for terms, w in cm.items():
            g.add_edge(terms[0], terms[1], w)
        nodes_rank = g.rank()
        nodes_rank = sorted(nodes_rank.items(), key=lambda asd: asd[1], reverse=True)

        return nodes_rank[:num_keywords]
