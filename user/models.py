#! python
# -*- coding: utf-8 -*-

import datetime
import string
from random import choice
from hashlib import md5
from uuid import uuid4
from pbkdf2 import crypt

from sqlalchemy import Column
from sqlalchemy import Integer, String, Boolean, DateTime, Float, Text

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from server import db


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    _is_admin = Column(Boolean, default=False)
    name = Column(String(64))
    mail = Column(String(64), unique=True)
    password = Column(String(256))
    last_pw_reset = Column(DateTime, default=datetime.datetime.utcnow)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def is_admin(self):
        return self._is_admin

    def create_random_password(self):
        chars=string.ascii_uppercase + string.digits
        random_pw = ''.join(choice(chars) for _ in range(12))
        # self.set_password(random_pw) # Do not add this
        return random_pw

    def set_password(self, password):
        self.last_pw_reset = datetime.datetime.utcnow()
        self.password = crypt(password)

    def check_password(self, password):
        return self.password == crypt(password, self.password)

    # Required for administrative interface
    def __unicode__(self):
        return self.mail

    def __init__(self, name, mail, unhashed_pw='openid_secret'):
        self.name = name
        self.mail = mail
        self.set_password(unhashed_pw)

