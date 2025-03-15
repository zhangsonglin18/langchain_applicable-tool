# -*- coding: utf-8 -*-
import time
from zhipuai import ZhipuAI
import asyncio
api_key = "6dc1fa42ad476a65c4e8ecfe94f9a127.wMiPAp0X3Q089VS5"
# 创建ZhipuAI客户端实例
class ZhiPu:
    def __init__(self):
        self.client = ZhipuAI(api_key=api_key)

    ##获取同步调用api
    def get_zhipu_answer(self,question):
        response = self.client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "user", "content":question},
            ],
        )
        result = response.choices[0].message
        return result.content

    ##异步调用
    async def get_zhipu_answer_async(self,question):
        response = self.client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "user", "content":question},
            ],
            stream=True
        )
        if response:
            for chunk in response:
                content = chunk.choices[0].delta
                yield content

    def get_zhipu_answer_async_base(self,question):
        response = self.client.chat.asyncCompletions.create(
            model="glm-4",
            messages=[
                {"role": "user", "content":question},
            ],
        )
        return response.choices[0].message.content

    ##图片识别
    def image_answer(self,url):
        response = self.client.chat.completions.create(
            model="glm-4v",  # 填写需要调用的模型名称
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "图里有什么"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": url
                            }
                        }
                    ]
                }
            ]
        )
        return response.choices[0].message


if __name__ == '__main__':
    question = "写个诗"
    zhipu_api = ZhiPu()
    print(zhipu_api.get_zhipu_answer(question))




