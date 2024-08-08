import os
from abc import ABC


class BuildPrompt(ABC):

    def build(self, question_info, recall_response) -> str:
        pass


class ESBuildPrompt(BuildPrompt):

    def __init__(self):
        self.top_k = 2
        self.prompt_template = \
            '''你现在是一个hive sql的专家，给你一些数据表的结构，以及想要查询的指标名称，你从中挑选有用的数据表，给出对应的sql逻辑，并解释原因
上下文：{context}
问题：{question}'''

    def build(self, question_info, recall_response) -> str:
        context = self.select_table_field(question_info, recall_response)
        prompt = self.prompt_template.format(context=context, question=question_info['question'])
        return prompt

    def select_table_field(self, question_info, recall_info):
        # 表拿出来
        # 去掉维度字段
        # 拿出指标字段
        results = recall_info['results']
        assert 'hits' in results, 'result is empty'
        hits = results['hits']
        assert 'hits' in hits, 'hits is empty'
        hits = hits['hits'][:self.top_k]

        table_string = ''
        dim_words = question_info['dim_words']
        metric_words = question_info['metric_words']
        for hit in hits:
            assert '_source' in hit, 'keyerror _source'
            source = hit['_source']
            # dbname = source['dbname']
            tablename = source['tablename']
            tablecomment = source['tablecomment']
            # table_name = f'{dbname}.{tablename}'
            table_name = f'{tablename}'
            fields = []
            for column in source['columns_nst']:
                match column['category']:
                    case 'dim':
                        pass
                    case 'metric':
                        pass
                for word in dim_words:
                    if word in column['desc']:
                        break
                if column['category'] == 'dim' or column.get('status', 1) == 0:
                    continue
                name = column['name']
                comment = column['comment']
                string = f'{name} {comment}'
                fields.append(string)
            field_string = '\n'.join(fields)
            table_string += f'==== hive表：{table_name} 表注释:{tablecomment}====\n'
            table_string += field_string
            table_string += "\n"
        table_string += '========'
        return table_string


class MultiESBuildPrompt(BuildPrompt):

    def __init__(self):
        pass

    def build(self, question_info, recall_response) -> str:
        table_info = recall_response['table_info']
        field_info = recall_response['field_info']
        table = "" if len(table_info['table_names']) < 1 else table_info['table_names'][0]
        field = "" if len(table_info['table_names']) < 1 else os.linesep.join(field_info["field_names"])
        context = f'''====hive表:{table} ====
{field}
========
'''
        prompt = f'''你现在是一个hive sql的专家，给你一些数据表的结构，以及想要查询的指标名称，你从中挑选有用的数据表，给出对应的sql逻辑，并解释原因
上下文：{context}
问题：{question_info['question']}
                    '''
        return prompt
