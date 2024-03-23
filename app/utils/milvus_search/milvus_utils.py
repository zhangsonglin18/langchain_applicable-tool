from data_conn.milvus2.milvus_helpers import MilvusHelper
Milvus = MilvusHelper()

if __name__ == '__main__':
    collection_name = "milvus_medic"
    ##查看milvus 数据库中的collection中数据量
    print(Milvus.count(collection_name))
    ##调用collection接口
    collection = Milvus.set_collection(collection_name)
