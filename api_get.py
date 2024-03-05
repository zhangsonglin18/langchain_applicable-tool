import requests
import json
from flask import request

def get_embedding(text):
    url = "http://127.0.0.1:5000/emd//get_embeding"  # 替换为真正的API地址
    params1 = {"text":text}# 替换为真正的参数值
    headers = {"content-type":"application/json"}
    response = requests.post(url,data=json.dumps(params1),headers=headers)  # GET请求示例
    # response = requests.post(url, data=data)      # POST请求示例
    if response.status_code == 200:
        data = response.json()
    else:
        print("Request failed with status code", response.status_code)
    return data['data']

if __name__ == '__main__':
    print(get_embedding("Hello, world!"))
