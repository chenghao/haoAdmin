#coding:utf-8
__author__ = "chenghao"

import hashlib, base64, re, uuid, json
from datetime import datetime, date


def get_current_date(pattern="%Y-%m-%d %H:%M:%S", datetime_s=None):
	"""
	格式化日期
	:param pattern:
	:param datetime_s:
	:return:
	"""
	if datetime_s is None:
		result = datetime.now().strftime(pattern)
	elif isinstance(datetime_s, datetime):
		result = datetime_s.strftime(pattern)
	elif isinstance(datetime_s, date):
		result = datetime_s.strftime("%Y-%m-%d")
	else:
		result = datetime_s
	return result


def ver_mobile(data):
	"""
	验证手机号，正确返回True
	:param data:
	:return:
	"""
	p = re.compile(r"((13|14|15|17|18)\d{9}$)")
	return p.match(data)


def ver_email(data):
	"""
	验证邮箱，正确返回True
	:param data:
	:return:
	"""
	p = re.compile(r"(\w+[@]\w+[.]\w+)")
	return p.match(data)


def random_num():
	"""
	获取随机数
	:return:
	"""
	return uuid.uuid4().hex.lower()


class ComplexEncoder(json.JSONEncoder):
	"""
	json日期格式化
	"""
	def default(self, obj):
		if isinstance(obj, datetime):
			return obj.strftime('%Y-%m-%d %H:%M:%S')
		elif isinstance(obj, date):
			return obj.strftime('%Y-%m-%d')
		else:
			return json.JSONEncoder.default(self, obj)


def get_md5_s(s, salt="haoAdmin"):
	"""
	MD5加密
	:param s: 需要加密的字符串
	:param salt:  盐
	:return:  加密后的字符串
	"""
	if s == "":
		return ""
	md5code = hashlib.md5(s.encode()).hexdigest()[8:10]
	key = hashlib.md5(salt.encode()).hexdigest()
	len_key = len(key)
	_code = ""
	for i in range(len(s)):
		k = i % len_key
		# 先转为ascii在进行 ^ 运算
		_s = ord(s[i])
		_key = ord(key[k])

		_code += str(_s ^ _key)

	_encode = base64.b64encode(_code.encode("utf8"))
	_code = _encode.decode() + md5code
	return _code