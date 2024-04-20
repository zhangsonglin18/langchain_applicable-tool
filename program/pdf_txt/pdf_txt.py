import os
from langchain.document_loaders import PyPDFLoader
import re
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
# 源文件夹路径
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        # chunk_size=768,
        chunk_overlap=3000,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

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
def find_regular(content_raw):
    """去除内容中的各种信息"""
    content_raw1 = content_raw.replace('#', ' ').replace('【', '').replace('】', '').replace('<p>', ' ').replace('</p>', ' ')
    regular = re.compile(r'[a-zA-Z]+://[^\s]*[.com|.cn][/*\S*]*')  # 去除网址
    content = regular.sub('', content_raw1)
    results = re.compile(r'[http|https]*:[a-zA-Z0-9.?/]*', re.S)
    content = re.sub(results, '',content)
    content = mask_privacy(content, privacy_patterns)
    return content
def remove_multi_symbol(text):
    r = re.compile(r'([.,，/\\#!！？?。$%^&*;；:：{}=_`´︵~（）()-])[.,，/\\#!！？?。$%^&*;；:：{}=_`´︵~（）()-]+')
    text = r.sub(r'\1', text)
    pattern = r'作者日期-[^\u4e00-\u9fff]+'
    text = re.sub(pattern, '', text)
    return text

# pdf_file_path = "D:/model/data_set/tianya-docs-main/docs/15-戏说牛市合适崩盘.pdf"
def pdf_get(pdf_file_path):
    loader = PyPDFLoader(pdf_file_path)
    documents = loader.load()
    text_out =""
    for item in documents:
        text = remove_multi_symbol(item.page_content).replace("\n", "").replace(" ", "").replace("———","")
        text1 = get_text_chunks(find_regular(text))
        for item in text1:
            text_out += "".join(item)
    return text_out
# print(pdf_get(pdf_file_path))
target_folder = "docs_out"
if not os.path.exists(target_folder):
    os.makedirs(target_folder)
text_out = ""
source_folder = "D:/model/data_set/tianya-docs-main/docs"
for filename in os.listdir(source_folder):
    if filename.endswith(".pdf"):
        file_path = os.path.join(source_folder, filename)
        text = pdf_get(file_path)
        text_out += text
        print(text)
        txt_file_path = os.path.join(target_folder, filename.replace(".pdf", ".txt"))
        with open(txt_file_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(text_out)

# print(documents)
# source_folder = "D:\\daku\\东鹏\\pdf"
# # 目标文件夹路径，用于保存TXT文件
# target_folder = "D:\\daku\\东鹏\\txt_exports"
# # 如果目标文件夹不存在，则创建它
# if not os.path.exists(target_folder):
#     os.makedirs(target_folder)
#
# # 遍历源文件夹中的所有文件
# for filename in os.listdir(source_folder):
#     if filename.endswith(".pdf"):
#         # 构建完整的文件路径
#         file_path = os.path.join(source_folder, filename)
#         loader = PyPDFLoader(file_path)
#         documents = loader.load()

        # 使用pdfplumber打开PDF文件
        # with pdfplumber.open(file_path) as pdf:
        #     # 初始化一个空字符串来保存文本内容
        #     text = ""
        #     # 遍历PDF中的每一页
        #     for page in pdf.pages:
        #         # 提取页面的文本并添加到text变量中
        #         text += page.extract_text()
        #         text += "\n\n"  # 添加换行符以分隔不同页面的内容
        # # 构建目标TXT文件的路径，文件名保持不变，只是扩展名改为.txt
        # txt_file_path = os.path.join(target_folder, filename.replace(".pdf", ".txt"))
        # # 将文本内容写入TXT文件
        # with open(txt_file_path, "w", encoding="utf-8") as txt_file:
        #     txt_file.write(text)
        # print(f"已转换文件: {filename} -> {txt_file_path}")