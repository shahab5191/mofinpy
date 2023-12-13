from flask import Flask

from src.config import Config
from src.extensions import db
from src.models.user import User
from src.models.item import Item
from src.models.warehouse import Warehouse
from src.models.location import Location
from src.models.currency import Currency
from src.models.provider import Provider
from src.models.purchase_order import PurchaseOrder
from src.models.enums import Enum


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    from src.users import bp as user_bp
    from src.items import bp as items_bp
    from src.purchase import bp as purchase_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(items_bp)
    app.register_blueprint(purchase_bp)

    with app.app_context():
        db.create_all()

    return app
