#coding:utf-8
__author__ = "chenghao"

from bottle import Bottle, request, redirect, response, JSONPlugin, jinja2_view as view
from json import dumps
import handler, util, conf
from dal.haoAdmin import user
from util import singletons


login_app = Bottle()
login_app.install(JSONPlugin(json_dumps=lambda s: dumps(s, cls=util.ComplexEncoder)))


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