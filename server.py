#! python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import g
from flask import render_template
from flask.ext.login import login_user, current_user


# Initialize the App:
app = Flask(__name__)
app.config.from_object('config.Config')


# Init the DATABASE:
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# Init the LOGIN MANAGER:
from flask.ext.login import LoginManager
lm = LoginManager()
lm.init_app(app)



# Register the User View with Login:
from user.views import usermgmt
app.register_blueprint(usermgmt, url_prefix='/user') 


# Register the APPS::
from worker.views import workermgmt
app.register_blueprint(workermgmt, url_prefix='/worker')

from user.models import User
# Initialize Login Modul:
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# General Index-Page:
@app.route('/')
def index():
    return render_template('index.html')


@app.before_request
def before_request():
    if app.config.get('TESTING'):
        g.user = User.query.filter(User.id==1).one()
        login_user(g.user)
    else:
        g.user = current_user


if __name__ == '__main__':
    app.run(app.config.get('APP_HOST'), app.config.get('APP_PORT'))
