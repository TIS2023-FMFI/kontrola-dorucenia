from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from .config import get_env

db = SQLAlchemy()
DB_NAME = get_env("DB_NAME")


def create_app():
    app = Flask(__name__)
    key = get_env("SECRET_KEY")
    app.config['SECRET_KEY'] = key.encode()
    app.config['SQLALCHEMY_DATABASE_URI'] = get_env("SQLALCHEMY")
    db.init_app(app)
    
    from .views import views
    from .authorization import auth
    from .requests import requests
    from .communication import communication

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(requests, url_prefix='/')
    app.register_blueprint(communication, url_prefix='/')

    from .models import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
