from elasticsearch import Elasticsearch
import pandas as pd
from app.utils.embedding.m3e_embedding import *
from data_conn.es8.es_tool import ESConnector
embeding = M3E_embeddings()
es = ESConnector()

def main():
    # ES 信息
    index_name = "embedding1"
    # 数据地址
    path = "D:\\model\\data_set\\Chinese-medical-dialogue-data\\Data_数据\\IM_内科\\内科5000-33000.csv"
    # ES 连接
    # 读取数据写入ES
    data = pd.read_csv(path, encoding='ANSI')
    # data = tqdm(len(data))
    for index, row in data.iterrows():
        # 写入前 5000 条进行测试
        if index >= 1000:
            break
        title = row["ask"]
        content = row["answer"]
        # 文本转向量
        embedding_ask = embeding.embeddings_text(text=title)
        body = {
            "vector": embedding_ask.tolist(),
            "title": title,
            "text": content
        }
        es.insert_data(index_name=index_name,document_id=index,body=body)
        # result = add_doc(index_name, index, embedding_ask, title, content, es)
        print(es)

def main1():
    # ES 信息
    index_name = "embedding1"
    # 数据地址
    path = "D:\\model\\data_set\\Chinese-medical-dialogue-data\\Data_数据\\IM_内科\\内科5000-33000.csv"
    # ES 连接
    # 读取数据写入ES
    data = pd.read_csv(path, encoding='ANSI')
    # data = tqdm(len(data))
    for index, row in data.iterrows():
        # 写入前 5000 条进行测试
        if index>=30:
            break
        title = row["ask"]
        content = row["answer"]
        # 文本转向量
        embedding_ask = embeding.embeddings_text(text=title)
        embedding_content = embeding.embeddings_text(text=content)
        body = {
            "title_vector": embedding_ask.tolist(),
            "content_vector": embedding_content.tolist(),
            "title": title,
            "text": content
        }
        es.insert_data(index_name=index_name,document_id=index,body=body)
        # result = add_doc(index_name, index, embedding_ask, title, content, es)
        print(es)

if __name__ == '__main__':
    main()
