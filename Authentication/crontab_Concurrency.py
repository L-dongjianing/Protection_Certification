#redis库
import time

import redis
CONCURRENT = 550 #10/分钟最大并发数
REDIS_CONF_db14 = {
    "redis_host": "r-0jltklkgko5keufkclpd.redis.rds.aliyuncs.com",  #
    # "redis_host": "172.21.6.197",  #
    "redis_passwd": "Xueyiyang!",  # 本机器未设置
    "redis_port": 55379,
    # > 数据库库名
    # 搜索队列
    "db_search": 1,

    "db_other": 12,
    "search_queue_status_key": "HotBoardAllNew"
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