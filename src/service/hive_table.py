from src.common.qp.querys import QueryParser
from src.dao.index.search import ESClient


def get_hive_table_by_query(self, query, es_client: ESClient, qp: QueryParser):
    query_info = qp.parser(query)
    results = es_client.search('bi_sql', ' '.join(query_info['words']))
    return results
