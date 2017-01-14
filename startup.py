# coding:utf-8
__author__ = "chenghao"

from bottle import Bottle, static_file, request, JSONPlugin
from routes import Routes
import conf, handler, util
from beaker.middleware import SessionMiddleware
from json import dumps

bottle = Bottle()
bottle.install(JSONPlugin(json_dumps=lambda s: dumps(s, cls=util.ComplexEncoder)))
# Bottle Routes
bottle.merge(Routes)

_admin = conf.ADMIN_PREFIX


@bottle.get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='./static/')


@bottle.get('/upload/<filename:path>')
def static(filename):
    return static_file(filename, root='./upload/')


@bottle.hook('before_request')
def login_hook():
    """
    请求之前先判断是否登录
    :return:
    """
    hook_path = _admin + "/*"
    exclude_path = [_admin + "/login", _admin + "/logout"]

    path_info = request.environ.get("PATH_INFO")
    if path_info == _admin or (path_info in exclude_path) is False:
        flag = hook_path[-1]
        path = hook_path[:-2]
        if flag == "*":
            if path in path_info:
                is_user_login(request.environ)
        else:
            if _admin in path_info:
                is_user_login(request.environ)


def is_user_login(environ):
    user_id = handler.get_user_id()
    if user_id is None:
        environ["PATH_INFO"] = _admin + "/login/login"


app = SessionMiddleware(bottle, conf.session_opts)


def dev_run():
    from bottle import run
    run(app=app, host="0.0.0.0", port=8000, reloader=True, debug=True)


if __name__ == "__main__":
    dev_run()
