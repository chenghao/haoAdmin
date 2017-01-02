#coding:utf-8
__author__ = "chenghao"

from bottle import Bottle
from . import admin_app
from .login import login_app
from .menu import menu_app
from .type import type_app

route_bottle = Bottle()

route_bottle.merge(admin_app)
route_bottle.mount("/login", login_app)
route_bottle.mount("/menu", menu_app)
route_bottle.mount("/type", type_app)
