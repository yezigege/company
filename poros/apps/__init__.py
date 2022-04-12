from flask import Flask
import logging


def create_app(config_filename: str = 'conf.settings'):
    """应用工厂
    https://dormousehole.readthedocs.io/en/latest/patterns/appfactories.html

    Args:
        config_filename (str, optional): 配置文件
    """
    app = Flask(__name__)
    app.config.from_object(config_filename)
    
    configure_logger(app)
    return app


def configure_logger(app):
    """Configure loggers. 配置日志打印等级为设定等级以上才打印"""
    rootLogger = logging.getLogger()
    rootLogger.setLevel(app.config.get('LOG_LEVEL') or 'WARN')