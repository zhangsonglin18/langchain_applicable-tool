import ollama
from langchain.llms.base import LLM
import asyncio
from ollama import AsyncClient
from ollama import Client
class ollama_model:
    def __init__(self,model="qwen:7b"):
        self.url = "http://127.0.0.1:11434/v1"
        self.model = model

    def generate_chat(self,content):
        response = ollama.chat(model='llama3', messages=[
          {
            'role': 'user',
            'content': content,
          },
        ])
        return response['message']['content']

    def stream_chat(self,content):
        stream = ollama.chat(
            model='qwen:7b',
            messages=[{'role': 'user', 'content': content}],
            stream=True,
        )

        for chunk in stream:
          return chunk['message']['content']
        
    def url_chat(self,content):
        client = Client(host=self.url)
        response = client.chat(model='llama3', messages=[
            {
                'role': 'user',
                'content': content,
            },
        ])
        return response['message']['content']

    async def chat(self,content):
        message = {'role': 'user', 'content': content}
        response = await AsyncClient().chat(model=self.model, messages=[message])
        return response['message']['content']

    def __call__(self, prompt):
        return asyncio.run(self.chat(prompt))

if __name__ == '__main__':
    print(ollama_model()(prompt = "你能帮我写一个Python脚本吗"))







