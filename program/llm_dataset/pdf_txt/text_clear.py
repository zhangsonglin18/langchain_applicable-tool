from harvesttext import HarvestText
ht0 = HarvestText()
from program.llm_dataset.pdf_txt.nltk_clear import *
def clear_txt(path):
    with open(path, 'r',encoding="utf-8") as f:
        content = f.read()
        content = clean_code(content).replace("天涯kk完整版此文档为PDF精编版，已设置好、","")
        pattern = r'作者.*?日期-[^\u4e00-\u9fff]+'
        content = re.sub(pattern, '', content)
        pattern = r'\{.*?\}.*?'
        content = re.sub(pattern, '', content)
        pattern = r'\.\*{2,15}[/|-]\d{1,}[/|-]\d{1,}'
        content = re.sub(pattern, '', content)
        pattern = r'\*{2,15}[^\u4e00-\u9fff]+\*{2,15}'
        content = re.sub(pattern, '', content)
        pattern = r'目录.*总论一'
        content = re.sub(pattern, '', content)
        pattern = r'•[^\u4e00-\u9fff]+'
        content = re.sub(pattern, '', content)
        result = ht0.clean_text(content)
        return result
import os
text_out = ""
source_folder = "D:/model/data_set/docs_out"
for filename in os.listdir(source_folder):
    if filename.endswith(".txt"):
        file_path = os.path.join(source_folder, filename)
        text = clear_txt(file_path)
        text_out += text
with open("tianya.txt", "w", encoding="utf-8") as txt_file:
    txt_file.write(text_out)

