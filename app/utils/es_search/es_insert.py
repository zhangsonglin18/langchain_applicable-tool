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
                        "type": "keyword"
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
                      # "title_vector": {
                      #     "type": "dense_vector",
                      #     "dims": 768,
                      #     "index": True,
                      #     "similarity": "dot_product"
                      # },
                      "title": {
                          "type": "text","index": False
                      },
                      "text": {"type": "text","index": False}
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
    print(es.creat_index(index_name=index_name, mapping=x))

