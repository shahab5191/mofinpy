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
from src.models.customer import Customer


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    from src.users import bp as user_bp
    from src.items import bp as items_bp
    from src.purchase import bp as purchase_bp
    from src.provider import bp as provider_bp
    from src.locations import bp as location_bp
    from src.customers import bp as customers_bp
    from src.warehouses import bp as warehouses_bp
    from src.sell_orders import bp as sell_orders_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(items_bp)
    app.register_blueprint(purchase_bp)
    app.register_blueprint(provider_bp)
    app.register_blueprint(location_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(warehouses_bp)
    app.register_blueprint(sell_orders_bp)

    with app.app_context():
        db.create_all()

    return app
