from elasticsearch import Elasticsearch
from transformers import BertTokenizer, BertModel
import torch
from app.utils.embedding.m3e_embedding import *
from data_conn.es8.es_tool import ESConnector
embeding = M3E_embeddings()
Es = ESConnector()

def embeddings_doc(doc, tokenizer, model, max_length=300):
    encoded_dict = tokenizer.encode_plus(
        doc,
        add_special_tokens=True,
        max_length=max_length,
        padding='max_length',
        truncation=True,
        return_attention_mask=True,
        return_tensors='pt'
    )
    input_id = encoded_dict['input_ids']
    attention_mask = encoded_dict['attention_mask']

    # 前向传播
    with torch.no_grad():
        outputs = model(input_id, attention_mask=attention_mask)

    # 提取最后一层的CLS向量作为文本表示
    last_hidden_state = outputs.last_hidden_state
    cls_embeddings = last_hidden_state[:, 0, :]
    return cls_embeddings[0]


def search_similar_cos(index_name, query_text, tokenizer, model, es, top_k=3):
    query_embedding = embeddings_doc(query_text, tokenizer, model)
    print(query_embedding.tolist())
    query = {
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.queryVector, 'vector') + 1.0",
                    "lang": "painless",
                    "params": {
                        "queryVector": query_embedding.tolist()
                    }
                }
            }
        },
        "size": top_k
    }
    res = es.search(index=index_name, body=query)
    hits = res['hits']['hits']
    similar_documents = []
    for hit in hits:
        similar_documents.append(hit['_source'])
    return similar_documents


def search_similar_dot(index_name, query_text, tokenizer, model, es, top_k=3):
    query_embedding = embeddings_doc(query_text, tokenizer, model)
    # print(query_embedding.tolist())
    query = {
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "dotProduct(params.queryVector, 'vector')+1.0",
                    "lang": "painless",
                    "params": {
                        "queryVector": query_embedding.tolist()
                    }
                }
            }
        },
        "size": top_k
    }
    res = es.search(index=index_name, body=query)
    hits = res['hits']['hits']
    similar_documents = []
    for hit in hits:
        similar_documents.append(hit['_source'])
    return similar_documents


def search_similar_l1(index_name, query_text, tokenizer, model, es, top_k=3):
    query_embedding = embeddings_doc(query_text, tokenizer, model)
    # print(query_embedding.tolist())
    query = {
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "1 / (1 + l1norm(params.queryVector, doc['vector']))",
                    "lang": "painless",
                    "params": {
                        "queryVector": query_embedding.tolist()
                    }
                }
            }
        },
        "size": top_k
    }
    res = es.search(index=index_name, body=query)
    hits = res['hits']['hits']
    similar_documents = []
    for hit in hits:
        similar_documents.append(hit['_source'])
    return similar_documents


def search_similar_l2(index_name, query_text, tokenizer, model, es ,top_k=3):
    query_embedding = embeddings_doc(query_text, tokenizer, model)
    # print(query_embedding.tolist())
    query = {
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "1 / (1 + l2norm(params.queryVector, doc['vector']))",
                    "lang": "painless",
                    "params": {                        "queryVector": query_embedding.tolist()
                    }
                }
            }
        },
        "size": top_k
    }
    res = es.search(index=index_name, body=query)
    hits = res['hits']['hits']
    similar_documents = []
    for hit in hits:
        similar_documents.append(hit['_source'])
    return similar_documents

def search_knn(index_name, query_text, tokenizer, model, es ,top_k=3):
    query_embedding = embeddings_doc(query_text, tokenizer, model)
    # print(query_embedding.tolist())
    query = {
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "1 / (1 + l2norm(params.queryVector, doc['vector']))",
                    "lang": "painless",
                    "params": {"queryVector": query_embedding.tolist()
                    }
                }
            }
        },
        "size": top_k
    }

    res = es.search(index=index_name, body=query)
    hits = res['hits']['hits']
    similar_documents = []
    for hit in hits:
        similar_documents.append(hit['_source'])
    return similar_documents




def main():
    es = Es.es()
    query_text = "我有高血压可以拿党参泡水喝吗"
    similar_documents = search_similar_dot(index_name="embedding",query_text=query_text,
                                           tokenizer=embeding.tokenizer, model=embeding.model, es=es)
    for item in similar_documents:
        print("================================")
        print('title：', item['title'])
        print('content', item['text'])


if __name__ == '__main__':
    main()

