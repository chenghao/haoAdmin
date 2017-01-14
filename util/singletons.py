# coding:utf-8
__author__ = "chenghao"

import ConfigParser, os, logging
from logging import handlers
from beaker.cache import CacheManager
import conf

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


class SingletonCache(type):
    """
    缓存单例
    """
    def __init__(cls, name, bases, dict):
        super(SingletonCache, cls).__init__(name, bases, dict)
        cls._instances = None

    def __call__(cls, *args, **kwargs):
        if cls._instances is None:
            super(SingletonCache, cls).__call__(*args, **kwargs)
            cache = CacheManager(cache_regions=conf.cache_opts)
            cls._instances = cache
        return cls._instances


class Cache(object):
    """
    获取缓存实例
    """
    __metaclass__ = SingletonCache


if __name__ == "__main__":
    conf = Conf()
    print conf.get("mysql", "db")

    log = Log()
    log.info("wwwwwwwwwwww")
