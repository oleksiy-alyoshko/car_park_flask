import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True


SECRET_KEY = 'testkey'
DATABASE_URI = os.environ.get("DATABASE_URI") or 'sqlite:///' + os.path.join(_basedir, 'MyCars.sqlite')
DATABASE_CONNECT_OPTIONS = {}
ADMINS = frozenset(['http://lucumr.pocoo.org/'])


del os