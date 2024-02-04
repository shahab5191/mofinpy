from datetime import UTC, datetime, timedelta
from faker import Faker
from flask import current_app
import jwt

from src.models.user import User


def generate_test_token(db):
    fake = Faker()
    email = fake.email()
    password = fake.password()
    new_user = User(email=email, password=password, salt="test")
    db.session.add(new_user)
    db.session.commit()

    secret = current_app.config['SECRET_KEY']
    token = jwt.encode(
        {
            "id": str(new_user.id),
            "email": email,
            "exp": datetime.now(UTC) + timedelta(minutes=1)
        },
        secret,
        algorithm='HS256'
    )
    return token
