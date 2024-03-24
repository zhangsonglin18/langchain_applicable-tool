from data_conn.milvus2.milvus_helpers import MilvusHelper
from app.utils.embedding.m3e_embedding import *
embeding = M3E_embeddings()
Milvus = MilvusHelper()
from data_conn.mysql8.mysql_conn import *
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
from utils.chinese_clip_model import ChineseClipModel
##muilvus向量检索的field设计，对应不同的设计不同类型
def creat_collection_field(collection_name):
    field1 = FieldSchema(name="id", dtype=DataType.INT64, descrition="int64", is_primary=True, auto_id=True)
    field2 = FieldSchema(name="text", dtype=DataType.VARCHAR, descrition="text", is_primary=False, max_length=1000)
    field3 = FieldSchema(name="content", dtype=DataType.VARCHAR, descrition="content", is_primary=False, max_length=1000)
    field4 = FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, descrition="float vector",
                         dim=768, is_primary=False)
    if Milvus.has_collection(collection_name = collection_name):
        has = utility.has_collection("hello_milvus")
        print(f"Does collection hello_milvus exist in Milvus: {has}")
    else:
        Milvus.create_collection(collection_name = collection_name,fields=[field1, field2, field3, field4])
        print(f"创建了新的Milvus集合：{collection_name}")
        Milvus.create_index(collection_name=collection_name)

def creat_collection_field_news(collection_name):
    field1 = FieldSchema(name="id", dtype=DataType.INT64, descrition="int64", is_primary=True, auto_id=True)
    field2 = FieldSchema(name="ids", dtype=DataType.INT64, descrition="ids", is_primary=False)
    field4 = FieldSchema(name="title", dtype=DataType.VARCHAR, descrition="text", is_primary=False, max_length=512)
    field5 = FieldSchema(name="content", dtype=DataType.VARCHAR, descrition="content", is_primary=False, max_length=4086)
    field6 = FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, descrition="float vector",
                         dim=512, is_primary=False)
    if Milvus.has_collection(collection_name = collection_name):
        has = utility.has_collection("hello_milvus")
        print(f"Does collection hello_milvus exist in Milvus: {has}")
    else:
        Milvus.create_collection(collection_name = collection_name,fields=[field1, field2, field4,field5,field6])
        print(f"创建了新的Milvus集合：{collection_name}")
        Milvus.create_index(collection_name=collection_name)

#insert_news
def insert_collection_news(collection_name):
    collection_name = "news1"
    embeding_vector = ChineseClipModel()
    creat_collection_field_news(collection_name)
    mysql = MySql()
    query = "SELECT * FROM `q_intelligence`.`news1` limit 5"
    data = mysql.sql_search(query)
    for row in data:
        ids = row[0]
        title = row[2][:500]
        content = row[3].replace("\n","")
        embedding = embeding_vector.generate_text_features_m(title)
        out = Milvus.insert(collection_name=collection_name, data=[[ids],[title[:512]],[content[:1000]],[embedding]])
        print(out)

#search_news
def search_collection_news(collection_name, query_text, topk=10):
    print(embeding)

if __name__ == '__main__':
    collection_name = "news8"
    # embeding_vector = ChineseClipModel()
    # creat_collection_field_news(collection_name)
    # mysql = MySql()
    # query = "SELECT * FROM `q_intelligence`.`news1`"
    # data = mysql.sql_search(query)
    # for row in data:
    #     ids = row[0]
    #     title = row[2][:500]
    #     content = row[3].replace("\n","").replace(" ","")[:1024]
    #     embedding = embeding_vector.generate_text_features_m(title)
    #     print(content)
    #     print(len(content))
    #     out = Milvus.insert(collection_name=collection_name, data=[[ids],[title],[content],[embedding]])
    #     print(out)
    title = "台军在佩洛西抵达前提高战备"
    # collection_name = "news"
    embeding_vector = ChineseClipModel()
    embeding = embeding_vector.generate_text_features_m(title)
    vector = embeding
    ##输出结果
    out_list = ['ids','title','content']
    result = Milvus.search_vectors(collection_name=collection_name, vectors=[vector], top_k=5,output_list=out_list)
    res =[]
    for hits in result:
        for hit in hits:
            print(hit.entity.get('title'))
            res.append(hit.entity.get('title'))




