#coding:utf-8
__author__ = "chenghao"

from bottle import Bottle, request, redirect, response, JSONPlugin, jinja2_view as view
from json import dumps
from haoAdmin import handler, util, conf
from haoAdmin.dal import user

login_app = Bottle()
login_app.install(JSONPlugin(json_dumps=lambda s: dumps(s, cls=util.ComplexEncoder)))


@login_app.get("/login", apply=[view("./login/login")])
def login():
	"""
	显示登录页面, 如果已经登录就重定向到后台管理主页
	:return:
	"""
	pid = handler.get_user_id()
	if pid:
		redirect(conf.ADMIN_PREFIX)
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

	result = admin_dal.login(login_name, login_pwd)
	if result:
		# 设置 cookie
		cookie_id = util.random_num()
		dogpile_session = util.GetDogpile()[1]
		dogpile_session.set(cookie_id, result)

		conf = util.config.Config()
		max_age = conf.getint("cookie", "max_age")
		path = conf.get("cookie", "path")
		response.set_cookie(util.BLOG_COOKIE, cookie_id, max_age=max_age, path=path)

		return {"code": 0}
	else:
		return {"code": -1, "msg": "用户名或密码错误"}