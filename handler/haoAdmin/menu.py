# coding:utf-8
__author__ = "chenghao"

from bottle import Bottle, request, jinja2_view as view
from dal import haoAdmin
from util import singletons
import conf

menu_app = Bottle()
cache = singletons.Cache()


@menu_app.get("/index", apply=[view("./haoAdmin/menu/index")])
def index():
    return {}


@menu_app.get("/get_parent_menu", apply=[cache.region(conf.cache_key, 'menu_parentMenu')])
def get_parent_menu():
    menus = haoAdmin.get_menu()
    one_level_menu = [r for r in menus.dicts()]
    return {"one_level_menu": one_level_menu}


@menu_app.get("/get_child_menu")
def get_child_menu():
    parent_id = request.params.getunicode("parent_id")

    cache_key = "menu_childMenu_" + parent_id
    ca = cache.get_cache(conf.cache_key, **conf.cache_opt)
    if cache_key in ca:
        two_level_menu = ca.get(cache_key)
    else:
        menus = haoAdmin.get_menu(parent_id=parent_id)
        two_level_menu = [r for r in menus.dicts()]
        ca.put(cache_key, two_level_menu)

    return {"two_level_menu": two_level_menu}
