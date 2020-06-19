import os
from pathlib import Path


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', ":'(")
    APP_STATIC_DIR = Path(os.getenv('APP_STATIC_DIR',
                                    str(Path(__file__).parent / 'app' / 'static')))
    APP_DATA_VENDOR = os.getenv('APP_DATA_VENDOR', 'sqlite')
    APP_DATABASE_FILE = Path(os.getenv('APP_DATABASE_FILE',
                                       str(Path(__file__).parent / 'data.db')))
    APP_DATABASE_HOST = os.getenv('APP_DATABASE_HOST', '127.0.0.1')
    APP_DATABASE_PORT = int(os.getenv('APP_DATABASE_PORT', '5432'))
    APP_DATABASE_NAME = os.getenv('APP_DATABASE_NAME', 'stepik_flask_teachers')
    APP_DATABASE_USER = os.getenv('APP_DATABASE_USER', '')
    APP_DATABASE_PASSWORD = os.getenv('APP_DATABASE_PASSWORD', '')

    @classmethod
    def init_app(cls, app):
        database_url = os.getenv('DATABASE_URL')
        if database_url is None:
            data_vendor = app.config.get('APP_DATA_VENDOR')
            if data_vendor == 'sqlite':
                app.config['SQLALCHEMY_DATABASE_URI'] = \
                    f"sqlite:///{app.config['APP_DATABASE_FILE']}"

            elif data_vendor == 'postgresql':
                url_parts = ['postgresql+psycopg2://']

                database_user = app.config.get('APP_DATABASE_USER', '').strip()
                if database_user:
                    url_parts.append(database_user)

                    database_password = app.config.get('APP_DATABASE_PASSWORD', '')
                    if database_password:
                        url_parts.append(':')
                        url_parts.append(database_password)

                    url_parts.append('@')

                url_parts.append(app.config['APP_DATABASE_HOST'])
                url_parts.append(':')
                url_parts.append(str(app.config['APP_DATABASE_PORT']))
                url_parts.append('/')
                url_parts.append(app.config['APP_DATABASE_NAME'])

                database_url = ''.join(url_parts)
                os.environ['DATABASE_URL'] = database_url

            else:
                raise RuntimeError(f"Unknown data vendor {data_vendor}")

        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
