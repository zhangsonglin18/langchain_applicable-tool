from nltk import word_tokenize as wt  # 分词库
from nltk.stem import WordNetLemmatizer  # 词形还原库
from nltk.corpus import stopwords  # 停用词库
from nltk.tag import pos_tag
import re
import nltk
import jieba
def clean_code(codes):
    code = codes
    # 删除单行注释
    code = re.sub(r'//.*$', '', code)
    code = re.sub(r'@.*$', '', code)
    # 匹配并删除"/**/"之间的内容
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)  # flags=re.DOTALL匹配文本中所有字符
    # 删除多余文本
    code = re.sub(r'Nonnull|Nullable', '', code, flags=re.MULTILINE)  # flags=re.MULTILINE为多行匹配
    code = re.sub(r'{(\w+)\s+public', '{public', code, flags=re.MULTILINE)
    code = re.sub(r'{(\w+)\s+private', '{private', code, flags=re.MULTILINE)
    code = re.sub(r'{(\w+)\s+protected', '{protected', code, flags=re.MULTILINE)
    code = re.sub(r'(\w+)\s+final', 'final', code, flags=re.MULTILINE)
    code = re.sub(r'(\w+)\s+default', 'default', code, flags=re.MULTILINE)
    # 单引号替换为双引号
    code = re.sub(r"'", '"', code)
    # 删除特殊符号
    code = re.sub(r'[@#$&%~`\\……|]', '', code, flags=re.MULTILINE)
    # 删除换行、多余空格和多余括号
    code = re.sub(r'\s+', ' ', code, flags=re.MULTILINE)
    code = re.sub(r'\(\s+', '(', code, flags=re.MULTILINE)
    code = re.sub(r'\s+\)', ')', code, flags=re.MULTILINE)
    code = re.sub(r'\{\s+', '{', code, flags=re.MULTILINE)
    code = re.sub(r'\s+}', '}', code, flags=re.MULTILINE)
    code = code.strip()
    return code

def splitStop(data_split): # 创建停用词列表
    # 从txt文档中读取停用词，放进列表中
    path_stop = 'stop_list.txt'
    def stopwordslist(): # 返回列表
        with open(path_stop, 'r', encoding='utf-8', errors='ignore') as f:
            stopwords = [line.strip() for line in f.readlines()]
        return stopwords

    stop_words_list = stopwordslist()
    stopwords = {}.fromkeys(stop_words_list)
    # 建立一个函数去掉字符串中的停用词
    def cutStopWords(word):
        segs = jieba.cut(word, cut_all=False)
        final = ''
        for seg in segs:
            if seg not in stopwords:
                final += seg
                final +=' '
        return final
    splitStopData = cutStopWords(data_split)
    return splitStopData

def data_clean(x):
    x = x.encode('ascii', 'ignore').decode()     # 删除 unicode 字符（乱码,例如：pel韈ula）
    x = re.sub("@\S+", " ", x)                   # 删除提及(例如：@zhangsan)
    x = re.sub("https*\S+", " ", x)              # 删除URL链接
    x = re.sub("#\S+", " ", x)                   # 删除标签（例如：#Amazing）
    x = re.sub("\'\w+", '', x)                   # 删除记号和下一个字符（例如：he's）
    x = re.sub(r'[’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！\[\\\]^_`{|}~]+', ' ', x)   # 删除特殊字符
    x = re.sub(r'\w*\d+\w*', '', x)              # 删除数字
    x = re.sub('\s{2,}', " ", x)                 # 删除2个及以上的空格                             # 删除两端无用空格
    return x


if __name__ == '__main__':
    text = "新民主主义革命是什么革命.*****、西部城市..*****、新穷三代..*****、网友求教房产投资实操集锦.*****、拉美的生活水平..*****、砖家与媒体..*****、人民币资产兑换转移.*****、投资房产不是炒股.*****、中国与西方最大的不同.*****、GDP保8..*****、中国可以无限印钞票吗？.*****、三国志：..*****、贵阳.*****、政府精减膨胀..*****、深圳.*****、长春.*****、济南的房市..*****、哈尔滨.263446、重庆.*****、俄罗斯.*****、珠海.*****、苏州.*****、房奴苏东坡..*****、开书单.*****、王安石变法..*****、空空没钱？..30651、总论一、2010年的房地产调控，让很多人看到了希望：让房价降得再猛烈些吧。"
    print(data_clean(text))



