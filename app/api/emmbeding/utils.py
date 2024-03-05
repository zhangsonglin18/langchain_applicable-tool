from sentence_transformers import SentenceTransformer

def text_decoding(sentences):
    #todo 模型的调用是否经过最开始
    embeeding_model = SentenceTransformer('D:\\model\\m3e')
    embeddings = embeeding_model.encode(sentences)
    return embeddings
