import pandas as pd
import numpy as np
import json
import os
import uuid

from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('D:\\model\\m3e')

import elasticsearch
from elasticsearch import Elasticsearch
from elasticsearch import helpers

from tqdm.auto import tqdm

tqdm.pandas()

df = pd.read_csv("data job posts.csv")


class Tokenizer(object):
    def __init__(self):
        self.model = SentenceTransformer('D:\\model\\m3e')

    def get_token(self, documents):
        sentences = [documents]
        sentence_embeddings = self.model.encode(sentences)
        encod_np_array = np.array(sentence_embeddings)
        encod_list = encod_np_array.tolist()
        return encod_list[0]


token_instance = Tokenizer()

# df = df.head(5000)
# df = df.dropna(how='all')
# length = len(list(df['Title'].unique()))
# print(f"length = {length}")
#
# df['vector'] = df['jobpost'].progress_apply(token_instance.get_token)
# elk_data = df.to_dict("records")

es = Elasticsearch(["https://elastic:YGP1ww5oWzuagMHeN7aM@192.168.248.131:9200"], verify_certs=False)
es.ping()

# for x in elk_data:
#     try:
#         _ = {
#             "title": x.get("Title", ""),
#             "company": x.get("Company", ""),
#             "location": x.get("Location", ""),
#             "salary": x.get("Salary", ""),
#             "vector": x.get("vector", ""),
#             "job_description": x.get("JobDescription", ""),
#
#         }
#         es.index(index='posting1', document=_)
#     except Exception as e:
#         pass

INPUT = input("Enter the Input Query: ")
token_vector = token_instance.get_token(INPUT)
# print(token_vector)

res = es.knn_search(index='posting1', source=["title", "job_description"],
                    knn={
                        "field": "vector",
                        "k": 5,
                        "num_candidates": 10,
                        "query_vector": token_vector
                    })

title = [x['_source'] for x in res['hits']['hits']]

for item in title:
    print(item)