# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

client = OpenAI(api_key="sk-de3d39dbb82e4d1b9635412451a2b97b-1", base_url="https://api.deepseek.com")
text = '今天星期几'
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": text},
    ],
    stream=False
)

print(response.choices[0].message.content)