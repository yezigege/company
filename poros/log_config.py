import logging
import logging.config
import cloghandler  # 不可缺少 参见 https://pypi.org/project/ConcurrentLogHandler/

from os import path
from util.logger_base import LoggerBase

project_path = path.dirname(path.abspath(__file__))
log_file_path = path.join(project_path, 'conf/log.conf')

# 读取日志配置文件
# https://www.cnblogs.com/yyds/p/6885182.html
logging.config.fileConfig(log_file_path, defaults={'project_path': project_path})
logger = LoggerBase("server_access")
logger_error = LoggerBase("server_error")
logger_celery = LoggerBase("celery_root")
