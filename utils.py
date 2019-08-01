# coding:utf-8
__author__ = "gaunt"

from hashlib import md5
import json
from datetime import datetime, date
import conf
from conf import redis_conn_param as redis_config
import jwt
import enums
from functools import wraps
from bottle import request
import redis
from peewee import DoesNotExist
from singletons import Log


def md5_salt(pwd, salt=""):
    """
    MD5加密
    :param pwd:     明文密码
    :param salt:    盐
    :return:
    """
    if pwd == "":
        return ""
    md5_obj = md5()
    md5_obj.update((pwd + salt).encode("utf-8"))
    return md5_obj.hexdigest()

####################################################################################################


class ComplexEncoder(json.JSONEncoder):
    """
    json日期格式化
    """
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

####################################################################################################


class TokenUtil(object):
    @staticmethod
    def encode_auth_token(user_id):
        """
        生成认证Token
        :param user_id:
        :return:
        """
        try:
            payload = {
                'data': {
                    'user_id': user_id
                }
            }
            return jwt.encode(payload, conf.jwt_key, algorithm=conf.jwt_algorithm).decode("utf-8")
        except Exception as e:
            return None

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return:
        """
        try:
            # 取消过期时间验证 options={'verify_exp': False}
            payload = jwt.decode(auth_token, conf.jwt_key, algorithm=conf.jwt_algorithm, options={'verify_exp': False})
            if 'data' in payload and 'user_id' in payload['data']:
                return payload
            else:
                return '无效Token'
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'

    def get_user_id(self):
        """
        直接获取 user_id , 因为请求之前已经调用identify方法判断token信息了
        :return:
        """
        auth_header = request.headers.get('Authorization')
        auth_token_arr = auth_header.split(" ")
        auth_token = auth_token_arr[1]
        payload = self.decode_auth_token(auth_token)
        return payload["data"]["user_id"]

    def identify(self, request):
        """
        用户鉴权
        :return: list
        """
        code = enums.ResultEnum.error401.value["code"]
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token_arr = auth_header.split(" ")
            flag = auth_token_arr[0]
            if not auth_token_arr or (flag != 'JWT' and flag != 'Bearer') or len(auth_token_arr) != 2:
                result = enums.error_result(code=code, msg='请传递正确的验证头信息')
            else:
                auth_token = auth_token_arr[1]
                payload = self.decode_auth_token(auth_token)
                if not isinstance(payload, str):
                    user = SysUserDao.get(payload['data']['user_id'])
                    if user is None:
                        result = enums.error_result(msg='找不到该用户信息')
                    else:
                        if user.state == enums.UserStateEnum.NORMAL.value:
                            result = enums.success_result(data=user.user_id)
                        else:
                            result = enums.error_result(msg='该账号已被冻结，请联系管理员')
                else:
                    result = enums.error_result(code=code, msg=payload)
        else:
            result = enums.error_result(code=code, msg='没有提供认证token')
        return result

####################################################################################################


def permissions_auth(value=None, logical=enums.Logical.AND.value):
    """
    权限认证
    :param value:
    :param logical:
    :return:
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            error401 = enums.ResultEnum.error401.value
            if value:
                # 获取该请求的user_id
                user_id = TokenUtil().get_user_id()

                # 获取该用户的所有权限
                auths = RedisUtil().hget(conf.prefix_permit, user_id)
                if auths:  # 有数据
                    auths = json.loads(auths)
                    if isinstance(value, str):
                        if value not in auths:
                            return enums.error_result(code=error401["code"], msg="您没有该权限")
                    elif isinstance(value, list):
                        bo = []  # 一个成功的标识
                        for val in value:
                            if val in auths:
                                bo.append(True)
                        if logical == enums.Logical.AND.value:
                            if len(value) != len(bo):
                                return enums.error_result(code=error401["code"], msg="您没有该全部权限")
                        else:
                            if len(bo) == 0:
                                return enums.error_result(code=error401["code"], msg="您没有该权限")
                    else:
                        return enums.error_result(code=error401["code"], msg="参数只支持 str 和 list")
                else:  # 无数据
                    return enums.error_result(code=error401["code"], msg="该用户没有权限")
            else:
                return enums.error_result(code=error401["code"], msg="参数不能为空")
            # 后续操作
            rv = f(*args, **kwargs)
            return rv
        return decorated_function
    return decorator


def permissions_role(value=None, logical=enums.Logical.AND.value):
    """
    角色认证
    :param value:
    :param logical:
    :return:
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            error401 = enums.ResultEnum.error401.value
            if value:
                # 获取该请求的user_id
                user_id = TokenUtil().get_user_id()

                # 获取该用户的所有角色
                roles = RedisUtil().hget(conf.prefix_role, user_id)
                if roles:  # 有数据
                    roles = json.loads(roles)
                    if isinstance(value, str):
                        if value not in roles:
                            return enums.error_result(code=error401["code"], msg="您没有该角色")
                    elif isinstance(value, list):
                        bo = []  # 一个成功的标识
                        for val in value:
                            if val in roles:
                                bo.append(True)
                        if logical == enums.Logical.AND.value:
                            if len(value) != len(bo):
                                return enums.error_result(code=error401["code"], msg="您没有该全部角色")
                        else:
                            if len(bo) == 0:
                                return enums.error_result(code=error401["code"], msg="您没有该角色")
                    else:
                        return enums.error_result(code=error401["code"], msg="参数只支持 str 和 list")
                else:  # 无数据
                    return enums.error_result(code=error401["code"], msg="该用户没有角色")
            else:
                return enums.error_result(code=error401["code"], msg="参数不能为空")
            # 后续操作
            rv = f(*args, **kwargs)
            return rv
        return decorated_function
    return decorator

####################################################################################################


pool = redis.ConnectionPool(host=redis_config["host"], port=redis_config["port"], db=redis_config["db"],
                            password=redis_config["password"], max_connections=redis_config["max_connections"])
redis_conn = redis.StrictRedis(connection_pool=pool)


class RedisUtil(object):
    """
    Redis工具类
    """
    def set(self, key, value, ex=-1):
        redis_conn.set(key, value, ex)

    def get(self, key):
        return redis_conn.get(key)

    def deltele(self, key):
        redis_conn.delete(key)

    def hset(self, name, key, value):
        redis_conn.hset(name, key, value)

    def hget(self, name, key):
        return redis_conn.hget(name, key)

####################################################################################################


def decorator_does_not_exist(fc):
    """
    使用peewee获取单条数据为空时会出DoesNotExist异常
    :param fc:
    :return:
    """
    @wraps(fc)
    def decorated_function(*args, **kwargs):
        try:
            res = fc(*args, **kwargs)
            return res
        except DoesNotExist as e:
            Log().warn("获取数据失败。" + str(e) + "， args：【" + json.dumps(args) + "】，kwargs：【" + json.dumps(kwargs) + "】")
            return None
    return decorated_function


from models import SysUserDao

if __name__ == "__main__":
    print(md5_salt('123456', 'gaunt'))

    tu = TokenUtil()
    #token = tu.encode_auth_token(111)
    #print((token))
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NjI3NzAwMDYsImlhdCI6MTU2Mjc2ODIwNiwiaXNzIjoiZ2F1bnQiLCJkYXRhIjp7InVzZXJfaWQiOjF9fQ.yZoQhO0MOLCiZ-XIy02pQ6aW-3F-ZrQ5ZUYgPT8K2fI"
    print(tu.decode_auth_token(token))
