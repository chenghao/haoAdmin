# coding:utf-8
__author__ = "gaunt"

from json import dumps

from bottle import Bottle, JSONPlugin, request
from webargs import fields
from webargs.bottleparser import use_kwargs
import conf
from enums import ResultEnum
from utils import (RedisUtil, ComplexEncoder, TokenUtil)
from service.sys import SysUserService

login_app = Bottle()
login_app.install(JSONPlugin(json_dumps=lambda s: dumps(s, cls=ComplexEncoder)))


login_args = {
    "username": fields.Str(required=True),
    "password": fields.Str(required=True),
}


@login_app.post("/login", apply=use_kwargs(login_args))
def login(username, password):
    """
    登录
    :param username:
    :param password:
    :return:
    """
    user = SysUserService.login(username, password)
    if user:
        user_id = user.user_id
        token = TokenUtil().encode_auth_token(user_id)
        if token:
            # 获取用户角色并保存redis
            roles = SysUserService.get_roles(user_id)
            RedisUtil().hset(conf.prefix_role, user_id, dumps(roles))

            # 获取用户的所有权限并保存redis
            auths = SysUserService.get_authorities(roles)
            RedisUtil().hset(conf.prefix_permit, user_id, dumps(auths))

            # token 保存到redis
            RedisUtil().set("{}:{}".format(conf.prefix_token, user_id), token, conf.jwt_exp)

            obj = ResultEnum.success.value
            return {"code": obj["code"], "msg": obj["msg"], "token": token}
        else:
            return ResultEnum.error.value
    else:
        return ResultEnum.login_error.value


@login_app.get("/test")
def test():
    abc = request.params.getunicode("abc")
    print(abc)
    return ResultEnum.success.value
