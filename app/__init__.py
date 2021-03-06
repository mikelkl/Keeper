# -*- coding: utf-8 -*-

from config import config
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

    # 主要功能的蓝图
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # 认证功能的蓝图
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # 实现REST API,为移动端提供数据的蓝图
    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
