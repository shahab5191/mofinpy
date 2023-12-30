from datetime import datetime, UTC
from sqlalchemy.types import UUID
from src.extensions import db
import uuid


class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(40))
    username = db.Column(db.String(40))
    password = db.Column(db.String())
    salt = db.Column(db.String())
    created_date = db.Column(db.DateTime, default=datetime.now(UTC))
    update_date = db.Column(
        db.DateTime,
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC)
    )

    def __init__(
            self,
            email,
            password,
            salt,
            username=None,
    ):
        self.email = email
        self.password = password
        self.salt = salt
        self.username = username

    def json(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
        }

    def __repr__(self):
        return f'<User "{self.email}">'
