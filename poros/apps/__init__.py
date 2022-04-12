from flask import Flask


def create_app(config_filename: str = 'conf.settings'):
    """应用工厂
    https://dormousehole.readthedocs.io/en/latest/patterns/appfactories.html

    Args:
        config_filename (str, optional): 配置文件
    """
    app = Flask(__name__)
    app.config.from_object(config_filename)
    
    return app