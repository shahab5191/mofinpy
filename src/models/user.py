from copy import Error
from datetime import datetime
from sqlalchemy.types import UUID
from src.extensions import db
import uuid

from src.utils.encryption import compare_password, hash_password


class UserModel(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(40))
    password = db.Column(db.String())
    salt = db.Column(db.String())
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        default_factory=datetime.utcnow, nullable=False
    )

    def json(self):
        return {"email": self.email, "id": self.id}

    def __repr__(self):
        return f'<Post "{self.email}">'


class User():
    user = UserModel()

    def __init__(self, email, password):
        if self.emailIsRegistered(email):
            raise Exception('Email is already taken!')

        hashed = hash_password(password)
        createdUser = UserModel()
        createdUser.email = email
        createdUser.password = hashed['hash']
        createdUser.salt = hashed['salt']
        db.session.add(createdUser)
        db.session.commit()
        self.user = createdUser
        return

    def emailIsRegistered(self, email):
        try:
            foundUser = UserModel.query.filter_by(email=email).first()
        except Error:
            return False
        return True if foundUser else False

    @classmethod
    def getUser(cls, email, password):
        try:
            user = UserModel.query.filter_by(email=email).first()
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

    @classmethod
    def userIsValid(cls, email, password):
        try:
            requestedUser = UserModel.query.filter_by(email=email).first()
        except Exception:
            return False

        if not requestedUser:
            return False

        password_hash = requestedUser.password
        return compare_password(
            password.encode('utf-8'),
            password_hash.encode('utf-8')
        )

    def json(self):
        if not self.user:
            return None
        return {"id": self.user.id, "email": self.user.email}
