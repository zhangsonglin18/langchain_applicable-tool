from data_conn.milvus2.milvus_helpers import MilvusHelper
import pandas as pd
import time
from app.utils.embedding.m3e_embedding import *
embeding = M3E_embeddings()
Milvus = MilvusHelper()
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
fmt = "\n=== {:30} ===\n"
search_latency_fmt = "search latency = {:.4f}s"

##向量检索
def collection_search(collection_name,embeding):
    # collection_name ="milvus_collection1"
    ##向量转换
    embeding = embeding.embeddings_text(text="糖尿病患者如何治疗")
    vector = embeding.numpy()
    ##输出结果
    out_list = ['content']
    result = Milvus.search_vectors(collection_name=collection_name, vectors=[vector], top_k=1,output_list=out_list)
    res =[]
    for hits in result:
        for hit in hits:
            print(hit.entity.get('content'))
            res.append(hit.entity.get('content'))
    return res

##混合检索
def collection_multisearch(collection_name,embeding):
    embeding = embeding.embeddings_text(text="糖尿病患者如何治疗")
    vector = [embeding.numpy()]
    # expr = f'pk in ["{ids[0]}" , "{ids[1]}"]'
    # expr = "random > 0.5"
    start_time = time.time()
    expr= ""
    result = Milvus.search_vectors(collection_name=collection_name, expr=expr,vectors=vector, top_k=1, output_list=['content'])
    end_time = time.time()
    print(search_latency_fmt.format(end_time - start_time))
    res =[]
    for hits in result:
        for hit in hits:
            print(hit.entity.get('content'))
            res.append(hit.entity.get('content'))
    return res

if __name__ == '__main__':
    collection_name = "milvus_medic"
    res = collection_search(collection_name, embeding)
    print(res)
