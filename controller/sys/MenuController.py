# coding:utf-8
__author__ = "gaunt"

from bottle import Bottle, JSONPlugin
from enums import success_result, error_result
from service.sys import SysMenuService
import utils, conf
from json import dumps, loads

menu_app = Bottle()
menu_app.install(JSONPlugin(json_dumps=lambda s: dumps(s, cls=utils.ComplexEncoder)))


@menu_app.get("/user_menu")
def get_user_menu():
    """
    获取主菜单
    :return:
    """
    token_util = utils.TokenUtil()
    user_id = token_util.get_user_id()
    redis_util = utils.RedisUtil()
    auths = redis_util.hget(conf.prefix_permit, user_id)
    if not auths:
        return error_result(msg="该用户没有菜单")
    data = SysMenuService.get_user_menu(loads(auths))
    return success_result(data)
