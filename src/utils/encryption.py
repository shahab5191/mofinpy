import bcrypt
import jwt

from src.config import Config


def hash_password(password, salt=None):
    if salt is None:
        salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return {"hash": hashed.decode('utf-8'), "salt": salt}


def compare_password(password, hash):
    return bcrypt.checkpw(password=password, hashed_password=hash)


def validate_token(token):
    secret = Config.SECRET_KEY

    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
    except Exception as err:
        print(err)
        return None

    return payload
