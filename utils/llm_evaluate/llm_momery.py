from llm_api.openai_api import openai
llm = openai().chat_model()
from langchain.memory import ConversationTokenBufferMemory
memory = ConversationTokenBufferMemory(llm=llm,max_token_limit=1000,memory_key="session_chat")
# print(memory.save_context({"input":"你是谁"},outputs={"output":"我是你的助手"}))
# print(memory.load_memory_variables({}))
print(memory.chat_memory.add_user_message("你好"))


from langchain.callbacks import StdOutCallbackHandler
from langchain.chains import
