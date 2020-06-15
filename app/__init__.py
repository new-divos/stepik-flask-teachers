from flask import Flask

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_cls):
    app = Flask(__name__)
    app.config.from_object(config_cls)
    if hasattr(config_cls, 'init_app') and callable(config_cls.init_app):
        config_cls.init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
