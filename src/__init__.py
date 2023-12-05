from flask import Flask

from src.config import Config
from src.extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    from src.users import bp as user_bp
    app.register_blueprint(user_bp)

    return app
