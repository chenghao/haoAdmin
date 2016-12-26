# coding:utf-8
__author__ = "chenghao"

from bottle import Bottle, static_file
from routes import Routes
from util.middleware import LoginMiddleware

bottle = Bottle()
# Bottle Routes
bottle.merge(Routes)


@bottle.get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='./static/')


@bottle.get('/upload/<filename:path>')
def static(filename):
    return static_file(filename, root='./upload/')


app = LoginMiddleware(bottle, "/admin/*", ["/admin/login", "/admin/logout"])


def dev_run():
    from bottle import run
    run(app=app, host="0.0.0.0", port=8000, reloader=True, debug=True)


if __name__ == "__main__":
    dev_run()
