from elasticsearch import Elasticsearch
from transformers import BertTokenizer, BertModel
import torch


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
                    "source": "cosineSimilarity(params.queryVector, 'ask_vector') + 1.0",
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
    print(query_embedding.tolist())
    query = {
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "dotProduct(params.queryVector, 'ask_vector')+1.0",
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
    print(query_embedding.tolist())
    query = {
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "1 / (1 + l1norm(params.queryVector, doc['ask_vector']))",
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


def search_similar_l2(index_name, query_text, tokenizer, model, es, top_k=3):
    query_embedding = embeddings_doc(query_text, tokenizer, model)
    print(query_embedding.tolist())
    query = {
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "1 / (1 + l2norm(params.queryVector, doc['ask_vector']))",
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



def main():
    # 模型下载的地址
    model_name = 'D:\model\m3e'
    # ES 信息
    index_name = "medical_index"
    # 分词器和模型
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertModel.from_pretrained(model_name)

    # ES 连接
    es = Elasticsearch(["http://elastic:YGP1ww5oWzuagMHeN7aM@152.136.174.19:9200"], verify_certs=False)

    query_text = "我有高血压可以拿党参泡水喝吗"

    similar_documents = search_similar_dot(index_name, query_text, tokenizer, model, es)
    for item in similar_documents:
        print("================================")
        print('ask：', item['ask'])
        print('answer：', item['answer'])


if __name__ == '__main__':
    main()

