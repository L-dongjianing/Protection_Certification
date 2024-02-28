import redis

#redis配置库（本地）
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
#mysql配置库（本地）
DATABASES_MYSQL_DATA = {

    'USER': 'root', #用户名
    'PASSWORD': '', #密码
    'HOST': 'localhost', #mysql地址
    'PORT': 3306, #端口
    'NAME': 'role_verify',
    'CHARSET': 'utf8mb4',
}

AUTHENTICATE = 'authenticate' #认证用户表
PROFILE = 'profile' #用户个人信息报表
EFFECTIVENESS = 43200 #实效性
CONCURRENT = 550 #10/分钟最大并发数