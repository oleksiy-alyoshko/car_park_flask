from sqlalchemy import create_engine, Column, Integer, String, DateTime, \
     ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, backref, relation
from sqlalchemy.ext.declarative import declarative_base
import click

from flask import current_app
from flask.cli import with_appcontext

engine = create_engine(current_app.config['DATABASE_URL'],
                       convert_unicode=True,
                       **current_app.config['DATABASE_CONNECT_OPTIONS'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Model = declarative_base(name='Model')
Model.query = db_session.query_property()


class User(Model):
    __tablename__ = 'users'
    id = Column('user_id', Integer, primary_key=True)
    email = Column(String(200))
    password = Column(String(200))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    @property
    def is_admin(self):
        return self.id in current_app.config['ADMINS']


class Car(Model):
    __tablename__ = 'cars'
    id = Column('car_id', String(200), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    make = Column(String(50))
    access_token = Column(String(100))
    expiration = Column(DateTime)
    refresh_token = Column(String(100))
    refresh_expiration = Column(DateTime)

    user = relation(User, backref=backref('cars'))

    def __init__(self, make, access_token, expiration, refresh_token, refresh_expiration):
        self.make = make
        self.access_token = access_token
        self.expiration = expiration
        self.refresh_token = refresh_token
        self.refresh_expiration = refresh_expiration


def init_db():
    Model.metadata.create_all(bind=engine)


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.cli.add_command(init_db_command)

