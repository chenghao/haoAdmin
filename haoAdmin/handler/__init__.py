#coding:utf-8
__author__ = "chenghao"

from bottle import request
import haoAdmin
from haoAdmin.util import singletons


def get_user_id():
	"""
	获取user_id
	:return:
	"""
	cookie_id = request.get_cookie(haoAdmin.ADMIN_COOKIE)
	dogpile_session = singletons.Dogpiles()[1]
	result = dogpile_session.get(cookie_id)
	if result:
		user_id = result.get("pid")
	else:
		user_id = None
	return user_id
