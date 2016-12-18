# coding:utf-8
__author__ = "chenghao"

from peewee import Model, PrimaryKeyField, DateTimeField, CharField, ForeignKeyField, IntegerField, CompositeKey
from playhouse.pool import PooledMySQLDatabase
from haoAdmin.util import singletons

conf = singletons.Conf()

database = PooledMySQLDatabase(conf.get("mysql", "db"), max_connections=conf.getint("mysql", "max_connections"),
							stale_timeout=conf.getint("mysql", "stale_timeout"),
							user=conf.get("mysql", "user"), passwd=conf.get("mysql", "passwd"),
							host=conf.get("mysql", "host"), port=conf.getint("mysql", "port"))


class BaseModel(Model):
	pid = PrimaryKeyField(unique=True)  # 主键
	create_time = DateTimeField()  # 创建日期

	class Meta:
		database = database


class BaseModel2(Model):
	class Meta:
		database = database


class HOrg(BaseModel):
	"""
	机构表
	"""
	name = CharField(max_length=50)  # 机构名称
	parent_org = ForeignKeyField('self', null=True, related_name='children', db_column="parent_org")

	class Meta:
		db_table = "h_org"


class HRole(BaseModel):
	"""
	角色表
	"""
	name = CharField(max_length=20)  # 角色名

	class Meta:
		db_table = "h_role"


class HUser(BaseModel):
	"""
	用户表
	"""
	login_name = CharField(max_length=20, unique=True)  # 登录名
	login_pwd = CharField(max_length=64)  # 登录密码
	user_name = CharField(max_length=20)  # 用户名
	org = ForeignKeyField(HOrg)  # 所属机构
	role = ForeignKeyField(HRole)  # 所属角色

	class Meta:
		db_table = "h_user"


class HMenu(BaseModel):
	"""
	菜单表
	"""
	menu_name = CharField(max_length=50)
	menu_url = CharField(max_length=500)
	is_active = CharField(max_length=1)
	sort = IntegerField()
	parent_menu = ForeignKeyField('self', null=True, related_name='children', db_column="parent_menu")

	class Meta:
		db_table = "h_menu"


class HTypeGroup(BaseModel):
	group_name = CharField(max_length=20)
	group_value = CharField(max_length=20, unique=True)
	is_active = CharField(max_length=1)

	class Meta:
		db_table = "h_typegroup"


class HType(BaseModel):
	type_name = CharField(max_length=20)
	type_value = CharField(max_length=20, unique=True)
	is_active = CharField(max_length=1)
	group = ForeignKeyField(HTypeGroup)

	class Meta:
		db_table = "h_type"


class HUserRoleMenu(BaseModel2):
	"""
	用户表、角色表和菜单表关联关系
	"""
	user = ForeignKeyField(HUser)
	role = ForeignKeyField(HRole)
	menu = ForeignKeyField(HMenu)

	class Meta:
		db_table = "h_user_role_menu"
		primary_key = CompositeKey('user', 'role', 'menu')


if __name__ == "__main__":
	user = HUser.select().where(HUser.pid == 1)
	print user
	for u in user:
		print u.login_name, u.user_name

		org = u.org
		role = u.role
		print org.name, role.name

	userRoleMenu = HUserRoleMenu.select().where(HUserRoleMenu.user == 1)
	print userRoleMenu
	for urm in userRoleMenu:
		user = urm.user
		role = urm.role
		menu = urm.menu
		print user.user_name, role.name, menu.menu_name


