#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 2
# admin
# pbkdf2:sha256:150000$ZM1sixkC$f8fb011fb75325fff5537551df788e56bc2af6c4d4711a737fcc62b3bbc421ac


from app import db
from sqlalchemy.orm import relationship

from werkzeug.security import generate_password_hash, check_password_hash


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = relationship("Role")

    username = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))

    surname = db.Column(db.String(100))
    name = db.Column(db.String(100))
    middle_name = db.Column(db.String(100))

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User")

    def __repr__(self):
        return '<User %r>' % self.user.username
