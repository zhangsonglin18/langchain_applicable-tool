import openai
# 设置api_base
openai.api_key = "111" #不可为空，为空会报错
openai.api_base = "http://127.0.0.1:11434/v1"
# 2. 设置提示词
prompt = """
You: 今天天气如何?

"""

# 3.调用（可切换模型）
# resp = openai.ChatCompletion.create(model="llama2", messages=[{"role": "user", "content": prompt}], stream = False)
resp = openai.ChatCompletion.create(model="qwen:7b", messages=[{"role": "user", "content": prompt}], stream = False)
# resp = openai.ChatCompletion.create(model="gemma:7b", messages=[{"role": "user", "content": prompt}], stream = False)

# 4.输出
print(resp.choices[0].message.content)

