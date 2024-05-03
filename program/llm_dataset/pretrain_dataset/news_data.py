from data_conn.mysql8.mysql_conn import *
import re
def remove_multi_symbol(text):
    r = re.compile(r'([.,，/\\#!！？?。$%^&*;；:：{}=_`´︵~（）()-])[.,，/\\#!！？?。$%^&*;；:：{}=_`´︵~（）()-]+')
    text = r.sub(r'', text)
    pattern = r'【责任编辑:[\u4e00-\u9fff]{1,10}】'
    text = re.sub(pattern, '', text)
    return text
content_all = ""
mysql = MySql()
query = "SELECT title,content,published FROM `q_intelligence`.`news1`"
data = mysql.sql_search(query)
dict1 = {}
for i in data:
    title = i[0]
    content = (remove_multi_symbol(i[1]).replace("\n", "").
               replace("  ", "").replace(" ", "").replace("【纠错】","").
               replace("【责任编辑:王金志】","").replace("原标题：","").replace(u'\xa0', '')
               )
    content = "".join(str(content).split())
    time = str(i[2])
    pattern = r'[^\u4e00-\u9fff]'
    pat = re.sub(pattern, '', content[0])
    if pat:
        print(time)
        print(content)
        res = "时间为：" +time + "," +content + ";"
        content_all += res

with open("news.txt", "w", encoding="utf-8") as txt_file:
    txt_file.write(content_all)
