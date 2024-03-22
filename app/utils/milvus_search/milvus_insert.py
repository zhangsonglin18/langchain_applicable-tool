from data_conn.milvus2.milvus_helpers import MilvusHelper
import pandas as pd
from app.utils.embedding.m3e_embedding import *
embeding = M3E_embeddings()
Milvus = MilvusHelper()
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility

field1 = FieldSchema(name="id", dtype=DataType.INT64, descrition="int64", is_primary=True, auto_id=True)
field2 = FieldSchema(name="text", dtype=DataType.VARCHAR, descrition="text", is_primary=False, max_length=1000)
field3 = FieldSchema(name="content", dtype=DataType.VARCHAR, descrition="content", is_primary=False, max_length=1000)
field4 = FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, descrition="float vector",
                     dim=768, is_primary=False)

collection_name ="milvus_collection1"

if Milvus.has_collection(collection_name = collection_name):
    has = utility.has_collection("hello_milvus")
    print(f"Does collection hello_milvus exist in Milvus: {has}")
else:
    Milvus.create_collection(collection_name = collection_name,fields=[field1, field2, field3, field4])
    print(f"创建了新的Milvus集合：{collection_name}")
    Milvus.create_index(collection_name=collection_name)

if __name__ == '__main__':
    path = "D:\\model\\data_set\\Chinese-medical-dialogue-data\\Data_数据\\IM_内科\\内科5000-33000.csv"
    # ES 连接
    # 读取数据写入ES
    data = pd.read_csv(path, encoding='ANSI')
    # data = tqdm(len(data))
    title_list =[]
    embeding_list = []
    content_list = []
    for index, row in data.iterrows():
        # 写入前 5000 条进行测试
        if index >= 500:
            break
        title = row["ask"]
        content = row["answer"]
        # 文本转向量
        embedding_ask = embeding.embeddings_text(text=title)
        title_list.append(title[:1000])
        content_list.append(content[:1000])
        embeding_list.append(embedding_ask.tolist())

    ids = Milvus.insert(collection_name=collection_name, data=[title_list,content_list,embeding_list])
    print(ids)





