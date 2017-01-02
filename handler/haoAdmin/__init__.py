# coding:utf-8
__author__ = "chenghao"

from bottle import Bottle, JSONPlugin, jinja2_view as view
from json import dumps
import util
from util import singletons
from dogpile.cache import api
from dal import haoAdmin

admin_app = Bottle()
admin_app.install(JSONPlugin(json_dumps=lambda s: dumps(s, cls=util.ComplexEncoder)))


@admin_app.get("/", apply=[view("./haoAdmin/index")])
def index():
    cache_m = singletons.get_cache_memory()
    menus = cache_m.get("one_level_menu")
    if isinstance(menus, api.NoValue):
        menus = haoAdmin.get_menu()
    return {"menus": menus}


@admin_app.get("/main", apply=[view("./haoAdmin/main")])
def main():
    return {}
