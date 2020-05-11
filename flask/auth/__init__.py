#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import *
from dateutil.relativedelta import *
from time import mktime

from flask_jwt_extended import jwt_required, create_access_token, get_jwt_claims

from flask import Blueprint, request
from flask import jsonify
from app import db
from app import jwt

from app.models import Role, User

auth_api = Blueprint('auth_api', __name__)


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {'uid': identity}


@auth_api.route('/sign-in', methods=['POST'])
def sign_in():
    response = {"is_auth": False, "token": "", "err": "Логин или пароль не правильны."}

    name = request.form['name']

    object = User.query.filter_by(username=name).first()

    if object is not None:

        psw = request.form['psw']

        if object.verify_password(psw):
            access_token = create_access_token(identity=object.id)

            response = {"is_auth": True, "token": access_token}

    return jsonify(response)


@auth_api.route('/user/get', methods=['GET'])
@jwt_required
def user_get():
    claims = get_jwt_claims()
    uid = claims['uid']

    object = User.query.filter_by(id=uid).first()

    return jsonify({"role": object.role.name, "is_auth": True})


@auth_api.route('/user/registration', methods=['POST'])
def registration():
    respone = {'is': True, 'name': "Введите корректный логин и пароль!"}

    name = request.form['name']

    if len(name) > 0:

        object = User.query.filter_by(username=name).first()

        if object is None:

            psw = request.form['psw']

            if len(psw) > 0:
                role = Role.query.filter_by(name='user').first()

                surname = request.form['surname']
                name = request.form['name']
                middle_name = request.form['middle_name']

                object = User(role=role, username=name, password=psw, surname=surname, name=name,
                              middle_name=middle_name)

                db.session.add(object)
                db.session.commit()

                respone['is'] = False
                respone['name'] = ""
        else:

            respone['name'] = "Выберите другой логин!"

    return jsonify(respone)
