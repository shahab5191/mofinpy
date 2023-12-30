import pytest
from sqlalchemy import text
from src import create_app
from tests.config import TestConfig
from src.extensions import db


@pytest.fixture()
def app():
    app = create_app(config_class=TestConfig)
    yield app


@pytest.fixture()
def client(app, database):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def database(app):
    print('-----run inside database------')
    with app.app_context():
        db.drop_all()
        db.create_all()
    yield db
