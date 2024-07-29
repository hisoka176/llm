from openai import OpenAI


class LLMModel(object):
    def __init__(self):
        history = [
            {"role": "system",
             "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"}
        ]
        self.history = history
        self.client = OpenAI(
            api_key="sk-1CXkvPbfEazTm8OlmRAfhW7ysz1awy1YXa5ECM4bimVp4Fa1",
            base_url="https://api.moonshot.cn/v1",
        )

    def chat(self, query, model='moonshot-v1-32k'):
        self.history.append({
            "role": "user",
            "content": query
        })
        completion = self.client.chat.completions.create(
            model=model,
            messages=self.history,
            temperature=0.0,
        )
        result = completion.choices[0].message.content
        # self.history.append({
        #     "role": "assistant",
        #     "content": result
        # })
        return result
