
import os
# os.environ["OPENAI_API_KEY"] = '你的Open AI API Key'
from  llm_api.openai_api import  openai
# 1.Load 导入Document Loaders
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import TextLoader

# 加载Documents
base_dir = 'D:\\model\\data_set\\tianya-docs-main\\kk' # 文档的存放目录
documents = []
for file in os.listdir(base_dir):
    # 构建完整的文件路径
    file_path = os.path.join(base_dir, file)
    if file.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
        documents.extend(loader.load())
    elif file.endswith('.docx'):
        loader = Docx2txtLoader(file_path)
        documents.extend(loader.load())
    elif file.endswith('.txt'):
        loader = TextLoader(file_path)
        documents.extend(loader.load())
print("pass")
# 2.Split 将Documents切分成块以便后续进行嵌入和向量存储
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=10)
chunked_documents = text_splitter.split_documents(documents)

# 3.Store 将分割嵌入并存储在矢量数据库Qdrant中
from langchain.vectorstores import Qdrant
vectorstore = Qdrant.from_documents(
    documents=chunked_documents, # 以分块的文档
    embedding=openai().embbeding_model(), # 用OpenAI的Embedding Model做嵌入
    location=":memory:",  # in-memory 存储
    collection_name="my_documents",) # 指定collection_name

# 4. Retrieval 准备模型和Retrieval链
import logging # 导入Logging工具
from langchain.retrievers.multi_query import MultiQueryRetriever # MultiQueryRetriever工具
from langchain.chains import RetrievalQA # RetrievalQA链

# 设置Logging
logging.basicConfig()
logging.getLogger('langchain.retrievers.multi_query').setLevel(logging.INFO)

# 实例化一个MultiQueryRetriever
retriever_from_llm = MultiQueryRetriever.from_llm(retriever=vectorstore.as_retriever(), llm=openai().chat_model())

# 实例化一个RetrievalQA链
qa_chain = RetrievalQA.from_chain_type(openai().chat_model(),retriever=retriever_from_llm)

question = "用中文回答：房子太贵了这个现象会导致什么问题"

# RetrievalQA链 - 读入问题，生成答案
result = qa_chain({"query": question})
print(result)

from langchain.prompts import PromptTemplate


# 获取检索型问答链
def get_qa_chain(vector_store):
    prompt_template = """基于以下已知内容，简洁和专业的来回答用户的问题。
                                            如果无法从中得到答案，清说"根据已知内容无法回答该问题"
                                            答案请使用中文。
                                            已知内容:
                                            {context}
                                            问题:
                                            {question}"""

    prompt = PromptTemplate(template=prompt_template,
                            input_variables=["context", "question"])

    return RetrievalQA.from_llm(llm=openai().chat_model(), retriever=vector_store.as_retriever(),
                                prompt=prompt)


## 利用FAISS生成向量库
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
# 保存
def save_vector_store(textChunks):
    db = FAISS.from_texts(textChunks, openai().embbeding_model())
    db.save_local('faiss')

# 加载
def load_vector_store():
    return FAISS.load_local('faiss', OpenAIEmbeddings())

##加载pdf
from PyPDF2 import PdfReader
# 获取pdf文件内容
def get_pdf_text(pdf):
    text = ""
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

from langchain.text_splitter import RecursiveCharacterTextSplitter
# 拆分文本
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        # chunk_size=768,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter


# 获取对话式问答链
def get_history_chain(vector_store):
    prompt_template = """基于以下已知内容，简洁和专业的来回答用户的问题。
                                            如果无法从中得到答案，清说"根据已知内容无法回答该问题"
                                            答案请使用中文。
                                            已知内容:
                                            {context}
                                            问题:
                                            {question}"""

    prompt = PromptTemplate(template=prompt_template,
                            input_variables=["context", "question"])

    return ConversationalRetrievalChain.from_llm(llm=openai().embbeding_model(),
                                                 retriever=vector_store.as_retriever(),
                                                 combine_docs_chain_kwargs={'prompt': prompt})

# 将pdf切分块，嵌入和向量存储
if __name__ == '__main__':
    pdf_path = './test/demo.pdf'
    raw_text = get_pdf_text(pdf_path)
    text_chunks = get_text_chunks(raw_text)
    save_vector_store(text_chunks)
    print(pdf_path + ' is ok')








