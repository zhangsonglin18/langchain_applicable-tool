from transformers import BertTokenizer, BertModel
import torch


class M3E_embeddings:
    def __init__(self,max_length=768):
        self.model_name = 'D:\model\m3e'
        self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
        self.model = BertModel.from_pretrained(self.model_name)
        # self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        # self.model.to(self.device)
        # self.model.eval()
        self.max_length = max_length
    def embeddings_text(self,text, max_length = 512):
        encoded_dict = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=max_length,
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