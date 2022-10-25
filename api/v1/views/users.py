#!/usr/bin/python3
"""view for User objects that handles all
default RESTFul API actions"""

from flask import abort, jsonify, request
from models import storage
from models.user import User
from api.v1.views import app_views

all = storage.all


@app_views.route('/users', methods=['GET', 'POST'])
def all_users():
    """retrieves all users or create an user"""
    if request.method == 'GET':
        all_users = all(User).values()
        json_users = [user.to_dict() for user in all_users]
        return jsonify(json_users)

    else:
        data = request.get_json()
        # if not request.is_json:
        # abort(400, {'message': 'Not a JSON'})
        if 'email' not in data:
            abort(400, 'Missing email')
        if 'password' not in data:
            abort(400, 'Missing password')
        obj = User(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_object(user_id):
    """retrieves, deletes and updates an user"""
    try:
        user = all()[f'User.{user_id}']
    except KeyError:
        abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        all().__delitem__(f'User.{user_id}')
        storage.save()
        return jsonify({}), 200
    else:
        data = request.get_json
        obj = user

        for key, value in request.get_json().items():
            if key not in ['created_at', 'updated_at', 'id', 'email']:
                obj.__dict__[key] = value
        obj.save()
        return jsonify(obj.to_dict()), 200
