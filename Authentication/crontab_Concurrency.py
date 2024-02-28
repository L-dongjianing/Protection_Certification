#redis库
import time

import redis
CONCURRENT = 550 #10/分钟最大并发数
REDIS_CONF_db14 = {
    "redis_host": "127.0.0.1",  # redis地址
    "redis_passwd": "",  # 本地尚未设置
    "redis_port": 6379,  #端口
    "db_other": 14, #数据库库名
}

#链接redis
redis_data = redis.Redis(host=REDIS_CONF_db14.get("redis_host"),
                         port=REDIS_CONF_db14.get("redis_port"),
                         decode_responses=True,
                         password=REDIS_CONF_db14.get("redis_passwd"),
                         db=REDIS_CONF_db14.get("db_other"))

def run():
    cache = redis_data
    all_key = cache.hkeys('Land') #获取全部key
    for i in all_key:
        if int(time.time())>int(cache.hget('Land',i)): #判断过期时间
            #重制并发量
            cache.sadd(i,CONCURRENT)#创建最大并发数量
        else:
            cache.hdel('Land',i) #已过期删除

if __name__ == '__main__':
    run()