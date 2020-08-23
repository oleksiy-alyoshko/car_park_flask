import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

SECRET_KEY = 'testkey'
DATABASE_URI = os.getenv("DATABASE_URI") or 'sqlite:///' + os.path.join(_basedir, 'MyCars.sqlite')
DATABASE_CONNECT_OPTIONS = {}
ADMINS = frozenset(['http://lucumr.pocoo.org/'])


del os