
import redis






#redis库
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
# 连接redis
redis_data = redis.Redis(host=REDIS_CONF_db14.get("redis_host"),
                         port=REDIS_CONF_db14.get("redis_port"),
                         decode_responses=True,
                         password=REDIS_CONF_db14.get("redis_passwd"),
                         db=REDIS_CONF_db14.get("db_other"))



DATABASES_MYSQL_DATA = {

    'USER': 'root',
    'PASSWORD': 'hexi123456!',
    # 'HOST': 'rm-0jlw6a7q3e3c0bp911o.mysql.rds.aliyuncs.com',
    'HOST': '172.21.6.204',
    'PORT': 55306,
    'NAME': 'web_role_management',
    'CHARSET': 'utf8mb4',
}
# print(USER_REDIS_CONF_db14)

AUTHENTICATE = 'authenticate' #认证用户表
PROFILE = 'profile' #用户个人信息报表
EFFECTIVENESS = 43200 #实效性
CONCURRENT = 550 #10/分钟最大并发数