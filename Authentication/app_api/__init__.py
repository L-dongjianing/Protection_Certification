import json
from jwt_ import Jwt
from app_api.views import init_view
from flask import Flask, request
from flask_cors import CORS
from app_api.views.sign import pc
from tool import  api_result,throughput
import app_api
# import app_Interface
# > Flask
FLASK_CONF = {
    'SECRET_KEY': 'vr^%WH5wB(y3)5e1^VVw2Pw(k10nByAQzdNOwM(Bzn$*9@9uP^EvLuVht4qgPMdL'  # 64 !@#$%^&*()_+ 1Aa
}
app = Flask(__name__)


def create_app():
    # app创建
    # 配置导入
    app.config.update()
    # 设置跨域
    CORS(app, supports_credentials=True)
    # 初始化第三方
    # init_ext(app)
    # 初始化应用
    # app_Interface.__init__(app)
    app_api.__init__(app)

    return app

def __init__(app):
    init_view(app)



# ##钩子函数 (接口执行前执行 解密sign
@app.before_request
def before_request():
    # 加密部分
    if request.method == 'POST':
        post_form = request.form.get('sign', '')
        try:
            post_json = request.get_json().get('sign', '')
        except:
            post_json = ''
        if  'first/verify_user' in  request.url:  #走登陆接口
            print('走登陆接口')
            print(post_form)
            # 以下是解密
            try:
                if post_form:
                    sign = json.loads(pc.decrypt(post_form))
                    request.form = sign
                elif post_json:
                    sign = json.loads(pc.decrypt(post_json))
                    request.form = sign
            except Exception as e:
                print('错误信息：',e)
                print('解密失败')
                return api_result(msg='缺少必要参数', code=401)
        else:
            # 以下是解密
            try:
                if post_form:
                    sign = json.loads(pc.decrypt(post_form))
                    request.form = sign
                elif post_json:
                    sign = json.loads(pc.decrypt(post_json))
                    request.form = sign
            except:
                print('解密失败')
                return api_result(msg='缺少必要参数', code=401)
            # print('解析完成：',request.form)
            #以下是判断token与ip是否一致
            ip = request.headers.get('Serialgate', '') #用户每次请求的ip
            token = request.headers.get('Publicprotect', '') #token
            if ip and token:
                # print('进来了')
                try: #解成功了
                    token = Jwt.decode(token.encode('Utf-8'),"7749") #token解析
                    # token = etoken) #字符串转字典
                    if str(token.get('present','')) != str(ip):
                        return  api_result(msg='登录失效、请重新登陆',code=401)
                    #验证并发（是否为人工操作）
                    inspect = throughput(token)
                    if inspect != '200':
                        return api_result(msg='账号访问异常请注意操作',code=401)
                except Exception as e: #用户登录时效过期了
                    print('错了',e)
                    return api_result(msg='缺少必要参数',code=401)
            else:
                return api_result(msg='缺少必要参数',code=401)

