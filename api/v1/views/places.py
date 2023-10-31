#!/usr/bin/python3
"""Creates a new view for Places objects that handles
all default RESTFul API actions
"""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State


@app_views.route("cities/<city_id>/places", strict_slashes=False,
                 methods=['GET'])
def get_place(city_id=None):
    """Retrieves the list of all State objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    cities = []
    for ct in city.places:
        cities.append(item.to_dict())
    return jsonify(cities)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """Deletes a State object"""
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    places.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>", strict_slashes=False, methods=['GET'])
def get_place_id(place_id):
    """Get Place by place id"""
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    return jsonify(places.to_dict())


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['POST'])
def create_place():
    """Creates a place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400
    if storage.get(User, data['user_id']) is None:
        abort(404)
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    place = Place(**data)
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['PUT'])
def update_place(place_id):
    """Updates a places object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())


@app_views.route('/places_search', strict_slashes=False, methods=['POST'])
def search_places():
    """Search for Place objects based on JSON parameters"""
    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if data and len(data):
        states = data.get('states', [])
        cities = data.get('cities', [])
        amenities = data.get('amenities', [])

    if not data or not len(data) or (
            not states and not cities and not amenities):
        places = storage.all(Place).values()
        list_places = [place.to_dict() for place in places]
        return jsonify(list_places)

    list_places = []

    if states:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    list_places.extend(city.places)

    if cities:
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                list_places.extend(city.places)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [place for place in list_places if all(
            [am in place.amenities for am in amenities_obj])]

    places = [place.to_dict() for place in list_places]
    for place in places:
        place.pop('amenities', None)

    return jsonify(places)
