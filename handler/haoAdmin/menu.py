# coding:utf-8
__author__ = "chenghao"

from bottle import Bottle, request, redirect, response, jinja2_view as view
from dal import haoAdmin
from util import singletons
from dogpile.cache import api

menu_app = Bottle()


@menu_app.get("/index", apply=[view("./haoAdmin/menu/index")])
def index():
    return {}


@menu_app.get("/get_parent_menu")
def get_parent_menu():
    cache_m = singletons.get_cache_memory()
    menus = cache_m.get("one_level_menu")
    if isinstance(menus, api.NoValue):
        menus = haoAdmin.get_menu()
    one_level_menu = [r for r in menus.dicts()]
    return {"one_level_menu": one_level_menu}


@menu_app.get("/get_child_menu")
def get_child_menu():
    parent_id = request.params.getunicode("parent_id")

    cache_m = singletons.get_cache_memory()
    key = "child_menu_%s" % str(parent_id)
    two_level_menu = cache_m.get(key)
    if isinstance(two_level_menu, api.NoValue):
        menus = haoAdmin.get_menu(parent_id=parent_id)
        two_level_menu = [r for r in menus.dicts()]
        cache_m.set(key, two_level_menu)

    return {"two_level_menu": two_level_menu}
