from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
from config.configs import BaseConfig
import os
from langchain.agents import create_react_agent
from langchain.agents import AgentExecutor
from langchain.agents import initialize_agent
from llm_api.openai_api import openai
from langchain.agents import load_tools
from llm_api.agentl.langchain_agentl.agent_tools import weekday
from llm_api.agentl.langchain_agentl.agent_prompt import prompt
configs =BaseConfig()
os.environ["SERPAPI_API_KEY"] = configs.serpapi
llm = openai().chat_model()
# 定义 tools
tools = load_tools(["serpapi"])
tools += [weekday] ## 将自定义的tool添加到tools数组中
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
agent_executor.invoke({"input": "周杰伦生日那天是星期几"})
# agent = initialize_agent(tools, llm, verbose=True,handle_parsing_errors=True)
# # 运行 agent
# agent.run("今天的日期是什么? 历史上的今天发生了什么大事?用中文回答")
