from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv, find_dotenv
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import config


load_dotenv(find_dotenv())

mail = Mail()
bootstrap = Bootstrap()
db = SQLAlchemy()


login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    app.url_map.strict_slashes = False

    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)

    login_manager.init_app(app)

    with app.app_context():
        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)

        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # with app.app_context():
    #     from . import db
    #     db.init_app(app)
    #     db.init_db()
    #
    #     from .main import main as main_blueprint
    #     app.register_blueprint(main_blueprint)
    #
    #     from .auth import auth as auth_blueprint
    #     app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
