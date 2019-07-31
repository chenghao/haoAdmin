# coding:utf-8
__author__ = "gaunt"
import os, logging
from logging import handlers
from conf import log as log_obj


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
            # 按每天生成日志文件 linux
            file_path = log_obj["log_file_path"]
            parent_path = os.path.dirname(file_path)
            if not os.path.exists(parent_path):
                os.makedirs(parent_path)
            log_handler = handlers.TimedRotatingFileHandler(file_path, log_obj["log_when"], log_obj["log_interval"])
            # 格式化日志内容
            log_formatter = logging.Formatter(log_obj["log_format"])
            log_handler.setFormatter(log_formatter)
            # 设置记录器名字
            log = logging.getLogger('bottle_admin')
            log.addHandler(log_handler)

            # 再创建一个handler，用于输出到控制台
            console = logging.StreamHandler()
            console.setFormatter(log_formatter)
            log.addHandler(console)

            # 设置日志等级
            log.setLevel(log_obj["log_level"])
            cls._instances = log
        return cls._instances


class Log(metaclass=SingletonLog):
    """
    获取log实例
    """

