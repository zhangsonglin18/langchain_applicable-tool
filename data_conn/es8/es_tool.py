from config.configs import ESParams
from elasticsearch import Elasticsearch
es_params = ESParams()
index_name = es_params.index_name

##ES数据库连接的基本使用手册
class ESConnector(object):
    def __init__(self):
        self.es_params = ESParams()
        self.client = Elasticsearch(['{}:{}'.format(self.es_params.url, self.es_params.port)],
                                    basic_auth=(self.es_params.username, self.es_params.passwd),
                                    verify_certs=False)
    ##测试是否可以ping通
    def ping(self):
        return self.client.ping()

    def es(self):
        return self.client

    # %% 检查索引是否存在
    def index_exsits(self,index_name):
        return self.client.indices.exists(index=index_name)
#
# %% 新建索引
    def creat_index(self,index_name,mapping):
        response = self.client.indices.create(index=index_name, body=mapping)
        return response

# # %% 插入数据
    def insert_data(self,index_name,document_id,body):
        response = self.client.index(index=index_name, id=document_id, document=body)
        return response
#
# # %% 更新
    def update_data(self,index_name,document_id,data):
        rp = self.client.update(index=index_name, id=document_id, body={"doc": data})
        return rp

    def delete_index(self,index_name):
        return self.client.indices.delete(index=index_name)

    def search(self,index_name,query):
        return self.client.search(index=index_name, body=query)

    def scroll(self,index_name,scroll_id):
        return self.client.scroll(scroll_id=scroll_id, scroll="1m")

    def clear_scroll(self,scroll_id):
        return self.client.clear_scroll(scroll_id=scroll_id)

    def close(self):
        self.client.close()

    def __call__(self, *args, **kwargs):
        return self.ping()

