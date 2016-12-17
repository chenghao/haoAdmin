#coding:utf-8
__author__ = "chenghao"

import ConfigParser

path = "./haoAdmin/conf.ini"


class SingletonConf(type):
	"""
	配置文件单例
	"""
	def __init__(cls, name, bases, dict):
		super(SingletonConf, cls).__init__(name, bases, dict)
		cls._instances = None

	def __call__(cls, *args, **kwargs):
		if cls._instances is None:
			super(SingletonConf, cls).__call__(*args, **kwargs)
			cls._instances = ConfigParser.SafeConfigParser()
			cls._instances.read(path)
		return cls._instances


class Conf(object):
	"""
	获取配置文件
	"""
	__metaclass__ = SingletonConf