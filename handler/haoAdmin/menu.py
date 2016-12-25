#coding:utf-8
__author__ = "chenghao"

from bottle import Bottle, request, redirect, response, jinja2_view as view
from dal import haoAdmin
from util import singletons
from dogpile.cache import api

menu_app = Bottle()


@menu_app.get("/get_child_menu")
def get_child_menu():
	parent_id = request.params.getunicode("parent_id")

	cache_ = singletons.get_cache_memory()
	key = "child_menu_%s" % str(parent_id)
	two_level_menu = cache_.get(key)
	if isinstance(two_level_menu, api.NoValue):
		menus = haoAdmin.get_menu(parent_id=parent_id)
		two_level_menu = [r for r in menus.dicts()]
		cache_.set(key, two_level_menu)

	return {"two_level_menu": two_level_menu}
