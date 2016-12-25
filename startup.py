#coding:utf-8
__author__ = "chenghao"

from bottle import Bottle, static_file
from routes import Routes

bottle = Bottle()
# Bottle Routes
bottle.merge(Routes)


@bottle.get('/static/<filename:path>')
def static(filename):
    """ Serve static files """
    return static_file(filename, root='./static/')


@bottle.get('/upload/<filename:path>')
def static(filename):
    """ Serve static files """
    return static_file(filename, root='./upload/')


@bottle.get('/views/admin/<filename:path>')
def static(filename):
    return static_file(filename, root='views/admin/')


def dev_run():
    from bottle import run
    run(app=bottle, host="0.0.0.0", port=8000, reloader=True, debug=True)


if __name__ == "__main__":
    dev_run()
