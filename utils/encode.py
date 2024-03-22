from transformers import BertTokenizer, BertModel
import torch

class SentenceModel:
    """
    SentenceModel
    """

    def __init__(self,model_name="D:\\model\\m3e"):
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name)
        self.max_length = 512

    def sentence_encode(self,text):
        encoded_dict = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
        input_id = encoded_dict['input_ids']
        attention_mask = encoded_dict['attention_mask']

        # 前向传播
        with torch.no_grad():
            outputs = self.model(input_id, attention_mask=attention_mask)

        # 提取最后一层的CLS向量作为文本表示
        last_hidden_state = outputs.last_hidden_state
        cls_embeddings = last_hidden_state[:, 0, :]
        return cls_embeddings[0]


if __name__ == '__main__':
    MODEL = SentenceModel()
    # Warm up the model to build image
    result = MODEL.sentence_encode(['hello world'])
    print(result)
    print(len(result))

