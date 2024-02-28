import os

env = os.getenv('env')
# 内网数据库
info = '@'*50 + ' {} ' + '@'*50
if not env:
    print(info.format('服务器内网生产环境') + '\n' + info.format('服务器内网生产环境'))
    from app_api.settings.setting import *
# 公网数据库
elif env == 'local':
    print(info.format('本地生产环境') + '\n' + info.format('本地生产环境'))
    from app_api.settings.local_settings import *