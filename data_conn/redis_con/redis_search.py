from data_conn.redis_con.redis_conn import *
import json
redis = RedisService()
import ast
def search_mdict(name,key):
    # result = redis.get_mdict(name, key)
    value = redis.get_dict(name, key)
    dict_lens = redis.len_dict(name)
    # value= [char for char in value if not char.isascii()]
    return value,dict_lens

##todo 获取图片的地址信息
def get_news_pic(name = "m1",key = 3007):
    result, dict_lens = search_mdict(name,key)
    result ="["+result[2:-2]+"]"
    result = ast.literal_eval(result)
    return result[0]

if __name__ == '__main__':
    # name = "m1"
    values = redis.r.mget([6947, 6202])
    # print(type(json.loads(result)))
    print(values)
