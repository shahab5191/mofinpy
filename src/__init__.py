from flask import Flask
from config import Config
import os


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def main():
        return "<h1>main page</h1>"

    return app
