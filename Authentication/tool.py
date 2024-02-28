import hashlib
import pymysql
from app_api.settings import DATABASES_MYSQL_DATA,redis_data
from itsdangerous import json
import  redis
import datetime
# md5加密
def str_md5(_str: str):
    return hashlib.md5(_str.encode()).hexdigest()

# 数据库配置
def get_mysql_migrate(host=DATABASES_MYSQL_DATA.get('HOST'), user=DATABASES_MYSQL_DATA.get('USER'),
                      password=DATABASES_MYSQL_DATA.get('PASSWORD'), database=DATABASES_MYSQL_DATA.get('NAME'),
                      port=DATABASES_MYSQL_DATA.get('PORT'), charset=DATABASES_MYSQL_DATA.get('CHARSET')):
    return pymysql.connect(host=host, user=user,
                           password=password, database=database,
                           port=port, charset=charset)

#用户库连接查询
def role_verify_sel(format_sql, format_values=(), cursor_setting=pymysql.cursors.DictCursor):
    con = get_mysql_migrate()
    cur = con.cursor(cursor_setting)
    cur.execute(query=format_sql, args=format_values)
    data = cur.fetchall()
    cur.close()
    con.close()
    return data

#用户库连接更新、插入
def role_verify_up(format_sql, format_values=(), cursor_setting=pymysql.cursors.DictCursor):
    con = get_mysql_migrate()
    cur = con.cursor(cursor_setting)
    cur.execute(query=format_sql, args=format_values)
    con.commit()
    data = cur.fetchall()
    cur.close()
    con.close()
    return data

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

# 接口返回的json数据结果格式
def api_result(data=None, code=200,  msg='成功'):
    r_data = {}
    if data is not None:
        r_data['data'] = data
    r_data['msg'] = msg
    r_data['code'] = code
    return json.dumps(r_data, cls=DateEncoder)


#验证并发数量
def throughput(token):
    cache = redis_data  #连接
    try:
        ex = cache.ttl(f'{token.get("present")}_{token.get("uid")}') #获取过期时间
        print('ex',ex)
        num = int(cache.spop(f'{token.get("present")}_{token.get("uid")}')) #当前剩余并发数
        cache.sadd(f'{token.get("present")}_{token.get("uid")}',int(num)-1) #当前请求-
        cache.expire(f'{token.get("present")}_{token.get("uid")}', ex)  # 设置过期时间
        # 1
        if num <=0:
            return '401'
        else:
            return '200'
    except:
        print('用户登陆已经过期了')
        return'401'


if __name__ == '__main__':
    print(str_md5('admin_1'))