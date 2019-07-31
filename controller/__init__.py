# coding:utf-8
__author__ = "gaunt"

from bottle import Bottle, redirect
from .sys import sys_route

Routes = Bottle()
# 主路径（默认）
Routes.merge("")
# 挂载其它模块路径
Routes.mount("/sys", sys_route)


@Routes.get('/')
def index():
    redirect("/index.html")
