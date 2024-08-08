import json
import sys
import traceback

from elasticsearch import Elasticsearch

from src.config import load_yaml


def insert_data(index_name, datas):
    # es = Elasticsearch(hosts=['10.27.76.5:9200', '10.27.76.6:9200', '10.27.26.32:9200'])
    es = Elasticsearch(hosts='http://yz-rcm-es811.search.corpautohome.com:80', timeout=3000)
    for index, data in enumerate(datas):
        try:
            # data = data.asDict()
            if index % 1000 == 0:
                print(f'index:{index} data:{data}', file=sys.stderr)
            print('hisoka', data)
            # data['columns_nst'] = json.loads(data['columns_nst'])
            es.index(index=index_name, id=data['tablename'], body=data)
        except:
            print(f'error:{json.dumps(data, ensure_ascii=False)}', file=sys.stderr)
            traceback.print_exc()


if __name__ == '__main__':
    index_name = 'bi_sql'
    data = load_yaml('offline/es/data.yaml')
    print('pp', data)
    insert_data(index_name, data)
