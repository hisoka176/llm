from src.llm.moonshot import LLMModel
from src.prompt.prompt import indicator_template

question = '次留如何计算'

inputs = indicator_template.format(question=question)

moonshot = LLMModel()
# outputs = moonshot.chat(inputs)
# print(outputs)
