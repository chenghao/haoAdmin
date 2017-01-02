#coding:utf-8
__author__ = "chenghao"

from bottle import Bottle, request, redirect, response, jinja2_view as view

type_app = Bottle()


@type_app.get("/index", apply=[view("./haoAdmin/type/index")])
def index():
    return {}