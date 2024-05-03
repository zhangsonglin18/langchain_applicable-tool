from langchain.agents import tool, AgentType, initialize_agent, load_tools
from datetime import date
# from YiYan import YiYan
import os
from config.configs import BaseConfig
configs =BaseConfig()
os.environ["SERPAPI_API_KEY"] = configs.serpapi
from llm_api.openai_api import openai
llm = openai().chat_model()

tools = load_tools(["llm-math", "wikipedia"], llm=llm)

@tool
def time(text: str) -> str:
    """
    Returns todays date, use this for any \
    questions related to knowing todays date. \
    The input should always be an empty string, \
    and this function will always return todays \
    date - any date mathmatics should occur \
    outside this function.
    """
    return str(date.today())


@tool
def sumarize(text: str) -> str:
    """
    Extract the key event information in the given text, the event information can represent the core content,
    input a piece of text, output its summary information,
    and do not call the function for other capabilities of summary extraction
    """
    prompt = "抽取给出事件文本中的关键信息，这些信息可以代表核心内容，输入一段文本，输出其摘要信息，不要调用该函数实现摘要抽取之外的其他功能，其中抽取的文本信息为：\n\n" + text + "\n\n其中抽取的摘要信息为："
    return openai().chat(prompt)
@tool
def translate(text: str) -> str:
    """
    Translate the given text into English and get the summary analysis result, input as Chinese text, output as English text
    do not call the function to implement functions other than digest extraction
    """
    prompt = f"""
    1-用一句话概括下面用<>括起来的文本。
    2-将摘要翻译成英语。
    3-在英语摘要中列出每个名称。
    4-输出一个 JSON 对象，其中包含以下键：English_summary，num_names。
    请使用以下格式：
    摘要：<摘要>
    翻译：<摘要的翻译>
    名称：<英语摘要中的名称列表>
    输出 JSON 格式：<带有 English_summary 和 num_names 的 JSON 格式>
    Text: <{text}>
    """
    return openai().chat(prompt)

@tool
def text_large(text: str) -> str:
    """
    Please write a continuation text information according to the given input, the content of the continuation should be vivid, smooth and coherent, and the subject of the continuation should be consistent with the given text, the function supports input a text message,
    output a continuation of the text information, do not call the function to achieve the function of text continuation.
    """
    prompt = "请根据给定输入续写文本信息，续写的内容应该生动、通顺、连贯，并且续写的主题应该与给定的文本一致，该函数支持输入一段文本信息，输出一段续写的文本信息，不要调用该函数实现文本续之外功能。，其中输入的文本信息为：\n\n" + text + "\n\n其中输出的续写内容为："
    return openai().chat(prompt)


agent = initialize_agent(
    tools + [time] + [sumarize] + [text_large] + [translate], llm, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

agent("给出下述文本：据俄罗斯《消息报》网站4月20日报道，俄军20日全线向乌军阵地发射炮弹，以悼念在特别军事行动中牺牲的俄罗斯《消息报》战地记者谢苗·叶廖明。"
      "报道称，20日早些时候，《消息报》网站播放了炮兵作战的镜头。先是装填弹药，弹壳上写着“为了谢苗”。此后，俄军战士向乌军阵地开火。发射完成后，监控视频确认目标被击中。"
      "首先，请对上述文本进行摘要，然后将摘要进行扩写，最后进行翻译。")