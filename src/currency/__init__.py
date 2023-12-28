from flask import Blueprint


bp = Blueprint('currency', __name__)


from src.currency import routes
