from flask import Blueprint

bp = Blueprint('warehouses', __name__)

from src.warehouses import routes
