# coding:utf-8
__author__ = "gaunt"

import conf
from playhouse.pool import PooledMySQLDatabase
from peewee import Model, AutoField, BigAutoField, CharField, IntegerField, DateTimeField, SQL


database = PooledMySQLDatabase(conf.mysql_db, **conf.mysql_conn_param)


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class SysAuthorities(BaseModel):
    authority = CharField(primary_key=True)
    authority_name = CharField()
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    parent_name = CharField(null=True)
    sort = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'sys_authorities'


class SysConfig(BaseModel):
    config_name = CharField()
    config_value = CharField()
    mark = CharField(null=True)

    class Meta:
        table_name = 'sys_config'


class SysDictData(BaseModel):
    del_state = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    name = CharField(null=True)
    parent_id = IntegerField(null=True)
    sort = IntegerField(null=True)
    value = CharField(null=True)

    class Meta:
        table_name = 'sys_dict_data'


class SysMenu(BaseModel):
    authority = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    menu_icon = CharField(null=True)
    menu_id = AutoField()
    menu_name = CharField()
    menu_url = CharField(null=True)
    parent_id = IntegerField(constraints=[SQL("DEFAULT -1")])
    sort_number = IntegerField(constraints=[SQL("DEFAULT 0")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'sys_menu'


class SysOperLog(BaseModel):
    business_type = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    error_msg = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    id = BigAutoField()
    method = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    oper_id = IntegerField(null=True)
    oper_ip = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    oper_location = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    oper_param = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    oper_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    oper_url = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    status = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    title = CharField(constraints=[SQL("DEFAULT ''")], null=True)

    class Meta:
        table_name = 'sys_oper_log'


class SysRole(BaseModel):
    comments = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    role_code = CharField(unique=True)
    role_id = AutoField()
    role_name = CharField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'sys_role'


class SysRoleAuthorities(BaseModel):
    authority = CharField(index=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    role_id = IntegerField(index=True)

    class Meta:
        table_name = 'sys_role_authorities'
        indexes = (
            (('role_id', 'authority'), True),
        )


class SysUser(BaseModel):
    avatar = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    department_id = IntegerField(null=True)
    nick_name = CharField(null=True)
    password = CharField()
    phone = CharField(null=True)
    sec_key = CharField(null=True)
    sex = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    state = IntegerField(constraints=[SQL("DEFAULT 1")])
    true_name = CharField(index=True, null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    user_id = AutoField()
    username = CharField(unique=True)

    class Meta:
        table_name = 'sys_user'


class SysUserRole(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    role_id = IntegerField(index=True)
    user_id = IntegerField(index=True)

    class Meta:
        table_name = 'sys_user_role'
        indexes = (
            (('user_id', 'role_id'), True),
        )