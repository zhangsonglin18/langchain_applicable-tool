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

    # %% 检查索引是否存在
    def index_exsit(self,index_name):
        return self.client.indices.exists(index=index_name)
#
# %% 新建索引
    def creat_index(self,index_name,mapping):
        response = self.client.indices.create(index=index_name, body=mapping)
        return response

# # %% 插入数据
    def insert_data(self,index_name,document_id,data):
        response = self.client.index(index=index_name, id=document_id, document=data)
        return response
#
# # %% 更新
    def update_data(self,index_name,document_id,data):
        rp = self.client.update(index=index_name, id=document_id, body={"doc": data})
        return rp

    def __call__(self, *args, **kwargs):
        return self.ping()
#
# # %% 检查文档是否存在
# document_exists = client.exists(index=index_name, id=document_id)
#
# # %% 根据ID删除文档
# response = client.delete(index=index_name, id=document_id)
