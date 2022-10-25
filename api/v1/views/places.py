#!/usr/bin/python3
"""view for Place objects that handles all
default RESTFul API actions"""

from flask import abort, jsonify, request
from models import storage
from models.place import Place
from api.v1.views import app_views

all = storage.all


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def all_places(city_id):
    """retrieves all places in a city or create a place in a city"""
    if request.method == 'GET':
        all_places = all(Place).values()
        city_places = [
            place.to_dict() for place in all_places if place.city_id == city_id]
        return jsonify(city_places)

    else:
        data = request.get_json() | {"city_id": city_id}
        # if not request.is_json:
        # abort(400, {'message': 'Not a JSON'})
        if 'user_id' not in data:
            abort(400, 'Missing user_id')
        if 'name' not in data:
            abort(400, 'Missing name')
        obj = Place(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT', 'GET', 'DELETE'])
def place_objects(place_id):
    """retrieves, deletes and creates a place"""
    try:
        place = all()[f'Place.{place_id}']
    except KeyError:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())
    elif request.method == 'DELETE':
        all().__delitem__(f'Place.{place_id}')
        storage.save()
        return jsonify({}), 200
    else:
        data = request.get_json()
        obj = place

        for key, value in data.items():
            if key not in ['created_at', 'updated_at', 'id',
                           'user_id', 'city_id']:
                obj.__dict__[key] = value
        obj.save()
        return jsonify(obj.to_dict()), 200
