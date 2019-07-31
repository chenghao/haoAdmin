# coding:utf-8
__author__ = "gaunt"

from . import SysMenu


def get_all_menu():
    """
    获取所有菜单
    :return:
    """
    sql = SysMenu.select().order_by(SysMenu.sort_number.asc())
    result = [f for f in sql.dicts()]
    return result
