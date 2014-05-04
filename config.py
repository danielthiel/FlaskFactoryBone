#! python
# -*- coding: utf-8 -*-



class Config(object):
    APP_HOST = '0.0.0.0'
    APP_PORT =  5000
    DEBUG = True
    TESTING = False
    PRODUCTION = False
    SECRET_KEY = 'some_secret_key'


    SQLALCHEMY_DATABASE_URI = 'sqlite:///dummy.db'
