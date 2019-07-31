# coding:utf-8
__author__ = "gaunt"

from bottle import Bottle, JSONPlugin
from json import dumps
import utils
from enums import success_result, error_result
from service.sys import SysUserService

user_app = Bottle()
user_app.install(JSONPlugin(json_dumps=lambda s: dumps(s, cls=utils.ComplexEncoder)))


@user_app.get('/info')
def info():
    """
    获取用户信息
    :return:
    """
    token_util = utils.TokenUtil()
    user_id = token_util.get_user_id()
    user = SysUserService.get_user(user_id)
    if user:
        result_user = {
            'user_id': user.user_id,
            'username': user.username,
            'nick_name': user.nick_name,
            'state': user.state
        }
        return success_result(result_user)
    else:
        return error_result(msg="用户为空")


@user_app.get('/user')
@utils.permissions_auth("get:list3")
def get():
    """
    获取用户信息
    :return: json
    """
    token_util = utils.TokenUtil()
    user_id = token_util.get_user_id()
    user = SysUserService.get_user(user_id)
    if user:
        return_user = {
            'user_id': user.user_id,
            'username': user.username,
            'nick_name': user.nick_name,
            'state': user.state
        }
        return success_result(return_user)
    else:
        return error_result(msg="用户为空")
