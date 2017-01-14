# coding:utf-8
__author__ = "chenghao"

from bottle import Bottle, request, redirect, jinja2_view as view
import conf, handler
from dal.haoAdmin import user

login_app = Bottle()


@login_app.get("/login", apply=[view("./haoAdmin/login/login")])
def login():
    """
    显示登录页面, 如果已经登录就重定向到后台管理主页
    :return:
    """
    pid = handler.get_user_id()
    if pid:
        redirect(handler.conf.ADMIN_PREFIX)
    else:
        return {}


@login_app.post("/login")
def login():
    """
    用户登录
    :return:
    """
    login_name = request.params.getunicode("login_name")
    login_pwd = request.params.getunicode("login_pwd")

    result = user.login(login_name, login_pwd)
    if result:
        # 设置 session
        s = request.environ[conf.ADMIN_SESSION]
        s[conf.CURRENT_USER] = result

        return {"code": 0}
    else:
        return {"code": -1, "msg": "用户名或密码错误"}


@login_app.post("/logout")
def logout():
    sess = request.environ[conf.ADMIN_SESSION]
    sess[conf.CURRENT_USER] = None

    from util import singletons
    cache = singletons.Cache()
    ca = cache.get_cache(conf.cache_key, **conf.cache_opt)
    ca.clear()

    return {"code": 0}
