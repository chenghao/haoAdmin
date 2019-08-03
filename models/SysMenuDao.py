# coding:utf-8
__author__ = "gaunt"

from . import SysMenu
from utils import decorator_does_not_exist


def get_all_menu():
    """
    获取所有菜单
    :return:
    """
    sql = SysMenu.select().order_by(SysMenu.sort_number.asc())
    result = [f for f in sql.dicts()]
    return result


@decorator_does_not_exist
def get(menu_id):
    """
    根据ID获取菜单
    :param menu_id:
    :return:
    """
    menu = SysMenu.get(SysMenu.menu_id == menu_id)
    return menu


def get_child_menu(parent_id):
    """
    获取子菜单
    :param parent_id:
    :return:
    """
    sql = SysMenu.select().where(SysMenu.parent_id == parent_id)
    result = [f for f in sql.dicts()]
    return result


def del_menu(menu_id):
    """
    根据ID删除菜单
    :param menu_id:
    :return:
    """
    sql = SysMenu.delete().where(SysMenu.menu_id == menu_id)
    sql.execute()


def add_menu(data):
    """
    新增
    :param data:
    :return:
    """
    i = SysMenu.insert(data).execute()
    return i


def up_menu(data):
    """
    修改
    :param data:
    :return:
    """
    i = SysMenu.update(data).where(SysMenu.menu_id == data["menu_id"]).execute()
    return i
