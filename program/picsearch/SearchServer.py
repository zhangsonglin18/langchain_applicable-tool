import gradio as gr
from program.picsearch.tools.MilvusTools import MilvusTools
# from tools.ResNetEmbeding import ResNetEmbeding
from program.picsearch.tools.MinioTools import MinioTools
from utils.chinese_clip_model import ChineseClipModel
miniotool = MinioTools()
from PIL import Image
embedding = ChineseClipModel()
milvusTool = MilvusTools()
from data_conn.minio_con.minio_file.image_pro import view_image2
# resnet = ResNetEmbeding("./model/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5")
# images = view_image1(miniotool.client,"pictures",i)
# emb = embedding.generate_image_features_m(images)

def process(res):
    rest = []
    for item in res:
        item = item.split("pictures")[-1]
        images = view_image2(miniotool.client, "pictures", item)
        rest.append(images)
    return rest

def seach(path):
    # emb = resnet.extract_feature(path.file, distant=False)
    img = Image.open(path)
    emb = embedding.generate_image_features_m(img)
    res = milvusTool.search("picture", "pic_vec", [emb])
    res = process(res)
    return res


if __name__ == '__main__':
    demo = gr.Interface(title="以图搜图",
                        css="",
                        fn=seach,
                        inputs=[gr.outputs.Image(type="filepath", label="图片")],
                        outputs=[gr.outputs.Image(type="filepath", label="图片") for _ in range(4)])
    demo.launch(inline=True, height=100)
