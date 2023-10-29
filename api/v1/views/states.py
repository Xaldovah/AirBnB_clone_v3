#!/usr/bin/python3
"""Creates a new view for State objects that handles
all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False, methods=['GET'])
@app_views.route("/states/<state_id>", strict_slashes=False, methods=['GET'])
def get_states(state_id=None):
    """Retrieves the list of all State objects"""
    new_list = []
    key = "State." + str(state_id)
    if state_id is None:
        objs = storage.all(State)
        for key, value in objs.items():
            new_list.append(value.to_dict())
    elif key in storage.all(State).keys():
        return jsonify(storage.all(State)[key].to_dict())
    else:
        abort(404)
    return jsonify(new_list)


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/", strict_slashes=False, methods=['POST'])
def create_state():
    """Creates a State object"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    state = State(**request.get_json())
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def update_state(state_id):
    """Updates a State object"""
    key = "State." + str(state_id)
    if key not in storage.all(State).keys():
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ["created_at", "updated_at", "id"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
