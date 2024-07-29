from fastapi import FastAPI
import uvicorn

from src.llm.moonshot import LLMModel
from src.prompt.prompt import indicator_template

app = FastAPI()

moonshot = LLMModel()


@app.get("/v1/")
def read_item(question: str):
    inputs = indicator_template.format(question=question)
    print(inputs)
    answer = moonshot.chat(inputs)
    return {'question': question, 'answer': answer}


if __name__ == '__main__':
    uvicorn.run(app='main:app',host='0.0.0.0', port=8000)
