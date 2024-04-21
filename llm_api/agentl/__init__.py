from config.configs import BaseConfig
import os
configs =BaseConfig()
os.environ["SERPAPI_API_KEY"] = configs.serpapi
from llm_api.openai_api import openai
llm = openai().chat_model()