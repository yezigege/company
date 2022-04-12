from distutils.debug import DEBUG
from distutils.log import INFO


DEBUG=True

# 记录日志级别
LOG_LEVEL='INFO'

# 基础连接配置
REDIS_HOST = '127.0.0.1'
REDIS_PSWD = 'redis'

# redis连接配置
REDIS_SETTINGS = {
    'host': REDIS_HOST,
    'port': 6379,
    'db': 1,
    'password': REDIS_PSWD
}