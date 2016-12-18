# coding:utf-8
__author__ = 'chenghao'
import os, datetime, base64, urllib, random


class Uploader:
    stateMap = [
        "SUCCESS",  # 上传成功标记，在UEditor中内不可改变，否则flash判断会出错
    ]
    stateError = {
        "ERROR_SIZE_EXCEED": "文件大小超出网站限制",
        "ERROR_TYPE_NOT_ALLOWED": "文件类型不允许",
        "ERROR_CREATE_DIR": "目录创建失败",
        "ERROR_DIR_NOT_WRITEABLE": "目录没有写权限",
        "ERROR_FILE_MOVE": "文件保存时出错",
        "ERROR_UNKNOWN": "未知错误",
    }

    def __init__(self, fileobj, config, static_folder, _type=None):
        """
        :param fileobj: FileStorage, Base64Encode Data or Image URL
        :param config: 配置信息
        :param static_folder: 文件保存的目录
        :param _type: 上传动作的类型，base64，remote，其它
        """
        self.fileobj = fileobj
        self.config = config
        self.static_folder = static_folder
        self._type = _type
        if _type == 'base64':
            self.up_base64()
        elif _type == 'remote':
            self.save_remote()
        else:
            self.up_file()

    def up_file(self):
        # 上传文件的主处理方法
        self.ori_name = self.fileobj.filename
        # 获取文件大小
        self.file_size = os.path.getsize(self.fileobj.file.name)
        self.file_type = self.get_file_ext()
        self.full_name = self.get_full_name()
        self.file_path = self.get_file_path()
        # 检查文件大小是否超出限制
        if not self.check_size():
            self.stateInfo = self.get_state_error('ERROR_SIZE_EXCEED')
            return
        # 检查是否不允许的文件格式
        if not self.check_type():
            self.stateInfo = self.get_state_error('ERROR_TYPE_NOT_ALLOWED')
            return
        # 检查路径是否存在，不存在则创建
        dirname = os.path.dirname(self.file_path)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                self.stateInfo = self.get_state_error('ERROR_CREATE_DIR')
                return
        elif not os.access(dirname, os.W_OK):
            self.stateInfo = self.get_state_error('ERROR_DIR_NOT_WRITEABLE')
            return
        # 保存文件
        try:
            self.fileobj.save(self.file_path)
            self.stateInfo = self.stateMap[0]
        except:
            self.stateInfo = self.get_state_error('ERROR_FILE_MOVE')
            return

    def up_base64(self):
        # 处理base64编码的图片上传
        img = base64.b64decode(self.fileobj)
        self.ori_name = self.config['oriName']
        self.file_size = len(img)
        self.file_type = self.get_file_ext()
        self.full_name = self.get_full_name()
        self.file_path = self.get_file_path()
        # 检查文件大小是否超出限制
        if not self.check_size():
            self.stateInfo = self.get_state_error('ERROR_SIZE_EXCEED')
            return
        # 检查路径是否存在，不存在则创建
        dirname = os.path.dirname(self.file_path)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                self.stateInfo = self.get_state_error('ERROR_CREATE_DIR')
                return
        elif not os.access(dirname, os.W_OK):
            self.stateInfo = self.get_state_error('ERROR_DIR_NOT_WRITEABLE')
            return
        try:
            with open(self.file_path, 'wb') as fp:
                fp.write(img)
            self.stateInfo = self.stateMap[0]
        except:
            self.stateInfo = self.get_state_error('ERROR_FILE_MOVE')
            return

    def save_remote(self):
        _file = urllib.urlopen(self.fileobj)
        self.ori_name = self.config['oriName']
        self.file_size = 0
        self.file_type = self.get_file_ext()
        self.full_name = self.get_full_name()
        self.file_path = self.get_file_path()
        # 检查文件大小是否超出限制
        if not self.check_size():
            self.stateInfo = self.get_state_error('ERROR_SIZE_EXCEED')
            return
        # 检查路径是否存在，不存在则创建
        dirname = os.path.dirname(self.file_path)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                self.stateInfo = self.get_state_error('ERROR_CREATE_DIR')
                return
        elif not os.access(dirname, os.W_OK):
            self.stateInfo = self.get_state_error('ERROR_DIR_NOT_WRITEABLE')
            return
        try:
            with open(self.file_path, 'wb') as fp:
                fp.write(_file.read())
            self.stateInfo = self.stateMap[0]
        except:
            self.stateInfo = self.get_state_error('ERROR_FILE_MOVE')
            return

    def get_state_error(self, error):
        # 上传错误检查
        return self.stateError.get(error, 'ERROR_UNKNOWN')

    def check_size(self):
        # 文件大小检测
        return self.file_size <= self.config['maxSize']

    def check_type(self):
        # 文件类型检测
        return self.file_type.lower() in self.config['allowFiles']

    def get_file_path(self):
        # 获取文件完整路径
        root_path = self.static_folder
        file_path = ''
        for path in self.full_name.split('/'):
            file_path = os.path.join(file_path, path)
        return os.path.join(root_path, file_path)

    def get_file_ext(self):
        # 获取文件扩展名
        return ('.%s' % self.ori_name.split('.')[-1]).lower()

    def get_full_name(self):
        # 替换日期事件
        path_format = self.config['pathFormat']
        now = datetime.datetime.now()
        _time = now.strftime('%H%M%S')
        r = random.randint(1000, 9999)
        d = now.strftime("%Y-%y-%m-%d-%H-%M-%S").split("-")
        path_format = path_format.replace("{yyyy}", d[0])
        path_format = path_format.replace("{yy}", d[1])
        path_format = path_format.replace("{mm}", d[2])
        path_format = path_format.replace("{dd}", d[3])
        path_format = path_format.replace("{hh}", d[4])
        path_format = path_format.replace("{ii}", d[5])
        path_format = path_format.replace("{ss}", d[6])
        self.ori_name = "%s%s%s" % (_time, r, self.file_type)
        return "%s%s%s" % (path_format, "/", self.ori_name)

    def get_file_info(self):
        # 获取当前上传成功文件的各项信息
        return {
            'state': self.stateInfo,
            'url': self.full_name,
            'title': self.ori_name,
            'original': self.ori_name,
            'type': self.file_type,
            'size': self.file_size,
        }