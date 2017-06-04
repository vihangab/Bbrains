#app/auth/__init__.py

from flask import Blueprint

auth = Blueprint('admin', __name__)

from . import views
