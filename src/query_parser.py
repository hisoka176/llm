import json
import re
from typing import Any, Dict

import importlib

import jieba


class QueryParser(object):

    def build(self, subclass: str):
        pass

    def parser(self, question) -> Dict[str, Any]:
        pass


class SQLQueryParser(QueryParser):

    def __init__(self, *args, **kwargs):
        if 'filepath' not in kwargs:
            raise KeyError('filepath not in exists')

        filepath = kwargs['filepath']
        self.table_regex = re.compile('adm[_0-9a-z]+|rdm[_0-9a-z]+|gdm[_0-9a-z]+|dim[_0-9a-z]+|fdm[_0-9a-z]+')
        self.regex_dim, self.regex_metric = self.build_regex(filepath)

    def build_regex(self, filepath):
        with open(filepath, 'r') as f:
            mapping = json.load(f)
        dim_words = mapping['dim_words']
        regex_dim = re.compile('|'.join(dim_words))
        metric_words = mapping['metric_words']
        regex_metric = re.compile('|'.join(metric_words))
        return regex_dim, regex_metric

    def parser(self, question) -> Dict[str, Any]:
        question_normalize = question.lower()
        words = jieba.cut(question_normalize, cut_all=True)
        words = [word for word in words if word.strip() != '']

        dim_words = [word for word in self.regex_dim.findall(question_normalize) if word.strip() != '']
        metric_words = [word for word in self.regex_metric.findall(question_normalize) if word.strip() != '']
        response = {
            'question': question,
            'question_normalize': question_normalize,
            'words': words,
            'dim_words': dim_words,
            'metric_words': metric_words
        }
        return response


if __name__ == '__main__':
    pass
