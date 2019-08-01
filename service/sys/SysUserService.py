# coding:utf-8
__author__ = "gaunt"

import utils
from models import (SysUserDao, SysUserRoleDao, SysRoleAuthoritiesDao)


def login(username, password):
    """
    登录
    :param username:
    :param password:
    :return:
    """
    password = utils.md5_salt(password, username)
    user = SysUserDao.login(username, password)
    return user


def get_user(user_id):
    """
    根据ID获取用户信息
    :param user_id:
    :return:
    """
    user = SysUserDao.get(user_id)
    return user


def get_roles(user_id):
    """
    根据ID获取用户角色
    :param user_id:
    :return:
    """
    result = SysUserRoleDao.get_roles(user_id)

    roles = []
    for res in result:
        roles.append(res["role_id"])
    return roles


def get_authorities(roles):
    """
    根据角色ID获取用户权限
    :param roles:
    :return:
    """
    auths = []
    for role in roles:
        result = SysRoleAuthoritiesDao.get_authorities(role)

        authorities = []
        for res in result:
            authorities.append(res["authority"])

        [auths.append(r) for r in authorities if r not in auths]
    return auths


def update_pwd(user_id, new_psw):
    """
    修改密码
    :param user_id:
    :param new_psw:
    :return:
    """
    rowid = SysUserDao.update_pwd(user_id, new_psw)
    return rowid
