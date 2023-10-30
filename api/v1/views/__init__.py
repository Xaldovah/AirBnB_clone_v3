#!/usr/bin/python3
<<<<<<< HEAD
=======
"""This module handles all the initializations"""
>>>>>>> storage_get_count
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
<<<<<<< HEAD
from api.v1.views.users import *
=======
>>>>>>> storage_get_count
