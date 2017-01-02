#coding:utf-8
__author__ = "chenghao"

from bottle import Bottle
import conf
from ueditor.ueditor import ueditor_bottle
from handler.haoAdmin.admin_route import route_bottle


Routes = Bottle()
# 主路径（默认）
Routes.merge("")
# 挂载其它模块路径
Routes.mount(conf.ADMIN_PREFIX, route_bottle)
Routes.mount(conf.UEDITOR_PREFIX, ueditor_bottle)


