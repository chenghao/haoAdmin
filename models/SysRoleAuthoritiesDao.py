# coding:utf-8
__author__ = "gaunt"

from . import SysRoleAuthorities


def get_authorities(role_id):
    sql = SysRoleAuthorities.select(SysRoleAuthorities.authority).where(SysRoleAuthorities.role_id == role_id)
    result = [f for f in sql.dicts()]
    return result

