#coding:utf-8
__author__ = "chenghao"

from bottle import Bottle, request, redirect, response, JSONPlugin, jinja2_view as view
from json import dumps
import util
from util import singletons
from handler.haoAdmin.login import login_app
from handler.haoAdmin.menu import menu_app
from dogpile.cache import api
from dal import haoAdmin

admin_app = Bottle()
admin_app.install(JSONPlugin(json_dumps=lambda s: dumps(s, cls=util.ComplexEncoder)))
admin_app.merge(login_app)
admin_app.merge(menu_app)


@admin_app.get("/", apply=[view("./haoAdmin/index")])
def index():
	cache_memory = singletons.get_cache_memory()
	menus = cache_memory.get("one_level_menu")
	if isinstance(menus, api.NoValue):
		menus = haoAdmin.get_menu()
	return {"menus": menus}


@admin_app.get("/main", apply=[view("./haoAdmin/main")])
def main():
	return {}