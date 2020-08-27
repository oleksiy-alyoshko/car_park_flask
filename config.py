import os

_basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'testkey')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    CLIENT_ID = os.getenv('CLIENT_ID', '')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET', '')
    REDIRECT_URI = os.getenv('REDIRECT_URI', '')
    GOOGLE_MAPS_KEY = os.getenv('GOOGLE_MAPS_KEY', '')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', 'sqlite:///' + os.path.join(_basedir, 'data-dev.sqlite'))


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite:///' + os.path.join(_basedir, 'data-test.sqlite'))


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(_basedir, 'data.sqlite'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}