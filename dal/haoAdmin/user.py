# coding:utf-8
__author__ = "chenghao"

from models import HUser, HUserOrg, HRoleUser, HOrg, HRole
import util
import peewee


def login(login_name, login_pwd):
    """
    根据账号和密码登录
    :param login_name:
    :param login_pwd:
    :return:
    """
    if not login_name and not login_pwd:
        return None
    else:
        login_pwd_md5 = util.get_md5_s(login_pwd, login_name)

        user = HUser.select(
            HUser.pid, HUser.user_name, HUser.login_name,
            HOrg.pid.alias("org_id"), HOrg.name.alias("org_name"),
            HRole.pid.alias("role_id"), HRole.role_name
        ).join(
            HUserOrg, on=(HUser.pid == HUserOrg.user), join_type=peewee.JOIN_LEFT_OUTER
        ).join(
            HOrg, on=(HUserOrg.org == HOrg.pid), join_type=peewee.JOIN_LEFT_OUTER
        ).join(
            HRoleUser, on=(HUser.pid == HRoleUser.user), join_type=peewee.JOIN_LEFT_OUTER
        ).join(
            HRole, on=(HRoleUser.role == HRole.pid), join_type=peewee.JOIN_LEFT_OUTER
        ).where(HUser.login_name == login_name, HUser.login_pwd == login_pwd_md5)

        if len(user):
            return [r for r in user.dicts()][0]
        return None
