import json
import sys
import traceback

from elasticsearch import Elasticsearch
from pyspark.sql import SparkSession
import jieba
from pyspark.sql.functions import udf
from pyspark.sql import functions
from pyspark.sql.types import StringType, MapType

ss = SparkSession.builder.enableHiveSupport().getOrCreate()

df = ss.read.csv('hive.csv', header=True, escape='"')

df.show()


def text_normalize(text):
    text = text.lower()
    return text


@udf(returnType=StringType())
def cutwords(text):
    text = text_normalize(text)
    words = jieba.cut(text, cut_all=True)
    words = [word for word in words if word != '']
    words = ' '.join(words)
    return words


df = df.withColumn('tablecomment_ltks', cutwords(functions.col('tablecomment'))) \
    .withColumn('business_ltks', cutwords(functions.col('business'))) \
    .withColumn('tabledesc_ltks', cutwords(functions.col('tabledesc'))) \
    .withColumn('tablename_ltks', functions.col('tablename')) \
    .withColumn('columns_nst', functions.col('columns')) \
    .selectExpr('tablename_ltks',
                'tablename',
                'tablecomment_ltks',
                'tablecomment',
                'business_ltks',
                'business',
                'tabledesc_ltks',
                'tabledesc',
                'dbname',
                'columns_nst'
                ).cache()

df = df.withColumn('id', functions.concat_ws('.', functions.col('dbname'), functions.col('tablename')))
df.show(truncate=False)


def insert_data(index_name, datas):
    # es = Elasticsearch(hosts=['10.27.76.5:9200', '10.27.76.6:9200', '10.27.26.32:9200'])
    es = Elasticsearch(hosts='http://yz-rcm-es811.search.corpautohome.com:80', timeout=3000)
    for index, data in enumerate(datas):
        try:
            data = data.asDict()
            if index % 1000 == 0:
                print(f'index:{index} data:{data}', file=sys.stderr)
            data['columns_nst'] = json.loads(data['columns_nst'])
            es.index(index=index_name, id=data['id'], body=data)
        except:
            print(f'error:{json.dumps(data, ensure_ascii=False)}', file=sys.stderr)
            traceback.print_exc()


index_name = 'bi_sql'
df.rdd.foreachPartition(lambda datas: insert_data(index_name, datas))
