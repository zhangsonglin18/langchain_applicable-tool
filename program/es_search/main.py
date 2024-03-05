import re
import gradio as gr
from doc_search import ES
from llm_api.chatglm_llm import ChatLLM
from config.configs import ModelParams

PROMPT_TEMPLATE = """已知信息：
{context} 

根据上述已知信息，简洁和专业的来回答用户的问题。如果无法从中得到答案，请说 “根据已知信息无法回答该问题” 或 “没有提供足够的相关信息”，不允许在答案中添加编造成分，答案请使用中文。 问题是：{question}"""

model_config = ModelParams()
es = ES()
llm = ChatLLM()
llm.load_llm()

def clear_session():
    return '', [], ''

def search_doc(question, search_method, top_k, knn_boost, threshold):
    res = es.doc_search(method=search_method, query=question, top_k=top_k, knn_boost=knn_boost)
    if threshold > 0:
        result = [i for i in res if i['score'] > threshold]
    else:
        result = res
    return result


def doc_format(doc_list):
    result = ''
    for i in doc_list:
        source = re.sub('data/', '', i['source'])
        result += f"source: {source}\nscore: {i['score']}\ncontent: {i['content']}\n"
    return result


def predict(question, search_method, top_k, max_token, temperature, top_p, knn_boost, history, history_length,
            threshold):
    llm.max_token = max_token
    llm.temperature = temperature
    llm.top_p = top_p
    llm.history_len = history_length
    search_res = search_doc(question, search_method, top_k, knn_boost, threshold)
    search_result = doc_format(search_res)

    informed_context = ''
    for i in search_res:
        informed_context += i['content'] + '\n'
    prompt = PROMPT_TEMPLATE.replace("{question}", question).replace("{context}", informed_context)
    for answer_result in llm.generatorAnswer(prompt=prompt, history=history, streaming=True):
        history = answer_result.history
        history[-1][0] = question
        yield history, history, search_result, ""

if __name__ == '__main__':
    print("pass")
    print(llm.generatorAnswer(prompt="你是谁"))