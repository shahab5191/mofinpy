from flask import Blueprint

bp = Blueprint('purchases', __name__)

from src.purchase import routes
