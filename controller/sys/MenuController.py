# coding:utf-8
__author__ = "gaunt"

from bottle import Bottle, JSONPlugin, request
from enums import success_result, error_result, layui_table_code
from service.sys import SysMenuService
import utils, conf
from json import dumps, loads
from webargs import fields
from webargs.bottleparser import use_kwargs

menu_app = Bottle()
menu_app.install(JSONPlugin(json_dumps=lambda s: dumps(s, cls=utils.ComplexEncoder)))


@menu_app.get("/user_menu")
def get_user_menu():
    """
    获取左侧主菜单
    :return:
    """
    token_util = utils.TokenUtil()
    user_id = token_util.get_user_id()
    redis_util = utils.RedisUtil()
    auths = redis_util.hget(conf.prefix_permit, user_id)
    if not auths:
        return error_result(msg="该用户没有菜单")
    data = SysMenuService.get_user_menu(loads(auths))
    return success_result(data=data)


@menu_app.get("/list")
@utils.permissions_auth("get:/v1/sys/menu")
def list():
    """
    获取菜单列表
    :return:
    """
    keyword = request.params.getunicode("keyword")

    menus = SysMenuService.get_menu_list(keyword)
    return success_result(data=menus, code=layui_table_code)


del_menu_args = {
    "menu_id": fields.Integer(required=True),
}


@menu_app.delete("/del", apply=use_kwargs(del_menu_args))
@utils.permissions_auth("del:/v1/sys/menu")
def del_menu(menu_id):
    """
    根据ID删除菜单
    :param menu_id:
    :return:
    """
    res = SysMenuService.del_menu(menu_id)  # 如果删除错误，就返回错误信息
    if res:
        return error_result(msg=res)
    else:
        return success_result()


add_menu_args = {
    "parent_id": fields.Integer(required=False),
    "menu_name": fields.Str(required=True),
    "menu_url": fields.Str(required=False),
    "menu_icon": fields.Str(required=False),
    "sort_number": fields.Integer(required=False),
    "authority": fields.Str(required=False),
}


@menu_app.post("/addOrUpMenu", apply=use_kwargs(add_menu_args))
@utils.permissions_auth("post:/v1/sys/menu")
def add_menu(parent_id, menu_name, menu_url, menu_icon, sort_number, authority):
    """
    新增菜单
    :param parent_id:
    :param menu_name:
    :param menu_url:
    :param menu_icon:
    :param sort_number:
    :param authority:
    :return:
    """
    menu_name = utils.encode_utf8(menu_name)
    res = SysMenuService.add_menu(parent_id, menu_name, menu_url, menu_icon, sort_number, authority)
    if res:
        return error_result(msg=res)
    else:
        return success_result()


up_menu_args = {
    "menu_id": fields.Integer(required=True),
    "parent_id": fields.Integer(required=False),
    "menu_name": fields.Str(required=True),
    "menu_url": fields.Str(required=False),
    "menu_icon": fields.Str(required=False),
    "sort_number": fields.Integer(required=False),
    "authority": fields.Str(required=False),
}


@menu_app.put("/addOrUpMenu", apply=use_kwargs(up_menu_args))
@utils.permissions_auth("put:/v1/sys/menu")
def up_menu(menu_id, parent_id, menu_name, menu_url, menu_icon, sort_number, authority):
    """
    修改菜单
    :param menu_id:
    :param parent_id:
    :param menu_name:
    :param menu_url:
    :param menu_icon:
    :param sort_number:
    :param authority:
    :return:
    """
    menu_name = utils.encode_utf8(menu_name)
    res = SysMenuService.up_menu(menu_id, parent_id, menu_name, menu_url, menu_icon, sort_number, authority)
    if res:
        return error_result(msg=res)
    else:
        return success_result()
