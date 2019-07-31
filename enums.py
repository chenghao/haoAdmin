# coding:utf-8
__author__ = "gaunt"

import enum


class BaseEnum(enum.Enum):
    pass


class ResultEnum(BaseEnum):
    success = {"code": 200, "msg": "操作成功"}
    error = {"code": 500, "msg": "操作失败"}
    error400 = {"code": 400, "msg": "400 - 请求参数错误"}
    error401 = {"code": 401, "msg": "401 - 未授权"}
    error404 = {"code": 404, "msg": "404 - 未找到资源"}
    error405 = {"code": 405, "msg": "405 - 没有找到请求方法"}
    error422 = {"code": 422, "msg": "422 - 请求参数不完整"}
    login_error = {"code": 1000, "msg": "用户名或密码失败"}


def success_result(data=None):
    value = ResultEnum.success.value
    return {
        "code": value["code"],
        "msg": value["msg"],
        "data": data if data else ""
    }


def error_result(data=None, code=None, msg=None):
    value = ResultEnum.error.value
    return {
        "code": code if code else value["code"],
        "msg": msg if msg else value["msg"],
        "data": data if data else ""
    }


class Logical(BaseEnum):
    AND = "and"
    OR = "or"


class UserStateEnum(BaseEnum):
    NORMAL = 1  # 正常
    FREEZE = 0  # 冻结


if __name__ == "__main__":
    print(Logical.AND.value)
