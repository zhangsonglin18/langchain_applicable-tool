import os
from config.configs import BaseConfig
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from llm_api.openai_api import openai
llm = openai().chat_model()
configs =BaseConfig()
os.environ["SERPAPI_API_KEY"] = configs.serpapi
# 定义 tools
from langchain.agents import load_tools
tools = load_tools(["serpapi"])


# 工具加载后都需要初始化，verbose 参数为 True，会打印全部的执行详情
if __name__ == '__main__':
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    # 运行 agent
    agent.run("今天的日期是什么? 历史上的今天发生了什么大事?用中文回答")
