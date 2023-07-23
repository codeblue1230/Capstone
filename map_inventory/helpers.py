# External Imports
from flask import request, jsonify
from functools import wraps
import secrets
import decimal
import requests
import json

# Internal Imports
from map_inventory.models import User


def token_required(my_flask_function):
    @wraps(my_flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split()[1]
            print(token)

        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            my_user = User.query.filter_by(token=token).first()
            print(my_user)
            if not my_user or my_user.token != token:
                return jsonify({'message': 'Token is invalid'}), 401
            
        except:
            my_user = User.query.filter_by(token=token).first()
            if token != my_user.token and secrets.compare_digest(token, my_user.token):
                return jsonify({'message': 'Token is invalid'}), 401
        return my_flask_function(my_user, *args, **kwargs)
    return decorated


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return json.JSONEncoder(JSONEncoder, self).default(obj)