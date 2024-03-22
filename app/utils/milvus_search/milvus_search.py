from data_conn.milvus2.milvus_helpers import MilvusHelper
import pandas as pd
from app.utils.embedding.m3e_embedding import *
embeding = M3E_embeddings()
Milvus = MilvusHelper()
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
collection_name ="milvus_collection1"
# Milvus.create_index(collection_name=collection_name)
embeding = embeding.embeddings_text(text="糖尿病患者如何治疗")
Milvus.search_vectors(collection_name=collection_name, vectors=embeding.tolist(), top_k=10)
