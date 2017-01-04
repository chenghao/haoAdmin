#coding:utf-8
__author__ = "chenghao"

import conf
from models import HTypegroup
import operator


def get_typegroup(page, page_row=conf.ROWS, **kv):
    """
    获取字典分类
    :param page:
    :param page_row:
    :param kv:
    :return:
    """
    and_conditions = None
    where_params = []

    keyword = kv["keyword"]
    if keyword:
        where_params.append(HTypegroup.group_name.contains(keyword))
        where_params.append(HTypegroup.group_value.contains(keyword))

    if where_params:
        and_conditions = reduce(operator.or_, where_params)

    result = HTypegroup.select(HTypegroup.pid, HTypegroup.group_name, HTypegroup.group_value)
    if and_conditions:
        result = result.where(and_conditions)
    result = result.order_by(-HTypegroup.create_time)

    result_page = result.paginate(page, paginate_by=page_row)
    return result_page, result.count()