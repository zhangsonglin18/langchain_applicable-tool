from pymilvus import Milvus
from program.picsearch.tools.MinioTools import MinioTools
from pymilvus import DataType
from utils.embedding_pro.chinese_clip_model import ChineseClipModel
embedding = ChineseClipModel()
class MilvusTools:

    def __init__(self):
       self.client = Milvus("101.200.135.154", "19530")

    def create_collection(self, collection_name):
        fields = {"fields": [{"name": "pic_path",
                            "type": DataType.VARCHAR,
                            "is_primary": True,
                            "params": {"max_length": 200}}
                          ,{
                            "name": "pic_vec",
                            "type": DataType.FLOAT_VECTOR,
                            "params": {"dim": 512}
                            }]}

        if collection_name not in self.client.list_collections():
            self.client.create_collection(collection_name=collection_name, fields=fields)

        else:
            print("已存在")

    def insert_data(self, collection_name, data):
        entities = [
            {"name": "pic_path", "type": DataType.VARCHAR, "values": data[0]},
            {"name": "pic_vec", "type": DataType.FLOAT_VECTOR, "values": data[1]},
        ]
        self.client.insert(collection_name, entities)
        self.client.flush([collection_name])

    def build_index(self, collection_name, field_name):
        index_param = {
            "metric_type": "L2",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 20}
        }
        self.client.create_index(collection_name, field_name, index_param, timeout=10)
        print("Create index: {}".format(index_param))

    def load(self, collection_name):
        self.client.load_collection(collection_name, timeout=10)
        print("load {} success".format(collection_name))

    def search(self, collection_name, vector_field, search_vectors):
        search_params = {"metric_type": "L2", "params": {"nprobe": 20}}
        results = self.client.search(collection_name, search_vectors, vector_field, param=search_params, limit=9)
        print(
            results
        )
        return results[0].ids


if __name__ == '__main__':
    from data_conn.minio_con.minio_file.image_pro import view_image1
    milvusTool = MilvusTools()
    miniotool = MinioTools()
    pics = miniotool.lists_bucket("pictures")
    # resnet = ResNetEmbeding("/root/autodl-tmp/pic_search/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5")
    paths = []
    embs = []
    for i in pics:
        path = "http://152.136.174.19:9000/minio/pictures/" + str(i)
        print(path)
        images = view_image1(miniotool.client,"pictures",i)
        emb = embedding.generate_image_features_m(images)
        paths.append(path)
        embs.append(emb)
    data = [paths, embs]
    print(len(data[1]))
    milvusTool.create_collection("picture")
    milvusTool.insert_data("picture", data)
    milvusTool.build_index("picture", "pic_vec")
    milvusTool.load("picture")
   # print(milvusTool.search("picture", "pic_vec", [data[1][0]]))
