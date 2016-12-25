#coding:utf-8
__author__ = "chenghao"

import ConfigParser, os, logging
from logging import handlers
from dogpile.cache import make_region

path = "./conf.ini"
# path = "../conf.ini"


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


class SingletonLog(type):
	"""
	日志单例
	"""
	def __init__(cls, name, bases, dict):
		super(SingletonLog, cls).__init__(name, bases, dict)
		cls._instances = None

	def __call__(cls, *args, **kwargs):
		if cls._instances is None:
			super(SingletonLog, cls).__call__(*args, **kwargs)
			conf = Conf()
			# 按每天生成日志文件 linux
			file_path = conf.get("log", "path")
			parent_path = os.path.dirname(file_path)
			if not os.path.exists(parent_path):
				os.makedirs(parent_path)
			log_handler = handlers.TimedRotatingFileHandler(file_path, conf.get("log", "when"), conf.getint("log", "interval"))
			# 格式化日志内容
			format_ = "%(asctime)s %(pathname)-5s %(funcName)-5s %(lineno)-5s %(levelname)-5s %(message)s"
			log_formatter = logging.Formatter(format_)
			log_handler.setFormatter(log_formatter)
			# 设置记录器名字
			log = logging.getLogger('haoAdmin')
			log.addHandler(log_handler)
			# 设置日志等级
			log.setLevel(conf.get("log", "level"))
			cls._instances = log
		return cls._instances


class Log(object):
	"""
	获取log实例
	"""
	__metaclass__ = SingletonLog


class SingletonDogpile(type):
	"""
	缓存单例
	"""
	def __init__(cls, name, bases, dict):
		super(SingletonDogpile, cls).__init__(name, bases, dict)
		cls._instances_cache_m = None
		cls._instances_cache_f = None
		cls._instances_session_m = None
		cls._instances_session_m = None

	def __call__(cls, *args, **kwargs):
		if cls._instances_cache_m is None and cls._instances_cache_f is None \
			and cls._instances_session_m is None and cls._instances_session_m is None:

			super(SingletonDogpile, cls).__call__(*args, **kwargs)
			conf = Conf()
			file_path = conf.get("dogpile", "cache.file.arguments.filename")
			parent_path = os.path.dirname(file_path)
			if not os.path.exists(parent_path):
				os.makedirs(parent_path)

			dogpile_conf = {
				"cache.memory.backend": conf.get("dogpile", "cache.memory.backend"),
				"cache.memory.expiration_time": conf.getint("dogpile", "cache.memory.expiration_time"),
				"cache.file.backend": conf.get("dogpile", "cache.file.backend"),
				"cache.file.expiration_time": conf.getint("dogpile", "cache.file.expiration_time"),
				"cache.file.arguments.filename": conf.get("dogpile", "cache.file.arguments.filename"),

				"session.memory.backend": conf.get("dogpile", "session.memory.backend"),
				"session.memory.expiration_time": conf.getint("dogpile", "session.memory.expiration_time"),
				"session.file.backend": conf.get("dogpile", "session.file.backend"),
				"session.file.expiration_time": conf.get("dogpile", "session.file.expiration_time"),
				"session.file.arguments.filename": conf.get("dogpile", "session.file.arguments.filename")
			}
			cls._instances_cache_m = make_region().configure_from_config(dogpile_conf, "cache.memory.")
			cls._instances_cache_f = make_region().configure_from_config(dogpile_conf, "cache.file.")
			cls._instances_session_m = make_region().configure_from_config(dogpile_conf, "session.memory.")
			cls._instances_session_f = make_region().configure_from_config(dogpile_conf, "session.file.")
		return cls._instances_cache_m, cls._instances_cache_f, cls._instances_session_m, cls._instances_session_f


class Dogpiles(object):
	"""
	获取缓存实例
	"""
	__metaclass__ = SingletonDogpile


def get_cache_memory():
	return Dogpiles()[0]


def get_cache_file():
	return Dogpiles()[1]


def get_session_memory():
	return Dogpiles()[2]


def get_session_file():
	return Dogpiles()[3]


if __name__ == "__main__":
	conf = Conf()
	print conf.get("mysql", "db")

	log = Log()
	log.info("wwwwwwwwwwww")

	dogpiles = Dogpiles()
	dogpile_cache = dogpiles[1]
	dogpile_cache.set("chenghao", "222333444")
	print dogpile_cache.get("chenghao")
	dogpile_cache.delete("chenghao")
	print dogpile_cache.get("chenghao")