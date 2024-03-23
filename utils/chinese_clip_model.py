from PIL import Image
import requests
from transformers import ChineseCLIPProcessor, ChineseCLIPModel
import torch
from io import BytesIO
device = torch.device("mps")

class ChineseClipModel():
    def __init__(self, model_path="D:\model\chinese-clip-vit-base-patch16"):
        self.model = ChineseCLIPModel.from_pretrained(model_path)
        self.processor = ChineseCLIPProcessor.from_pretrained(model_path)
        # self.model.to(device)
    def generate_image_features(self, image):
        inputs = self.processor(images=image, return_tensors="pt")
        with torch.no_grad():
            image_features = self.model.get_image_features(**inputs)
            image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)
        return image_features

    def generate_image_features_m(self, image):
        # image = Image.open(requests.get(path, stream=True).raw)
        inputs = self.processor(images=image, return_tensors="pt")
        with torch.no_grad():
            image_features = self.model.get_image_features(**inputs)
            image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)
        return image_features.squeeze(0).tolist()

    def generate_text_features(self, text):
        inputs = self.processor(text=text, padding=True, return_tensors="pt")
        with torch.no_grad():
            text_features = self.model.get_text_features(**inputs)
            text_features = text_features / text_features.norm(p=2, dim=-1, keepdim=True)
        return text_features

    def get_simliar_tp(self,texts,image):
        inputs = self.processor(text=texts, images=image, return_tensors="pt", padding=True)
        outputs = self.model(**inputs)
        logits_per_image = outputs.logits_per_image  # this is the image-text similarity score
        probs = logits_per_image.softmax(dim=1)
        return probs

    def __call__(self, image, text):
        return self.model(image, text)

if __name__ == '__main__':
    clip = ChineseClipModel()
    url = "https://clip-cn-beijing.oss-cn-beijing.aliyuncs.com/pokemon.jpeg"
    url1 = "http://152.136.174.19:9000/minio/pictures/news/2024-03-23/1.jpg"
    image = Image.open(requests.get(url, stream=True).raw)
    image.show()
    # Squirtle, Bulbasaur, Charmander, Pikachu in English
    # texts = ["杰尼龟", "妙蛙种子", "小火龙", "皮卡丘"]
    # embeding = clip.generate_image_features(image).squeeze(0).tolist()
    # print(embeding)
