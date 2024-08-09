import json
import sys
import traceback
from typing import List
import argparse

import jieba
from elasticsearch import Elasticsearch
from pyspark.sql import SparkSession, functions as F, DataFrame
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

from src.base import root_path

stop_words = set()
with open('../resources/stopwords.txt') as f:
    for line in f:
        line = line.rstrip('\n').rstrip('\r')
        stop_words.add(line)
print('stopword:', len(stop_words))


def cutwords(question):
    if question is None:
        return ''
    jieba.load_userdict('../resources/query_parser_offline/words.txt')
    words = [word for word in jieba.cut(question, cut_all=True) if word not in stop_words and len(word) > 1]
    return ' '.join(words)


def load_filepaths(ss: SparkSession, filepaths: List[str], sheet_names: List[str]):
    data = None
    for sheet_name, filepath in zip(sheet_names, filepaths):
        tmp = ss.read.format("com.crealytics.spark.excel") \
            .option("dataAddress", sheet_name) \
            .option("header", "true") \
            .option("treatEmptyValuesAsNulls", "false") \
            .option("inferSchema", "true") \
            .option("addColorColumns", "false") \
            .option("timestampFormat", "MM-dd-yyyy HH:mm:ss") \
            .option("maxRowsInMemory", 20) \
            .load(filepath)

        data = tmp if not data else data.unionAll(tmp)
    data.show(truncate=False)
    ##
    data = data.withColumn('tabletopic', F.col('主题')) \
        .withColumn('tablename', F.col('表名')) \
        .withColumn('tablecomment', F.lower(F.col('表中文名'))) \
        .withColumn('tabledesc', F.lower(F.col('表标签描述'))) \
        .withColumn('name', F.col('字段')) \
        .withColumn('comment', F.lower(F.col('字段中文名'))) \
        .withColumn('alias', F.lower(F.col('字段别名'))) \
        .withColumn('category', F.col('类型')) \
        .withColumn('desc', F.lower(F.col('指标/枚举')))
    # .withColumn('caculation', F.col('计算方式'))

    data.registerTempTable('temp')
    sql = f'''

    select 
        concat_ws('-',tablename, name) as id,
        tabletopic,
        tablename,
        tablecomment,
        cutwords(tablecomment) as tablecomment_tks,
        cutwords(tabledesc) as tabledesc_tks,
        name,
        comment, 
        cutwords(comment) as comment_tks, 
        alias, 
        cutwords(alias) as alias_tks,
        category, 
        desc, 
        cutwords(desc) as desc_tks
    from temp

    '''
    data = ss.sql(sql)
    data.show(truncate=False)

    return data


def delete_all_es_data():
    es = Elasticsearch(hosts='http://yz-rcm-es811.search.corpautohome.com:80')
    index_name = 'bi_sql'
    cnt_dsl = {
        'query': {
            'match_all': {}
        }
    }
    print(f'es count dsl:{cnt_dsl}')
    if es.count(index=index_name, body=cnt_dsl)['count'] > 1:
        res = es.delete_by_query(index=index_name, body=cnt_dsl, wait_for_completion=True)
        print(f'delete {index_name} data:{res}')


def insert_es(df: DataFrame):
    # es = Elasticsearch(hosts=['10.27.76.5:9200', '10.27.76.6:9200', '10.27.26.32:9200'])
    def process(index_name, datas):
        es = Elasticsearch(hosts='http://yz-rcm-es811.search.corpautohome.com:80')
        for index, data in enumerate(datas):
            try:
                data = data.asDict()
                if index % 1000 == 0:
                    print(f'index:{index} data:{data}', file=sys.stderr)
                # data['columns_nst'] = json.loads(data['columns_nst'])
                es.index(index=index_name, id=data['id'], body=data)
            except:
                print(f'error:{json.dumps(data, ensure_ascii=False)}', file=sys.stderr)
                traceback.print_exc()

    df.rdd.repartition(10).foreachPartition(lambda datas: process('bi_sql', datas))


# def insert_es(df: DataFrame):
#     # .option("es.net.http.auth.user", "") \
#     # .option("es.net.http.auth.pass", "") \
#     df.write \
#         .format('org.elasticsearch.spark.sql') \
#         .option("spark.es.nodes", 'http://yz-rcm-es811.search.corpautohome.com') \
#         .option("spark.es.port", '80') \
#         .option('es.resource', 'bi_sql') \
#         .option("es.mapping.id", "id") \
#         .option("es.nodes.wan.only", "true").save()


def main(args):
    ss = SparkSession.builder \
        .config('spark.default.parallelism', 32) \
        .config('spark.sql.shuffle.partitions', 32) \
        .config('spark.jars',
                'spark-excel_2.12-3.4.1_0.20.3.jar,elasticsearch-spark-30_2.12-8.11.1.jar') \
        .config('spark.executor.extraClassPath',
                'spark-excel_2.12-3.4.1_0.20.3.jar:elasticsearch-spark-30_2.12-8.11.1.jar') \
        .config('spark.driver.extraClassPath',
                'spark-excel_2.12-3.4.1_0.20.3.jar:elasticsearch-spark-30_2.12-8.11.1.jar') \
        .enableHiveSupport().getOrCreate()
    ss.udf.register('cutwords', cutwords, returnType=StringType())

    data = load_filepaths(ss, args.filepaths, args.sheet_names)
    if args.mode == 'overwrite':
        delete_all_es_data()
    insert_es(data)
    # insert_es(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepaths', type=str, nargs='+', default=['问表知识库-0731.xlsx'])
    parser.add_argument('--sheet_names', type=str, nargs='+', default=['Sheet1'])
    parser.add_argument('--mode', choices=['append', 'overwrite'], default='overwrite')
    args = parser.parse_args()
    main(args)
