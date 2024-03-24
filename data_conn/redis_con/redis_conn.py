import redis

# r = redis.Redis(host='152.136.174.19', port=6379, db=0)
class RedisService:
    def __init__(self):
        # self.pool = redis.ConnectionPool(host='152.136.174.19', port=6379, db=1, decode_responses=True)
        self.r = redis.Redis(host='152.136.174.19', port=6379, db=0,decode_responses=True)

    def set_key(self, key, value, expire=None):
        self.r.set(key, value, expire)

    def get_key(self, key):
        return self.r.get(key)

    def insert_dict(self,name,dict_list):
        return self.r.hmset(name, dict_list)

    ##取单值
    def get_dict(self,name,key):
        return self.r.hget(name, key)

    def get_mdict(self,name,key_list):
        return self.r.hmget(name, key_list)

    def len_dict(self, name):
        return self.r.hlen(name)

    def get_alldict(self, name):
        return self.r.hgetall(name)

    ##todo 获取redisstring输入key与value
    def insert_string(self,dict1):
        return self.r.mset(dict1)

    def get_stringvalue(self,key_list):
        return self.r.mget(key_list)










