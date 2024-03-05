import os
from langchain.vectorstores.neo4j_vector import Neo4jVector
from langchain.document_loaders import WikipediaLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from config.configs import BaseConfig
configs = BaseConfig()
os.environ['OPENAI_API_KEY'] = configs.open_ai
from langchain.document_loaders import WikipediaLoader
from langchain.text_splitter import CharacterTextSplitter

# Read the wikipedia article
# raw_documents = WikipediaLoader(query="Leonhard Euler").load()
raw_documents = "利用 Neo4j 进行向量相似性搜索和图形数据库检索，可确保生成的响应不仅通过 Mistral-7b 的大量预先训练的知识获得信息，而且还通过来自向量和图形数据库的实时数据进行上下文丰富和验证。"
# Define chunking strategy
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=1000, chunk_overlap=20
)
# Chunk the document
documents = text_splitter.create_documents(raw_documents)

# Remove summary from metadata
# for d in documents:
#     del d.metadata['summary']

from langchain.vectorstores import Neo4jVector
from langchain.embeddings.openai import OpenAIEmbeddings

# Neo4j Aura credentials
url="bolt://http://101.200.135.154:7474"
username="neo4j"
pd="mmkg12#$"

# Instantiate Neo4j vector from documents
neo4j_vector = Neo4jVector.from_documents(
    documents,
    OpenAIEmbeddings(),
    url=url,
    username=username,
    password=pd
)

