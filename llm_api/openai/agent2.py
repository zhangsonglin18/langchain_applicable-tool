from langchain.agents import AgentType, initialize_agent
from langchain.tools import BaseTool, StructuredTool, Tool, tool, DuckDuckGoSearchRun
from langchain.tools.retriever import create_retriever_tool

from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.prompts import PromptTemplate
# %pip install --upgrade --quiet  wikipedia
import getpass
import os
from langchain.agents import load_tools
from config.configs import BaseConfig
import os
configs =BaseConfig()
os.environ["SERPAPI_API_KEY"] = configs.serpapi
from llm_api.openai_api import openai
llm = openai().chat_model()
os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'
# #  agentl + retriever_tool
# os.environ["TAVILY_API_KEY"] = getpass.getpass()
# os.environ["OPENAI_API_KEY"] = "sk-1AK***************"


# 实现机器人Tora执行各种任务的接口调用
# 1.tools
@tool("first_case", return_direct=True)
def tora_cap_water(input: str) -> str:
    """Tora 是一个人形智能机器人，可以帮助用户倒水"""
    print("*****************************************************执行水的检测和位姿估计")
    print("*****************************************************执行抓取水动作")
    print("*****************************************************执行人物的检测和位姿估计")
    print("*****************************************************执行递水动作")
    return "完成任务"


@tool("second_case", return_direct=True)
def tora_navigate(input: str) -> str:
    """Tora 是一个人形智能机器人，可以帮助用户带路"""
    print("*****************************************************执行定位")
    print("*****************************************************执行导航")
    return "完成任务"


@tool("third_case", return_direct=True)
def tora_talk(input: str) -> str:
    """Tora聊天机器人，用户会提各种问题，一些关键名词，tora会回答"""
    print("*****************************************************聊天")
    response = llm.invoke(input)
    return response


@tool("fourth_case", return_direct=True)
def tora_name(input: str) -> str:
    """当用户询问：你是谁，你叫什么等咨询agent身份信息的时候"""
    print("*****************************************************身份")
    return "我是paxini科技的人形智能机器人Tora"


# 本地知识库
loader = TextLoader("D:/llm/llm_4_doc_qa/files/dengyue.txt",encoding="utf-8")  # 文档读取
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)  # 分割 词P
embeddings = openai().embbeding_model()
vector = FAISS.from_documents(documents, embeddings)  # embedding 词2 数字
tora_local_retriever = vector.as_retriever()  # docs vector 2 retriever

# search = TavilySearchResults()
tora_retriever_tool = create_retriever_tool(  # retriever 2 tool
    tora_local_retriever,
    "paxini_search",
    "Search for information about paxini and tora. For any questions about paxini and tora, you must use this tool!",
    # 描述很重要
)

# search = TavilySearchResults()  # 网络搜索功能

# api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
# tool_wiki = WikipediaQueryRun(api_wrapper=api_wrapper)
search = load_tools(["serpapi"])
# llm = ChatOpenAI(temperature=0)
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
tools = [tora_navigate, tora_retriever_tool,  tora_cap_water,search, tora_name]
tools.append(tora_talk)
prompt_template = """  
请用中文回答
{input}  
"""
prompt_template = PromptTemplate.from_template(prompt_template)
agent2 = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    prompt=prompt_template,
)
# agentl.run("What is the Apple TV show Foundation about? Return the answer in all lower case")
# 把用户的prompt做一个优化：比如add 一个请用中文回答
# print("------------------------------1.聊天任务--------------------")
# resp = agent2.run("你是谁")
# print("…resp:", resp)  # 返回结果
# print("------------------------------1.取水任务--------------------")
# resp = agent2.run("Tora帮我拿瓶水")
# print("…resp:", resp)  # 返回结果
# print("------------------------------2.知识库问答任务--------------------")
# resp = agent2.run("你知道paxini吗？")  # 问答而非执行任务
# print("…resp:", resp)  # 返回结果
# print("------------------------------3.导航任务--------------------")
# resp = agent2.run("Tora可以带我去你们公司前台吗")
# print("…resp:", resp)  # 返回结果
print("------------------------------4.聊天任务--------------------")
resp = agent2.run("你知道特斯拉吗？")  # 问答而非执行任务
print("…resp:", resp)  # 返回结果
print("------------------------------5.取水任务--------------------")
agent2.run("我口渴怎么办")  # 知道在问tora,知道口渴 = 找水