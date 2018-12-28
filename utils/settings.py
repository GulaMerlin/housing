import os

# 基础路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# static目录
STATIC_PATH = os.path.join(BASE_DIR, 'static')

# templates路径
TEMPLATES_PATH = os.path.join(BASE_DIR, 'templates')

# media路径
MEDIA_PATH = os.path.join(STATIC_PATH, 'media')


DATABASE = {
    'USER': 'root',
    'PASSWORD': '123456',
    'PORT': '3306',
    'HOST': '127.0.0.1',
    'NAME': 'housing',
    'DRIVER': 'pymysql',
    'ENGINE': 'mysql'
}