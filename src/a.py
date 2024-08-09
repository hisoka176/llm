import os
import threading

from src.base import root_path
from src.query_parser import SQLQueryParser


def cutwords_handler():
    sql_query_parser = None

    def cutwords(question):
        global sql_query_parser
        if sql_query_parser is None:
            with threading.Lock():
                if sql_query_parser is None:
                    query_parser_json = os.path.join(root_path, 'resources/query_parser.json')
                    query_extend_yaml = os.path.join(root_path, 'resources/query_parser_offline/query_extend.yaml')
                    query_field_yaml = os.path.join(root_path, 'resources/query_parser_offline/query_entity.yaml')
                    stop_words = os.path.join(root_path, 'resources/stopwords.txt')
                    sql_query_parser = SQLQueryParser(query_parser_json, query_extend_yaml, query_field_yaml,
                                                      stop_words)

        return sql_query_parser.parser(question)

    return cutwords


print(cutwords_handler()("dau"))

# def hello():
#     msg = "hello"
#
#     def say():
#         print(f'{msg} world')
#
#     return say
#
#
# hello()()
