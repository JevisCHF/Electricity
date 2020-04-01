# -*- coding: utf-8 -*-
import jieba
import numpy as np
import re
# from Scrapy_RoBoDatabase_V1_15.Mysqldb import DB
# from Scrapy_RoBoDatabase_V1_15.file_name_list import m
from Scrapy_RoBodata_V1_01.new_cate import cate


class similarity():
    # 初始化处理
    def __init__(self):
        # 链接mysql
        # mysqldb = DB()
        # 查询第四层目录
        # self.sql = 'SELECT id,dir_name,level FROM lab_chinese_menu WHERE level=4'
        # self.file_name_list = mysqldb.query(self.sql)
        self.file_name_list = cate

    def get_word_vector(self, s1, s2):
        """
        :param s1: 句子1
        :param s2: 句子2
        :return: 返回句子的余弦相似度
        """
        # 分词
        cut1 = jieba.cut(s1)
        # print("/".join(cut1))
        cut2 = jieba.cut(s2)
        # print("/".join(cut2))
        list_word1 = (','.join(cut1)).split(',')
        list_word2 = (','.join(cut2)).split(',')

        # 列出所有的词,取并集
        key_word = list(set(list_word1 + list_word2))
        # 给定形状和类型的用0填充的矩阵存储向量
        word_vector1 = np.zeros(len(key_word))
        word_vector2 = np.zeros(len(key_word))

        # 计算词频
        # 依次确定向量的每个位置的值
        for i in range(len(key_word)):
            # 遍历key_word中每个词在句子中的出现次数
            for j in range(len(list_word1)):
                if key_word[i] == list_word1[j]:
                    word_vector1[i] += 1
            for k in range(len(list_word2)):
                if key_word[i] == list_word2[k]:
                    word_vector2[i] += 1

        # 输出向量
        # print(word_vector1)
        # print(word_vector2)
        return word_vector1, word_vector2

    def cos_dist(self, vec1, vec2):
        """
        :param vec1: 向量1
        :param vec2: 向量2
        :return: 返回两个向量的余弦相似度
        """
        dist1 = float(np.dot(vec1, vec2) /
                      (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
        return dist1

    def filter_html(self, html):
        """
        :param html: html
        :return: 返回去掉html的纯净文本
        """
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', html).strip()
        return dd

    def calcSimilarity(self, title):
        compare_list = []
        compare = {}
        title = title.replace('(', '').replace(')', '').replace(':', '').strip()

        for key, value in self.file_name_list.items():
            if len(key) >= 13:
                value = value.replace('(', '').replace(')', '').replace(':', '').strip()
                # 通过余弦定理计算相似度
                vec1, vec2 = self.get_word_vector(title, value)
                compare_result = self.cos_dist(vec1, vec2)
                # 将相似度对应的key与value保存在compare
                compare_list.append(compare_result)
                compare[compare_result] = key
                compare[key] = value

        if len(compare_list) >= 1:
            # 取出相似度最高的 key 与 value
            max_num = max(compare_list)
            key = compare[max_num]
            value = compare[key]
            new_id = str(key)

            if max_num >= 0.9:
                print(title, '与', value, '进行对比')
                print('两个标题相似度为：', str(round(max_num, 3) * 100) + '%')
                print('得到所属父级ID为：', new_id + '\n')
                return new_id
            else:
                print(title, '与', value, '进行对比')
                print('两个标题相似度为：', str(round(max_num, 3) * 100) + '%')
                print('相似度太低，取消写入\n')
                return None


if __name__ == '__main__':
    s = similarity()

    title = '进口数量:电流:当月值'
    title1 = '价格指数:原油:OPEC'
    title2 = 'OECD成员国:库存:陆上商业石油:原油'

    result = s.calcSimilarity(title1)
