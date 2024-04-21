from langchain import LLMMathChain, SerpAPIWrapper
from langchain.agents import AgentType, initialize_agent
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from config.configs import BaseConfig
import os
configs =BaseConfig()
os.environ["SERPAPI_API_KEY"] = configs.serpapi
from llm_api.openai_api import openai
llm = openai().chat_model()
# Load the tool configs that are needed.
search = SerpAPIWrapper()
llm_math_chain = LLMMathChain(llm=llm, verbose=True)
tools = [
    Tool.from_function(
        func=search.run,
        name = "Search",
        description="useful for when you need to answer questions about current events"
        # coroutine= ... <- you can specify an async method if desired as well
    ),
]
from pydantic import BaseModel, Field
class CalculatorInput(BaseModel):
    question: str = Field()

tools.append(
    Tool.from_function(
        func=llm_math_chain.run,
        name="Calculator",
        description="useful for when you need to answer questions about math",
        # args_schema=CalculatorInput
        # coroutine= ... <- you can specify an async method if desired as well
    )
)
# Construct the agent. We will use the default agent type here.
# See documentation for a full list of options.
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,verbose=True)
agent.run("用中文回答：Leonardo DiCaprio的女朋友是谁？她现在的年龄提高到0.43次方是多少？")
