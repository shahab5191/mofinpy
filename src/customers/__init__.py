from flask import Blueprint

bp = Blueprint('customers', __name__)

from src.customers import routes
