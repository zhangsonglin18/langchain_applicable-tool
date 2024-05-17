# %%
import os
import random
from http import HTTPStatus


# %%

ali_api_key = os.environ.get("ALI_API_KEY", None)
# qwen_model = "qwen1.5-7b-chat"
qwen_model = "qwen-max"
# qwen_model = "qwen1.5-14b-chat"
# qwen_model="qwen1.5-72b-chat"
def chatLLM(
    messages: list,
    stream=False,
    temperature=0.85,
    top_p=0.8,
) -> dict:
    import openai
    openai.api_base = "http://localhost:8000/v1"
    openai.api_key = "none"
    if not stream:
        response = openai.ChatCompletion.create(
            model="Qwen",
            messages=messages)
        return {"content":response.choices[0].message.content,"total_tokens": 10}
    else:
    # 使用流式回复的请求
        def respGenerator():
            content = ""
            for chunk in openai.ChatCompletion.create(
                    model="Qwen",
                    messages=messages,
                    stream=stream
                    # 流式输出的自定义stopwords功能尚未支持，正在开发中
            ):
                content += chunk.choices[0].delta.content
                yield {
                        "content": content,
                        "total_tokens": 10,
                    }
        return respGenerator()


# %%

if __name__ == "__main__":
    content = "请用一个成语介绍你自己"
    messages = [{"role": "user", "content": content}]
    resp = chatLLM(messages)
    print(resp)
    for resp in chatLLM(messages, stream=False):
        print(resp)
