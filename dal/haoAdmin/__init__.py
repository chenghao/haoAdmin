#coding:utf-8
__author__ = "chenghao"

from models import *
import handler


def get_menu(user_id=None, parent_id=None):
	if not user_id:
		user_id = handler.get_user_id()

	menu = HMenu.select(
		HMenu.pid, HMenu.menu_name.alias("title"), HMenu.menu_url.alias("href"), HMenu.parent_menu,
		HMenu.icon
	).join(
		HRoleMenu, on=(HMenu.pid == HRoleMenu.menu)
	).join(
		HRole, on=(HRoleMenu.role == HRole.pid)
	).join(
		HRoleUser, on=(HRole.pid == HRoleUser.role)
	).join(
		HUser, on=(HRoleUser.user == HUser.pid)
	).join(
		HUserOrg, on=(HUser.pid == HUserOrg.user)
	).join(
		HOrg, on=(HUserOrg.org == HOrg.pid)
	).where(HMenu.parent_menu == parent_id, HRoleUser.user == user_id).order_by(HMenu.sort)

	return menu

