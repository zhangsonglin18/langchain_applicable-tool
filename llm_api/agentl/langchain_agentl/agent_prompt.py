from langchain import hub
import json
# 下载一个现有的 Prompt 模板
# from langchain import hub
# import json
# # 下载一个现有的 Prompt 模板
# prompt = hub.pull("hwchase17/react")
# print(prompt.template)

from langchain_core.prompts import ChatPromptTemplate
prompt_template = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action，如果其中有日期，请确保只输入日期，格式为:YYYY-MM-DD，不要有任何其它字符
Observation: the result of the action，如果其中有日期，请确保输出的日期格式为:YYYY-MM-DD，不要有任何其它字符
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin! Let's think step by step. Take a deep breath.

Question: {input}
Thought:{agent_scratchpad}
"""
prompt = ChatPromptTemplate.from_template(prompt_template)

prompt = hub.pull("hwchase17/react")
print(prompt.template)
