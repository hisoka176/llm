import os.path
from typing import Dict, Any

from src.query_parser import QueryParser, SQLQueryParser
from src.recall import Recall, ESRecall, MultiESRecall
from src.build_prompt import BuildPrompt, ESBuildPrompt, MultiESBuildPrompt
from src.chat_model import ChatModel, KimiChatModel

root_path = os.path.dirname(__file__)
resource_path = os.path.join(root_path, 'resources')


class Flow(object):
    query_parser_handler: QueryParser = None
    recall_handler: Recall = None
    build_prompt_handler: BuildPrompt = None
    chat_model: ChatModel = None

    def __new__(cls, *args, **kwargs):
        cls.query_parser_handler = SQLQueryParser(filepath=os.path.join(root_path, 'resources/query_parser.json'))
        cls.recall_handler = MultiESRecall(index_name='bi_sql',
                                           filepath=os.path.join(root_path, 'resources/search.json'))
        cls.build_prompt_handler = MultiESBuildPrompt()
        cls.chat_model = KimiChatModel()
        object = super(Flow, cls).__new__(cls, *args, **kwargs)
        return object

    def __init__(self, *args, **kwargs):
        pass

    def flow(self, question) -> Dict[str, Any]:
        query_info = self.query_parser_handler.parser(question)
        recall_info = self.recall_handler.recall(query_info)
        prompt = self.build_prompt_handler.build(query_info, recall_info)
        chat_response = self.chat_model.chat(prompt, model='moonshot-v1-8k')

        response = {
            'question': question,
            'query_info': query_info,
            'recall_response': recall_info,
            'prompt': prompt,
            'chat_response': chat_response
        }
        from pprint import pp
        pp(response)
        # print(json.dumps(response, ensure_ascii=False, indent=4))
        return response


if __name__ == '__main__':
    pass
