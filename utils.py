#! python
# -*- coding: utf-8 -*-


from flask import jsonify
from flask import make_response

_FLAG_DICT = {
    200: True,
    201: True,
    300: False,
    400: False,
    401: False,
    404: False,
    500: False
}

def create_json_response(data={}, statuscode=300, message=''):
    meta = {'flag': _FLAG_DICT[statuscode], 'code': statuscode, 'message': message}
    j = jsonify({'meta': meta, 'data': data})
    r = make_response(j, statuscode)
    return r