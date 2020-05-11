#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request
from flask import jsonify
from app import db

from app.models import Role, User

users_api = Blueprint('users_api', __name__)


@users_api.route('/get')
@jwt_required
def get_all():
    uid = get_jwt_identity()
    user = User.query.filter_by(id=uid).first()

    if user.role.name == "admin":
        return jsonify([{"id": object.id, "name": object.username, } for object in db.session.query(User).all()])

    return jsonify([])


@users_api.route('/get/<int:id>')
@jwt_required
def get(id):
    uid = get_jwt_identity()
    user = User.query.filter_by(id=uid).first()

    if user.role.name == "admin":
        object = User.query.filter_by(id=id).first()
        return jsonify(
            {"rid": object.role.id, "username": object.username, "password": object.password_hash, "name": object.name,
             "surname": object.surname, "middle_name": object.middle_name, })

    return jsonify({})


@users_api.route('/add', methods=['POST'])
@jwt_required
def add():
    uid = get_jwt_identity()
    user = User.query.filter_by(id=uid).first()

    if user.role.name == "admin":
        rid = request.form['rid']
        role = Role.query.filter_by(id=rid).first()

        name = request.form['name']
        psw = request.form['psw']

        surname = request.form['surname']
        name = request.form['name']
        middle_name = request.form['middle_name']

        object = User(role=role, username=name, password=psw, surname=surname, name=name, middle_name=middle_name)

        db.session.add(object)
        db.session.commit()

        return jsonify({"response": True})

    return jsonify({})


@users_api.route('/delete/<int:id>', methods=['GET'])
@jwt_required
def delete(id):
    uid = get_jwt_identity()
    user = User.query.filter_by(id=uid).first()

    if user.role.name == "admin":
        object = User.query.filter_by(id=id).first()

        db.session.delete(object)
        db.session.commit()

        return jsonify({"response": True})

    return jsonify({})


@users_api.route('/update/<int:id>', methods=['POST'])
@jwt_required
def update(id):
    uid = get_jwt_identity()
    user = User.query.filter_by(id=uid).first()

    if user.role.name == "admin":
        name = request.form['name']

        object = User.query.filter_by(id=id).first()
        object.username = name

        # psw = request.form['psw']
        # print(object.verify_password(psw))

        db.session.commit()

        return jsonify({"response": True})

    return jsonify({})
