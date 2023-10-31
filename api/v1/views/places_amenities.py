#!/usr/bin/python3
"""Create a new view for the link between Place objects and Amenity objects
that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.amenity import Amenity
import os


@app_views.route("/places/<place_id>/amenities", strict_slashes=False,
                 methods=['GET'])
def get_place_amenity(place_id=None):
    """
    Retrieves the list of all Amenity objects of a Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get(Amenity, amenity_id.to_dict()
            for amenity_id in place.amenity_ids]

    return jsonify(amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes a Amenity object to a Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity.id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity.id)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=['POST'])
def post_place_amenity(place_id=None, amenity_id=None):
    """
    Link a Amenity object to a Place
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
