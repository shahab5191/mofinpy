from flask import Blueprint


bp = Blueprint('Upload', __name__)


from src.upload import routes

