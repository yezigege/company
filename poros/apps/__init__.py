from flask import Flask, request
import logging

from util.profile import Profiler


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
    register_redis(app)
    register_request_handle(app)
    register_apispec(app)
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


def register_redis(app):
    from redis import Redis
    cfg = app.config['REDIS_SETTINGS']
    app.redis = Redis(**cfg, max_connections=20)
    app.redis_decode = Redis(**cfg, decode_responses=True, max_connections=30)


def register_request_handle(app):
    app.before_request(before_request)
    app.after_request(after_request)


def before_request():
    try:
        request.pr = Profiler.get_profiler(request.path)
    except:
        request.pr = None


def after_request(resp):
    try:
        if resp.status.startswith('200 '):
            pr = getattr(request, 'pr', None)
            if pr:
                pr.disable()
                Profiler.end(request.path, pr)
    except Exception:
        pass
    return resp


def register_apispec(app):
    from apispec import APISpec
    from apispec.ext.marshmallow import MarshmallowPlugin
    from util.flask_apispec import FlaskPlugin, FlaskApiSpec
    from webargs.flaskparser import FlaskParser
    from marshmallow import EXCLUDE

    class Parser(FlaskParser):
        DEFAULT_UNKNOWN_BY_LOCATION = {"json": EXCLUDE}

    app.config.update({
        'APISPEC_SPEC': APISpec(
            title="POROS",
            version="1.0.0",
            openapi_version="2.0",
            info=dict(description="POROS API"),
            plugins=[FlaskPlugin(), MarshmallowPlugin()],
        ),
        'APISPEC_FORMAT_RESPONSE': None,
        'APISPEC_WEBARGS_PARSER': Parser(),
    })
    docs = FlaskApiSpec(app, document_options=False)
    docs.register_existing_resources()
