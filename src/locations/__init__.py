from flask import Blueprint

bp = Blueprint("locations", __name__)

from src.locations import routes
