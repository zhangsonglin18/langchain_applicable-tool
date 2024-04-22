from langchain.agents import AgentType, initialize_agent
from langchain.tools import BaseTool
from config.configs import BaseConfig
import os
configs =BaseConfig()
os.environ["SERPAPI_API_KEY"] = configs.serpapi
from llm_api.openai_api import openai
llm = openai().chat_model()

class douban(BaseTool):
    name = "Douban Movie"
    description = "当需要查询热播电影时使用该工具。返回为电影名称。"
    def _run(self, query: str) -> str:
        # 中间交互过程省略，直接返回结果
        return "星际穿越"
    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")


class taopp(BaseTool):
    name = "TaoPiaoPiao"
    description = "当需要购买电影票时使用该工具。输入必需为电影名称。"
    def _run(self, query: str) -> str:
        # 中间交互过程省略，直接返回结果
        return "购买成功。"
    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")

agent = initialize_agent([douban(), taopp()], llm, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

res = agent("帮我买张最近的热播电影票")
print(res)