#coding:utf-8
__author__ = "chenghao"

from haoAdmin.models import HUser
from haoAdmin import util


def login(login_name, login_pwd):
	login_pwd_md5 = util.get_md5_s(login_pwd, login_name)
	user = HUser.select().where(HUser.login_name == login_name, HUser.login_pwd == login_pwd_md5)
	if len(user):
		return user
	pass