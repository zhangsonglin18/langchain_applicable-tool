from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import Ollama

prompt_template = "请给制作 {product} 的公司起个名字,只回答公司名即可"

ollama_llm = Ollama(model="qwen:7b")
llm_chain = LLMChain(
    llm = ollama_llm,
    prompt = PromptTemplate.from_template(prompt_template)
)
print(llm_chain("书店"))
# print(llm_chain.run("袜子"))    # 加个.run也可
