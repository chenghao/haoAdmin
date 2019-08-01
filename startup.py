# coding:utf-8
__author__ = "gaunt"

from bottle import Bottle, response, HTTPError, request, static_file
from controller import Routes
from enums import ResultEnum
from conf import intercept_path, exclude_path, prefix
import utils

bottle = Bottle()
bottle.mount(prefix, Routes)


@bottle.get('/<filename:path>')
def static(filename):
    """
    访问静态数据，后期static目录的数据可以直接挂在nginx
    :param filename:
    :return:
    """
    return static_file(filename, root='./static/')

#####################################################################################


@bottle.hook('before_request')
def login_hook():
    """
    请求之前的处理
    :return:
    """
    path_info = request.environ.get("PATH_INFO")

    bo1 = True  # 判断是否排除路径，False排除
    bo2 = False  # 判断是否拦截路径，True排除
    # 判断是否排除路径
    for exclude in exclude_path:
        flag = exclude[-1]
        if flag == "*":
            if exclude[0: -2] in path_info:
                bo1 = False
                break
        else:
            if exclude in path_info:
                bo1 = False
                break
    # 判断拦截路径
    if bo1:
        for intercept in intercept_path:
            flag = intercept[-1]
            if flag == "*":
                if intercept[0: -2] in path_info:
                    bo2 = True
                    break
            else:
                if intercept in path_info:
                    bo2 = True
                    break
    # 判断是否登录
    if bo2:
        token_util = utils.TokenUtil()
        result = token_util.identify(request)
        if result["code"] != 200:
            raise HTTPError(result["code"], result["msg"])


#####################################################################################


@bottle.hook("after_request")
def after_request():
    """
    请求之后的处理
    :return:
    """
    status_code = response.status_code
    if status_code == ResultEnum.error400.value["code"]:
        raise HTTPError(400, ResultEnum.error400.value["msg"])
    elif status_code == ResultEnum.error401.value["code"]:
        raise HTTPError(401, ResultEnum.error401.value["msg"])
    elif status_code == ResultEnum.error404.value["code"]:
        raise HTTPError(404, ResultEnum.error404.value["msg"])
    elif status_code == ResultEnum.error405.value["code"]:
        raise HTTPError(405, ResultEnum.error405.value["msg"])
    elif status_code == ResultEnum.error422.value["code"]:
        raise HTTPError(422, ResultEnum.error422.value["msg"])
    elif status_code == ResultEnum.error.value["code"]:
        raise HTTPError(500, ResultEnum.error500.value["msg"])


#####################################################################################


@bottle.error(400)
def handle_error_400(error):
    obj = ResultEnum.error400.value
    return _handle_error(obj, error)


@bottle.error(401)
def handle_error_401(error):
    obj = ResultEnum.error401.value
    return _handle_error(obj, error)


@bottle.error(404)
def handle_error_404(error):
    obj = ResultEnum.error404.value
    return _handle_error(obj, error)


@bottle.error(405)
def handle_error_405(error):
    obj = ResultEnum.error405.value
    return _handle_error(obj, error)


@bottle.error(422)
def handle_error_422(error):
    obj = ResultEnum.error422.value
    return _handle_error(obj, error)


@bottle.error(500)
def handle_error_500(error):
    obj = ResultEnum.error.value
    return _handle_error(obj, error)


def _handle_error(obj, error):
    response.content_type = 'application/json'  # 返回json格式
    # response.status = 200  # 返回http状态码为成功的标识
    return '{"code": %s, "msg": "%s"}' % (obj["code"], error.body if error.body else obj["msg"])


if __name__ == "__main__":
    from bottle import run

    run(app=bottle, host="0.0.0.0", port=8888, reloader=True, debug=True)
