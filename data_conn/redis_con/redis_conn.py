import redis
import time
# redis_conn = redis.Redis(host='152.136.174.19', port= 6379, db= 0)
# print(redis_conn.ping())
# key = redis_conn.keys()
# print(key)

pool = redis.ConnectionPool(host='152.136.174.19', port= 6379, db=0, decode_responses=True)
r = redis.Redis(connection_pool=pool)  # 或者用redis.StrictRedis

key = r.keys()
print(key)
r.set('test', '123456', ex=10)  # 设置键 test的值为123456，过期时间为3秒
print("test的值为：{}".format(r.get('test')))

time.sleep(10)
print("10秒后test的值为：{}".format(r.get('test')))
