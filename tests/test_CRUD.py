from tests.config import TestConfig


def test_CRUD_get(client):
    response = client.post(
        f'{TestConfig.URL_PREFIX}/users/signup',
        json={
            "email": "shahab5191@live.com",
            "password": "Gorgi0098"
        }
    )
    assert response.status_code == 201
