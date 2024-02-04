from faker import Faker
from flask import current_app
from tests.config import TestConfig
from tests.factories.item_factory import ItemFactory
from tests.utils.token_gen import generate_test_token


def test_CRUD_get_not_found(app, client, database):
    """Test getting a none existing item"""
    with app.app_context():
        response = client.get(
            f'{TestConfig.URL_PREFIX}/items/1',
            headers={'AUTHORIZATION': f'Bearer {
                generate_test_token(database)}'}
        )
        assert response.status_code == 404


def test_CRUD_get_found(app, client, database):
    with app.app_context():
        new_item = ItemFactory()
        database.session.add(new_item)
        database.session.commit()
        """Test getting an existing item"""
        response = client.get(
            f'{TestConfig().URL_PREFIX}/items/1',
            headers={'AUTHORIZATION': f'Bearer {
                generate_test_token(database)}'}
        )
        assert response.status_code == 200


def test_CRUD_get_all_found(app, client, database):
    with app.app_context():
        """Test getting 10 existing items"""
        for _ in range(10):
            new_item = ItemFactory()
            database.session.add(new_item)

        database.session.commit()
        response = client.get(
            f'{TestConfig().URL_PREFIX}/items/',
            headers={'AUTHORIZATION': f'Bearer {
                generate_test_token(database)}'}
        )
        assert response.status_code == 200 or 308


def test_CRUD_create(app, client, database):
    """Test creating new item with CRUD"""
    fake = Faker()
    with app.app_context():
        response = client.post(
            f'{current_app.config["URL_PREFIX"]}/items/',
            headers={'AUTHORIZATION': f'Bearer {
                generate_test_token(database)}'},
            json={
                "name": fake.first_name(),
                "brand": fake.first_name(),
                "description": fake.paragraph()
            }
        )
        assert response.status_code == 201


def test_CRUD_delete(app, client, database):
    item = ItemFactory()
    with app.app_context():
        database.session.add(item)
        database.session.commit()

        response = client.delete(
            f'{current_app.config["URL_PREFIX"]}/items/1',
            headers={
                'AUTHORIZATION': f'Bearer {
                    generate_test_token(database)}'
            }
        )
        assert response.status_code == 201


def test_CRUD_delete_not_found(app, client, database):
    with app.app_context():
        response = client.delete(
            f'{current_app.config["URL_PREFIX"]}/items/1',
            headers={'AUTHORIZATION': f'Bearer {generate_test_token(database)}'}
        )
        assert response.status_code == 404


def test_CRUD_update(app, client, database):
    item = ItemFactory()
    with app.app_context():
        database.session.add(item)
        database.session.commit()
        response = client.patch(
            f'{current_app.config["URL_PREFIX"]}/items/1',
            headers={'AUTHORIZATION': f'Bearer {generate_test_token(database)}'},
            json={'name': "test"}
        )
        assert response.status_code == 201
