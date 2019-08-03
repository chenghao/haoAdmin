# coding:utf-8
__author__ = "gaunt"

from models import (SysMenuDao)


def get_user_menu(auths):
    """
    根据权限获取主菜单
    :param auths:
    :return:
    """
    menus = SysMenuDao.get_all_menu()

    # 获取自己权限的菜单
    self_menus = []
    [self_menus.append(m) for m in menus if not m["authority"] or m["authority"] in auths]

    # 上级菜单集合
    ids = []
    [ids.append(menu["parent_id"]) for menu in self_menus if menu["parent_id"] not in ids]

    # 删除空菜单
    menus = []
    [menus.append(m) for m in self_menus if m["menu_url"] or (not m["menu_url"] and m["menu_id"] in ids)]

    # 构建树形菜单
    tree_menus = _build_tree_menu(menus, -1)

    return tree_menus


def _build_tree_menu(menus, parent_id):
    tree_menus = []
    for menu in menus:
        if parent_id == menu["parent_id"]:
            name = menu["menu_name"]
            icon = menu["menu_icon"]
            url = menu["menu_url"] if menu["menu_url"] else "javascript:;"
            sub_menus = _build_tree_menu(menus, menu["menu_id"])
            tree_menus.append({"name": name, "icon": icon, "url": url, "subMenus": sub_menus})
    return tree_menus


def get_menu_list(keyword):
    """
    获取菜单列表
    :param keyword:
    :return:
    """
    menus = SysMenuDao.get_all_menu()

    # 设置父节点名称
    for menu in menus:
        bo = True
        for m in menus:
            if menu["parent_id"] == m["menu_id"]:
                menu["parent_name"] = m["menu_name"]
                bo = False
                break
        if bo:
            menu["parent_name"] = ""

    # 筛选结果
    menu_list = []
    if keyword:
        [menu_list.append(m) for m in menus if keyword in m["menu_name"] or (m["parent_name"] and keyword in m["parent_name"])]
    else:
        menu_list = menus

    # 排序
    menu_dict = {}
    list_dict = {}
    for m in menu_list:
        menu_id_key = "menu{}".format(m["menu_id"])
        parent_id_key = "menu{}".format(m["parent_id"])
        if m["parent_id"] == -1:
            menu_dict[menu_id_key] = m
        else:
            if len(list_dict) == 0:
                list_dict[parent_id_key] = [m]
            else:
                if parent_id_key in list_dict.keys():
                    list = list_dict[parent_id_key]
                    list.append(m)
                    list_dict[parent_id_key] = list
                else:
                    list_dict[parent_id_key] = [m]

    lists = []
    # 父级数据为空，菜单数据有值
    if len(menu_dict) == 0 and len(list_dict) > 0:
        for key in list_dict:
            [lists.append(l) for l in list_dict[key]]

    # 都有值时
    for key in menu_dict.keys():
        lists.append(menu_dict[key])
        ll = list_dict[key]
        [lists.append(l) for l in ll]

    return lists


def del_menu(menu_id):
    """
    根据ID删除菜单
    :param menu_id:
    :return:
    """
    # 先判断该菜单是否存在
    menu = SysMenuDao.get(menu_id)
    if menu is None:
        return "该菜单不存在"

    # 获取该菜单的子菜单
    childs = SysMenuDao.get_child_menu(menu_id)
    if len(childs) > 0:
        return "该菜单还有子菜单，不能删除"

    # 删除菜单
    SysMenuDao.del_menu(menu_id)


def add_menu(parent_id, menu_name, menu_url, menu_icon, sort_number, authority):
    """
    新增菜单
    :param parent_id:
    :param menu_name:
    :param menu_url:
    :param menu_icon:
    :param sort_number:
    :param authority:
    :return:
    """
    # 判断父级ID是否存在
    if parent_id and parent_id != -1:
        menu = SysMenuDao.get(parent_id)
        if menu is None:
            return "该父级ID不存在"

    # 保存
    data = {"parent_id": parent_id, "menu_name": menu_name, "menu_url": menu_url, "menu_icon": menu_icon,
            "sort_number": sort_number, "authority": authority}
    i = SysMenuDao.add_menu(data)
    if i <= 0:
        return "保存菜单失败"


def up_menu(menu_id, parent_id, menu_name, menu_url, menu_icon, sort_number, authority):
    """
    修改菜单
    :param menu_id:
    :param parent_id:
    :param menu_name:
    :param menu_url:
    :param menu_icon:
    :param sort_number:
    :param authority:
    :return:
    """
    # 判断当前菜单是否存在
    menu = SysMenuDao.get(menu_id)
    if menu is None:
        return "该菜单不存在"

    # 判断父级ID是否存在
    if parent_id and parent_id != -1:
        menu = SysMenuDao.get(parent_id)
        if menu is None:
            return "该父级ID不存在"

    # 保存
    data = {"menu_id": menu_id, "parent_id": parent_id, "menu_name": menu_name, "menu_url": menu_url,
            "menu_icon": menu_icon, "sort_number": sort_number, "authority": authority}
    i = SysMenuDao.up_menu(data)
    if i <= 0:
        return "修改菜单失败"
