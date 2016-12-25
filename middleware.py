#coding:utf-8
__author__ = "chenghao"

import conf, handler


class LoginMiddleware(object):
    """
    登录拦截器
    """
    def __init__(self, app, path=None, exclude_path=None):
        self.app = app
        self.path = path
        self.exclude_path = exclude_path

    def __call__(self, environ, start_response):
        path_info = environ.get("PATH_INFO")
        if path_info == conf.ADMIN_PREFIX or (path_info in self.exclude_path) is False:
            flag = self.path[-1]
            path = self.path[:-2]

            if flag == "*":
                if path in path_info:
                    self.is_user_login(environ)
            else:
                if conf.ADMIN_PREFIX in path_info:
                    self.is_user_login(environ)

        return self.app(environ, start_response)

    def is_user_login(self, environ):
        user_id = handler.get_user_id()
        if not user_id:
            environ["PATH_INFO"] = conf.ADMIN_PREFIX + "/login"