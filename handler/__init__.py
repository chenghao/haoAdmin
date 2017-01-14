# coding:utf-8
__author__ = "chenghao"

from bottle import request
import conf


def get_user_id():
    """
    获取user_id
    :return:
    """
    user_id = None

    env = request.environ
    sess = env.get(conf.ADMIN_SESSION, None)
    if sess:
        user = sess.get(conf.CURRENT_USER, None)
        if user:
            user_id = user.get("pid", None)

    return user_id
