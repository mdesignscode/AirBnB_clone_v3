#!/usr/bin/python3
"""view for Review objects that handles all
default RESTFul API actions"""

from flask import abort, jsonify, request
from models import storage
from models.review import Review
from api.v1.views import app_views

all = storage.all


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def all_reviews(place_id):
    """retrieves all reviews in a place or create a review in a place"""
    if request.method == 'GET':
        all_reviews = all(Review).values()
        place_reviews = [
            review.to_dict() for review in all_reviews if review.place_id == place_id]
        return jsonify(place_reviews)

    else:
        data = request.get_json() | {"place_id": place_id}
        # if not request.is_json:
        # abort(400, {'message': 'Not a JSON'})
        if 'user_id' not in data:
            abort(400, 'Missing user_id')
        if 'name' not in data:
            abort(400, 'Missing name')
        obj = Review(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT', 'GET', 'DELETE'])
def review_objects(review_id):
    """retrieves, deletes and creates a review"""
    try:
        review = all()[f'Review.{review_id}']
    except KeyError:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())
    elif request.method == 'DELETE':
        all().__delitem__(f'Review.{review_id}')
        storage.save()
        return jsonify({}), 200
    else:
        data = request.get_json()
        obj = review

        for key, value in data.items():
            if key not in ['created_at', 'updated_at', 'id',
                           'user_id', 'place_id']:
                obj.__dict__[key] = value
        obj.save()
        return jsonify(obj.to_dict()), 200
