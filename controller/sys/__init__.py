# coding:utf-8
__author__ = "gaunt"

from bottle import Bottle
from .LoginController import login_app
from .UserController import user_app
from .MenuController import menu_app

sys_route = Bottle()

sys_route.merge("")
sys_route.mount("/login", login_app)
sys_route.mount("/user", user_app)
sys_route.mount("/menu", menu_app)
