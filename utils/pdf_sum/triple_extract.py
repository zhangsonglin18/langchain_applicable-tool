from langchain.indexes import GraphIndexCreator
from langchain.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader, SeleniumURLLoader
from langchain.llms import OpenAI
from llm_api.openai_api import openai
llm = openai().chat_model()
# llm = TransformersLLM.from_model_id(
#     model_id="lmsys/vicuna-7b-v1.5",
#     model_kwargs={"temperature": 0, "max_length": 1024, "trust_remote_code": True},
# )
with open("D:\\langchain_applicable-doc\\files\\yayun.txt",encoding="utf-8") as f:
    all_text = f.read()
text = "\n".join(all_text.split("\n\n"))
# print(text)
# text = "据俄罗斯军事工业综合体网站2022年8月21日报道，俄罗斯军队在乌克兰战场上缴获了多套M777榴弹炮、“海马斯”多管火箭炮、“标枪”反坦克导弹、“毒刺”便携式防空导弹、小型武器和装甲车等美国和西方对乌军援武器。俄罗斯国防部正组织力量对这些武器开展系统研究，在掌握对抗和反击的方法的同时，寻找这些武器可能存在的弱点和缺陷。"
index_creator = GraphIndexCreator(llm=llm)
graph = index_creator.from_text(text)
print(graph.get_triples())

from langchain.chains import GraphQAChain

chain = GraphQAChain.from_llm(llm, graph=graph, verbose=True)
chain.run("杭州亚运村总占地面积?")

graph.write_to_gml("graph.gml")
from langchain.indexes.graph import NetworkxEntityGraph
loaded_graph = NetworkxEntityGraph.from_gml("graph.gml")
loaded_graph.get_triples()
# [('Intel', '$20 billion semiconductor "mega site"', 'is going to build'),
#  ('Intel', 'state-of-the-art factories', 'is building'),
#  ('Intel', '10,000 new good-paying jobs', 'is creating'),
#  ('Intel', 'Silicon Valley', 'is helping build'),
#  ('Field of dreams',
#   "America's future will be built",
#   'is the ground on which')]
from langchain.prompts import PromptTemplate,ChatPromptTemplate,SystemMessagePromptTemplate
from langchain.prompts.example_selector import LengthBasedExampleSelector,NGramOverlapExampleSelector

