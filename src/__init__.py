from flask import Flask

from src.config import Config
from src.extensions import db
from src.models.user import User
from src.models.item import Item


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    from src.users import bp as user_bp
    from src.items import bp as items_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(items_bp)
    return app
