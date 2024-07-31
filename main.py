import os

dir = os.path.dirname(__file__)
os.environ['PYTHONPATH'] = f'$PYTHONPATH:{dir}'
print(os.environ['PYTHONPATH'])
import uvicorn
from fastapi import FastAPI
from src.common.llm.moonshot import LLMModel
from src.common.prompt.prompt import prompt_template, main_hive_table_context
from src.common.qp.querys import QueryParser
from src.dao.index.search import ESClient

app = FastAPI()

print(f'=====初始化====')

global_context = {}
qp = QueryParser()
es_client = ESClient()
global_context['qp'] = qp
global_context['es_client'] = es_client
global_context['llm'] = LLMModel()


@app.get('/test')
async def hello():
    return {
        "message": "hello world"
    }


@app.get(path='/table')
async def get_hive_table(question: str):
    qp: QueryParser = global_context['qp']
    es_client: ESClient = global_context['es_client']
    qp_info = qp.parser(question)

    results = es_client.search('bi_sql', ' '.join(qp_info['words']))
    response = {
        'query': question,
        'qp': qp_info,
        'results': results
    }
    return response


@app.get(path='/metric')
async def qa(question: str):
    llm: LLMModel = global_context['llm']
    prompt = prompt_template.format(context=main_hive_table_context, question=question)
    answer = llm.chat(prompt)
    response = {
        'question': question,
        'answer': answer
    }
    return response


@app.get(path='/bisql')
async def build_sql(question: str):
    response = {}
    qp: QueryParser = global_context['qp']
    es_client: ESClient = global_context['es_client']
    qp_info = qp.parser(question)

    results = es_client.search('bi_sql', ' '.join(qp_info['words']))
    context = {
        'query': question,
        'qp': qp,
        'context': results
    }
    prompt = prompt_template.format(context=context['context'], question=question)
    llm: LLMModel = global_context['llm']
    answer = llm.chat(prompt)
    response['question'] = question
    response['prompt'] = prompt
    response['answer'] = answer
    return response


if __name__ == '__main__':
    uvicorn.run(app="main:app", host="localhost", port=8000, reload=True)
