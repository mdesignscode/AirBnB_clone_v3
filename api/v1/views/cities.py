#!/usr/bin/python3
"""view for City objects that handles all
default RESTFul API actions"""

from flask import abort, jsonify, request
from models import storage
from models.city import City
from api.v1.views import app_views

all = storage.all


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def all_cities(state_id):
    """retrieves all cities in a state or create a city in a state"""
    if request.method == 'GET':
        all_cities = all(City).values()
        state_cities = [
            city.to_dict() for city in all_cities if city.state_id == state_id]
        return jsonify(state_cities)

    else:
        data = request.get_json() | {"state_id": state_id}
        # if not request.is_json:
        # abort(400, {'message': 'Not a JSON'})
        if 'name' not in data:
            abort(400, 'Missing name')
        obj = City(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT', 'GET', 'DELETE'])
def city_objects(city_id):
    """retrieves, deletes and creates a city"""
    try:
        city = all()[f'City.{city_id}']
    except KeyError:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())
    elif request.method == 'DELETE':
        all().__delitem__(f'City.{city_id}')
        storage.save()
        return jsonify({}), 200
    else:
        data = request.get_json()
        obj = city

        for key, value in data.items():
            if key not in ['created_at', 'updated_at', 'id', 'state_id']:
                obj.__dict__[key] = value
        obj.save()
        return jsonify(obj.to_dict()), 200
