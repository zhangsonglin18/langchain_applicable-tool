from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from llm_api.openai_api import openai
from langchain.vectorstores.chroma import Chroma
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import YoutubeLoader, UnstructuredURLLoader
from langchain.prompts import PromptTemplate

class summarize():

    def __init__(self):
        self.llm = openai().chat_model()
        self.summarize = openai().embbeding_model()

    def text_summarize(self,source_text):
        text_splitter = CharacterTextSplitter()
        texts = text_splitter.split_text(source_text)
        # Create Document objects for the texts (max 3 pages)
        docs = [Document(page_content=t) for t in texts[:3]]
        # Initialize the OpenAI module, load and run the summarize chain
        chain = load_summarize_chain(self.llm, chain_type="map_reduce")
        summary = chain.run(docs)
        return summary

    ##获取pdf总结的结果
    def pdf_summarize(self,pdf_path):
        # Read the PDF file
        ##todo 此处的loader需要进行修改
        loader = PyPDFLoader(pdf_path)
        pages = loader.load_and_split()
        # Create embeddings for the pages and insert into Chroma database
        vectordb = Chroma.from_documents(pages, self.summarize)
        chain = load_summarize_chain(self.llm, chain_type="stuff")
        search = vectordb.similarity_search(" ")
        summary = chain.run(input_documents=search, question="Write a summary within 200 words.")
        return summary

    def url_summarize(self,url):
        if "youtube.com" in url:
            loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
        else:
            loader = UnstructuredURLLoader(urls=[url], ssl_verify=False, headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
        data = loader.load()
        # Initialize the ChatOpenAI module, load and run the summarize chain
        prompt_template = """用250-300个字总结以下内容：

                           {text}

                       """
        prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
        chain = load_summarize_chain(self.llm, chain_type="stuff", prompt=prompt)
        summary = chain.run(data)
        return summary



if __name__ == '__main__':
    # print(openai()(prompt = "你能帮我写一个Python脚本吗"))

    print(summarize().url_summarize(url="https://www.youtube.com/watch?v=4OsY7Ag1OQ0"))

