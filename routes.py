#coding:utf-8
__author__ = "chenghao"

from bottle import Bottle
import haoAdmin
from haoAdmin.handler.login import login_app
from haoAdmin.ueditor.ueditor import ueditor_bottle


Routes = Bottle()
# 主路径（默认）
Routes.merge("")
# 挂载其它模块路径
Routes.mount(haoAdmin.ADMIN_PREFIX, login_app)
Routes.mount(haoAdmin.UEDITOR_PREFIX, ueditor_bottle)



