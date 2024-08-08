import os

from src.base import Flow

dir = os.path.dirname(__file__)
os.environ['PYTHONPATH'] = f'$PYTHONPATH:{dir}'
print(os.environ['PYTHONPATH'])
import uvicorn
from fastapi import FastAPI

app = FastAPI()

print(f'=====初始化====')

flow = Flow()


@app.get('/')
async def flow_process(question: str):
    response = flow.flow(question=question)
    return response


if __name__ == '__main__':
    uvicorn.run(app="main:app", host="localhost", port=8000, reload=True)
