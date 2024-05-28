# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin

from sqlalchemy.orm import relationship
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

from apps import db, login_manager

from apps.authentication.util import hash_pass

class Clients(db.Model, UserMixin):

    __tablename__ = 'client-list'

    id            = db.Column(db.Integer, primary_key=True)
    first_name      = db.Column(db.String(15))
    second_name      = db.Column(db.String(15))
    first_last_name      = db.Column(db.String(15))
    second_last_name      = db.Column(db.String(15))
    document      = db.Column(db.String(15))
    age      = db.Column(db.Integer)
    state = db.Column(db.Boolean, default=True)
    addres      = db.Column(db.String(45))
    phone      = db.Column(db.String(15))
    medicall_info      = db.Column(db.String(50))
    email      = db.Column(db.String(45),unique=True)


