#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request
from flask import jsonify
from app import db

from app.models import Role, User

roles_api = Blueprint('roles_api', __name__)


@roles_api.route('/get')
@jwt_required
def get_all():
    uid = get_jwt_identity()
    user = User.query.filter_by(id=uid).first()

    if user.role.name == "admin":
        return jsonify([{"id": role.id, "name": role.name, } for role in Role.query.all()])

    return jsonify([])


@roles_api.route('/get/<int:id>')
@jwt_required
def get(id):
    uid = get_jwt_identity()
    user = User.query.filter_by(id=uid).first()

    if user.role.name == "admin":
        role = Role.query.filter_by(id=id).first()
        return jsonify({"id": role.id, "name": role.name, })

    return jsonify({})


@roles_api.route('/add', methods=['POST'])
@jwt_required
def add():
    uid = get_jwt_identity()
    user = User.query.filter_by(id=uid).first()

    if user.role.name == "admin":
        name = request.form['name']

        admin = Role(name=name, )
        db.session.add(admin)
        db.session.commit()

        return jsonify({"response": True})

    return jsonify({})


@roles_api.route('/delete/<int:id>', methods=['GET'])
@jwt_required
def delete(id):
    uid = get_jwt_identity()
    user = User.query.filter_by(id=uid).first()

    if user.role.name == "admin":
        role = Role.query.filter_by(id=id).first()

        db.session.delete(role)
        db.session.commit()

        return jsonify({"response": True})

    return jsonify({})


@roles_api.route('/update/<int:id>', methods=['POST'])
@jwt_required
def update(id):
    uid = get_jwt_identity()
    user = User.query.filter_by(id=uid).first()

    if user.role.name == "admin":
        name = request.form['name']

        role = Role.query.filter_by(id=id).first()
        role.name = name
        db.session.commit()

        return jsonify({"response": True})

    return jsonify({})
