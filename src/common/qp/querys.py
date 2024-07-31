"""
query解析模块：
"""
import re
import jieba


class ExtraTableName(object):

    @staticmethod
    def extract(query, *args, **kwargs):
        regex = re.compile('adm[_0-9a-z]+|rdm[_0-9a-z]+|gdm[_0-9a-z]+|dim[_0-9a-z]+|fdm[_0-9a-z]+')
        return regex.findall(query)


class QueryParser(object):

    def __init__(self):
        pass

    def extra_table_name(self, query):
        return ExtraTableName.extract(query)

    def normalize(self, query: str):
        query = query.strip().lower()
        return query

    def cutwords(self, query):
        words = jieba.cut(query, cut_all=True)
        words = [word for word in words if word.strip() != '']
        return words

    def parser(self, query):
        query_normalize = self.normalize(query)
        words = self.cutwords(query_normalize)
        table_name = self.extra_table_name(query)
        return {
            'normalize': query_normalize,
            'words': words,
            'table_name': table_name
        }
