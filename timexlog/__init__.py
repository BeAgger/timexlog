"""
Initialize app

Imports:
    Flask:
        Flask
    flask_sqlalchemy, ORM to handle db
    flask_bcrypt, pw encryption
    flask_login, handle logins, user auth etc
    flask_mail, send emails
    timexlog: config
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from timexlog.config import app_config


db = SQLAlchemy()
bcrypt_flask = Bcrypt()
login_mgr = LoginManager()
login_mgr.login_view = 'users.login'
login_mgr.login_message_category = 'info'
mail = Mail()

# App factory function
# def create_app(config_class=Config):
def create_app(config_name):
    """
    App factory function
    Args: Configuration object for our app, ie dev, prod etc.
    Imports:
        timexlog:
            users.routes: user blueprint
            blog.routes: post blueprint
            main.routes: main blueprint
            error.handlers: error blueprint
    """
    # app = Flask(__name__)
    # app.config.from_object(Config)
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    # app.config.from_pyfile('config.py')

    from timexlog.users.routes import users
    from timexlog.blog.routes import blog
    from timexlog.main.routes import main
    from timexlog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(blog)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    db.init_app(app)
    bcrypt_flask.init_app(app)
    login_mgr.init_app(app)
    mail.init_app(app)

    migrate = Migrate(app, db)

    # from timexlog import models

    return app
