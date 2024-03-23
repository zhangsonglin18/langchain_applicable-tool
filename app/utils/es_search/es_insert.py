from data_conn.es8.es_tool import *

##传统es向量搜索
mapping1 = {"settings": {"number_of_shards": 5,
                 "number_of_replicas": 1},
            "mappings":
            {
                "properties": {
                    "text": {"type": "text"},
                    "vector": {
                        "type": "dense_vector",
                        "dims": 768,
                        "index": True,
                        "similarity": "cosine",
                    },
                    "title": {
                        "type": "text",
                        "analyzer": "ik_smart",
                    }
                }}}

##面向knn的向量搜索
mapping2 = {"settings": {"number_of_shards": 5,
                   "number_of_replicas": 1},
            "mappings": {
                  "properties": {
                      "content_vector": {
                          "type": "dense_vector",
                          "dims": 768,
                          "index": True,
                          "similarity": "dot_product"
                      },
                      "title_vector": {
                          "type": "dense_vector",
                          "dims": 768,
                          "index": True,
                          "similarity": "dot_product"
                      },
                      "title": {
                          "type": "text"
                      },
                      "text": {
                          "type": "text"
                      }
                  }
              }
              }

mapping3 =  {
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "Question": { "type": "text" },
      "Answer": { "type": "text" },
      "question_emb": {
        "type": "dense_vector",
        "dims": 768,
        "index": "true",
        "similarity": "dot_product"
      },
      "answer_emb": {
        "type": "dense_vector",
        "dims": 768,
        "index": "true",
        "similarity": "dot_product"
      }
    }
  }
}

configurations = {}
configurations["settings"] = {"settings": {
        "analysis": {
            "filter": {
                 "ngram_filter": {
                     "type": "edge_ngram",
                     "min_gram": 2,
                     "max_gram": 15,
                 },
                "english_stop": {
                  "type":       "stop",
                  "stopwords":  "_english_"
                },
                 "english_keywords": {
                   "type":       "keyword_marker",
                   "keywords":   ["example"]
                 },
                "english_stemmer": {
                  "type":       "stemmer",
                  "language":   "english"
                },
                "english_possessive_stemmer": {
                  "type":       "stemmer",
                  "language":   "possessive_english"
                }
            },
            "analyzer": {
                "en_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase",
                                "ngram_filter",
                                "english_stemmer",
                               "english_possessive_stemmer",
                                "english_stop"
                                "english_keywords",
                                ]
                }
            }
        }
    }}

configurations["mapping"]= {
    "mappings": {
        "properties": {
            "Embeddings": {
                "type": "dense_vector",
                "dims": 512,
                "index": True,
                "similarity": "cosine"
            },
        }
    }
}



if __name__ == '__main__':
    es = ESConnector()
    index_name = "embedding1"
    if es.index_exsits(index_name):
        es.delete_index(index_name=index_name)
    ##传统的创建向量
    # print(es.creat_index(index_name="embedding",mapping=x))
    ##knn的创建向量
    print(es.creat_index(index_name=index_name, mapping=mapping1))

    # es.indices.create(index='my_new_index',
    #                     settings=configurations["settings"],
    #                     mappings=configurations["mappings"]
    #                     )

