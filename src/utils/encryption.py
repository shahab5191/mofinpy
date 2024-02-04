from datetime import datetime, timedelta, UTC
import bcrypt
from flask import current_app
import jwt


def hash_password(password, salt=None):
    if salt is None:
        salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return {"hash": hashed.decode('utf-8'), "salt": salt}


def compare_password(password, hash):
    return bcrypt.checkpw(password=password, hashed_password=hash)


def validate_token(token):
    secret = current_app.config['SECRET_KEY']

    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
    except Exception as err:
        print(err)
        return None

    return payload


def generate_token(user_id, email):
    secret = current_app.config['SECRET_KEY']
    try:
        token = jwt.encode(
            {
                "id": user_id,
                "email": email,
                "exp": datetime.now(UTC) + timedelta(hours=24)
            },
            secret,
            algorithm='HS256')
    except Exception as err:
        print(err)
        return None
    return token
