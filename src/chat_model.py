from abc import ABC

from openai import OpenAI


class ChatModel(ABC):

    def chat(self, prompt, model='moonshot-v1-32k') -> str:
        pass


class KimiChatModel(ChatModel):
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

    def chat(self, prompt, model='moonshot-v1-32k'):
        history = [
            {"role": "system",
             "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"}
        ]
        history.append({
            "role": "user",
            "content": prompt
        })
        completion = self.client.chat.completions.create(
            model=model,
            messages=history,
            temperature=0.0,
        )
        result = completion.choices[0].message.content

        return result


if __name__ == '__main__':
    chat_model = KimiChatModel()
    prompt = f'''你现在是一个hive sql的专家，给你一些数据表的结构，以及想要查询的指标名称，你从中挑选有用的数据表，给出对应的sql逻辑，对于问题中没有提到的筛选条件，sql不能带上
====表名为：adm_anaflw_app_device_visit_di:
====表中的筛选字段有：
app_key  APP标识符 枚举值：auto_android代表主软件Android端,auto_iphone代表主软件iOS端,che_ios代表二手车iOS端,che_android代表二手车Android端,price_android代表报价Android端,ics_android代表爱车商Android端,ics_ios代表爱车商iOS端,price_ios代表报价iOS端,autospeed_android代表极速版Android端,explore_auto_iphone代表主软件探索版iOS端,autospeed_ios代表极速版iOS端,auto_ipad代表主软件ipad端,wz_android代表违章查询Android端,auto_harmony代表主软件harmony端即主软鸿蒙端,wz_ios代表违章查询iOS端,testdrive_ios代表试驾仪iOS端,vixrapp_ios代表销冠神器iOS端,vixrapp_android代表销冠神器Android端
soft_id  软件标识符 auto代表主软件， che代表二手车， price代表报价， ics代表爱车商， czyp代表车智赢， autospeed代表极速版app， wz代表违章查询， ahoh代表汽车之家能源空间站销售助手平台，vixrapp代表销冠神器， testdrive代表试驾仪， carcomment代表汽车点评， ark代表全息端， svideo代表新视频，mall代表车商城， hc代表嘿car， club代表论坛
channel_package 渠道，渠道包名 渠道包,渠道,渠道包名
is_new_user 是否新用户 标识是否新用户，1代表新用户，0代表老用户
channel_clean_flag 是否渠道排水黑名单用户 标识是否是渠道排水黑名单用户，1代表是，0代表否
l2_clean_flag  是否L2排水黑名单用户 标识是否是L2排水黑名单用户，1代表是，0代表否
device_type 启动用户分类 用户类型，1代表唤醒仅启，2代表PUSH仅启，3代表主启
====统计字段有：
pv PV, 浏览量，浏览页面个数  PV, pv，浏览页面个数
duration  时长，访问时长
visits_num  访次数
device_id 设备id
====分区字段有：
dt 日期 格式为yyyy-MM-dd
====
问题：二手车dau
'''
    ans = chat_model.chat(prompt)
    print(ans)
