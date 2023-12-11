from flask import Blueprint

bp = Blueprint('inventory', __name__)

from src.inventory import rotute
