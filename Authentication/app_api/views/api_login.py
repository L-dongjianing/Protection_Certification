import json
import random
import time
from app_api.views.sign  import pc
from tool import str_md5
from flask import Blueprint,request
from app_api.settings import AUTHENTICATE,PROFILE,redis_data,EFFECTIVENESS,CONCURRENT
from jwt_ import Jwt
from tool import  role_verify_sel,api_result,role_verify_up
api_login = Blueprint('api_login', __name__, )

@api_login.route('/')
def hello():
    return api_result(data='认证中心', code=200)

#用户首次登陆验证
@api_login.route('/first/verify_user/', methods=['POST'])
def verify_user():
    print(request.form)
    print(type(request.form))
    # 获取前端传递的参数
    username = request.form.get('uname','')  #用户名
    password = str_md5(str(request.form.get('password',''))) #密码
    ip =  request.form.get('presentIP','')  #ip
    if username and password and ip:
        insert_sql = f'select uid,login_type,expiration,state,level from {AUTHENTICATE} where u_name="{username}" and u_passwd="{password}"'
        data = role_verify_sel(insert_sql) #调用sql 的返回值
        if data:
            dic_user = data[0] #用户信息
            new_data = dic_user
            new_data['present'] = ip
            token = Jwt.encode(new_data, "77897159", EFFECTIVENESS)  #jwt生成
            dic_user['tok'] = token.decode() #字节转字符串
            print('tok')
            print(dic_user['tok'])
            # 登陆成功后 redis添加最大吞吐数
            cache = redis_data #连接redis
            cache.sadd(f'{ip}_{dic_user.get("uid")}',CONCURRENT)#创建最大并发数量
            cache.expire(f'{ip}_{dic_user.get("uid")}',EFFECTIVENESS)#设置过期时间
            cache.hset('Land',f'{ip}_{dic_user.get("uid")}',int(time.time())+EFFECTIVENESS) #总键

            return api_result(data=dic_user, code=200)

        else:
            return api_result(msg='用户不存在', code=401)
    else:
        return  api_result(msg='缺少必要参数',code=401)


#用户注册
@api_login.route('/information/contact/register/', methods=['POST'])
def contact_register():
    # 获取前端传递的参数
    username = request.form.get('uname','')
    password = str_md5(request.form.get('password',''))
    expiration = int(request.form.get('expiration',1024)) #截止日期时间戳
    if username and password:
        sel_sql = f'select name_md5 from {AUTHENTICATE} where name_md5="{str_md5(username)}"'
        data = role_verify_sel(sel_sql)  #先判断用户是否存在了
        if data:
            return api_result(msg='用户已存在', code=200)

        else:
            uid = int(random.randint(111, 999)+int(time.time())/1000) #唯一uid
            print('我当前在打印uid',uid)
            insert_pro =f'insert into {PROFILE} (uid,u_name) values ("{uid}","{username}")'
            role_verify_up(insert_pro)
            insert_au = f'insert into {AUTHENTICATE} (uid,u_name,u_passwd,name_md5,login_type,expiration,state,level) values ("{uid}","{username}","{password}","{str_md5(username)}",1,{expiration},1,2)'
            role_verify_up(insert_au)
            return api_result(msg='注册成功',code=200)
    else:
        return  api_result(msg='缺少必要参数',code=401)

@api_login.route('/demo/', methods=['POST'])
def demo():
    print('接口内部打印form')
    print(request.form)
    return api_result(msg='成功',code=200,data={'age':18,'name':'djn'})



# ##钩子函数 (接口执行之后执行
@api_login.after_request
def after_request(response):
    try:
        on_data = json.loads(response.data)
        # print(on_data)
    except Exception as e:
        print('接口执行后报错了：',e)
        return response
    if on_data.get('code') == 200:
        try:
            on_data['data'] = pc.encrypt(pc.iv + str(on_data.get('data')))  # 传过去数据在加密
        except:
            # print(pc.iv)
            on_data['data'] = pc.encrypt(pc.iv.decode(encoding='UTF-8') + str(on_data.get('data')))  # 传过去数据在加密
        # print(on_data['data'])
        on_data = json.dumps(on_data)
        response.data = on_data
        return response
    else:
        return response

