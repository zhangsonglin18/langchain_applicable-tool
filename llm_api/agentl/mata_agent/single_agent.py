import os
from config.configs import BaseConfig
import asyncio
from metagpt.roles.di.data_interpreter import DataInterpreter

# configs =BaseConfig()
# os.environ["SERPAPI_API_KEY"] = configs.serpapi
# os.environ["OPENAI_API_KEY"] = configs.open_ai1
# os.environ["OPENAI_API_MODEL"] = "gpt-3.5-turbo-16k" # 选择你要使用的模型，例如：gpt-4, gpt-3.5-turbo
# os.environ["OPENAI_API_BASE"] = "https://api.chatgptid.net/v1"
async def main():
    di = DataInterpreter()
    await di.run("Run data analysis on sklearn Iris dataset, include a plot")

asyncio.run(main())  # or await main() in a jupyter notebook setting