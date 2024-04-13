from PyPDF2 import PdfReader
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
OpenAIEmbeddings = HuggingFaceEmbeddings(model_name="D:\\model\\m3e")
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from llm_api.openai_api import openai
llm = openai().chat_model()
# 获取pdf文件内容
def get_pdf_text(pdf):
    text = ""
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

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
# 保存
def save_vector_store(textChunks):
    db = FAISS.from_texts(textChunks, OpenAIEmbeddings())
    db.save_local('faiss')

# 加载
def load_vector_store():
    return FAISS.load_local('faiss', OpenAIEmbeddings())

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
    return RetrievalQA.from_llm(llm=ChatOpenAI(model_name='gpt-3.5-turbo-16k'), retriever=vector_store.as_retriever(),
                                prompt=prompt)

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

    return ConversationalRetrievalChain.from_llm(llm=llm,
                                                 retriever=vector_store.as_retriever(),
                                                 combine_docs_chain_kwargs={'prompt': prompt})

# 将pdf切分块，嵌入和向量存储
if __name__ == '__main__':
    ##向量存储
    pdf_path = './test/demo.pdf'
    raw_text =get_pdf_text(pdf_path)
    text_chunks = get_text_chunks(raw_text)
    save_vector_store(text_chunks)
    print(pdf_path + ' is ok')

    ##向量问答
    text= ""
    vector_store = load_vector_store()
    chain = get_qa_chain(vector_store)
    response = chain({"query": text})

    ##另一种问答

    chain = get_history_chain(vector_store)
    # 使用session缓存对话
    chat_history = ""
    if chat_history is None:
        chat_history = []
    # Convert chat history to list of tuples
    chat_history_tuples = []
    for message in chat_history:
        chat_history_tuples.append((message[0], message[1]))
    response = chain({"question": text, "chat_history": chat_history_tuples})
    print(response)


