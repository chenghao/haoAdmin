# coding:utf-8
__author__ = "gaunt"

from bottle import Bottle, JSONPlugin
from json import dumps
import utils, conf
from enums import success_result, error_result
from service.sys import SysUserService
from webargs import fields
from webargs.bottleparser import use_kwargs

user_app = Bottle()
user_app.install(JSONPlugin(json_dumps=lambda s: dumps(s, cls=utils.ComplexEncoder)))


@user_app.get('/info')
def info():
    """
    获取用户信息
    :return:
    """
    token_util = utils.TokenUtil()
    user_id = token_util.get_user_id()
    user = SysUserService.get_user(user_id)
    if user:
        result_user = {
            'user_id': user.user_id,
            'username': user.username,
            'nick_name': user.nick_name,
            'state': user.state
        }
        return success_result(data=result_user)
    else:
        return error_result(msg="用户为空")


psw_args = {
    "old_psw": fields.Str(required=True),
    "new_psw": fields.Str(required=True),
}


@user_app.put('/psw', apply=use_kwargs(psw_args))
@utils.permissions_auth("put:/v1/sys/user/psw")
def psw(old_psw, new_psw):
    """
    修改密码
    :param old_psw:
    :param new_psw:
    :return:
    """
    token_util = utils.TokenUtil()
    user_id = token_util.get_user_id()
    # 先判断原密码是否正确
    user = SysUserService.get_user(user_id)
    if user.password == utils.md5_salt(old_psw, user.username):
        rowid = SysUserService.update_pwd(user_id, utils.md5_salt(new_psw, user.username))
        if rowid > 0:
            # 移除该用户的token
            redis_util = utils.RedisUtil()
            redis_util.deltele("{}:{}".format(conf.prefix_token, user_id))

            return success_result()
        else:
            return error_result(msg="修改密码失败")
    else:
        return error_result(msg="原密码不正确")
