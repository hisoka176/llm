import elasticsearch
import jieba
from elasticsearch import Elasticsearch


class ESClient(object):

    def __init__(self):
        self.client = Elasticsearch(hosts='http://yz-rcm-es811.search.corpautohome.com:80')
        if not self.client.ping():
            raise Exception('es connection build failure')
        self.topK = 3

    def search(self, index_name, query: str):
        dsl = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": [
                        "tablename_ltks^3.0",
                        "tablecomment_ltks^1.5",
                        "business_ltks^0.5",
                        "tabledesc_ltks^1.0"
                    ],
                    "type": "best_fields",
                    "operator": "OR",
                    "slop": 0,
                    "prefix_length": 0,
                    "max_expansions": 50,
                    "minimum_should_match": "60%",
                    "auto_generate_synonyms_phrase_query": True
                }
            },
            "_source": {
                "includes": ["tablecomment",
                             "tablecomment",
                             "business",
                             "tabledesc",
                             "columns_nst",
                             "dbname",
                             "tablename"],
                "excludes": []
            }
        }
        data = self.client.search(index=index_name, body=dsl).body
        results = self.build_result(data)
        return results

    def build_result(self, result):
        if not result or len(result['hits']) == 0:
            return []
        hits = result['hits']['hits']

        results = []
        for hit_info in hits[0:self.topK]:
            hit = hit_info['_source']
            table_column = self.wrapper(hit['columns_nst'])
            hit['columns_nst'] = table_column
            results.append(hit)
        context = self.build_context(results)
        return context

    def wrapper(self, columns_nst):
        results = []
        for col in columns_nst:
            row = f'{col["name"]} {col["type"]} {col["comment"]}'
            results.append(row)
        return '\n'.join(results)

    def build_context(self, results):
        context = ""
        for result in results:
            string = f'''====hive表:{result["dbname"]}.{result["tablename"]} #### 表注释：{result["tablecomment"]}#### 表描述：{result["tabledesc"]}====
{result["columns_nst"]}\n'''
            context += string
        context += "========"
        return context
