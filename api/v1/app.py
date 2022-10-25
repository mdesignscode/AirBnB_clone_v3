#!/usr/bin/python3
"""returns api status code"""

import api.v1.views.index
import api.v1.views.amenities
import api.v1.views.cities
import api.v1.views.places_reviews
import api.v1.views.places
import api.v1.views.states
import api.v1.views.users
from api.v1.views import app_views
from flask_cors import CORS, cross_origin
from flask import Flask, jsonify
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")
CORS(app)


@app.teardown_appcontext
def close_session(session):
    """close a session"""
    storage.close()


@app.errorhandler(404)
def missing(e):
    """return not found"""
    return jsonify({"error": "Not found"})


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST') if getenv('HBNB_API_HOST') else '0.0.0.0'
    port = getenv('HBNB_API_PORT') if getenv('HBNB_API_PORT') else 5000
    app.run(port=port, host=host, threaded=True, debug=True)
