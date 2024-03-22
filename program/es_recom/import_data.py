from elasticsearch import Elasticsearch
from transformers import BertTokenizer, BertModel
import torch
import pandas as pd


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


def add_doc(index_name, id, embedding_ask, ask, answer, es):
    body = {
        "ask_vector": embedding_ask.tolist(),
        "ask": ask,
        "answer": answer
    }
    result = es.create(index=index_name, id=id, body=body)
    return result


def main():
    # 模型下载的地址
    model_name = 'D:\model\m3e'
    # ES 信息
    es_host = "http://152.136.174.19"
    es_port = 9200
    es_user = "elastic"
    es_password = "elastic"
    index_name = "medical_index"

    # 数据地址
    path = "D:\\model\\data_set\\Chinese-medical-dialogue-data\\Data_数据\\IM_内科\\内科5000-33000.csv"

    # 分词器和模型
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertModel.from_pretrained(model_name)

    # ES 连接
    es = Elasticsearch(["http://elastic:YGP1ww5oWzuagMHeN7aM@152.136.174.19:9200"], verify_certs=False)

    # 读取数据写入ES
    data = pd.read_csv(path, encoding='ANSI')
    for index, row in data.iterrows():
        # 写入前 5000 条进行测试
        if index >= 500:
            break
        ask = row["ask"]
        answer = row["answer"]
        # 文本转向量
        embedding_ask = embeddings_doc(ask, tokenizer, model)
        result = add_doc(index_name, index, embedding_ask, ask, answer, es)
        print(result)


if __name__ == '__main__':
    main()
