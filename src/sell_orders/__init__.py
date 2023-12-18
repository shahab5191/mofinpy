from flask import Blueprint

bp = Blueprint('sell_orders', __name__)

from src.sell_orders import routes
