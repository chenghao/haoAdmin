# coding:utf-8
__author__ = "gaunt"

from . import SysUserRole


def get_roles(user_id):
    sql = SysUserRole.select(SysUserRole.role_id).where(SysUserRole.user_id == user_id)
    result = [f for f in sql.dicts()]
    return result
