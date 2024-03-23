from urllib import request
from data_conn.mysql8.mysql_conn import *
import ast
mysql = MySql()
url = "https://cdn.sputniknews.cn/img/07e4/0c/08/1032676708_0:63:1201:738_1920x0_80_0_0_cee43b287494bf97375311d22afe71e4.jpg"
path = "D:\\langchain_applicable-doc\\images\\"
query = "SELECT id,external_images FROM `q_intelligence`.`news1`"
data = mysql.sql_search(query)
dict1 = {}
i = 0
for item in data:
    external_images = item[1]
    result = "[" + external_images[2:-2] + "]"
    result = ast.literal_eval(result)
    if len(result)>=1:
        result = result[0]
        try:
            if result.endswith(".jpg") or result.endswith(".jpeg") or result.endswith(".png"):
                filename = path + str(item[0]) + ".jpg"
                request.urlretrieve(result, filename)
        except:
            pass
