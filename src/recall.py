import json
import os
from abc import ABC
from typing import Any, Dict

import jieba
from elasticsearch import Elasticsearch


class Recall(ABC):

    def recall(self, question) -> Dict[str, Any]:
        pass


class ESRecall(Recall):

    def __init__(self, *args, **kwargs):
        assert 'filepath' in kwargs, 'filepath not in kwargs for object esrecall'
        assert 'index_name' in kwargs, 'keyerror "index_name"  '
        self.dsl = self.load_dsl(kwargs['filepath'])
        self.client: Elasticsearch = Elasticsearch(hosts='http://yz-rcm-es811.search.corpautohome.com:80')
        self.index_name = kwargs['index_name']
        assert self.client.ping(), 'failed to establish a connection to es'

    def load_dsl(self, filepath):
        with open(filepath, 'r') as f:
            # dsl = json.load(f)
            dsl = '\n'.join([line.rstrip('\r').rstrip('\n') for line in f.readlines()])
        return dsl

    def build_body(self, question_info):
        body = self.dsl
        question = question_info['words'] + question_info['dim_words'] + question_info['metric_words']
        body = body.replace('{question}', ' '.join(question))
        return body

    def recall(self, question_info) -> Dict[str, Any]:
        body = self.build_body(question_info=question_info)
        body = json.loads(body)
        results = self.client.search(index=self.index_name, body=body).body
        recall_info = {
            'dsl': body,
            'results': results
        }
        return recall_info


class MultiESRecall(Recall):

    def __init__(self, *args, **kwargs):
        self.client: Elasticsearch = Elasticsearch(hosts='http://yz-rcm-es811.search.corpautohome.com:80')
        self.index_name = 'bi_sql'

    def recall(self, question_info) -> Dict[str, Any]:
        # question_info = {
        #     'words': ' '.join(jieba.cut('主软dau', cut_all=True)),
        #     'question': '主软dau'
        # }
        table_info = self.select_table(question_info)

        field_info = self.select_fields(question_info, table_info)
        recall_info = {
            'table_info': table_info,
            'field_info': field_info,
        }
        return recall_info

    def select_table(self, question_info):
        table_dsl = {
            "_source": ["tablename"],
            "query": {
                "bool": {
                    "must": [
                        {
                            "bool": {
                                "should": [
                                    {
                                        "multi_match": {
                                            "query": f"{' '.join(question_info['words'])}",
                                            "fields": [
                                                "tablecomment_tks^0.8",
                                                "tabledesc_tks^1.2",
                                                "alias_tks^0.8",
                                                "comment_tks^0.8",
                                                "desc_tks^1.2"
                                            ],
                                            "operator": "or",
                                            "type": "most_fields"
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        }

        result = self.client.search(index=self.index_name, body=table_dsl).body
        if result['hits']['total']['value'] > 0:
            result = result['hits']['hits']
            table_names = [res['_source']['tablename'] for res in result]
        else:
            table_names = []

        table_info = {
            'table_dsl': json.dumps(table_dsl, ensure_ascii=False, indent=4),
            'table_names': table_names
        }
        return table_info

    def select_fields(self, question_info, table_info):
        # top1
        #
        if len(table_info['table_names']) < 1:
            return ""
        field_dsl = {
            "_source": ["name", "desc"],
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                "tablename": f"{table_info['table_names'][0]}"
                            }
                        }
                    ],
                    "should": [
                        {
                            "multi_match": {
                                "query": f"{' '.join(question_info['words'])}",
                                "fields": [
                                    "alias_tks^0.8",
                                    "comment_tks^0.8",
                                    "desc_tks^1.2"
                                ],
                                "operator": "or",
                                "type": "most_fields"
                            }
                        }
                    ],
                    "minimum_should_match": 1
                }
            }
        }

        result = self.client.search(index=self.index_name, body=field_dsl)
        if result['hits']['total']['value'] > 0:
            result = result['hits']['hits']
            field_names = [f"{res['_source']['name']} {res['_source']['desc']}" for res in result]
        else:
            field_names = []

        table_info = {
            'field_dsl': json.dumps(field_dsl, ensure_ascii=False, indent=4),
            'field_names': field_names
        }
        return table_info


if __name__ == '__main__':
    multi_es_recall = MultiESRecall()
    d = multi_es_recall.recall({})
    print(json.dumps(d, indent=4, ensure_ascii=False))
