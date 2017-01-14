# coding:utf-8
__author__ = "chenghao"

from bottle import Bottle, jinja2_view as view
import conf
from dal import haoAdmin
from util import singletons

admin_app = Bottle()
cache = singletons.Cache()


@admin_app.get("/", apply=[view("./haoAdmin/index"), cache.region(conf.cache_key, 'main_menus')])
def index():
    menus = haoAdmin.get_menu()
    return {"menus": menus}


@admin_app.get("/main", apply=[view("./haoAdmin/main")])
def main():
    return {}
