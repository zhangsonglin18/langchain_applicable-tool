from data_conn.mysql8.mysql_conn import *
from data_conn.redis_con.redis_conn import *
import json
mysql = MySql()
redis = RedisService()

##todo 测试redis存储dict值
# r.set('name', 'junxi')  # key是"name" value是"junxi" 将键值对存入redis缓存
# print(r['name'])
# mysql = MySql()
# query = "SELECT id,external_images FROM `q_intelligence`.`news1`"
# data = mysql.sql_search(query)
# dict1 = {}
# for item in data:
#     id = item[0]
#     external_images = item[1]
# dict1 = {item[0]: item[1] for item in data}
# print(dict1)
# redis.insert_dict('m1', dict1)

def insert_dict(data,r,name="m2"):
    dict1 = {item[0]: item[1] for item in data}
    r.insert_dict(name,dict1)

##todo 测试redis存储list值
    # query = "SELECT id,external_images FROM `q_intelligence`.`news1`"
    # data = mysql.sql_search(query)
    # dict1 = {item[0]: item[1] for item in data}
    # redis.r.mset(dict1)

if __name__ == '__main__':
    # redis.r.lpush('queue', 'message')
    # message = redis.r.rpop('queue')
    # print(message)
    # redis.r.save()
    mysql = MySql()
    query = "SELECT id,external_images FROM `q_intelligence`.`news1`"
    data = mysql.sql_search(query)
    dict1 = {}
    for item in data:
        id = item[0]
        external_images = item[1]
    dict1 = {item[0]: item[1] for item in data}
    print(dict1)
    redis.insert_dict('m1', dict1)





