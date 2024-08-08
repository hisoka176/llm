import requests
import json


def create_conv(userid):
    # api_key = 'ragflow-RiYmM4MzhjM2Q5YjExZWZiZGQxMDI0Mm'
    api_key = 'ragflow-QwZTMxODkwNTRhMzExZWZhZTk3NDJjOT'
    url = 'http://rag.corpautohome.com/v1/api/new_conversation'
    headers = {
        "Content-Type": "application/json", "Authorization": "Bearer " + api_key
    }
    data = {"user_id": userid}
    response = requests.get(url=url, headers=headers, json=data)
    response_json = response.json()
    return response_json['data']['id']


def get_ragflow_answer(query, conversation_id='fd04499239e311ef80f500155d42b6f0'):
    # api_key = 'ragflow-RiYmM4MzhjM2Q5YjExZWZiZGQxMDI0Mm'
    api_key = 'ragflow-QwZTMxODkwNTRhMzExZWZhZTk3NDJjOT'

    url = 'http://rag.corpautohome.com/v1/api/completion'
    headers = {
        "Content-Type": "application/json", "Authorization": "Bearer " + api_key
    }
    data = {"conversation_id": conversation_id,'is_only_recall': True,
            "messages": [{'role': 'user', 'content': query}], "stream": False}
    print(json.dumps(data, ensure_ascii=False))
    response = requests.post(url=url, headers=headers, json=data)
    print(response)
    response_json = response.json()
    print(response_json)
    return response_json


if __name__ == '__main__':
    cvst_id = create_conv("363619322b1d11ef921f0242ac140006")
    get_ragflow_answer('宝马i3最新价格', cvst_id)
