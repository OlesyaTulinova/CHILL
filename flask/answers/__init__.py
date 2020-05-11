#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request
from flask import jsonify
from app import db

from app.models import User, Answer

answer_api = Blueprint('answer_api', __name__)


@answer_api.route('/get')
@jwt_required
def get_all():
    uid = get_jwt_identity()
    user = User.query.filter_by(id=uid).first()

    if user.role.name == "admin":
        return jsonify([{"id": object.id, "name": object.user.username, } for object in Answer.query.all()])

    return jsonify([])


@answer_api.route('/get/<int:id>')
@jwt_required
def get(id):
    uid = get_jwt_identity()
    user = User.query.filter_by(id=uid).first()

    if user.role.name == "admin":
        object = Answer.query.filter_by(id=id).first()
        return jsonify({"id": object.id, "name": object.name, "uid": object.user.id})

    return jsonify({})


@answer_api.route('/add', methods=['POST'])
@jwt_required
def add():
    uid = get_jwt_identity()
    user = User.query.filter_by(id=uid).first()

    if user.role.name == "admin":
        uid = request.form['uid']
        user_add = User.query.filter_by(id=uid).first()

        name = request.form['name']
        object = Answer(name=name, user=user_add)

        db.session.add(object)
        db.session.commit()

        return jsonify({"response": True})

    return jsonify({})


@answer_api.route('/delete/<int:id>', methods=['GET'])
@jwt_required
def delete(id):
    uid = get_jwt_identity()
    user = User.query.filter_by(id=uid).first()

    if user.role.name == "admin":
        object = Answer.query.filter_by(id=id).first()

        db.session.delete(object)
        db.session.commit()

        return jsonify({"response": True})

    return jsonify({})


@answer_api.route('/user/add', methods=['POST'])
@jwt_required
def user_add():
    uid = get_jwt_identity()
    user = User.query.filter_by(id=uid).first()

    if user.role.name == "user":
        name = request.form['name']
        object = Answer(name=name, user=user)

        db.session.add(object)
        db.session.commit()

        return jsonify({"response": True})

    return jsonify({})
