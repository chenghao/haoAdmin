#coding:utf-8
__author__ = "chenghao"

from models import HUser
import util


def login(login_name, login_pwd):
	"""
	根据账号和密码登录
	:param login_name:
	:param login_pwd:
	:return:
	"""
	if not login_name and not login_pwd:
		return None
	else:
		login_pwd_md5 = util.get_md5_s(login_pwd, login_name)
		user = HUser.select().where(HUser.login_name == login_name, HUser.login_pwd == login_pwd_md5)
		if len(user):
			return [r for r in user.dicts()][0]
		return None

