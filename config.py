import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = os.getenv('DEBUG', False)

SECRET_KEY = os.getenv('SECRET_KEY', 'testkey')

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(_basedir, 'MyCars.sqlite'))
DATABASE_CONNECT_OPTIONS = {}

CLIENT_ID = os.getenv('CLIENT_ID', '')
CLIENT_SECRET = os.getenv('CLIENT_SECRET', '')
REDIRECT_URI = os.getenv('REDIRECT_URI', '')

ADMINS = frozenset(['http://lucumr.pocoo.org/'])

del os
