#!/usr/bin/python3
"""view for Amenity objects that handles all
default RESTFul API actions"""

from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views

all = storage.all


@app_views.route('/amenities', methods=['GET', 'POST'])
def all_amenities():
    """retrieves all amenities or create an amenity"""
    if request.method == 'GET':
        all_amenities = all(Amenity).values()
        json_amenities = [amenity.to_dict() for amenity in all_amenities]
        return jsonify(json_amenities)

    else:
        data = request.get_json()
        # if not request.is_json:
        # abort(400, {'message': 'Not a JSON'})
        if 'name' not in data:
            abort(400, 'Missing name')
        obj = Amenity(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'PUT', 'DELETE'])
def amenity_object(amenity_id):
    """retrieves, deletes and updates an amenity"""
    try:
        amenity = all()[f'Amenity.{amenity_id}']
    except KeyError:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    elif request.method == 'DELETE':
        all().__delitem__(f'Amenity.{amenity_id}')
        storage.save()
        return jsonify({}), 200
    else:
        data = request.get_json
        obj = amenity

        for key, value in request.get_json().items():
            if key not in ['created_at', 'updated_at', 'id']:
                obj.__dict__[key] = value
        obj.save()
        return jsonify(obj.to_dict()), 200
