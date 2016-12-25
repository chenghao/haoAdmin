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


class HOrg(BaseModel):
	"""
	机构表
	"""
	description = CharField(null=True, max_length=100)  # 机构描述
	name = CharField(max_length=50)  # 机构名称
	parent_org = ForeignKeyField('self', null=True, related_name='children', db_column="parent_org")

	class Meta:
		db_table = 'h_org'


class HRole(BaseModel):
	"""
	角色表
	"""
	role_code = CharField(max_length=20)  # 角色code
	role_name = CharField(max_length=20)  # 角色名

	class Meta:
		db_table = 'h_role'


class HUser(BaseModel):
	"""
	用户表
	"""
	login_name = CharField(max_length=20, unique=True)  # 登录名
	login_pwd = CharField(max_length=64)  # 登录密码
	phone = CharField(null=True, max_length=16)
	qq = CharField(null=True, max_length=12)
	sex = IntegerField(null=True)
	user_name = CharField(max_length=20)  # 用户名
	wx = CharField(null=True, max_length=20)

	class Meta:
		db_table = 'h_user'


class HMenu(BaseModel):
	"""
	菜单表
	"""
	is_active = CharField(max_length=1)
	level = IntegerField(null=True)
	menu_name = CharField(max_length=50)
	menu_url = CharField(max_length=500)
	parent_menu = ForeignKeyField('self', null=True, related_name='children', db_column="parent_menu")
	sort = IntegerField()

	class Meta:
		db_table = 'h_menu'


class HTypegroup(BaseModel):
	group_name = CharField(max_length=20)
	group_value = CharField(max_length=20, unique=True)

	class Meta:
		db_table = 'h_typegroup'


class HType(BaseModel):
	group = ForeignKeyField(HTypegroup, db_column='group_id')
	type_name = CharField(max_length=20)
	type_value = CharField(max_length=20)

	class Meta:
		db_table = 'h_type'


class HRoleMenu(BaseModel):
	"""
	角色和菜单关联关系表
	"""
	menu = ForeignKeyField(HMenu, db_column='menu_id')
	role = ForeignKeyField(HRole, db_column='role_id')

	class Meta:
		db_table = 'h_role_menu'
		primary_key = CompositeKey('menu', 'role')


class HRoleOrg(BaseModel):
	"""
	角色和机构关联关系表
	"""
	org = ForeignKeyField(HOrg, db_column='org_id')
	role = ForeignKeyField(HRole, db_column='role_id')

	class Meta:
		db_table = 'h_role_org'
		primary_key = CompositeKey('org', 'role')


class HRoleUser(BaseModel):
	"""
	角色和用户关联关系表
	"""
	role = ForeignKeyField(HRole, db_column='role_id')
	user = ForeignKeyField(HUser, db_column='user_id')

	class Meta:
		db_table = 'h_role_user'
		primary_key = CompositeKey('user', 'role')


class HUserOrg(BaseModel):
	"""
	用户和机构关联关系表
	"""
	org = ForeignKeyField(HOrg, db_column='org_id')
	user = ForeignKeyField(HUser, db_column='user_id')

	class Meta:
		db_table = 'h_user_org'
		primary_key = CompositeKey('user', 'org')


if __name__ == "__main__":
	from haoAdmin.util import singletons
	from playhouse import shortcuts

	user = HUser.select().where(HUser.pid == 1)
	print user
	print len(user)
	print [r for r in user.dicts()][0]
	dogpile_cache = singletons.Dogpiles()[0]
	dogpile_cache.set("login_user", user)

	for u in user:
		print u.login_name, u.user_name

	user = dogpile_cache.get("login_user")
	print user
	for u in user:
		print u.login_name, u.user_name

	roleUser = HRoleUser.select().where(HRoleUser.user == 1)
	print roleUser
	print [shortcuts.model_to_dict(r) for r in roleUser]
	for ru in roleUser:
		user = ru.user
		role = ru.role
		print user.user_name, role.role_name, role.role_code


