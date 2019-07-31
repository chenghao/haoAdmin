# coding:utf-8
__author__ = "gaunt"

from . import SysUser
from utils import decorator_does_not_exist


@decorator_does_not_exist
def login(username, password):
    user = SysUser.get(SysUser.username == username, SysUser.password == password)
    return user


@decorator_does_not_exist
def get(user_id):
    user = SysUser.get(SysUser.user_id == user_id)
    return user
