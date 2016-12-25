#coding:utf-8
__author__ = "chenghao"

from bottle import Bottle, request, redirect, response, JSONPlugin, jinja2_view as view
from json import dumps
import util
from handler.haoAdmin.login import login_app


admin_app = Bottle()
admin_app.install(JSONPlugin(json_dumps=lambda s: dumps(s, cls=util.ComplexEncoder)))
admin_app.merge(login_app)


@admin_app.get("/", apply=[view("./haoAdmin/index")])
def index():
	return {}


@admin_app.get("/main", apply=[view("./haoAdmin/main")])
def main():
	return {}