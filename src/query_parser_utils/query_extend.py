import os.path
from collections import defaultdict

from src.config import load_yaml


class QueryExtend(object):
    def __init__(self, filepath):
        assert os.path.exists(filepath), 'filepath not exists'
        mapping = load_yaml(filepath)
        # self.mapping = mapping
        self.prepare(mapping)

    def prepare(self, mapping):
        reverse_mapping = defaultdict(set)
        forward_mapping = defaultdict(set)
        for key, value in mapping.items():
            forward_mapping[key.lower()] = set([v.lower() for v in value])
            for v in value:
                reverse_mapping[v.lower()].add(key.lower())

        self.reverse_mapping = reverse_mapping
        self.forward_mapping = forward_mapping
        # print(self.reverse_mapping)
        # print(self.forward_mapping)

    def extend_question(self, question_words):
        result = defaultdict(list)
        for word in question_words:
            extend_word = self.reverse_mapping.get(word, set())
            if extend_word:
                result[word].extend(list(extend_word))

            extend_word = self.forward_mapping.get(word, set())
            if extend_word:
                result[word].extend(list(extend_word))

        return dict(result)


if __name__ == '__main__':
    a = QueryExtend('../resources/query_parser_offline/query_extend.yaml')
    print(a.extend_question(['三端']))
