from unittest import TestCase

import jieba

from src.query_parser import SQLQueryParser


class TestSQLQueryParser(TestCase):
    def test_parser(self):
        question = "之家昨天生产的线索总量有多少"
        words = jieba.cut(question, cut_all=True)
        qp = SQLQueryParser(filepath='resources/query_parser.json')
        info = qp.parser(question)
        print(info)
        self.fail()
