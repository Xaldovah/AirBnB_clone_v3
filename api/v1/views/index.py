#!/usr/bin/python3
"""This mod cretes the status endpoint"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def get_status():
    """return the status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def get_stats():
    """Retrieves the number of objects by type"""
    stats = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(stats)


if __name__ == '__main__':
    pass
