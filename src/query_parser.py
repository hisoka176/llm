import json
import os
import re
from typing import Any, Dict

import importlib

import jieba
from src.config import root_path
from src.query_parser_utils.query_entity import RegexQueryField
from src.query_parser_utils.query_extend import QueryExtend


class QueryParser(object):

    def build(self, subclass: str):
        pass

    def parser(self, question) -> Dict[str, Any]:
        pass


class SQLQueryParser(QueryParser):

    def __init__(self, query_parser_json_filepath,
                 query_extend_yaml_filepath,
                 query_field_yaml_filepath,
                 stop_words_filepath):
        """
        :param query_parser_json_filepath:
        :param query_extend_yaml_filepath:
        :param query_field_yaml_filepath:
        :param stop_words_filepath:
        """
        self.table_regex = re.compile('adm[_0-9a-z]+|rdm[_0-9a-z]+|gdm[_0-9a-z]+|dim[_0-9a-z]+|fdm[_0-9a-z]+')
        self.regex_dim, self.regex_metric = self.build_regex(query_parser_json_filepath)

        self.query_extend = QueryExtend(query_extend_yaml_filepath)
        self.query_field = RegexQueryField(query_field_yaml_filepath)
        self.stop_words = self.load_stop_words(stop_words_filepath)

    def load_stop_words(self, filepath):
        stop_words = set()
        with open(filepath, 'r') as f:
            for line in f:
                word = line.rstrip('\n').rstrip('\r')
                stop_words.add(word)
        return stop_words

    def build_regex(self, filepath):
        with open(filepath, 'r') as f:
            mapping = json.load(f)
        dim_words = mapping['dim_words']
        regex_dim = re.compile('|'.join(dim_words))
        metric_words = mapping['metric_words']
        regex_metric = re.compile('|'.join(metric_words))
        cutword_filepath = os.path.join(root_path, 'resources/query_parser_offline/words.txt')
        with open(cutword_filepath, 'w') as f:
            for word in dim_words + metric_words:
                print(f'{word} 1000', file=f)
        jieba.load_userdict(cutword_filepath)
        return regex_dim, regex_metric

    def parser(self, question) -> Dict[str, Any]:
        question_normalize = question.lower()
        words = jieba.cut(question_normalize, cut_all=False)
        words = [word for word in words if word.strip() != '']

        dim_words = [word for word in self.regex_dim.findall(question_normalize) if word.strip() != '']
        metric_words = [word for word in self.regex_metric.findall(question_normalize) if word.strip() != '']

        extend_words = self.query_extend.extend_question(words)
        field_words = self.query_field.extract_entity(question_normalize)
        drop_stop_words = [word for word in words if word not in self.stop_words and len(word) > 1]
        response = {
            'question': question,
            'question_normalize': question_normalize,
            'words': words,
            'dim_words': dim_words,
            'metric_words': metric_words,
            'extend_words': extend_words,
            'field_words': field_words,
            'drop_stop_words': drop_stop_words
        }
        return response


if __name__ == '__main__':
    questions = [
        '主软浏览DAU',
        'APP DAU',
        '四端DAU',
        '小程序DAU',
        '付费新用户DAU',
        '主启老用户DAU',
        '新用户DAU',
        'M端DAU',
        'PC端DAU',
        '自然新用户DAU',
        'PUSH拉活仅启DAU',
        '搜索DAU',
        '主软主启DAU',
        '三端总pv',
        '三端总uv',
        'APP端pv',
        'APP端uv',
        'PC端uv',
        'APP端时长',
        'PC端时长',
        'APP端人均时长',
        '主软人均时长',
        '主软pv',
        '主软时长',
        '上个月注册用户量',
        '之家用户总量',
        '用户和手机号会不会出现多对多的情况',
        '注册用户来源',
        '怎么获取注册用户设备号',
        'UGC昨天的互动量是多少？',
        'OGC 视频播放量？',
        '车家号完播量是多少',
        '口碑的评论量',
        '帖子的评论量',
        '2、怎么获取"驱动方式"配置参数？',
        '4、怎么判断车型的在售状态？',
        '5、怎么获取车型全部配置参数',
    ]

    query_parser_json = os.path.join(root_path, 'resources/query_parser.json')
    query_extend_yaml = os.path.join(root_path, 'resources/query_parser_offline/query_extend.yaml')
    query_field_yaml = os.path.join(root_path, 'resources/query_parser_offline/query_entity.yaml')
    stop_words = os.path.join(root_path, 'resources/stopwords.txt')
    sql_query_parser = SQLQueryParser(query_parser_json, query_extend_yaml, query_field_yaml, stop_words)
    for question in questions:
        print(f'===={question}====')
        question_info = sql_query_parser.parser(question)
        print(question_info)
        print(json.dumps(sql_query_parser.parser(question), ensure_ascii=False, indent=4))
