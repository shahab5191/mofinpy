from src.models.user import User
from src.utils.encryption import hash_password, compare_password
from src.extensions import db


def create_user(email, password):
    if emailIsRegistered(email):
        raise Exception('Email is already taken!')

    hashed = hash_password(password)
    createdUser = User()
    createdUser.email = email
    createdUser.password = hashed['hash']
    createdUser.salt = hashed['salt']
    db.session.add(createdUser)
    db.session.commit()
    return createdUser


def emailIsRegistered(email):
    try:
        foundUser = User.query.filter_by(email=email).first()
    except Exception:
        return False
    return True if foundUser else False


def getUser(email, password):
    try:
        user = User.query.filter_by(email=email).first()
    except Exception:
        raise Exception('User was not found!')

    if not user:
        raise Exception('User was not found!')

    password_hash = user.password

    if not compare_password(
        password=password.encode('utf-8'),
        hash=password_hash.encode('utf-8')
    ):
        raise Exception('Email or Password is wrong!')

    return user


def userIsValid(email, password):
    try:
        requestedUser = User.query.filter_by(email=email).first()
    except Exception:
        return False

    if not requestedUser:
        return False

    password_hash = requestedUser.password
    return compare_password(
        password.encode('utf-8'),
        password_hash.encode('utf-8')
    )
