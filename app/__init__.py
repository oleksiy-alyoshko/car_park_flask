import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


from flask import Flask


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    with app.app_context():
        from . import db
        db.init_app(app)
        db.init_db()

        from . import auth
        app.register_blueprint(auth.bp)

        # from . import blog
        # app.register_blueprint(blog.bp)
        # app.add_url_rule('/', endpoint='index')

    return app
