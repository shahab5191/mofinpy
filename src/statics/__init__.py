from flask import Blueprint


bp = Blueprint('statics', __name__)


from src.statics import routes
