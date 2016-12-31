# coding:utf-8
__author__ = "chenghao"

from bottle import request
import conf
from util import singletons


def get_user_id():
    """
    获取user_id
    :return:
    """
    cookie_id = request.get_cookie(conf.ADMIN_COOKIE)
    dogpile_session_f = singletons.get_session_file()
    result = dogpile_session_f.get(cookie_id)
    if result:
        user_id = result.get("pid")
    else:
        user_id = None
    return user_id
