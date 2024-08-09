import os.path
import re
from collections import defaultdict
from typing import Dict
import jieba.analyse
from src.config import root_path
import yaml


class RegexQueryField(object):

    def __init__(self, meta_yaml):
        with open(meta_yaml, 'r') as f:
            mapping = yaml.load(f, Loader=yaml.FullLoader)
        self.mapping = mapping  # 不要使用这个，因为这个没有进行大小写转换
        # self.entity_keyword_filepath = f'{root_path}/resources/query_parser_offline/entity_keyword.txt'
        self.preprocess(self.mapping)

    def preprocess(self, mapping: Dict[str, str]):
        reverse_mapping = defaultdict(set)

        for element in mapping:
            for key, value in element.items():
                for v in value:
                    reverse_mapping[v.lower()].add(key.lower())

        self.reverse_mapping = reverse_mapping
        self.all_words_regex = re.compile('|'.join(reverse_mapping.keys()))
        # self.dump_word_mapping(self.reverse_mapping)

    # def dump_word_mapping(self, mapping):
    #     with open(self.entity_keyword_filepath, 'w') as f:
    #         for key, value in mapping.items():
    #             key = key.lower()
    #             print(f'{key} 1000', file=f)

    def extract_entity(self, question):
        entity_words = self.all_words_regex.findall(question)
        entity_words_mapping = dict(
            [(entity_word, list(self.reverse_mapping[entity_word])) for entity_word in entity_words])
        return entity_words_mapping

    # def keywords(self, question):
    #     jieba.load_userdict(self.entity_keyword_filepath)
    #     keywords = jieba.analyse.extract_tags(question, topK=5)
    #     print(keywords)


if __name__ == '__main__':

    questions = [
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

    filepath = os.path.join(root_path, 'resources/query_parser_offline', 'query_entity.yaml')
    d = RegexQueryField(filepath)
    for question in questions:
        print(f'===={question}====')
        print(d.extract_entity(question))
        # print(d.keywords(question))
