#coding:utf-8
__author__ = "chenghao"

from bottle import Bottle, request, redirect, response, jinja2_view as view
from dal.haoAdmin import type
import util

type_app = Bottle()


@type_app.get("/index", apply=[view("./haoAdmin/type/index")])
def index():
    return {}


@type_app.get("/get_typegroup")
def get_typegroup():
    """
    获取字典分类
    :return:
    """
    page_no = int(request.query.getunicode("page_no", 1))
    page = 0 if page_no < 1 else page_no
    keyword = request.query.getunicode("keyword")

    results = type.get_typegroup(page, keyword=keyword)
    groups = results[0]
    groups_count = results[1]

    return {"groups": [r for r in groups.dicts()], "page_no": page_no,
            "total_page": util.total_page(groups_count)}