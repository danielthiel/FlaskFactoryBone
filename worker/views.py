#! python
# -*- coding: utf-8 -*-


from flask import Blueprint, flash
from flask import render_template, redirect, url_for, request
from flask.ext.login import login_required

from utils import create_json_response

workermgmt = Blueprint('workermgmt', __name__)




# Main View:
@workermgmt.route('/')
def index():
    return render_template('worker/index.html')



@workermgmt.route('/apitest')
def test():
    return create_json_response({'myfield':True}, 200, 'extra message')