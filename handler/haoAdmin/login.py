# coding:utf-8
__author__ = "chenghao"

from bottle import Bottle, request, redirect, response, jinja2_view as view
import handler, util, conf
from dal.haoAdmin import user
from dal import haoAdmin
from util import singletons

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
        # 获取一级菜单,并缓存
        one_level_menu = haoAdmin.get_menu(result.get("pid"))
        cache_m = singletons.get_cache_memory()
        cache_m.set("one_level_menu", one_level_menu)

        # 设置 cookie
        cookie_id = util.random_num()
        dogpile_session_f = singletons.get_session_file()
        dogpile_session_f.set(cookie_id, result)

        conf_ = singletons.Conf()
        max_age = conf_.getint("cookie", "max_age")
        path = conf_.get("cookie", "path")
        response.set_cookie(conf.ADMIN_COOKIE, cookie_id, max_age=max_age, path=path)

        return {"code": 0}
    else:
        return {"code": -1, "msg": "用户名或密码错误"}


@login_app.post("/logout")
def logout():
    cookie_id = request.get_cookie(conf.ADMIN_COOKIE)
    dogpile_session_f = singletons.get_session_file()
    dogpile_session_f.delete(cookie_id)
    response.set_cookie(conf.ADMIN_COOKIE, "")
    return {"code": 0}
