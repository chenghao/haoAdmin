# coding:utf-8
__author__ = "gaunt"

# mysql配置
mysql_db = "bottle"
mysql_conn_param = {
    "user": "root",
    "passwd": "123456",
    "host": "192.168.0.122",
    "port": 3306,
    "max_connections": 1000,
    "stale_timeout": 600
}

# redis配置
redis_conn_param = {
    "host": "192.168.0.122",
    "port": 6379,
    "password": "lym123..",
    "db": 5,
    "max_connections": 1000
}

# log配置
log = {
    "log_file_path": "/home/logs/bottle",
    "log_format": "%(asctime)s %(pathname)-5s %(funcName)-5s %(lineno)-5s %(levelname)-5s %(message)s",
    "log_level": "DEBUG",
    "log_when": "D",
    "log_interval": 1
}

# jwt
jwt_key = "gaunt"
jwt_algorithm = "HS256"
jwt_exp = 60 * 30

# 请求拦截
intercept_path = ["/sys/*"]
exclude_path = ["/login/*", "/assets/*", "/components/*", "/login.html", "/index.html"]

# redis key前缀
prefix_token = "prefix:token"
prefix_permit = "prefix:permit"
prefix_role = "prefix:role"

# 项目请求前缀
prefix = "/v1"
