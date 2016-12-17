# coding:utf-8
__author__ = "chenghao"

from peewee import (Model, PrimaryKeyField, DateTimeField)
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
