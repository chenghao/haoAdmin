# coding:utf-8
__author__ = 'chenghao'
from bottle import Bottle, request, response, static_file
import os, re, json
from .upload import Uploader

ueditor_bottle = Bottle()
CONFIG = None


@ueditor_bottle.route('/ueditor', method=['GET', 'POST', 'OPTIONS'])
def ueditor():
	"""UEditor文件上传接口
	config 配置文件
	result 返回结果
	"""
	mimetype = 'application/json'
	result = {}
	action = request.query.get('action')

	if action == 'config':
		get_json_data(action)
		# 初始化时，返回配置文件给客户端
		result = CONFIG
	elif action in ('uploadimage', 'uploadfile', 'uploadvideo'):
		# 图片、文件、视频上传
		if action == 'uploadimage':
			field_name = CONFIG.get('imageFieldName')
			config = {
				"pathFormat": CONFIG['imagePathFormat'],
				"maxSize": CONFIG['imageMaxSize'],
				"allowFiles": CONFIG['imageAllowFiles']
			}
		elif action == 'uploadvideo':
			field_name = CONFIG.get('videoFieldName')
			config = {
				"pathFormat": CONFIG['videoPathFormat'],
				"maxSize": CONFIG['videoMaxSize'],
				"allowFiles": CONFIG['videoAllowFiles']
			}
		else:
			field_name = CONFIG.get('fileFieldName')
			config = {
				"pathFormat": CONFIG['filePathFormat'],
				"maxSize": CONFIG['fileMaxSize'],
				"allowFiles": CONFIG['fileAllowFiles']
			}
		if field_name in request.files:
			field = request.files.getall(field_name)[0]
			uploader = Uploader(field, config, CONFIG["absolutePath"] if CONFIG["absolutePath"] else os.getcwd())
			result = uploader.get_file_info()
		else:
			result['state'] = '上传接口出错'
	elif action in ('uploadscrawl'):
		# 涂鸦上传
		field_name = CONFIG.get('scrawlFieldName')
		config = {
			"pathFormat": CONFIG.get('scrawlPathFormat'),
			"maxSize": CONFIG.get('scrawlMaxSize'),
			"allowFiles": CONFIG.get('scrawlAllowFiles'),
			"oriName": "scrawl.png"
		}
		if field_name in request.forms:
			field = request.forms.get(field_name)
			uploader = Uploader(field, config, CONFIG["absolutePath"] if CONFIG["absolutePath"] else os.getcwd(),
								'base64')
			result = uploader.get_file_info()
		else:
			result['state'] = '上传接口出错'
	elif action in ('catchimage'):
		config = {
			"pathFormat": CONFIG['catcherPathFormat'],
			"maxSize": CONFIG['catcherMaxSize'],
			"allowFiles": CONFIG['catcherAllowFiles'],
			"oriName": "remote.png"
		}
		field_name = CONFIG['catcherFieldName']
		if field_name in request.forms:
			# 这里比较奇怪，远程抓图提交的表单名称不是这个
			source = []
		elif '%s[]' % field_name in request.forms:
			# 而是这个
			source = request.forms.getall('%s[]' % field_name)
		_list = []
		for imgurl in source:
			uploader = Uploader(imgurl, config, CONFIG["absolutePath"] if CONFIG["absolutePath"] else os.getcwd(),
								'remote')
			info = uploader.get_file_info()
			_list.append({
				'state': info['state'],
				'url': info['url'],
				'original': info['original'],
				'source': imgurl,
			})
		result['state'] = 'SUCCESS' if len(_list) > 0 else 'ERROR'
		result['list'] = _list
	else:
		result['state'] = '请求地址出错'

	if 'callback' in request.query:
		callback = request.args.get('callback')
		if re.match(r'^[\w_]+$', callback):
			result = '%s(%s)' % (callback, result)
			mimetype = 'application/javascript'
		else:
			result = {'state': 'callback参数不合法'}

	response.content_type = mimetype
	response.set_header('Access-Control-Allow-Origin', '*')
	response.set_header('Access-Control-Allow-Headers', 'X-Requested-With,X_Requested_With')
	return result


'''
@ueditor_bottle.get('/upload/<filename:path>')
def static(filename):
	""" Serve static files """
	return static_file(filename, root='./upload/')
'''


def get_json_data(action):
	"""
	获取json内容
	:param action:
	:return:
	"""
	global CONFIG
	path = os.path.join(os.path.dirname(__file__), "../static/ueditor1_4_3_1-utf8-py/")
	# 获取json文件的内容, 并把注释替换掉
	with open(path + "/" + action + ".json", "r") as f:
		try:
			r = re.compile(r"(\/\*[\s\S]+?\*\/)")
			CONFIG = json.loads(r.sub('', f.read()))
		except:
			CONFIG = {}
