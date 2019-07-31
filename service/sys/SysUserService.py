# coding:utf-8
__author__ = "gaunt"

import utils
from models import (SysUserDao, SysUserRoleDao, SysRoleAuthoritiesDao)


def login(username, password):
    password = utils.md5_salt(password, username)
    user = SysUserDao.login(username, password)
    return user


def get_user(user_id):
    user = SysUserDao.get(user_id)
    return user


def get_roles(user_id):
    result = SysUserRoleDao.get_roles(user_id)

    roles = []
    for res in result:
        roles.append(res["role_id"])
    return roles


def get_authorities(roles):
    auths = []
    for role in roles:
        result = SysRoleAuthoritiesDao.get_authorities(role)

        authorities = []
        for res in result:
            authorities.append(res["authority"])

        [auths.append(r) for r in authorities if r not in auths]
    return auths
