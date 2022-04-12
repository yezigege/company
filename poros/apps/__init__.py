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
    filter_warning()
    register_json_encoder(app)
    register_blueprints(app)
    return app


def configure_logger(app):
    """Configure loggers. 配置日志打印等级为设定等级以上才打印"""
    rootLogger = logging.getLogger()
    rootLogger.setLevel(app.config.get('LOG_LEVEL') or 'WARN')


def filter_warning():
    """警告过滤器
    通过设置 message 来正则匹配 warning 消息，如果匹配到。就忽略该警告。
    https://blog.csdn.net/TeFuirnever/article/details/94122670
    """
    import warnings
    warnings.filterwarnings(
        "ignore",
        message="Multiple schemas resolved to the name ",
    )


def register_json_encoder(app):
    """自定义app的json解析器
    https://dormousehole.readthedocs.io/en/latest/api.html?highlight=json_encoder#flask.json.JSONEncoder
    """
    from util.base_util import DateAndObjectIdEncoder
    app.json_encoder = DateAndObjectIdEncoder


def register_blueprints(app):
    from views import register_blueprints_views
    register_blueprints_views(app)
