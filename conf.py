# coding:utf-8
__author__ = "chenghao"

ROWS = 1  # 每页显示条数
STATIC_PREFIX = "./"  # 静态文件访问前缀
ADMIN_PREFIX = "/admin"  # 后台访问前缀
UEDITOR_PREFIX = ADMIN_PREFIX + "/ueditor"  # 后台福文本访问前缀

ADMIN_SESSION = "beaker.session"  # session KEY
CURRENT_USER = "current_user"  # 当前用户

session_opts = {
    'session.type': 'file',  # 'memory',         # 以文件的方式保存session
    'session.cookie_expires': 1800,              # session过期时间为300秒
    'session.cookie_path': ADMIN_PREFIX,         # session路径
    'session.data_dir': '/home/chenghao/cache',  # session保存目录
    'session.auto': True,                        # 自动保存session
}

cache_key = "short_term"
cache_opts = {
    cache_key: {
        'expire': 300,
        'type': 'memory'
    }
}
cache_opt = {
    "expire": 300,
    'type': 'memory'
}