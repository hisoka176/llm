import json
from pprint import pprint
from unittest import TestCase

from src.common.qp.querys import QueryParser
from src.dao.index.search import ESClient


class TestESClient(TestCase):

    @classmethod
    def setUpClass(self) -> None:
        self.es = ESClient()
        self.qp = QueryParser()

    def test_search(self):
        query = '次留计算'
        qp_info = self.qp.parser(query)
        print(qp_info)
        result = self.es.search('bi_sql', query=' '.join(qp_info['words']))
        print(result)
        context = self.es.build_context(result)
        print(context)

