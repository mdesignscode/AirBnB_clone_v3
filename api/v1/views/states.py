#!/usr/bin/python3
"""view for State objects that handles all
default RESTFul API actions"""

from flask import abort, jsonify, request
from models import storage
from models.state import State
from api.v1.views import app_views

all = storage.all

@app_views.route('/states/', methods=['GET', 'POST'])
def all_states():
    """retrieves all states or create a state"""
    if request.method == 'GET':
        states = all(State)
        json_states = [value.to_dict() for value in states.values()]

        return jsonify(json_states)

    else:
        data = request.get_json()

        # if not request.is_json:
            # abort(400, {'message': 'Not a JSON'})
        if 'name' not in data:
            abort(400, 'Missing name')
        obj = State(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'])
def state_object(state_id):
    """retrieve s, deletes and updates a state"""
    if request.method == 'GET':
        try:
            return jsonify(all()[f'State.{state_id}'].to_dict())
        except KeyError:
            abort(404)

    elif request.method == 'DELETE':
        try:
            all().__delitem__(f'State.{state_id}')
            storage.save()
            return jsonify({}), 200
        except KeyError:
            abort(404)

    else:
        try:
            data = request.get_json
            obj = all()[f'State.{state_id}']

            for key,value in request.get_json().items():
                if key not in ['created_at', 'updated_at', 'id']:
                    obj.__dict__[key] = value
            obj.save()
            return jsonify(obj.to_dict()), 200
        except KeyError:
            abort(404)
