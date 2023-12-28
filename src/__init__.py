import os
from flask import Flask
from flask_cors import CORS

from src.config import Config
from src.extensions import db


def create_app(config_class=Config):
    UPLOAD_FOLDER = './public/uploads'
    app = Flask(__name__)
    CORS(app)
    app.static_folder = os.path.join(app.root_path, 'public')
    app.config.from_object(config_class)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    db.init_app(app)

    from src.users import bp as user_bp
    from src.items import bp as items_bp
    from src.purchase import bp as purchase_bp
    from src.provider import bp as provider_bp
    from src.locations import bp as location_bp
    from src.customers import bp as customers_bp
    from src.warehouses import bp as warehouses_bp
    from src.sell_orders import bp as sell_orders_bp
    from src.history import bp as history_bp
    from src.transactions import bp as transaction_bp
    from src.currency import bp as currency_bp
    from src.upload import bp as upload_bp
    from src.statics import bp as statics_bp
    from src.inventory import bp as inventory_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(items_bp)
    app.register_blueprint(purchase_bp)
    app.register_blueprint(provider_bp)
    app.register_blueprint(location_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(warehouses_bp)
    app.register_blueprint(sell_orders_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(currency_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(statics_bp)
    app.register_blueprint(inventory_bp)
    with app.app_context():
        db.create_all()

    return app
