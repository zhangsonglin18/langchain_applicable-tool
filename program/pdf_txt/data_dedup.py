from sentence_transformers import util
import numpy as np
from sentence_transformers import SentenceTransformer

import re

email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
phone_pattern = r'\b\d{10,13}\b'
name_pattern = r'\b[A-Za-z ]+\b'  # 可根据需要自行修改，这里只是一个示例
id_pattern = r'\b\d{15}(\d{2}[0-9X])?\b'
workid_pattern = r'\b[A-Za-z0-9]{5,10}\b'  # 修改以匹配含英文大小写的工号
qq_pattern = r'\b[1-9][0-9]{4,}\b'
privacy_patterns = [email_pattern, phone_pattern, name_pattern, id_pattern, workid_pattern, qq_pattern]
def mask_privacy(text, patterns):
    for pattern in patterns:
        # Find all the matches
        matches = re.findall(pattern, text)
        for match in matches:
            # Replace each character in the match with '*'
            masked = '*' * len(match)
            # Replace the match in the text with the masked string
            text = text.replace(match, masked)
    return text


##去除相似文本信息
def get_deduplication(alpha, th=0.9):
    model = SentenceTransformer('D:\\model\\m3e')

    batch_size = 512 
    #pool = model.start_multi_process_pool()
    # batches = [alpha[i:i + batch_size] for i in range(0, len(alpha), batch_size)]
    # embedding = model.encode_multi_process(alpha, pool, batch_size=batch_size)
    embedding = model.encode(alpha, batch_size=batch_size)
    # embedding = model.encode([k for k in alpha])
    print("embedding_success")
    # 计算相似度矩阵
    similarity_matrix = util.cos_sim(embedding, embedding)
    # 找到相似度大于0.9的元素，并记录要删除的索引
    to_delete = set()
    threshold = th
    rows, cols = np.where(similarity_matrix > threshold)
    filtered_pairs = [(r, c) for r, c in zip(rows, cols) if r < c]
    for r, c in filtered_pairs:
        to_delete.add(c)
    print("to_delete", str(len(to_delete)))
    # 删除相似的元素
    #alpha = [item for idx, item in enumerate(alpha) if idx not in to_delete]
    return to_delete

