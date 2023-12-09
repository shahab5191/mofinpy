from flask import Blueprint

bp = Blueprint('items', __name__)

from src.items import routes
