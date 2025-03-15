from rank_bm25 import BM25Okapi
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
import jieba
from typing import List
def chinese_tokenizer(text: str) -> List[str]:
    tokens = jieba.lcut(text)
    return [token for token in tokens if token not in stopwords.words('chinese')]

corpus = [
    "Hello there good man!",
    "It is quite windy in London",
    "How is the weather today?"
]
# 分词使用空格
# tokenized_corpus = [doc.split(" ") for doc in corpus]
#todo 此处为中文分词，使用jieba分词
tokenized_corpus = [chinese_tokenizer(doc) for doc in corpus]
bm25 = BM25Okapi(tokenized_corpus)
query = "windy London"
# tokenized_query = query.split(" ")
tokenized_query = chinese_tokenizer(query)
doc_scores = bm25.get_scores(tokenized_query)
print(doc_scores)


# from nltk.stem import PorterStemmer
#
# def tokenize_remove_stopwords(text: str) -> List[str]:
#     # lowercase and stem words
#     text = text.lower()
#     stemmer = PorterStemmer()
#     words = list(simple_extract_keywords(text))
#     return [stemmer.stem(word) for word in words]


# from llama_index.retrievers.bm25 import BM25Retriever
# from llama_index.core import Document
# from llama_index.core.node_parser import SentenceSplitter
# from llama_index.core.response.notebook_utils import display_source_node
#
# documents = [Document(text="床前明月光"),
#              Document(text="疑是地上霜"),
#              Document(text="举头望明月"),
#              Document(text="低头思故乡")]
#
# splitter = SentenceSplitter(chunk_size=1024)
# nodes = splitter.get_nodes_from_documents(documents)
#
# retriever = BM25Retriever.from_defaults(
#     nodes=nodes,
#     similarity_top_k=2,
#     tokenizer=chinese_tokenizer
# )
#
# nodes = retriever.retrieve("故乡")
# for node in nodes:
#     display_source_node(node)

#todo
#参考链接：https://mp.weixin.qq.com/s/XBkMpcBmu2vpBpZi2Zh92g