from langchain.document_loaders import PyPDFLoader, UnstructuredFileLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
import os
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chains import RetrievalQAWithSourcesChain
embedding = HuggingFaceEmbeddings(model_name="D:\\model\\m3e")
from llm_api.openai_api import openai
llm = openai().chat_model()
def transfor_vector(file_name):
    file_path = os.path.join("D:\\model\\data_set\\tianya-docs-main\\docs\\",file_name)
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
    docs = text_splitter.split_documents(docs)
    # 构造向量库+conversation_id
    persist_directory = os.path.join("D:\\langchain_applicable-doc\\voc\\",file_name +"\\")
    # # 创建向量数据库
    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embedding,
        persist_directory=persist_directory
    )
    print("vectordb:", vectordb._collection.count())
    vectordb.persist() # 向量持久话

def vetor_search(file_name,query):
    persist_directory = os.path.join("D:\\langchain_applicable-doc\\voc\\",file_name +"\\")
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
    print(vectordb._collection.count())
    # query = "美国在海湾打了两场战争,对经济有什么影响"
    # # docs = vectordb.similarity_search(query, k=3)
    docs = vectordb.similarity_search(query, k=7)
    page = list(set([docs.metadata['page'] for docs in docs]))
    page.sort()
    context = [(docs.page_content).replace("\n","") for docs in docs]
    return context,docs

def prompt_set(question):
    prompt_template = """简洁和专业的来回答用户的问题。如果无法从中得到答案，请说"根据已知内容无法回答该问题,答案请使用中文.问题:{question}"""
    prompt = prompt_template.format(question=question)
    return prompt

def answer(context,query):
    prompt = f"已知PDF内容：\n{context}\n根据已知信息回答问题：\n{query}\n所有的回答都根据已知信息"
    response = llm(prompt)
    return response

## use LLM to get answering
def chain_qa(docs,query):
    chain = load_qa_chain(llm=llm,chain_type="stuff")
    query = prompt_set(query)
    result = chain.run(input_documents=docs, question=query)
    return result

def load_qa_chain_with_sources(docs,query):
    chain = load_qa_with_sources_chain(llm,
                                       chain_type="stuff")
    query = prompt_set(query)
    result = chain({"input_documents": docs, "question": query}, return_only_outputs=True)
    return result

# qa=RetrievalQA.from_chain_type(llm=ChatOpenAI(temperature=0.2,model_name='gpt-3.5-turbo'), chain_type="stuff",
#                                                 retriever=docsearch.as_retriever())
# query = "What is the operating income?"
# qa.run(query)

# chain=RetrievalQAWithSourcesChain.from_chain_type(ChatOpenAI(temperature=0.2,model_name='gpt-3.5-turbo'), chain_type="stuff",
#                                                     retriever=docsearch.as_retriever())
# chain({"question": "What is the operating income?"}, return_only_outputs=True)


if __name__ == '__main__':
    file_name = "45-理性分析今后几年房价的走势-光脚穿草鞋.pdf"

    # transfor_vector(file_name)
    query = "理性分析今后几年房价的走势"
    context,page =vetor_search(file_name, query)
    content = chain_qa(page, query)
    print(content)

