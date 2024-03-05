import os
from langchain.llms import OpenAI
from config.configs import BaseConfig
from langchain.embeddings.openai import OpenAIEmbeddings
configs = BaseConfig()

class openai():
    def __init__(self):
        os.environ["OPENAI_API_KEY"] = configs.open_ai1

    def chat(self, prompt):
        llm = OpenAI(model_name="gpt-3.5-turbo-16k",base_url = "https://api.chatgptid.net/v1")
        return llm(prompt)

    def chat_model(self):
        llm = OpenAI(model_name="gpt-3.5-turbo-16k",base_url = "https://api.chatgptid.net/v1")
        return llm

    def embbeding_model(self):
        embeddings = OpenAIEmbeddings(base_url = "https://api.chatgptid.net/v1",
                                      embedding_model_name="text-embedding-ada-002",
                                      model_kwargs={"device": "cuda"},
                                      encode_kwargs={"device": "cuda"},)
        return embeddings

    def original_chat(self):
        client = OpenAI(
            base_url="https://api.chatgptid.net/v1",
            api_key=configs.open_ai1
        )
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello!"}
            ]
        )
        return completion

    def __call__(self,prompt):
        return self.chat(prompt)

if __name__ == '__main__':
    print(openai()(prompt = "你能帮我写一个Python脚本吗"))

