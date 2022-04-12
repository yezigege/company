from views.hello import hello_bp


def register_blueprints_views(app):
    app.register_blueprint(hello_bp)