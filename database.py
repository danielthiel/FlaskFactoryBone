#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from server import db, app
from user.models import User



def create_user_data(dbsession, count=1):
    for u in range(0,count):
        user = User('Vorname Nachname {0}'.format(u), '{0}@hf.com'.format(u), '1234')
        dbsession.add(user)
        print user.mail, user.id
    dbsession.commit()


if __name__ == '__main__':
    """
    """

    DB_NAME = 'dummy.db'
    if os.path.isfile(DB_NAME):
        os.remove(DB_NAME)
    db.create_all()
    with app.test_request_context():
        create_user_data(db.session, 2)