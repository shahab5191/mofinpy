from flask import Blueprint


bp = Blueprint("history", __name__)


from src.history import routes
