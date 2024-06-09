# import torch
# from transformers import AutoModelForSequenceClassification, AutoTokenizer
#
# tokenizer = AutoTokenizer.from_pretrained('D:\\model\\bge-reranker-v2-m3')
# model = AutoModelForSequenceClassification.from_pretrained('D:\\model\\bge-reranker-v2-m3')
# model.eval()
#
# pairs = [['what is panda?', 'hi'], ['what is panda?', 'The giant panda (Ailuropoda melanoleuca), sometimes called a panda bear or simply panda, is a bear species endemic to China.']]
# with torch.no_grad():
#     inputs = tokenizer(pairs, padding=True, truncation=True, return_tensors='pt', max_length=512)
#     scores = model(**inputs, return_dict=True).logits.view(-1, ).float()
#     print(scores)

# !/usr/bin/env python
# encoding: utf-8
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from operator import itemgetter
from FlagEmbedding import FlagReranker


app = FastAPI()

reranker = FlagReranker('D:\\model\\bge-reranker-v2-m3', use_fp16=True)


class QuerySuite(BaseModel):
    query: str
    passages: list[str]
    top_k: int = 1


@ app.post('/bge_base_rerank')
def rerank(query_suite: QuerySuite):
    scores = reranker.compute_score([[query_suite.query, passage] for passage in query_suite.passages])
    if isinstance(scores, list):
        similarity_dict = {passage: scores[i] for i, passage in enumerate(query_suite.passages)}
    else:
        similarity_dict = {passage: scores for i, passage in enumerate(query_suite.passages)}
    sorted_similarity_dict = sorted(similarity_dict.items(), key=itemgetter(1), reverse=True)
    result = {}
    for j in range(query_suite.top_k):
        result[sorted_similarity_dict[j][0]] = sorted_similarity_dict[j][1]
    return result


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=50072)