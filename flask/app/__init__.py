#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import *
from dateutil.relativedelta import *
from time import mktime

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask import render_template


class ConfigClass(object):
    SECRET_KEY = 'asd'
    SQLALCHEMY_DATABASE_URI = 'C:/Users/user1/Desktop/GrishHelen/Python/PyCharm/O19/Olesya/flask/db.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USER_APP_NAME = "Question"
    JWT_SECRET_KEY = 'super-secret'


db = SQLAlchemy()
jwt = JWTManager()


def create_app(conﬁg_name):
    app = Flask(__name__)

    CORS(app)

    app.conﬁg.from_object(__name__ + '.ConfigClass')

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return render_template('index.html')

    from roles import roles_api
    app.register_blueprint(roles_api, url_prefix='/roles')

    from users import users_api
    app.register_blueprint(users_api, url_prefix='/users')

    from auth import auth_api
    app.register_blueprint(auth_api, url_prefix='/auth')

    from answers import answer_api
    app.register_blueprint(answer_api, url_prefix='/answers')

    return app
