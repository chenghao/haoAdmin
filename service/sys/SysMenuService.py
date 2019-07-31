# coding:utf-8
__author__ = "gaunt"

from models import (SysMenuDao)


def get_user_menu(auths):
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
